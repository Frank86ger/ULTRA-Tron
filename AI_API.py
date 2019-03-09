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
import random

# einen random input blub machen!

#ewige loop !
#Da der Init sich immer wiederholt, waere hier mehrfachvererbung sinnvoll, da __init__ immer gleich ist.
class CvCTrain(GameLoop):

    def __init__(self, record_replay=False):
        self.record_replay = record_replay
        #self.directions = {'up':0, 'down':1, 'left':2, 'right':3}
        self.directions = {0:'up', 1:'down', 2:'left', 3:'right'}
        GameLoop.__init__(self)

    def run(self):
        
        #  Counts game tact
        tact_counter = 0

        while True:
            #ok wie aendder ich die richtung?
            the_direc = self.directions[random.randint(0,3)]
            self.bike_1.set_direction(the_direc)
            #self.bike_2.set_direction(the_direc)
            print(tact_counter)



            #  Break loop when one bike has lost. Das ist noch unsauber
            if len(self.bike_1.bike) <= 0:
                self.bike_1.spawn_bike(70,70)
                self.bike_2.spawn_bike(70,70)
                #kein break -> reinit beide
            if len(self.bike_2.bike) <= 0:
                self.bike_1.spawn_bike(70,70)
                self.bike_2.spawn_bike(70,70)


            smaller_tact = self.game_step(tact_counter)

            tact_counter += 1

            #hier definiere ich auch die rewards?

            # win condition
        
         #next game?


class CvCPlayReplay(object):
    def __init__(self):
        pass
        #TODO
        #Ne, das hier ist nur zum trainieren - komplett ohne pyqt






if __name__ == "__main__":
    trainer = CvCTrain()
    trainer.run()