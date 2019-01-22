import numpy as np
import math
from typing import TypeVar
from typing import Mapping, Set, Tuple, Generic, Any, Callable

S = TypeVar('S')
A = TypeVar('A')
X = TypeVar('X')
Y = TypeVar('Y')
Z = TypeVar('Z')

class MDP(Generic[S, A]):
    
    def map_reconstruct(self, d: Mapping[X, Tuple[Y, Z]])\
        -> Tuple[Mapping[X, Y], Mapping[X, Z]]:
        d1 = {k: v1 for k, (v1, _) in d.items()}
        d2 = {k: v2 for k, (_, v2) in d.items()}
        return d1, d2
    
    def get_all_states(self, S):
        # return the names of each state in a dictionary
        return set(S.keys())
    
    def get_actions_set(self, mdp_data: Mapping[S, Mapping[A, Any]])\
        -> Mapping[S, Set[A]]:
        actions_set = {}
        for k, v in mdp_data.items():
            actions_set[k] = set(v.keys())
        return actiosn_set
    
    def get_actions_for_states(self, mdp_data: Mapping[S, Mapping[A, Any]])\
        -> Mapping[S, Set[A]]:
        return {k: set(v.keys()) for k, v in mdp_data.items()}
    
    def convert_to_MRP_transition(self, d1, d2):
        """
        The convert_to_MRP_transition should be a part of MDP class, where it takes two dictionary
        It will return a dictionary mapping from state -> {state: probability},
        which is the transition matrix for the MArkov Process
        """
        data = {k: {v : 0 for v in self.all_states} for k in self.all_states}
        for curt_state, mapping_s_a in d1.items():
            for action, tup in mapping_s_a.items():
                for next_state, probability in enumerate(tup):
                    data[curt_state][next_state] += probability * d2[curt_state][action]
        return data
    
    def convert_to_MRP_reward(self, d1, d2):
        """
        The convert_to_MRP_reward should be a part of the MDP class, where it takes two dictionary, namely d1, and d2
        """
        # where d1 is the mapping from state -> {action: (state, probability)
        # d2 is the mapping from the state -> {action : reward}

        # initialize the MRP with {state: {state: reward}} and the initial reward are all 0
        data = {k: {v : 0 for v in self.all_states} for k in self.all_states}
        for curt_state, mapping_s_a in d1.items():
            for action, tup in mapping_s_a.items():
                for next_state, probability in enumerate(tup):
                    data[curt_state][next_state] += probability * d2[curt_state][action]

        # another way to improve efficiency is to construct a 2D big matrix (state, state, probability) 
        # --- SEE MarkovDecisionProcess.convert_to_MRP()
        return data

    def __init__(self, info: Mapping[S, Mapping[A, Tuple[Mapping[S, float], float]]], gamma: float):
        
        # in this case, the params passes in into the init function is a big dictionary
        # the data structure can be described as {state:{action:({state:probability, reward})}
        
        d = {k: self.map_reconstruct(v) for k, v in info.items()}
        # after reconstructing the map, what we have here is a mapping from State -> {action: {state: probability}}, {action: reward}
        d1, d2 = self.map_reconstruct(d)
        # after reconstructing the map, what we have so far two dictionaries:
        # where d1 is a mapping from state -> {action: {state: probabilities}}
        # and d2 is a mapping from state -> {action, reward}
        self.d1 = d1
        self.d2 = d2
        self.all_states: Set[S] = self.get_all_states(info)
        
        # state_action_dict is a mapping from a state to a set, which is consist of all the actions it can make at current state
        self.state_action_dict: Mapping[S, Set[A]] = \
            self.get_actions_for_states(info)
        
        
        self.transitions: Mapping[S, Mapping[A, Mapping[S, float]]] = d1
        
        self.rewards: Mapping[S, Mapping[A, float]] = d2
        self.gamma: float = gamma
        self.terminal_states: Set[S] = self.get_terminal_states()

    def get_sink_states(self) -> Set[S]:
        return {k for k, v in self.transitions.items() if
                all(len(v1) == 1 and k in v1.keys() for _, v1 in v.items())
                }

    def get_terminal_states(self) -> Set[S]:

        sink = self.get_sink_states()
        return {s for s in sink if
                all(is_approx_eq(r, 0.0) for _, r in self.rewards[s].items())}
