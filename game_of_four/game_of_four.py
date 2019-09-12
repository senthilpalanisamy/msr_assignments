import numpy as np
import random
from game_constants import *
from utility_functions import *


class game_of_four:
  rows = ROWS 
  columns = COLUMNS
  board_state = np.zeros((rows,columns), dtype=np.uint8)
  player_to_character = ['X','1','2']
  current_player = 0
  all_players = [1,2]
  count_for_success = 4
  game_status = 'running'

  def initialise_player_state(self):
    self.current_player = random.choice(self.all_players)
    print 'player %d goes first'%(self.current_player)

  def draw_board(self):

    for row_id in range(self.rows):
      print '\n'
      for col_id in range(self.columns):
        print '---',
      for line in range(1):
        print '\n'
        for col_id in range(self.columns):
          character_to_print = self.player_to_character[self.board_state[row_id][col_id]]
          print'| %c' % (character_to_print),
        print('|'),


    # For printing last line
    print('\n')
    for i in range(self.columns):
      print('___'),
    

  def record_move_and_update_board(self):

    print '\nPlayer %d enter your move' % self.current_player
    while True:

      try:
        input_string = input("Enter the column_number: ")
        col_index = int(input_string) -1
      except:
        print '\nInvalid input! Please a valid column number'
        continue

      if col_index > self.columns or col_index < 0:
        print '\nInvalid input! Please a valid column number'
        continue

      is_the_move_valid, next_state = calculate_next_state(self.board_state,
                                                           col_index,
                                                           self.current_player) 
      
      if is_the_move_valid:
        self.board_state = next_state
        break
      else:
        print 'Invalid input! Please enter a box that\'s unoccupied'

    if self.current_player == 1:
      self.current_player = 2
    else:
      self.current_player = 1

  
  def check_for_game_termination(self):
    def check_if_the_sequence_is_valid(sequence_list):
      for row, col in sequence_list:
        if row < 0 or row >= self.rows or col < 0 or col >= self.columns:
          return False
      else:
        return True


    for row_index in range(self.rows):
      for col_index in range(self.columns):
        player_to_check = self.board_state[row_index, col_index]
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
          block_states = [self.board_state[row_index, col_index]
                          for row_index, col_index in sequence]
          if len(set(block_states)) == 1:
            self.game_status = 'ended'
            print 'player %d won' % (player_to_check)
            self.draw_board()
            return  True


    is_it_a_draw = True
    for row_id in range(self.rows):
      for col_id in range(self.columns):
        if self.board_state[row_id, col_id] == 0:
          is_it_a_draw = False

    if(is_it_a_draw):
      print 'game ends in a draw'
      return  True

    return False

          







if __name__=='__main__':
  new_game = game_of_four()
  new_game.initialise_player_state()
  has_game_ended = False
  while(not has_game_ended):
    new_game.draw_board()
    new_game.record_move_and_update_board()
    has_game_ended = new_game.check_for_game_termination()


  #new_game.draw_board()

