"""Unit tests for cognitive-reflection-synthesis-engine."""
import unittest
from cognitive_reflection_synthesis_engine.engine import ReflectionEngine


class TestReflectionEngine(unittest.TestCase):
    def setUp(self):
        self.engine = ReflectionEngine()

    def test_reflection_on_clean_run(self):
        steps = [{"tool": "read", "success": True}, {"tool": "write", "success": True}]
        rep = self.engine.reflect_on_trajectory("task1", steps)
        self.assertEqual(rep.error_count, 0)
        self.assertIn("Clean execution", rep.extracted_heuristics[0])

    def test_reflection_on_error(self):
        steps = [{"tool": "sql", "success": False, "error": "Table not found"}]
        rep = self.engine.reflect_on_trajectory("task2", steps)
        self.assertEqual(rep.error_count, 1)
        self.assertIn("sql", rep.extracted_heuristics[0])
        patch = self.engine.get_system_prompt_patch()
        self.assertIn("LEARNED AGENT HEURISTICS", patch)
