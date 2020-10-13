import gym
import numpy as np

env = gym.make("CliffWalking-v0")

print("观察空间 = {}".format(env.observation_space))
print("动作空间 = {}".format(env.action_space))
print("状态数量 = {},动作数量 = {}".format(env.nS,env.nA))
print("地图大小 = {}".format(env.shape))

def play_once(env, policy):
    total_reward = 0
    state = env.reset()
    while True:
        loc = np.unravel_index(state, env.shape)
        print('状态 = {}, 位置 = {}'.format(state, loc), end=' ')
        action = np.random.choice(env.nA, p=policy[state])
        next_state, reward, done, _ = env.step(action)
        print('动作 = {}, 奖励 = {}'.format(action, reward))
        total_reward += reward
        if done:
            break
        state = next_state
    return total_reward

actions = np.ones(env.shape, dtype=int)
actions[-1, :] = 0
actions[:, -1] = 2
optimal_policy = np.eye(4)[actions.reshape(-1)]


def evaluate_bellman(env, policy, gamma=1.):
    a, b = np.eye(env.nS), np.zeros((env.nS))
    for state in range(env.nS - 1):
        for action in range(env.nA):
            pi = policy[state][action]
            for p, next_state, reward, done in env.P[state][action]:
                a[state, next_state] -= (pi * gamma * p)
                b[state] += (pi * reward * p)
    v = np.linalg.solve(a, b)
    q = np.zeros((env.nS, env.nA))
    for state in range(env.nS - 1):
        for action in range(env.nA):
            for p, next_state, reward, done in env.P[state][action]:
                q[state][action] += ((reward + gamma * v[next_state]) * p)
    return v, q


policy = np.random.uniform(size=(env.nS, env.nA))
policy = policy / np.sum(policy, axis=1)[:, np.newaxis]
state_values, action_values = evaluate_bellman(env, policy)
print('状态价值 = {}'.format(state_values))
print('动作价值 = {}'.format(action_values))

optimal_state_values, optimal_action_values = evaluate_bellman(env, optimal_policy)
print('最优状态价值 = {}'.format(optimal_state_values))
print('最优动作价值 = {}'.format(optimal_action_values))

optimal_actions = optimal_action_values.argmax(axis=1)
print('最优策略 = {}'.format(optimal_actions))
