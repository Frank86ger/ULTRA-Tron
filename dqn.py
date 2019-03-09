
import numpy as np
import random
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.autograd as autograd
from collections import namedtuple

Transition = namedtuple('Transition', ('state', 'action', 'next_state', 'reward'))

# Network for Q learning
class Network(nn.Module):
    
    def __init__(self, state_size, first_hidden_size, second_hidden_size, q_size):
        super(Network, self).__init__()
        self.fc1 = nn.Linear(state_size, first_hidden_size)
        self.fc2 = nn.Linear(first_hidden_size, second_hidden_size)
        self.fc3 = nn.Linear(second_hidden_size, q_size)

    def forward(self, state):
        #first_hidden = F.tanh(self.fc1(state))
        #second_hidden = F.tanh(self.fc2(first_hidden))
        #q_values = F.tanh(self.fc3(second_hidden))
        first_hidden = F.relu(self.fc1(state))
        second_hidden = F.relu(self.fc2(first_hidden))
        q_values = self.fc3(second_hidden)
        return q_values


class ReplayMemory(object):

    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
        self.position = 0

    def push(self, *args):
        """Saves a transition."""
        if len(self.memory) < self.capacity:
            self.memory.append(None)
        self.memory[self.position] = Transition(*args)
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)




class Dqn():
    
    def __init__(self, input_size, nb_action, gamma):
        self.gamma = gamma
        #self.model = Network(input_size, 60, 30, nb_action)
        self.model = Network(input_size, 40, 40, nb_action)
        self.memory = [ReplayMemory(10000), ReplayMemory(10000)]
        self.optimizer = optim.Adam(self.model.parameters(), lr = 0.001)
        self.last_state = torch.Tensor(input_size)#.unsqueeze(0)
        self.last_action = 0
        self.last_reward = 0

    def select_action(self, state, temperature):
        probs = F.softmax(self.model(state)*temperature, dim=0) # T=100
        #print("Probs :: {}".format(probs))
        action = probs.multinomial(1)
        return action.data[0]

    def learn(self, batch_transitions):
        # oder kann ich hier stacken?
        batch_tmp = Transition(*zip(*batch_transitions))
        batch = Transition(*[torch.stack(x) for x in batch_tmp])
        #print("batch.state :::: {}".format(batch.state))
        #print("batch.state  size :::: {}".format(batch.state.size()))
 
        chosen_state_action_values = self.model(batch.state).gather(1, batch.action).squeeze(1)
        max_q_values = self.model(batch.next_state).detach().max(1)[0]#.unsqueeze(1)
        #print("Mean chosn Q :: {}".format(chosen_state_action_values.mean()))
        #print("Mean Q :: {}",format(self.model(batch.state).mean()))
        #print("Mean max Q :: {}".format(max_q_values.mean()))

        #print("QQ1 ::: {} --> {}".format(chosen_state_action_values.size(), chosen_state_action_values))
        #print("QQ2 ::: {} --> {}".format(max_q_values.size(), max_q_values))

        target = self.gamma * max_q_values + batch.reward
        td_loss = F.smooth_l1_loss(chosen_state_action_values, target)
        #print("Loss :: {}".format(td_loss))
        self.optimizer.zero_grad()
        td_loss.backward()
        self.optimizer.step()
        #print(max_q_values)
        #print((self.model(torch.tensor([0.5]*6))))

    def update(self, reward, new_signal, mem_idx=0):
        #new_signal kann auch new_state heissen oder?
        new_state = torch.Tensor(new_signal).float()
        #('state', 'action', 'next_state', 'reward')
        #print(int(self.last_action))
        self.memory[mem_idx].push(self.last_state, torch.LongTensor([int(self.last_action)]), new_state, torch.Tensor([self.last_reward]))
        #self.memory.push(self.last_state, torch.Tensor([int(self.last_action)]).int(), new_state, torch.Tensor([self.last_reward]))
        action = self.select_action(new_state, 1.)
        if len(self.memory[mem_idx].memory) > 100:
            batch_transitions = self.memory[mem_idx].sample(100)
            self.learn(batch_transitions)
        if len(self.memory[mem_idx].memory) > 100:
            batch_transitions = self.memory[mem_idx].sample(100)
            self.learn(batch_transitions)
        
        self.last_action = action
        self.last_reward = reward
        self.last_state = new_state

        #print(int(self.last_action))

        #print(torch.LongTensor([int(self.last_action)]))
        return action



if __name__=='__main__':
    ''''''
    import random
    brain = Dqn(6,4,0.8)
    
    for i in range(150):
        #reward, state
        
        brain.update(random.random(), torch.rand(6))
    
    #print(torch.rand(6))
    #print(brain.memory.memory)
