from dqn import Dqn


class AI(object):
    def __init__(self, state_size, discount, load_path):
        print("{0} dqn loaded!".format(load_path))
        action_size = 4
        self.brain = Dqn(state_size, action_size, discount)
        self.load(load_path) ##############
        self.directions = {0: 'up', 1: 'down', 2: 'left', 3: 'right'}
        self.loss = []
        self.probs = []

    def update(self, last_reward, last_signal, mem_idx, poison):
        action = self.brain.update(last_reward, last_signal, mem_idx=mem_idx, push=not poison)
        the_direc_idx = int(action.numpy())
        self.get_loss(self.brain.loss)
        self.get_probs(self.brain.probs)
        return self.directions[the_direc_idx]

    def get_loss(self, loss):
        self.loss.append(loss)
        if len(self.loss) > 100:
            self.loss.pop(0)

    def get_probs(self, probs):
        if probs is None:
            probs = [0., 0., 0., 0.]
        self.probs.append(sorted(probs))
        if len(self.probs) > 100:
            self.probs.pop(0)

    def save(self, path):
        self.brain.save(path)

    def load(self, path):
        self.brain.load()

