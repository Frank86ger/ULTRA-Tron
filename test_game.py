import numpy as np
from ai import Dqn


state_dim = 1
action_dim = 1
brain = Dqn(state_dim, action_dim, 0.9)