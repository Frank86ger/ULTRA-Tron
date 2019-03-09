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
from GameLoop import GameLoop
from dqn import Dqn

import random # kann wieder weg?

class GameThread(QThread, GameLoop):

    bike1_list = pyqtSignal(list)
    bike2_list = pyqtSignal(list)
    power_up_list = pyqtSignal(list)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        GameLoop.__init__(self)
        #super(GameThread, self).__init__()

        self.directions = {0:'up', 1:'down', 2:'left', 3:'right'} #kann auch egal sein.


        ##
        action_dim = 4
        state_dim = len(self.get_som_state())
        print("State dim {}".format(state_dim))
        self.state_dim = state_dim
        #self.brain = Dqn(state_dim,action_dim,0.9)
        #self.brain = Dqn(5,4,0.8)
        # state: 
        #last_reward = 0
        scores = []
        ##

        #len(self.blocked_blocks)*2
        #np.array(self.blocked_blocks).flatten()




    def run(self):
        last_reward = 0.0
        #  Counts game tact
        tact_counter = 0
        bike_length = len(self.bike_2.bike)
        while True:

            #random direction
            #the_direc = self.directions[random.randint(0,3)]#
            #self.bike_2.set_direction(the_direc)#

            #last_signal = self.get_som_state()#np.array(self.get_som_state(), dtype=int).tolist()
            #last_signal = np.array(self.get_som_state(), dtype=float).tolist()
            #print(last_signal)
            #action = self.brain.update(last_reward, last_signal)

            ##the_direc_idx = int(action.numpy())
            ##the_direc = self.directions[the_direc_idx]
            ##self.bike_1.set_direction(the_direc)#


            #action = self.brain.update(0.5, [0.5]*self.state_dim)

            smaller_tact = self.game_step(tact_counter)

            #  Emit power up list
            self.power_up_list.emit(self.powerUp.position)

            #  Break loop when one bike has lost. Das ist noch unsauber
            #if (len(self.bike_1.bike) <= 0) or (len(self.bike_2.bike) <= 0):
            #    break
            #  Win condition can be implemented here.


            # Das hier sind die win conditions
            if len(self.bike_1.bike) <= 0:
                self.bike_1.spawn_bike(70,70)
                self.bike_2.spawn_bike(150,150)
                #last_reward = -1.
            if len(self.bike_2.bike) <= 0:
                self.bike_1.spawn_bike(70,70)
                self.bike_2.spawn_bike(150,150)
                #last_reward = 1.
            if len(self.bike_1.bike) >= 30:
                self.bike_1.spawn_bike(70,70)
                self.bike_2.spawn_bike(70,70)
                #last_reward = 1.
            if len(self.bike_2.bike) >= 30:
                self.bike_1.spawn_bike(70,70)
                self.bike_2.spawn_bike(70,70)
                #last_reward = -1.





            self.bike2_list.emit(self.bike_2.bike)
            self.bike1_list.emit(self.bike_1.bike) # auch an den update gebunden
            
            #time.sleep(gameconfig.game_tact)
            time.sleep(gameconfig.game_base_tact / smaller_tact * gameconfig.game_tact)
            tact_counter += 1

        while True:
            #  BLACK RED LOST WON
            time.sleep(0.1)
    '''
    def get_som_state(self):
        blocked = np.array(self.blocked_blocks).flatten()
        bike_1_blocked = np.zeros(30, dtype=int)
        bike_1_blocked[0:len(self.bike_1.bike)] = 1
        bike_2_blocked = np.zeros(30, dtype=int)
        bike_2_blocked[0:len(self.bike_2.bike)] = 1
        bike_1 = np.ones((30, 2), dtype=int)*100#-1
        bike_2 = np.ones((30, 2), dtype=int)*100
        bike_1[0:len(self.bike_1.bike)] = np.array(self.bike_1.bike)
        bike_2[0:len(self.bike_2.bike)] = np.array(self.bike_2.bike)
        #bike_1 = bike_1.flatten()
        #bike_2 = bike_2.flatten()
        return np.concatenate([blocked.flatten(),
                                bike_1_blocked.flatten(),
                                bike_2_blocked.flatten(),
                                bike_1.flatten(),
                                bike_2.flatten()])
    

    def get_som_state(self):
        bike_1 = np.zeros((30, 2), dtype=float)
        bike_1[0:len(self.bike_1.bike)] = np.array(self.bike_1.bike, dtype=float)
        return bike_1.flatten()
    '''

    '''
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
        '''
