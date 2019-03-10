#from PyQt5.QtCore import QObject, pyqtSignal, QThread, pyqtSlot
from PyQt5.QtCore import pyqtSignal, QThread
import time
import gameconfig
from GameLoop import GameLoop


class GameThread(QThread, GameLoop):

    bike1_list = pyqtSignal(list)
    bike2_list = pyqtSignal(list)
    power_up_list = pyqtSignal(list)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        GameLoop.__init__(self)
        # super(GameThread, self).__init__()

    def run(self):

        tact_counter = 0
        while True:

            smaller_tact = self.game_step(tact_counter)

            # gamemode = gameconfig.gamemode
            # Das hier sind die win conditions
            if len(self.bike_1.bike) <= 0:
                self.bike_1.spawn_bike(50, 50)
                self.bike_2.spawn_bike(50, 50)
            if len(self.bike_2.bike) <= 0:
                self.bike_1.spawn_bike(50, 50)
                self.bike_2.spawn_bike(50, 50)
            if len(self.bike_1.bike) >= 30:
                self.bike_1.spawn_bike(50, 50)
                self.bike_2.spawn_bike(50, 50)
            if len(self.bike_2.bike) >= 30:
                self.bike_1.spawn_bike(50, 50)
                self.bike_2.spawn_bike(50, 50)

            # Emits
            # Emit power up list
            self.power_up_list.emit(self.powerUp.position)

            self.bike2_list.emit(self.bike_2.bike)
            self.bike1_list.emit(self.bike_1.bike)  # auch an den update gebunden
            
            # time.sleep(gameconfig.game_tact)
            time.sleep(gameconfig.game_base_tact / smaller_tact * gameconfig.game_tact)
            tact_counter += 1

        while True:
            #  BLACK RED LOST WON
            time.sleep(0.1)

    def save_dqn(self):
        if gameconfig.bike1_player == 'ai':
            self.ais['bike_1'].save()

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
