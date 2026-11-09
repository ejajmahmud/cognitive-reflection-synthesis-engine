"""Core Cognitive Reflection Synthesis Engine implementation."""
from typing import Dict, List, Optional, Tuple, Any


class ReflectionReport:
    def __init__(self, task_name: str, total_steps: int, error_count: int, extracted_heuristics: List[str]):
        self.task_name = task_name
        self.total_steps = total_steps
        self.error_count = error_count
        self.extracted_heuristics = extracted_heuristics


class ReflectionEngine:
    def __init__(self):
        self.persistent_heuristics: List[str] = []

    def reflect_on_trajectory(self, task_name: str, step_records: List[Dict[str, Any]]) -> ReflectionReport:
        errors = [s for s in step_records if not s.get("success", True)]
        heuristics = []

        # Analyze error patterns
        tools_with_errors = set(s.get("tool") for s in errors if s.get("tool"))
        for tool in tools_with_errors:
            heuristics.append(f"Tool [{tool}] encountered failures: verify input parameter constraints before calling.")

        # Check for excessive iteration
        if len(step_records) > 10:
            heuristics.append("Trajectory length was high (>10 steps): consider decomposing goal into sub-milestones earlier.")

        if not errors:
            heuristics.append("Clean execution: replicate tool sequence pattern for similar tasks.")

        # Store heuristics
        for h in heuristics:
            if h not in self.persistent_heuristics:
                self.persistent_heuristics.append(h)

        return ReflectionReport(task_name, len(step_records), len(errors), heuristics)

    def get_system_prompt_patch(self) -> str:
        if not self.persistent_heuristics:
            return ""
        rules = "\n".join(f"- {h}" for h in self.persistent_heuristics)
        return f"\n[LEARNED AGENT HEURISTICS - DERIVED FROM PREVIOUS RUNS]:\n{rules}\n"
