from game_constants import *

def calculate_next_state(current_state, action, player_id):

  next_state = current_state.copy()
  sliced_column = list(reversed(current_state[:, action]))
  if 0 in sliced_column:
    row_index = ROWS - sliced_column.index(0) - 1
    next_state[row_index, action] = player_id
    return [True, next_state]
  else:
    return [False, 0]


def check_for_game_termination(board_state):
  def check_if_the_sequence_is_valid(sequence_list):
    for row, col in sequence_list:
      if row < 0 or row >= rows or col < 0 or col >= columns:
        return False
    else:
      return True


  for row_index in range(ROWS):
    for col_index in range(COLUMNS):
      player_to_check = board_state[row_index, col_index]
      if(player_to_check == EMPTY_BOX):
        break

      sequeneces_to_check = [[[row_index+i,col_index] for i in range(4)],
                             [[row_index-i,col_index] for i in range(4)],
                             [[row_index,col_index+i] for i in range(4)],
                             [[row_index,col_index-i] for i in range(4)],
                             [[row_index+i,col_index+i] for i in range(4)],
                             [[row_index-i,col_index-i] for i in range(4)],
                             [[row_index-i,col_index+i] for i in range(4)],
                             [[row_index+i,col_index-i] for i in range(4)]]

      filtered_sequence = filter(check_if_the_sequence_is_valid, 
                                             sequeneces_to_check)
      for sequence in filtered_sequence:
        block_states = [board_state[row_index, col_index]
                        for row_index, col_index in sequence]
        if len(set(block_states)) == 1:
          if player_to_check == 1:
            game_state = game_status.player_1_won 
          else:
            game_state = game_status.player_2_won 
          return game_state


  is_it_a_draw = True
  for row_id in range(rows):
    for col_id in range(columns):
      if board_state[row_id, col_id] == 0:
        is_it_a_draw = False

  if(is_it_a_draw):
    print 'game ends in a draw'
    return  True

  return False
