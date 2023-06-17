import unittest
import csv
from main import LearnerStep, AddQuestions, QuestionsSetup

class TestLearnerStep(unittest.TestCase):
    def test_load_question_count(self):

        with open("questionss.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(["Question ID", "Question Type", "Question", "Choices", "Answer"])
            writer.writerow(["1333", "Quiz", "What is the capital of France?", "Paris, London, Rome", "paris"])

        learner_step = LearnerStep()
        learner_step.load_question_count()
        self.assertEqual(learner_step.question_count, 1)



    def test_get_enabled_question_count(self):

        with open("questionstatuss.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(["Question ID", "Status"])
            writer.writerow(["1", "enabled"])
            writer.writerow(["2", "disabled"])
            writer.writerow(["3", "enabled"])

        learner_step = LearnerStep()
        enabled_question_count = learner_step.get_enabled_question_count()
        self.assertEqual(enabled_question_count, 2)




    def test_select_activity(self):
        learner_step = LearnerStep()
        user_input = 1
        add_questions = AddQuestions()
        self.assertIsNone(learner_step.select_activity())


class TestAddQuestions(unittest.TestCase):
    def test_start(self):
        learner_step = LearnerStep()
        add_questions = AddQuestions()

        learner_step.select_activity = lambda: None
        add_questions.input = lambda prompt: "Quiz"
        add_questions.print = lambda text: None

        question_count = add_questions.start(0, learner_step)
        self.assertEqual(question_count, 1)

class TestQuestionsSetup(unittest.TestCase):
    def test_setup(self):
        learner_step = LearnerStep()
        questions_setup = QuestionsSetup(learner_step)

        with open("questionstatuss.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(["Question ID", "Status"])
            writer.writerow(["1", "enabled"])
            writer.writerow(["2", "disabled"])


        learner_step.select_activity = lambda: None
        questions_setup.input = lambda prompt: "1"
        questions_setup.print = lambda text: None

        questions_setup.setup("questionss.csv", "questionstatuss.csv")


if __name__ == "__main__":
    unittest.main()
