import gameconfig
import numpy as np
import random


class PowerUp(object):
    
    def __init__(self, bike1, bike2):

        #  Dieser name ist RICHTIG scheisse!!!!!
        #  [[position tuples], [types], [stay durations]]
        self.position = [[], [], []]

        self.power_up_types = ['+X', '+velo', '-velo, +X', '+velo, -X']

        self.bike1 = bike1
        self.bike2 = bike2

        self.next_spawn_time = np.random.normal(gameconfig.power_up_spawn_interval, gameconfig.power_up_spawn_variance)
        self.next_spawn_ticks = int(self.next_spawn_time / gameconfig.game_tact)
        self.despawn_tick = -1
        self.power_up_stay_duration = gameconfig.power_up_stay_duration
        self.power_up_stay_ticks = int(self.power_up_stay_duration / gameconfig.game_tact)
    
    def spawn_powerup(self, tact_counter):
        self.position[0].append(self.rtd_for_position())
        self.position[1].append(self.rtd_for_type())
        self.position[2].append(tact_counter + self.power_up_stay_ticks)

        self.next_spawn_time = np.random.normal(gameconfig.power_up_spawn_interval, gameconfig.power_up_spawn_variance)
        self.next_spawn_ticks = int(self.next_spawn_time / gameconfig.game_tact) + tact_counter

    def rtd_for_type(self):
        rnd = random.randint(0, len(self.power_up_types)-1)
        return self.power_up_types[rnd]
    
    def rtd_for_position(self):
        
        board_x_size = int(gameconfig.win_x_size/10)-1
        board_y_size = int(gameconfig.win_y_size/10)-1

        while True:
            rnd_pos = (random.randint(0, board_x_size), random.randint(0, board_y_size))
            
            if (rnd_pos not in self.bike1.bike) and (rnd_pos not in self.bike2.bike) and True:  # .. NICHT IN DER WAND
            
                break
        
        return rnd_pos

    def bike_collision(self, game_tick):

        # schoenere konstruktion moeglich?
        if len(self.position[0]) > 0:
            for (idx, posi) in enumerate(self.position[0]):
                if len(self.bike1.bike) > 0:
                    if self.bike1.bike[0] == posi:
                        self.execute_powerup(self.bike1, self.position[1][idx], game_tick)
                if len(self.bike2.bike) > 0:
                    if self.bike2.bike[0] == posi:
                        self.execute_powerup(self.bike2, self.position[1][idx], game_tick)
                if len(self.bike1.bike) > 0 and len(self.bike2.bike) > 0:
                    # moeglicher fehler wenn einer mit len 1 nen powerup nimmt?
                    if (self.bike1.bike[0] == posi) or (self.bike2.bike[0] == posi):
                        del self.position[0][idx]
                        del self.position[1][idx]
                        del self.position[2][idx]

    @staticmethod
    def execute_powerup(bike, powerup, game_tick):
        if powerup == '+X':
            bike.size_change += 5
        elif powerup == '+velo':
            bike.bike_tact = gameconfig.power_up_increased_velo_tact
            bike.reset_bike_tact_tick = game_tick + int(gameconfig.power_up_velo_duration / gameconfig.game_tact)
        elif powerup == '-velo, +X':
            bike.bike_tact = gameconfig.power_up_decreased_velo_tact
            bike.reset_bike_tact_tick = game_tick + int(gameconfig.power_up_velo_duration / gameconfig.game_tact)
            bike.size_change += 5
        elif powerup == '+velo, -X':
            bike.bike_tact = gameconfig.power_up_increased_velo_tact
            bike.reset_bike_tact_tick = game_tick + int(gameconfig.power_up_velo_duration / gameconfig.game_tact)
            bike.size_change -= 5

    def despawn_power_up(self, game_tick):
        
        if len(self.position[0]) > 0:
            for (idx, life_span) in enumerate(self.position[2]):
                if game_tick >= life_span:
                    del self.position[0][idx]
                    del self.position[1][idx]
                    del self.position[2][idx]
