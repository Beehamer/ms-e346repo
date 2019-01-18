import numpy as np
# two ways of constructing the class will be presented
# in the first way of constructing the the Markov Reward Process by passing the transition matrix and reward matrix separately
class MarkovRewardProcess:
    """ A class describing Markov Reward Process"""
    def get_all_states(self, S):
        # return the names of each state in a dictionary
        return set(S.keys())
    
    def construct_row_transition_matrix(self, row):
        # using the similar approximation function as MDP-DP-RL where two values are taken 
        # as the same when the absolute difference between them is smaller than 1e-8
        return {s: v for s, v in row.items() if not abs(v - 0.0) <= 1e-8}
    
    def get_transition_matrix(self, S):
        transition_matrix = {s : self.construct_row_transition_matrix(v) for s, v in S.items()}
        return transition_matrix
    
    def get_stationary_distribution(self):
        sz = len(self.all_states_list)
        mat = np.zeros((sz, sz))
        for i, s1 in enumerate(self.all_states_list):
            for j, s2 in enumerate(self.all_states_list):
                mat[i, j] = self.transition[s1].get(s2, 0.)

        eig_vals, eig_vecs = eig(mat.T)
        stat = np.array(
            eig_vecs[:, np.where(np.abs(eig_vals - 1.) < 1e-8)[0][0]].flat
        ).astype(float)
        norm_stat = stat / sum(stat)
        return {s: norm_stat[i] for i, s in enumerate(self.all_states_list)}
    
    def __init__(self, transition, reward):
        # in this case, the transition matrix and the reward matrix are separate dictionaries
        self.transition = transition
        self.reward = reward
#         self.all_state_list = list(self.get_all_states(transition))