"""CLI for cognitive-reflection-synthesis-engine."""
import sys
import argparse
from .engine import ReflectionEngine


def main():
    parser = argparse.ArgumentParser(description="Cognitive Reflection Synthesis Engine CLI")
    parser.add_argument("--demo", action="store_true", help="Run cognitive self-reflection synthesis demo")
    args = parser.parse_args()

    if args.demo:
        engine = ReflectionEngine()
        steps = [
            {"tool": "bash", "cmd": "pytest", "success": False, "error": "ImportError"},
            {"tool": "edit_file", "path": "main.py", "success": True},
            {"tool": "bash", "cmd": "pytest", "success": True}
        ]
        report = engine.reflect_on_trajectory("fix_unit_tests", steps)
        print("Self-Reflection Report:")
        print(f"  Task: {report.task_name} | Steps: {report.total_steps} | Errors: {report.error_count}")
        print("Synthesized Heuristics:")
        for h in report.extracted_heuristics:
            print(f"  -> {h}")

        print("
Generated Prompt Patch:")
        print(engine.get_system_prompt_patch())
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
