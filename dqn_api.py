from dqn import Dqn


brain = Dqn(5,4,0.8)

class AI(object):
    def __init__(self, state_size, discount, path):
        action_size = 4
        self.brain = Dqn(state_size,action_size,discount)
        self.directions = {0:'up', 1:'down', 2:'left', 3:'right'} #kann auch egal sein?

    def update(self, last_reward, last_signal, mem_idx):
        action = self.brain.update(last_reward, last_signal, mem_idx=mem_idx)
        the_direc_idx = int(action.numpy())
        return self.directions[the_direc_idx]

        #update
