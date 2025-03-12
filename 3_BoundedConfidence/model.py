import numpy as np
import random
from mesa.model import Model
from mesa.datacollection import DataCollector
from agent import BoundedConfidenceAgent


class BoundedConfidenceModel(Model):

    def __init__(self, num_agents, mu, epsilon, model_type, max_steps):
        """ Bounded Confidence Model for analysis of consensus and bias in a group.
        We have homogeneous agents, and hence we store mu and epsilon in the model
        but not in agent to save space.

        Args:
            num_agents: number of agents
            mu: convergence parameter, i.e. propensity to adjust own opinion
            epsilon: level of "open-mindedness". It could be a scalar or a vector of two.
                If a vector of two, epsilon[0] is preference for left and epsilon[1] for right
            model_type: "pairwise", "group symmetric", or "group asymmetric"
        """
        super().__init__()
        self.model_type = model_type
        self.max_steps = max_steps
        self.epsilon = epsilon
        self.mu = mu
        self.num_agents = num_agents
        self.step_count = 0

        # Initialize agent opinions.
        opinions = [random.uniform(0, 1) for _ in range(num_agents)]

        # Set up data collection.
        self.datacollector = DataCollector(
            agent_reporters={"Opinion": lambda agent: agent.opinion}
        )

        BoundedConfidenceAgent.create_agents(model=self, n=num_agents, opinion=opinions)

        self.datacollector.collect(self)
        self.running = True

    def step(self):
        """Advance the model by one step."""
        if self.model_type == "pairwise":
            # for this simple case, it is better not to use the ".do()" functions of the agents as only two agents have to interact per time step
            i, j = np.random.choice(self.agents, 2, replace=False)
            if abs(i.opinion - j.opinion) < self.epsilon:
                # make a pairwise interaction among i and j and update their opinions
                ...
            self.step_count += 1
        else:
            # For group updates, use simultaneous activation:
            self.agents.do("step")
            self.agents.do("advance")
            self.step_count += 1

        self.datacollector.collect(self)
        if self.step_count > self.max_steps:
            self.running = False
