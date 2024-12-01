
from abc import ABC, abstractmethod

class BaseRewardModel(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_reward(self, input, output, expected_output):
        pass

