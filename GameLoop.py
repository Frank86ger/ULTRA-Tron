import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, QThread, pyqtSlot
import time
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
from TronBike import TronBike
from PowerUp import PowerUp
import gameconfig
from BoardBlocks import BoardBlocks
from dqn import Dqn

class GameLoop(object):
    def __init__(self):

        #  Set up bikes, board and power ups.
        self.bike_1 = TronBike()
        self.bike_2 = TronBike()

        self.bike_1.spawn_bike(70,70)

        self.bike_2.inital_length = 10
        self.bike_2.spawn_bike(120,120)


        self.board_blocks = BoardBlocks()

        self.board_blocks.load_level(gameconfig.level_name)
        self.blocked_blocks = self.board_blocks.blocked_blocks

        self.powerUp = PowerUp(self.bike_1, self.bike_2)
        
        #NEW
        self.brain = Dqn(5,4,0.8)
        self.last_reward = 0
        self.directions = {0:'up', 1:'down', 2:'left', 3:'right'} #kann auch egal sein.

    def game_step(self, tact_counter):

        #  Spawn Power Up.
        if (tact_counter+1)%self.powerUp.next_spawn_ticks == 0:
            self.powerUp.spawn_powerup(tact_counter)

        #  Step bike 1
        if tact_counter%self.bike_1.bike_tact == 0:
            # DQN step here
            last_signal = self.get_som_state()
            action = self.brain.update(self.last_reward, last_signal)
            the_direc_idx = int(action.numpy())
            the_direc = self.directions[the_direc_idx]
            self.bike_1.set_direction(the_direc)#
            self.bike_1.do_next_step(tact_counter)
            if self.bike_1.bike:  # len>0
                if self.bike_1.bike[0] in self.bike_1.bike[1:]:
                    # or self.bike_1.bike[0] in self.bike_2.bike
                    self.last_reward = -0.1
                else:
                    self.last_reward = 0.1


        #  Step bike 2
        if tact_counter%self.bike_2.bike_tact == 0:
            self.bike_2.do_next_step(tact_counter)

        #  Collision detection and emit of signals
        #TODO: nachvollziehen warum ich hier kleinen tact hatte
        smaller_tact = min(self.bike_1.bike_tact, self.bike_2.bike_tact)
        if tact_counter%smaller_tact == 0:
            
            #  Collision of powerUp with bikes?
            self.powerUp.bike_collision(tact_counter)
            
            #  Check if power hup time has run out
            self.powerUp.despawn_power_up(tact_counter)
            
            #  Check bike-bike collision
            TronBike.bike_bike_collision(self.bike_1, self.bike_2)

            #  Bike 1 and Bike 2 self collisions
            self.bike_1.bike_self_collision()
            self.bike_2.bike_self_collision()

            #  Reset bike velocity
            self.bike_1.reset_bike_tact(tact_counter)
            self.bike_2.reset_bike_tact(tact_counter)

            #  Check bike wall collision
            self.bike_1.bike_wall_collision(self.blocked_blocks)
            self.bike_2.bike_wall_collision(self.blocked_blocks)
            
        return smaller_tact

    def get_som_state(self):
        the_state = []
        retard_dict = {(0,-1):0, (0,1):1, (-1,0):2, (1,0):3}
        if len(self.bike_1.bike) > 0:
            bike1_head = self.bike_1.bike[0]
            same_x = [x[1] for x in (self.bike_1.bike[1:]+self.blocked_blocks+self.bike_2.bike) if x[0]==bike1_head[0]]
            same_y = [x[0] for x in (self.bike_1.bike[1:]+self.blocked_blocks+self.bike_2.bike) if x[1]==bike1_head[1]]
        
            if len(same_x) > 0:
                tmp_lst = [y-bike1_head[1] for y in same_x if y>=bike1_head[1]]
                if len(tmp_lst) > 0:
                    the_state.append(abs(min(tmp_lst)))
                else:
                    the_state.append(100)
                tmp_lst = [y-bike1_head[1] for y in same_x if y<=bike1_head[1]]
                if len(tmp_lst) > 0:
                    the_state.append(abs(max(tmp_lst)))
                else:
                    the_state.append(100)
            else:
                the_state.append(100)
                the_state.append(100)
            
            if len(same_y) > 0:
                tmp_lst = [x-bike1_head[0] for x in same_y if x>=bike1_head[0]]
                if len(tmp_lst) > 0:
                    the_state.append(abs(min(tmp_lst)))
                else:
                    the_state.append(100)
                tmp_lst = [x-bike1_head[0] for x in same_y if x<=bike1_head[0]]
                if len(tmp_lst) > 0:
                    the_state.append(abs(max(tmp_lst)))
                else:
                    the_state.append(100)
            else:
                the_state.append(100)
                the_state.append(100)
                
            the_state.append(retard_dict[self.bike_1.direction])
        else:
            the_state = [0,0,0,0,0]
        return the_state