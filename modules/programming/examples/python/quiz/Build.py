import os
import sys
import random

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SRC_ROOT = os.path.join(PROJECT_ROOT, "src")

if SRC_ROOT not in sys.path:
    sys.path.insert(0, SRC_ROOT)

from dataclasses import dataclass
from typing import Callable, List, Tuple, Dict, Any

from modules.programming.examples.python.quiz.Quiz import Quiz



class Build:
    """
    Thin wrapper class you can plug into your app (e.g. Kivy).

    Assumes MorphicSemanticEngine already exists in mse.core.
    No changes made to that core.
    """

    def __init__(self, **kwargs):
        self.code = None
        self.questions = ["a", "b", "c", "d", "e"]
        self.answers = ["1", "2", "3", "4", "5"]

        self.session = Quiz()

        self.build_and_run_quiz([676, 612, 550, 490, 432])


    def get_code(self):
        self.code = [
            "def run_quiz():",
            "    questions = [",
            self.get_questions(),
            "    ]",
            "    correct_answers = [",
            self.get_answers(),
            "    ]",
            "    print('Answer the following U.S. history statements as True or False (T/F):\\n')",
            "    user_answers = []",
            "    for i, q in enumerate(questions, start=1):",
            "        while True:",
            "            raw = input(f'{i}. {q} (T/F): ').strip().lower()",
            "            if raw in ('t', 'true', 'f', 'false'):",
            "                user_answers.append(raw.startswith('t'))",
            "                break",
            "            else:",
            "                print(\"Please type 'T' or 'F' (or 'true'/'false').\")",
            "    score = 0",
            "    print('\\nResults:')",
            "    for i, (q, correct, user) in enumerate(zip(questions, correct_answers, user_answers), start=1):",
            "        is_correct = (correct == user)",
            "        if is_correct:",
            "            score += 1",
            "        correct_str = 'True' if correct else 'False'",
            "        user_str = 'True' if user else 'False'",
            "        status = '✅ Correct' if is_correct else '❌ Wrong'",
            "        print(f'{i}. {q}')",
            "        print(f'   Your answer: {user_str} | Correct: {correct_str} -> {status}')",
            "    print(f'\\nScore: {score} / {len(questions)}')"
        ]
        
  
    def get_questions(self):
        lines = []
        for q in self.questions:
            lines.append(f"        {repr(q)},")
        return lines
    

    def get_answers(self):
        lines = []
        for a in self.answers:
            lines.append(f"        {repr(a)},")
        return lines
    

    ###array of words for token stream..need to create a system that selects questions and answers based on a formula similar to ratings in fitness app
    def build_quiz_source(self, seed=[676, 612, 550, 490, 432], count=10) -> str:

        self.questions, self.answers = self.session.generate_seed(seed, count)

        print("\n\nquestions")
        print(self.questions)
        print("\nanswers")
        print(self.answers)
        self.get_code()

        lines: List[str] = []

        for line in self.code:
            if isinstance(line, list):
                lines.extend(line)
            else:
                lines.append(line)

        return "\n".join(lines)



    def build_and_run_quiz(self, seed: List[int], count: int = 10) -> None:
        """
        High-level demonstration:

        - Uses your MSE core + grammar to generate questions/answers.
        - Uses those to *write* a Python function's source code.
        - Compiles and executes that generated code.
        - Calls run_quiz().

        This shows "MSE writes Python code efficiently from a small seed".
        """
        src = self.build_quiz_source(seed, count)

        code_obj = compile(src, "<mse_generated_quiz>", "exec")
        ns: Dict[str, Any] = {}
        exec(code_obj, ns)

        ns["run_quiz"]()


Build()