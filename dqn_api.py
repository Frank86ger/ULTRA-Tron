from dqn import Dqn


class AI(object):
    def __init__(self, state_size, discount, load_path):
        print("{0} dqn loaded!".format(load_path))
        action_size = 4
        self.brain = Dqn(state_size, action_size, discount)
        self.directions = {0: 'up', 1: 'down', 2: 'left', 3: 'right'}

    def update(self, last_reward, last_signal, mem_idx):
        action = self.brain.update(last_reward, last_signal, mem_idx=mem_idx)
        the_direc_idx = int(action.numpy())
        return self.directions[the_direc_idx]

    def save(self, path):
        self.brain.save(path)
