import numpy as np
from mesa.agent import Agent

class BoundedConfidenceAgent(Agent):
    def __init__(self, model, opinion):
        """
        Initialize an agent for the Bounded Confidence Model.
        Args:
            unique_id: the agent's unique identifier.
            model: the model instance.
            opinion: a real number in [0, 1] representing the agent's opinion.
        """
        super().__init__(model=model)
        self.opinion = opinion
        self._next_opinion = None

    def step(self):
        epsilon = self.model.epsilon
        mu = self.model.mu
        delta = 0
        num_interacted = 0

        for agent in self.model.agents:
            if self == agent:
                continue
            if self.model.model_type == "group symmetric":
                to_interact = abs(self.opinion - agent.opinion) <= epsilon
            elif self.model.model_type == "group asymmetric":
                to_interact = (agent.opinion >= self.opinion - epsilon[0]) and \
                              (agent.opinion <= self.opinion + epsilon[1])
            else:
                to_interact = False

            if to_interact:
                delta += agent.opinion - self.opinion
                num_interacted += 1

        D = 0 if num_interacted == 0 else 1 / num_interacted
        self._next_opinion = self.opinion + mu * D * delta

    def advance(self):
        self.opinion = self._next_opinion

