from lesson_list import lesson_list

class LessonPlan:


    def __init__(self, user_id=None, **kwargs):
        super().__init__(**kwargs)


    def after_test(self, results):
        for question in results.items():
            self.adjust_related(question["question"], question["answer"])

    def adjust_related(self, question, answer):
        adjust = 5 if answer == True else -5
        for item in lesson_list:
            for term in item[list(item.keys())[0]]["data"]:
                term["rating"] = term["rating"] + adjust if len([x for x in term["attributes"] if question == x]) > 0 else term["rating"]