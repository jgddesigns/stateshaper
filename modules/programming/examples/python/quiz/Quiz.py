import os
import sys
import random

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SRC_ROOT = os.path.join(PROJECT_ROOT, "src")

if SRC_ROOT not in sys.path:
    sys.path.insert(0, SRC_ROOT)

from dataclasses import dataclass
from typing import Callable, List, Tuple
from mse.core import MorphicSemanticEngine


DOCS = [
    {"name": "the Declaration of Independence", "year": 1776},
    {"name": "the U.S. Constitution", "year": 1787},
    {"name": "the Bill of Rights", "year": 1791},
]

YEAR_POOL = [1776, 1783, 1787, 1791, 1861, 1920]

PRESIDENTS = [
    "George Washington",
    "John Adams",
    "Thomas Jefferson",
    "Abraham Lincoln",
]

WAR_FACTS = [
    {"name": "the American Civil War", "start_year": 1861},
]

PURCHASE_FACTS = [
    {"name": "the Louisiana Purchase", "country_true": "France", "country_false": "Spain"},
]

AMENDMENTS = [
    {
        "name": "the 19th Amendment",
        "true_year": 1920,
        "topic": "granted women the right to vote",
        "false_years": [1910, 1915, 1930],
    }
]

FOUNDING_FATHERS = {"George Washington", "John Adams", "Thomas Jefferson"}

BEFORE_1800_PRESIDENTS = {"George Washington", "John Adams", "Thomas Jefferson"}

CIVIL_WAR_PRESIDENT = "Abraham Lincoln"

LOUISIANA_PURCHASE_PRESIDENT = "Thomas Jefferson"



@dataclass
class Template:
    name: str
    generator: Callable[['MorphicSemanticEngine'], Tuple[str, bool]]

    def generate(self, engine: 'MorphicSemanticEngine') -> Tuple[str, bool]:
        return self.generator(engine)


class Quiz:

    TEMPLATE_SPECS = {
        # ORIGINAL 5
        "doc_year": {},
        "first_president": {},
        "war_start_year": {},
        "purchase_country": {},
        "amendment_vote": {},

        # DOC (3)
        "doc_century": {},
        "doc_before_year": {},
        "doc_ordering": {},

        # PRESIDENTS (3)
        "president_before_1800": {},
        "president_founding_father": {},
        "president_civil_war": {},

        # WAR (3)
        "war_century": {},
        "war_before_year": {},
        "war_on_us_soil": {},

        # PURCHASE (3)
        "purchase_century": {},
        "purchase_president": {},
        "purchase_size": {},

        # AMENDMENT (3)
        "amendment_century": {},
        "amendment_topic_statement": {},
        "amendment_expanded_voting": {},
    }

    def __init__(self, **kwargs):
        super(Quiz, self).__init__(**kwargs)

        self.TEMPLATES: List[Template] = [
            Template(name, lambda engine, name=name: self._generate_from_spec(engine, name))
            for name in self.TEMPLATE_SPECS
        ]

        self.total_templates = len(self.TEMPLATES)
        self.total_questions = 20

        self.function_map = {
            "generate_seed": self.generate_seed,
            "run_code": self.run_code,
        }

        self.max_seed = 999

        self.original_seed = 2

        self.seeds_size = 5

        #test if 1 number can be used as a seed. alter length of array for more precision
        # self.starting_seeds = self.get_seeds()

        #arbitray test numbers. based on defined rules, these keys create a token stream chain to compile the data from the map.
        self.starting_seeds = [2, 4, 6, 45, 4]

        self.question_count = 10


    def _generate_from_spec(self, engine, name: str):
        if name == "doc_year":
            idx = engine.step() % len(DOCS)
            doc = DOCS[idx]
            truth = (engine.step() % 2 == 0)

            if truth:
                year = doc["year"]
            else:
                flist = [y for y in YEAR_POOL if y != doc["year"]]
                year = flist[engine.step() % len(flist)]

            return f"{doc['name']} was signed in {year}.", truth

        if name == "first_president":
            idx = engine.step() % len(PRESIDENTS)
            person = PRESIDENTS[idx]
            truth = (person == "George Washington")
            return f"{person} was the first President of the United States.", truth

        if name == "war_start_year":
            war = WAR_FACTS[0]
            truth = (engine.step() % 2 == 0)

            if truth:
                year = war["start_year"]
            else:
                flist = [y for y in YEAR_POOL if y != war["start_year"]]
                year = flist[engine.step() % len(flist)]

            return f"{war['name']} began in {year}.", truth

        if name == "purchase_country":
            p = PURCHASE_FACTS[0]
            truth = (engine.step() % 2 == 0)
            country = p["country_true"] if truth else p["country_false"]
            return f"The {p['name']} was made with {country}.", truth

        if name == "amendment_vote":
            a = AMENDMENTS[0]
            truth = (engine.step() % 2 == 0)

            if truth:
                year = a["true_year"]
            else:
                flist = a["false_years"]
                year = flist[engine.step() % len(flist)]

            return f"{a['name']} {a['topic']} in {year}.", truth

        if name == "doc_century":
            idx = engine.step() % len(DOCS)
            doc = DOCS[idx]
            truth = (engine.step() % 2 == 0)

            century = "18th" if truth else "19th"
            return f"{doc['name']} was created in the {century} century.", truth

        if name == "doc_before_year":
            idx = engine.step() % len(DOCS)
            doc = DOCS[idx]
            truth = (engine.step() % 2 == 0)

            before = [y for y in YEAR_POOL if doc["year"] < y]
            after = [y for y in YEAR_POOL if doc["year"] >= y]

            if truth and before:
                year = before[engine.step() % len(before)]
            else:
                truth = False
                year = after[engine.step() % len(after)]

            return f"{doc['name']} was created before {year}.", truth

        if name == "doc_ordering":
            pairs_true = []
            pairs_false = []

            for i, a in enumerate(DOCS):
                for j, b in enumerate(DOCS):
                    if a["year"] < b["year"]:
                        pairs_true.append((i, j))
                    else:
                        pairs_false.append((i, j))

            truth = (engine.step() % 2 == 0)

            if truth and pairs_true:
                i, j = pairs_true[engine.step() % len(pairs_true)]
            else:
                truth = False
                i, j = pairs_false[engine.step() % len(pairs_false)]

            A = DOCS[i]
            B = DOCS[j]
            return f"{A['name']} was created before {B['name']}.", truth

        if name == "president_before_1800":
            truth = (engine.step() % 2 == 0)
            before = [p for p in PRESIDENTS if p in BEFORE_1800_PRESIDENTS]
            after = [p for p in PRESIDENTS if p not in BEFORE_1800_PRESIDENTS]

            if truth and before:
                person = before[engine.step() % len(before)]
            else:
                truth = False
                person = after[engine.step() % len(after)]

            return f"{person} served as President before 1800.", truth

        if name == "president_founding_father":
            truth = (engine.step() % 2 == 0)
            ff = [p for p in PRESIDENTS if p in FOUNDING_FATHERS]
            nf = [p for p in PRESIDENTS if p not in FOUNDING_FATHERS]

            if truth and ff:
                person = ff[engine.step() % len(ff)]
            else:
                truth = False
                person = nf[engine.step() % len(nf)]

            return f"{person} was one of the Founding Fathers.", truth

        if name == "president_civil_war":
            truth = (engine.step() % 2 == 0)

            if truth:
                person = CIVIL_WAR_PRESIDENT
            else:
                flist = [p for p in PRESIDENTS if p != CIVIL_WAR_PRESIDENT]
                person = flist[engine.step() % len(flist)]

            return f"{person} was President during the American Civil War.", truth

        if name == "war_century":
            war = WAR_FACTS[0]
            truth = (engine.step() % 2 == 0)

            century = "19th" if truth else "18th"
            return f"{war['name']} began in the {century} century.", truth

        if name == "war_before_year":
            war = WAR_FACTS[0]
            truth = (engine.step() % 2 == 0)

            before = [y for y in YEAR_POOL if war["start_year"] < y]
            after = [y for y in YEAR_POOL if war["start_year"] >= y]

            if truth and before:
                year = before[engine.step() % len(before)]
            else:
                truth = False
                year = after[engine.step() % len(after)]

            return f"{war['name']} began before {year}.", truth

        if name == "war_on_us_soil":
            war = WAR_FACTS[0]
            truth = (engine.step() % 2 == 0)
            place = "U.S. soil" if truth else "Europe"
            return f"{war['name']} was fought mostly on {place}.", truth

        if name == "purchase_century":
            p = PURCHASE_FACTS[0]
            truth = (engine.step() % 2 == 0)

            century = "19th" if truth else "18th"
            return f"The {p['name']} took place in the {century} century.", truth

        if name == "purchase_president":
            p = PURCHASE_FACTS[0]
            truth = (engine.step() % 2 == 0)

            if truth:
                pres = LOUISIANA_PURCHASE_PRESIDENT
            else:
                flist = [x for x in PRESIDENTS if x != LOUISIANA_PURCHASE_PRESIDENT]
                pres = flist[engine.step() % len(flist)]

            return f"The {p['name']} occurred under President {pres}.", truth

        if name == "purchase_size":
            p = PURCHASE_FACTS[0]
            truth = (engine.step() % 2 == 0)

            if truth:
                msg = "roughly doubled the size"
            else:
                msg = "had little impact on the size"

            return f"The {p['name']} {msg} of the United States.", truth

        if name == "amendment_century":
            a = AMENDMENTS[0]
            truth = (engine.step() % 2 == 0)
            century = "20th" if truth else "19th"
            return f"{a['name']} was added in the {century} century.", truth

        if name == "amendment_topic_statement":
            a = AMENDMENTS[0]
            truth = (engine.step() % 2 == 0)

            if truth:
                statement = a["topic"]
            else:
                statement = "abolished slavery"

            return f"{a['name']} {statement}.", truth

        if name == "amendment_expanded_voting":
            a = AMENDMENTS[0]
            truth = (engine.step() % 2 == 0)

            if truth:
                msg = "expanded voting rights"
            else:
                msg = "restricted voting rights"

            return f"{a['name']} {msg} in the United States.", truth

        raise ValueError(f"Unknown template: {name}")


    ##currently random questions. alter rules to get personalized questions. 
    def get_vocab(self):
        keys = []
        while len(keys) < self.seeds_size:
            keys.append(self.create_key(len(keys)))
        return keys
    

    def create_key(self, i):
        val = int(round((self.starting_seeds[i] / self.total_questions-1) * 19))
        val = max(0, min(19, val))
        return self.starting_seeds[i] 
    
    ##test to see ifonly one number can be used
    def get_seeds(self):
        seeds=[]
        while len(seeds) < self.seeds_size:
            seeds.append(self.seed_math(len(seeds)))
        return seeds


    def seed_math(self, i):
        i = self.seeds_size if i < 1 else i
        return abs(self.max_seed - (( int(self.original_seed / 2) * i ) % self.max_seed + 1))
        

    def generate_seed(self) -> Tuple[List[str], List[bool]]:
        """
        Use a shared grammar + facts and a seed to generate `count` True/False
        questions and their correct answers.

        No per-quiz questions are stored; everything comes from:
        - TEMPLATES
        - fact tables
        - MSE + seed
        """
        ###array of words for token stream..need to create a system that selects questions and answers based on a formula similar to ratings in fitness app
        engine = MorphicSemanticEngine(            
            initial_state=self.starting_seeds,
            vocab=self.get_vocab(),
            constants={"a": 3, "b": 5, "c": 7, "d": 11},
            mod=9973,
        )

        questions: List[str] = []
        answers: List[bool] = []

        for _ in range(self.question_count):
            template_index = engine.step() % len(self.TEMPLATES)
            q, truth = self.TEMPLATES[template_index].generate(engine)
            questions.append(q)
            answers.append(truth)

        return questions, answers


    def run_code(self, seed: List[int] | None = None, count: int = 10) -> None:
        """
        Simple command-line quiz runner.
        """
        if seed is None:
            seed = [676, 612, 550, 490, 432]

        questions, correct_answers = self.generate_seed(seed, count)

        print("Answer the following U.S. history statements as True or False (T/F):\n")

        user_answers: List[bool] = []
        for i, q in enumerate(questions, start=1):
            while True:
                raw = input(f"{i}. {q} (T/F): ").strip().lower()
                if raw in ("t", "true", "f", "false"):
                    user_answers.append(raw.startswith("t"))
                    break
                else:
                    print("Please type 'T' or 'F' (or 'true'/'false').")

        score = 0
        print("\nResults:")
        for i, (q, correct, user) in enumerate(zip(questions, correct_answers, user_answers), start=1):
            is_correct = (correct == user)
            if is_correct:
                score += 1
            correct_str = "True" if correct else "False"
            user_str = "True" if user else "False"
            status = "✅ Correct" if is_correct else "❌ Wrong"
            print(f"{i}. {q}")
            print(f"   Your answer: {user_str} | Correct: {correct_str} -> {status}")

        print(f"\nScore: {score} / {len(questions)}")