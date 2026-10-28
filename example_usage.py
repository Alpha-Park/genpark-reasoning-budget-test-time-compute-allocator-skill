# -*- coding: utf-8 -*-
"""
Example usage of GenParkReasoningBudgetTestTimeComputeAllocator
Demonstrates dynamic thinking token budgeting across varying complexity tiers.
"""

from client import GenParkReasoningBudgetTestTimeComputeAllocator

def main():
    allocator = GenParkReasoningBudgetTestTimeComputeAllocator()

    problems = [
        {
            "name": "Problem 1: Elementary Arithmetic",
            "text": "What is the total sum of 45 and 92?",
            "mode": "FAST_INTERACTIVE"
        },
        {
            "name": "Problem 2: Olympiad Level Math Proof",
            "text": "Prove that for any prime p > 3, p^2 - 1 is always divisible by 24 using modular arithmetic and prime invariants.",
            "mode": "MAXIMUM_REASONING_BENCHMARK"
        }
    ]

    print("================================================================")
    print("GenPark Reasoning Budget Allocator - Live Schedules")
    print("================================================================\n")

    for p in problems:
        res = allocator.allocate_compute_budget(p["text"], p["mode"])
        print(f"[{p['name']}]")
        print(f"  Complexity Score      : {res['estimated_problem_complexity_score']} / 10.0 [{res['complexity_grade']}]")
        print(f"  Thinking Token Budget : {res['allocated_thinking_tokens']:,} tokens ({res['test_time_compute_profile']['token_budget_utilization_pct']}%)")
        print(f"  Self-Consistency (N)  : Best-of-{res['sampling_best_of_n_count']} (Temp: {res['recommended_sampling_temperature']})")
        print(f"  Reflection Depth      : {res['recommended_reflection_passes']} passes")
        print(f"  MCTS Rollouts Active  : {res['test_time_compute_profile']['enable_mcts_rollouts']}\n")

if __name__ == "__main__":
    main()
