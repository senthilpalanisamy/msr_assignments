import numpy as np
from game_constants import *


def minimax_decision(state, agent_id):
  possible_actions = [0,1,2,3,4,5]  
  valid_actions = []
  next_states = []
  for action in possible_actions:
    does_the_state_exist, next_state = calculate_next_state(state, action, agent_id)
    if(does_the_state_exist):
      next_states.append(next_state)
      valid_actions.append(action)

   mini_max_values = map(next_states, find_min_value)
   best_action = valid_actions[mini_max_values.index(max(mini_max_values))]
   return best_action

def find_min_value(state):
  

def find_max_value(state):




if __name__=='__main__':
  state = np.array([[0,0,0,0,0,0,0]
                    [0,0,0,0,0,0,0]
                    [0,0,0,0,0,0,0]
                    [0,0,0,0,0,0,0]
                    [0,0,0,0,0,0,0]
                    [1,0,2,0,1,0,2]]) 
