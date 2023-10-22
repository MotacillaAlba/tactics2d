import sys

sys.path.append(".")
sys.path.append("./rllib")

from copy import deepcopy
from collections import deque

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import Normal
import numpy as np

from rllib.algorithms.ppo import *

OBS_SHAPE = {"state": (120+42+6,)}

agent_config = PPOConfig(
    {
        "state_space": None,
        "state_dim": 120 + 42 + 6,
        "action_space": None,
        "action_dim": 2,
        "gamma": 0.95,
        "lr_actor": 2e-6,
        "actor_kwargs": {
            "state_dim": 120 + 42 + 6,
            "action_dim": 2,
            "hidden_size": 256,
            "continuous": True,
        },
        "critic_kwargs": {
            "state_dim": 120 + 42 + 6,
            "hidden_size": 256,
        },
        "lr_critic": 2e-6 * 5,
        "horizon": 8192,
        "batch_size": 32,
        "adam_epsilon": 1e-8,
        "hidden_size": 256,
    }
)

VALID_STEER = [-0.75, 0.75]
MAX_SPEED = 2
PRECISION = 10
discrete_actions = []
for i in np.arange(
    VALID_STEER[-1], -(VALID_STEER[-1] + VALID_STEER[-1] / PRECISION), -VALID_STEER[-1] / PRECISION
):
    discrete_actions.append([i, MAX_SPEED])
for i in np.arange(
    VALID_STEER[-1], -(VALID_STEER[-1] + VALID_STEER[-1] / PRECISION), -VALID_STEER[-1] / PRECISION
):
    discrete_actions.append([i, -MAX_SPEED])


def choose_action(action_mean, action_std, action_mask):
    action_space = discrete_actions

    if isinstance(action_mean, torch.Tensor):
        action_mean = action_mean.cpu().numpy()
        action_std = action_std.cpu().numpy()
    if isinstance(action_mask, torch.Tensor):
        action_mask = action_mask.cpu().numpy()
    if len(action_mean.shape) == 2:
        action_mean = action_mean.squeeze(0)
        action_std = action_std.squeeze(0)
    if len(action_mask.shape) == 2:
        action_mask = action_mask.squeeze(0)

    def calculate_probability(mean, std, values):
        z_scores = (values - mean) / std
        log_probabilities = -0.5 * z_scores**2 - np.log((np.sqrt(2 * np.pi) * std))
        return np.sum(np.clip(log_probabilities, -10, 10), axis=1)

    possible_actions = np.array(action_space)
    # deal the scaling
    action_mean[1] = 1 if action_mean[1] > 0 else -1
    scale_steer = VALID_STEER[1]
    scale_speed = 1
    possible_actions = possible_actions / np.array([scale_steer, scale_speed])
    prob = calculate_probability(action_mean, action_std, possible_actions)
    exp_prob = np.exp(prob) * action_mask
    prob_softmax = exp_prob / np.sum(exp_prob)
    actions = np.arange(len(possible_actions))
    action_chosen = np.random.choice(actions, p=prob_softmax)

    return possible_actions[action_chosen]


class ReplayMemory(object):
    def __init__(self, memory_size: int, extra_items: list = []):
        self.items = ["state", "action", "reward", "done"] + extra_items
        self.memory = {}
        for item in self.items:
            self.memory[item] = deque([], maxlen=memory_size)

    def push(self, observations: tuple):
        """Save a transition"""
        for i, item in enumerate(self.items):
            self.memory[item].append(observations[i])

    def get_items(self, idx_list: np.ndarray):
        batches = {}
        for item in self.items:
            batches[item] = []
        batches["next_state"] = []
        for idx in idx_list:
            for item in self.items:
                batches[item].append(self.memory[item][idx])
            if idx == self.__len__() - 1 or self.memory["done"][idx]:
                batches["next_state"].append(None)
            else:
                batches["next_state"].append(self.memory["state"][idx + 1])
        for idx in batches.keys():
            if isinstance(batches[idx][0], np.ndarray) and idx not in ["state", "next_state"]:
                batches[idx] = np.array(batches[idx])
        return batches

    def sample(self, batch_size: int):
        idx_list = np.random.randint(self.__len__(), size=batch_size)
        return self.get_items(idx_list)

    def shuffle(self, idx_range: int = None):
        idx_range = self.__len__() if idx_range is None else idx_range
        idx_list = np.arange(idx_range)
        np.random.shuffle(idx_list)
        return self.get_items(idx_list)

    def clear(self):
        for item in self.items:
            self.memory[item].clear()

    def __len__(self):
        return len(self.memory["state"])


class DemoPPO(PPO):
    def __init__(
        self, configs = None, device = None
    ) -> None:
        device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        configs = agent_config
        super().__init__(configs, device)

        # the networks
        self.log_std = nn.Parameter(torch.zeros(2), requires_grad=False).to(self.device)
        self.log_std.requires_grad = True
        self.actor_optimizer = torch.optim.Adam(
            [{"params": self.actor_net.parameters()}, {"params": self.log_std}],
            self.configs.lr_actor,
            eps=self.configs.adam_epsilon,
        )
        self.critic_optimizer = torch.optim.Adam(
            self.critic_net.parameters(), self.configs.lr_critic, eps=self.configs.adam_epsilon
        )
        self.critic_target = deepcopy(self.critic_net)

        # As a on-policy RL algorithm, PPO does not have memory, the self.memory represents
        # the buffer
        self.memory = ReplayMemory(self.configs.horizon, ["log_prob", "next_obs"])

    def choose_action(self, obs: np.ndarray, info: dict):
        observation = deepcopy(obs)
        observation = torch.FloatTensor(observation).to(self.device)

        with torch.no_grad():
            policy_dist = self.actor_net(observation)
            mean = torch.clamp(policy_dist, -1, 1)
            log_std = self.log_std.expand_as(mean)
            std = torch.exp(log_std)
            dist = Normal(mean, std)

        # action = dist.sample()
        action_mask = info["action_mask"]
        action = choose_action(mean, std, action_mask)
        action = torch.FloatTensor(action).to(self.device)
        action = torch.clamp(action, -1, 1)
        log_prob = dist.log_prob(action)
        action = action.detach().cpu().numpy().flatten()
        log_prob = log_prob.detach().cpu().numpy().flatten()
        return action, log_prob

    def get_log_prob(self, obs: np.ndarray, action: np.ndarray):
        """get the log probability for given action based on current policy

        Args:
            observation(np.ndarray): np.ndarray with the same shape of self.state_dim.

        Returns:
            log_prob(np.ndarray): the log probability of taken action.
        """
        observation = deepcopy(obs)
        observation = torch.FloatTensor(observation).to(self.device)

        with torch.no_grad():
            policy_dist = self.actor_net(observation)
            mean = torch.clamp(policy_dist, -1, 1)
            log_std = self.log_std.expand_as(
                mean
            )  # To make 'log_std' have the same dimension as 'mean'
            std = torch.exp(log_std)
            dist = Normal(mean, std)

        action = torch.FloatTensor(action).to(self.device)
        log_prob = dist.log_prob(action)
        log_prob = log_prob.detach().cpu().numpy().flatten()
        return log_prob

    def push_memory(self, observations):
        """
        Args:
            observations(tuple): (obs, action, reward, done, log_prob, next_obs)
        """
        obs, action, reward, done, log_prob, next_obs = deepcopy(observations)
        observations = (obs, action, reward, done, log_prob, next_obs)
        self.memory.push(observations)

    def update(self):
        # convert batches to tensors

        # GAE computation cannot use shuffled data
        # batches = self.memory.shuffle()
        batches = self.memory.get_items(np.arange(len(self.memory)))
        state_batch = torch.FloatTensor(batches["state"]).to(self.device)

        action_batch = torch.FloatTensor(batches["action"]).to(self.device)
        rewards = torch.FloatTensor(np.array(batches["reward"])).unsqueeze(1)
        reward_batch = rewards
        reward_batch = reward_batch.to(self.device)
        done_batch = torch.FloatTensor(batches["done"]).to(self.device).unsqueeze(1)
        old_log_prob_batch = torch.FloatTensor(batches["log_prob"]).to(self.device)
        next_state_batch = torch.FloatTensor(batches["next_obs"]).to(self.device)
        self.memory.clear()

        # GAE
        gae = 0
        adv = []

        with torch.no_grad():
            value = self.critic_net(state_batch)
            next_value = self.critic_net(next_state_batch)
            deltas = reward_batch + self.configs.gamma * (1 - done_batch) * next_value - value

            # gae
            for delta, done in zip(
                reversed(deltas.cpu().flatten().numpy()),
                reversed(done_batch.cpu().flatten().numpy()),
            ):
                gae = delta + self.configs.gamma * self.configs.gae_lambda * gae * (1.0 - done)
                adv.append(gae)
            adv.reverse()
            adv = torch.FloatTensor(adv).view(-1, 1).to(self.device)

            v_target = adv + self.critic_target(state_batch)
            if self.configs.adv_norm:  # advantage normalization
                adv = (adv - adv.mean()) / (adv.std() + 1e-5)

        # apply multi update epoch
        for _ in range(self.configs.num_epochs):
            # use mini batch and shuffle data
            mini_batch = self.configs.batch_size
            batchsize = self.configs.horizon
            train_times = (
                batchsize // mini_batch
                if batchsize % mini_batch == 0
                else batchsize // mini_batch + 1
            )
            random_idx = np.arange(batchsize)
            np.random.shuffle(random_idx)
            for i in range(train_times):
                if i == batchsize // mini_batch:
                    ri = random_idx[i * mini_batch :]
                else:
                    ri = random_idx[i * mini_batch : (i + 1) * mini_batch]
                state = state_batch[ri]
                policy_dist = self.actor_net(state)
                mean = torch.clamp(policy_dist, -1, 1)
                log_std = self.log_std.expand_as(mean)
                std = torch.exp(log_std)
                dist = Normal(mean, std)

                log_prob = dist.log_prob(action_batch[ri])
                log_prob = torch.sum(log_prob, dim=1, keepdim=True)
                old_log_prob = torch.sum(old_log_prob_batch[ri], dim=1, keepdim=True)
                prob_ratio = (log_prob - old_log_prob).exp()

                loss1 = prob_ratio * adv[ri]
                loss2 = (
                    torch.clamp(
                        prob_ratio, 1 - self.configs.clip_epsilon, 1 + self.configs.clip_epsilon
                    )
                    * adv[ri]
                )

                actor_loss = -torch.min(loss1, loss2)
                critic_loss = F.mse_loss(v_target[ri], self.critic_net(state))

                self.actor_optimizer.zero_grad()
                self.critic_optimizer.zero_grad()
                actor_loss.mean().backward()
                critic_loss.mean().backward()

                if self.configs.gradient_clip:  # gradient clip
                    nn.utils.clip_grad_norm_(self.critic_net.parameters(), 0.5)
                    nn.utils.clip_grad_norm_(self.actor_net.parameters(), 0.5)
                self.actor_optimizer.step()
                self.critic_optimizer.step()
