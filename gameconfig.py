#Nicht so, sondern als object? Ne denke doch nicht

# Must be multiples of 10!
win_x_size = 1000
win_y_size = 1000

# Power up spawn specs - all in seconds
power_up_stay_duration = 8.
power_up_spawn_interval = 8.
power_up_spawn_variance = 1

# Power up specs
power_up_increased_velo_tact = 4
power_up_decreased_velo_tact = 6
power_up_velo_duration = 8.

# Color palette
blocked_blocks_color = 120,120,120
bike_1_color = 0,0,0
bike_2_color = 255,0,0
power_up_color_1 = 150,30,30
power_up_color_2 = 30,150,30
power_up_color_3 = 150,30,150
power_up_color_4 = 150,150,30
power_up_color_5 = 150,30,150
power_up_color_6 = 30,150,150

level_name = 'ima.bmp'

game_base_tact = 5
game_tact = 0.008  # rename
#game_tact = 0.025


gamemode = 'endless'

bike1_player = 'ai'
bike2_player = 'ai'
#bike2_player = 'human'

bike1_dqn = r'path/to/dqn'
bike2_dqn = r'path/to/dqn2'
bike1_mode = 'learn'
bike2_mode = 'play'

#TODO
#manual train?