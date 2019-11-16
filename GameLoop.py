# import numpy as np
# from PyQt5.QtCore import QObject, pyqtSignal, QThread, pyqtSlot
# import time
# from PyQt5 import QtCore, QtGui, QtWidgets
# import sys
# import os
from TronBike import TronBike
from PowerUp import PowerUp
import gameconfig
from BoardBlocks import BoardBlocks

if gameconfig.bike1_player == 'ai' or gameconfig.bike2_player == 'ai':
    from dqn_api import AI


class GameLoop(object):
    def __init__(self):

        # Set up bikes, board and power ups.
        self.bike_1 = TronBike()
        self.bike_2 = TronBike()

        self.bike_1.spawn_bike(50, 50)

        # self.bike_2.inital_length = 10
        self.bike_2.spawn_bike(50, 50)

        self.board_blocks = BoardBlocks()

        self.board_blocks.load_level(gameconfig.level_name)
        self.blocked_blocks = self.board_blocks.blocked_blocks

        self.powerUp = PowerUp(self.bike_1, self.bike_2)

        self.directions = {0: 'up', 1: 'down', 2: 'left', 3: 'right'}

        self.poisonous = False

        # Initialize DQNs
        discount = 0.8
        state_size = 6
        self.ais = {}
        if gameconfig.bike1_player == 'ai':
            self.ais['bike_1'] = AI(state_size, discount, gameconfig.bike1_dqn)
        if gameconfig.bike2_player == 'ai':
            if gameconfig.bike1_dqn == gameconfig.bike2_dqn and gameconfig.bike1_player == 'ai':
                self.ais['bike_2'] = self.ais['bike_1']
            else:
                self.ais['bike_2'] = AI(state_size, discount, gameconfig.bike2_dqn)

    def game_step(self, tact_counter):

        #  Spawn Power Up.
        if (tact_counter+1) % self.powerUp.next_spawn_ticks == 0:
            self.powerUp.spawn_powerup(tact_counter)

        #  Step bike 1
        if tact_counter % self.bike_1.bike_tact == 0:
            # dqn learn and update
            last_signal = self.get_som_state(self.bike_1, self.bike_2)  # die noch bike spezifisch machen.
            if gameconfig.bike1_player == 'ai':
                # mem_idx ist zue ueberarbeiten
                chosen_direc = self.ais['bike_1'].update(self.bike_1.last_reward, last_signal, 0, self.poisonous)
                self.poisonous = False
                self.bike_1.set_direction(chosen_direc)
            self.bike_1.do_next_step()
            self.bike_1.last_reward = self.calc_rewards(self.bike_1.bike, self.bike_2.bike)

        #  Step bike 2
        if tact_counter % self.bike_2.bike_tact == 0:
            # dqn learn and update
            last_signal = self.get_som_state(self.bike_2, self.bike_1)  # die noch bike spezifisch machen.
            if gameconfig.bike2_player == 'ai':
                chosen_direc = self.ais['bike_2'].update(self.bike_2.last_reward, last_signal, 1, self.poisonous)
                self.poisonous = False
                self.bike_2.set_direction(chosen_direc)
            self.bike_2.do_next_step()
            self.bike_2.last_reward = self.calc_rewards(self.bike_2.bike, self.bike_1.bike)

        # TODO: nachvollziehen warum ich hier kleinen tact hatte
        smaller_tact = min(self.bike_1.bike_tact, self.bike_2.bike_tact)
        if tact_counter % smaller_tact == 0:

            #  Collision detection    
            #  Collision of powerUp with bikes
            self.powerUp.bike_collision(tact_counter)
            
            #  Check if power up time has run out
            self.powerUp.despawn_power_up(tact_counter)
            
            #  Check bike-bike collision
            TronBike.bike_bike_collision(self.bike_1, self.bike_2)

            #  Check Bike 1 and Bike 2 self collisions
            self.bike_1.bike_self_collision()
            self.bike_2.bike_self_collision()

            #  Reset bike velocity if time has run out
            self.bike_1.reset_bike_tact(tact_counter)
            self.bike_2.reset_bike_tact(tact_counter)

            #  Check bike wall collision
            self.bike_1.bike_wall_collision(self.blocked_blocks)
            self.bike_2.bike_wall_collision(self.blocked_blocks)
            
        return smaller_tact

    ##################
    def calc_rewards(self, this_bike, other_bike):
        reward = 0
        if this_bike:  # len>0
            if this_bike[0] in this_bike[1:] or this_bike[0] in self.blocked_blocks:
                reward += -0.1
            if other_bike and this_bike[0] in other_bike:
                reward += -0.1
        else:
            reward = 0.1
        if len(this_bike) <= 0 or len(other_bike) > 100:  # 100 anpassen ! gameconfig !!!
            reward += -1.0
        if len(this_bike) >= 100 or len(other_bike) <= 0:
            reward += 1.0
        # Game lose rewards / uebergang zu neuem game genau ueberdenken
        return reward

    def get_som_state(self, this_bike, other_bike):
        the_state = []
        retard_dict = {(0, -1): 0, (0, 1): 1, (-1, 0): 2, (1, 0): 3}
        if len(this_bike.bike) > 0:
            this_bike_head = this_bike.bike[0]
            same_x = [x[1] for x in (this_bike.bike[1:]+self.blocked_blocks+other_bike.bike)
                      if x[0] == this_bike_head[0]]
            same_y = [x[0] for x in (this_bike.bike[1:]+self.blocked_blocks+other_bike.bike)
                      if x[1] == this_bike_head[1]]

            if len(same_x) > 0:
                tmp_lst = [y-this_bike_head[1] for y in same_x if y >= this_bike_head[1]]
                if len(tmp_lst) > 0:
                    the_state.append(abs(min(tmp_lst)))
                else:
                    the_state.append(100)
                tmp_lst = [y-this_bike_head[1] for y in same_x if y <= this_bike_head[1]]
                if len(tmp_lst) > 0:
                    the_state.append(abs(max(tmp_lst)))
                else:
                    the_state.append(100)
            else:
                the_state.append(100)
                the_state.append(100)
            
            if len(same_y) > 0:
                tmp_lst = [x-this_bike_head[0] for x in same_y if x >= this_bike_head[0]]
                if len(tmp_lst) > 0:
                    the_state.append(abs(min(tmp_lst)))
                else:
                    the_state.append(100)
                tmp_lst = [x-this_bike_head[0] for x in same_y if x <= this_bike_head[0]]
                if len(tmp_lst) > 0:
                    the_state.append(abs(max(tmp_lst)))
                else:
                    the_state.append(100)
            else:
                the_state.append(100)
                the_state.append(100)
                
            the_state.append(retard_dict[this_bike.direction])
            the_state.append(len(this_bike.bike))
        else:
            the_state = [0, 0, 0, 0, 0, 0]
        return the_state
