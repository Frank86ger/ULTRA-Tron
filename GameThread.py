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

class GameThread(QThread):

    bike1_list = pyqtSignal(list)
    bike2_list = pyqtSignal(list)
    power_up_list = pyqtSignal(list)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)

        #  Set up bikes, board and power ups.
        self.bike_1 = TronBike()
        self.bike_2 = TronBike()
        self.board_blocks = BoardBlocks()

        self.board_blocks.load_level(gameconfig.level_name)
        self.blocked_blocks = self.board_blocks.blocked_blocks

        self.powerUp = PowerUp(self.bike_1, self.bike_2)
    
    def run(self):
        
        #  Counts game tact
        tact_counter = 0

        while True:

            #  Spawn Power Up.
            if (tact_counter+1)%self.powerUp.next_spawn_ticks == 0:
                self.powerUp.spawn_powerup(tact_counter)

            #  Step bike 1
            if tact_counter%self.bike_1.bike_tact == 0:
                self.bike_1.do_next_step(tact_counter)
            
            #  Step bike 2
            if tact_counter%self.bike_2.bike_tact == 0:
                self.bike_2.do_next_step(tact_counter)

            #  Collision detection and emit of signals
            smaller_tact = min(self.bike_1.bike_tact, self.bike_2.bike_tact)
            if tact_counter%smaller_tact == 0:
                
                #  Collision of powerUp with bikes?
                self.powerUp.bike_collision(tact_counter)
                
                #  Check if power hup time has run out
                self.powerUp.despawn_power_up(tact_counter)
                
                #  CHeck bike-bike collision
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

                #  Emit power up list
                self.power_up_list.emit(self.powerUp.position)

                #  Break loop when one bike has lost.
                if (len(self.bike_1.bike) <= 0) or (len(self.bike_2.bike) <= 0):
                    break
                
                #  Win condition.

                self.bike2_list.emit(self.bike_2.bike)
                self.bike1_list.emit(self.bike_1.bike) # auch an den update gebunden
            
            #time.sleep(gameconfig.game_tact)
            time.sleep(gameconfig.game_base_tact / smaller_tact * gameconfig.game_tact)
            tact_counter += 1

        while True:
            #  BLACK RED LOST WON
            time.sleep(0.1)

