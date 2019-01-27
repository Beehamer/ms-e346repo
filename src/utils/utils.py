import numpy as np
import copy
import math
from scipy.linalg import eig

def state2index(data:dict) -> dict:
    list_of_states = list(data.keys())
    state2idx = {}
    for i, state in emuerate(list_of_states):
        state2idx[state] = i
    return state2idx

def action2index(data:dict) -> dict:
    list_of_states = list(data.keys())
    action2idx = {}
    index_of_action = 0
    for key, value in data.items():
        for action, tuples in data[key],items():
            if action not in action2idx:
                action2idx[action] = index_of_action
                index_of_action += 1
    return action2idxdef construct_state_action_state_matrix(data:dict, state2idx:dict, action2idx: dict):
    num_of_states = len(list(state2idx.keys()))
    num_of_actions = len(list(action2idx.keys()))
    transition_matrix = np.zeros((num_of_states, num_of_actions, num_of_states))
    Q_sa = np(zeros(num_of_state, num_of_actions, num_of_states))
    for state, dics in data.items():
        for action, tups in dics.items():
            for next_state, probs_reward in tups.item():
                curt_state_id = state2idx[state]
                next_state_id = state2idx[next_state]
                action_id = action2idx[action]
                transition_matrix[curt_state_id, action_id, next_state_id] += probs_reward[0]
                Q_sa[curt_state_id, action_id, next_state_id] += probs_reward[1]
    return (transition_matrix, Q_sa)

def construct_policy_matrix(policy: dict, state2idx:dict, action2idx:dict):
    current_policy = np.zeros((len(state2idx), len(action2idx)))
    for state, action_prob_dict in policy.items():
        for action, prob in action_prob_dict.items():
            current_policy[state2idx[state], action2idx[action]] += prob
    # the policy matrix
    return current_policy
    

def construct_transition(transition_matrix, Q_sa, current_policy, state2idx, action2idx):
        # the transition matrix of the current policy
        P = np.zeros((len(state2idx), len(state2idx)))
        # the Q value for current policy
        Q = np.zeros((len(state2idx), len(state2idx)))
        for state_index in range(len(state2idx)):
            # calculate the probability of the transition
            P[state_index,:] += np.dot(transition_matrix[state_index, :, :].T, current_policy[state_index])
            Q[state_index,:] += np.sum(np.multiply(transition_matrix[state_index, :, :], Q_sa[state_index,:,:]), axis = 0)
        return (P,Q)