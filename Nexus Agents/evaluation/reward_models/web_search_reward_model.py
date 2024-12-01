from evaluation.reward_models.based_reward_model import BaseRewardModel
from evaluation.metrics.accuracy import search_result_quality_metric

class WebSearchRewardModel(BaseRewardModel):
    def __init__(self):
        pass

    def get_reward(self, input, output, expected_output):
        reward = search_result_quality_metric(input, output, expected_output)
        return reward.score, reward.reason

    def get_aggregate_reward(self, inputs, outputs, expected_outputs, agg="mean"):
        scores = []
        for input, output, expected_output in zip(inputs, outputs, expected_outputs):
            score, _ = self.get_reward(input, output, expected_output)
            scores.append(score)
        if agg == "mean":
            return sum(scores) / len(scores)
        elif agg == "sum":
            return sum(scores)
        else:
            raise ValueError(f"Invalid aggregation method: {agg}")


