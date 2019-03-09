import random
import gameconfig


class TronBike(object):

    def __init__(self):

        self.inital_length = 20
        self.bike = []
        self.directions = {'up':(0,-1), 'down':(0,1), 'left':(-1,0), 'right':(1,0)}
        self.direction = (self.directions['up'])
        
        self.size_change = 0
        self.bike_tact = gameconfig.game_base_tact
        self.reset_bike_tact_tick = -1
        
        self.set_direction('up')
        ##self.spawn_bike(70,70)
        
        #random.randint(5,60)
        #self.spawn_bike(random.randint(5,45),random.randint(5,45))

        self.dqn_path = None
        self.last_reward = 0.0

    def spawn_bike(self, dots_x, dots_y):
        self.bike = []
        start_x = random.randint(self.inital_length+1, dots_x-self.inital_length-1)
        start_y = random.randint(self.inital_length+1, dots_y-self.inital_length-1)
        self.bike.append((start_x, start_y))
        for i in range(self.inital_length-1):
            new_x = self.bike[-1][0] - self.direction[0]
            new_y = self.bike[-1][1] - self.direction[1]
            self.bike.append((new_x, new_y))
    
    #needs rework
    def set_direction(self, direction):
        #  Version A
        #self.direction = self.directions[direction]

        #  Version B (das hier ist nicht ganz sauber .. vllt einfach version A als Standard)
        if (self.directions[direction][0] + self.direction[0], self.directions[direction][1] + self.direction[1]) != (0,0):
            self.direction = self.directions[direction]


    def move_bike(self):
        new_x = self.bike[0][0] + self.direction[0]
        new_y = self.bike[0][1] + self.direction[1]

        if new_x > int(gameconfig.win_x_size/10)-1:
            new_x = 0
        if new_y > int(gameconfig.win_y_size/10)-1:
            new_y = 0
        if new_x < 0:
            new_x = int(gameconfig.win_x_size/10)-1
        if new_y < 0:
            new_y = int(gameconfig.win_y_size/10)-1

        self.bike.insert(0, (new_x, new_y))

    def move(self):
        self.bike.pop(-1)

    def grow(self):
        pass

    def shrink(self):
        self.bike.pop(-1)
        self.bike.pop(-1)
    
    # der name koennte besser sein.
    # ueberlagerung von 2 events muessen sich aufsummieren
    def do_next_step(self, gametime):
        if self.size_change == 0:
            self.move_bike()
            self.move()
        if self.size_change > 0:
            self.move_bike()
            self.grow()
            self.size_change -= 1
        if self.size_change < 0:
            self.move_bike()
            self.shrink()
            self.size_change += 1

    @classmethod
    def bike_bike_collision(cls, bike1, bike2):
        #bei dieser und den naechsten methoden wird auf das erste element von bike zugegriffen
        #die lsite kann aber auch 0 lang sein.
        if len(bike1.bike) > 0:
            if bike1.bike[0] in bike2.bike:
                bike1.size_change -= 5
        if len(bike2.bike) > 0:
            if bike2.bike[0] in bike1.bike:
                bike2.size_change -= 5 
                #pass
    
    def bike_self_collision(self):
        if len(self.bike) > 0: #keine self collision wenn bike 0 lang ist
            if self.bike[0] in self.bike[1:]:
                self.size_change -= 5
    
    def bike_wall_collision(self, blocked_blocks):
        if len(self.bike) > 0:
            if self.bike[0] in blocked_blocks:
                del self.bike[0]

    def reset_bike_tact(self, game_tact):
        if (self.bike_tact != 5) and (game_tact >= self.reset_bike_tact_tick):
            self.bike_tact = 5