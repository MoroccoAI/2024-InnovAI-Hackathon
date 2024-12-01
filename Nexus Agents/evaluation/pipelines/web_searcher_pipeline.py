from evaluation.reward_models.web_search_reward_model import WebSearchRewardModel
from evaluation.metrics.memory_efficiency import measure_memory
from evaluation.metrics.latency import measure_latency
import json
import time
import asyncio
from agent_hub.web_searcher.web_searcher import WebSearcher

web_searcher = WebSearcher()
asyncio.run(web_searcher.setup())
web_searcher_benchmark = json.load(open("evaluation/benchmarks_datasets/web_search_benchmark.json"))
web_searcher_reward_model = WebSearchRewardModel()
dataset = web_searcher_benchmark["benchmark_data"][:1]

print("Benchmarking web searcher...")
print("--------------------------------")
print("Memory usage:")
avg_current_memory = []
avg_peak_memory = []
for query in dataset:
    result, current_memory, peak_memory = measure_memory(web_searcher.__call__)({
        "next_agent_input": {
            "query": query["query"]
        }
    })
    avg_current_memory.append(current_memory)
    avg_peak_memory.append(peak_memory)
    time.sleep(1)

print(f"Average current memory: {sum(avg_current_memory) / len(avg_current_memory)} MB")
print(f"Average peak memory: {sum(avg_peak_memory) / len(avg_peak_memory)} MB")

print("--------------------------------")
print("Latency:")
avg_latency = []
for query in dataset:
    result, latency = measure_latency(web_searcher.__call__)({
        "next_agent_input": {
            "query": query["query"]
        }
    })
    avg_latency.append(latency)
    time.sleep(1)

print(f"Average latency: {sum(avg_latency) / len(avg_latency)} seconds")

print("--------------------------------")
print("Quality:")
scores = []
for query in dataset:
    result = web_searcher.__call__({
        "next_agent_input": {
            "query": query["query"]
        }
    })
    score, reason = web_searcher_reward_model.get_reward(query["query"], result, query["expected_answer"])
    scores.append(score)

print(f"Average Quality score: {sum(scores) / len(scores)}")


