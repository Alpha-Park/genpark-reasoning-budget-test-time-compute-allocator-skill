# -*- coding: utf-8 -*-
"""
GenPark Reasoning Budget Test-Time Compute Allocator Client
Dynamically schedules thinking token budgets, reflection passes, and temperature annealing based on problem entropy.
Zero external dependencies -- Python 3.9+ standard library only.
"""

import math
from typing import Dict, Any, List

class GenParkReasoningBudgetTestTimeComputeAllocator:
    """
    Test-Time Compute (TTC) Optimizer (DeepSeek-R1 / o1 Paradigm):
    Estimates intrinsic problem difficulty and calculates optimal thinking token limits,
    self-consistency sampling count (N), and reflection depth.
    """

    DIFFICULTY_KEYWORDS = {
        "prove": 2.5, "theorem": 2.2, "invariant": 2.8, "contrapositive": 2.0,
        "integral": 1.8, "differential": 1.9, "asymptotic": 2.1, "np-hard": 3.0,
        "dynamic programming": 2.4, "recursive": 1.5, "combinatorics": 2.2,
        "counterexample": 2.0, "verify": 1.4, "calculate": 1.0, "sum": 0.8
    }

    def __init__(self, min_thinking_tokens: int = 1024, max_thinking_tokens: int = 32768):
        self.min_tokens = min_thinking_tokens
        self.max_tokens = max_thinking_tokens

    def estimate_problem_complexity(self, prompt: str) -> float:
        """
        Calculates normalized complexity score (1.0 to 10.0) based on
        lexical entropy, reasoning keywords, and constraint density.
        """
        words = prompt.lower().split()
        if not words:
            return 1.0

        # 1. Keyword semantic weight
        kw_score = 0.0
        for w in words:
            for kw, wt in self.DIFFICULTY_KEYWORDS.items():
                if kw in w:
                    kw_score += wt

        # 2. Shannon character entropy
        char_counts = {}
        for c in prompt.lower():
            if c.isalnum():
                char_counts[c] = char_counts.get(c, 0) + 1
        total_chars = sum(char_counts.values()) or 1
        entropy = -sum((cnt / total_chars) * math.log2(cnt / total_chars) for cnt in char_counts.values())

        # 3. Numeric & symbolic density
        sym_count = sum(1 for c in prompt if c in "=+-*/^<>{}[]()_")
        sym_density = min(3.0, (sym_count / max(1, len(words))) * 4.0)

        raw_score = 1.0 + (kw_score * 0.45) + (entropy * 0.8) + sym_density
        return round(max(1.0, min(10.0, raw_score)), 2)

    def allocate_compute_budget(
        self,
        problem_statement: str,
        target_accuracy_mode: str = "HIGH_VERIFICATION",
        max_latency_budget_sec: float = 60.0
    ) -> Dict[str, Any]:
        """
        Allocates exact token budget, best-of-N sample count, and temperature schedule.
        """
        complexity = self.estimate_problem_complexity(problem_statement)

        # Sigmoid token allocation curve
        # High complexity -> approaches 32,768 tokens; Simple problem -> approaches 1,024 tokens
        midpoint = 5.0
        k = 0.8
        logistic = 1.0 / (1.0 + math.exp(-k * (complexity - midpoint)))
        allocated_tokens = int(self.min_tokens + logistic * (self.max_tokens - self.min_tokens))

        # Self-consistency sample count (N)
        if target_accuracy_mode == "MAXIMUM_REASONING_BENCHMARK":
            sample_count = 16 if complexity >= 7.5 else (8 if complexity >= 4.5 else 4)
            temp = 0.65
        elif target_accuracy_mode == "HIGH_VERIFICATION":
            sample_count = 8 if complexity >= 7.0 else (4 if complexity >= 4.0 else 2)
            temp = 0.50
        else: # FAST_INTERACTIVE
            sample_count = 1
            temp = 0.20

        # Reflection passes recommended
        reflection_passes = max(1, int(round(complexity / 2.5)))

        return {
            "estimated_problem_complexity_score": complexity,
            "complexity_grade": "OLYMPIAD_RESEARCH" if complexity >= 8.0 else ("COMPLEX_MULTI_HOP" if complexity >= 5.0 else "STANDARD_DEDUCTION"),
            "allocated_thinking_tokens": allocated_tokens,
            "sampling_best_of_n_count": sample_count,
            "recommended_sampling_temperature": temp,
            "recommended_reflection_passes": reflection_passes,
            "estimated_reasoning_duration_sec": round(min(max_latency_budget_sec, (allocated_tokens / 1000.0) * 1.8), 1),
            "test_time_compute_profile": {
                "system_2_deliberate_search": (complexity >= 4.0),
                "enable_mcts_rollouts": (complexity >= 7.0),
                "token_budget_utilization_pct": round((allocated_tokens / self.max_tokens) * 100.0, 1)
            }
        }
