import numpy as np
from mesa.agent import Agent


class BoundedConfidenceAgent(Agent):
    def __init__(self, model, opinion):
        """ Initialize an agent for Bounded Confidence Model

        Args:
            opinion: a real number in [0, 1]
        """

        super().__init__(model=model)
        self.opinion = opinion
        self._next_opinion = None





