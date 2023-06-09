import csv
import random
import os
import datetime


class LearnerStep:
    def __init__(self):
        self.question_count = 0
        self.user_name = ""

    def start(self):
        print(
            "Welcome to LearnerStep\n\nYour pathway for a better learning experience.\n"
        )
        user_name = input("Enter your Name: ")
        self.user_name = user_name
        print(
            "Welcome",
            user_name,
            "\nMake sure to add the questions, decide on their status then you can start practicing and testing your knowledge!",
        )
        self.load_question_count()
        self.select_activity()

    def load_question_count(self):
        if os.path.isfile("questions.csv"):
            with open("questions.csv", "r") as file:
                reader = csv.reader(file)
                next(reader)
                self.question_count = sum(1 for _ in reader)
        else:
            self.question_count = 0

    def get_enabled_question_count(self):
        if os.path.isfile("questionstatus.csv"):
            with open("questionstatus.csv", "r") as file:
                reader = csv.reader(file)
                next(reader)
                return sum(1 for row in reader if row[1] == "enabled")
        else:
            return 0

    def select_activity(self):
        print(
            "Select the action you would like to perform and press the corresponding number:\n\n1.Add questions\n\n2.View Statistics\n\n3.Disable/enable questions\n\n4.Practice mode\n\n5.Test mode\n"
        )
        try:
            user_input = int(input("Enter choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            self.select_activity()
            return

        if user_input == 1:
            add_questions = AddQuestions(self.user_name)
            self.question_count = add_questions.start(
                self.question_count, self, self.user_name
            )
        elif user_input == 2:
            self.view_statistics = ViewStatistics()
            self.view_statistics.show()
        elif user_input == 3:
            disable_enable_questions = QuestionsSetup(self)
            disable_enable_questions.setup("questions.csv", "questionstatus.csv")
        elif user_input == 4:
            enabled_question_count = self.get_enabled_question_count()
            if enabled_question_count >= 5:
                practice_mode = PracticeMode(self, self.user_name)
                practice_mode.start("questions.csv")
            else:
                print("You need to enable at least 5 questions.")
                self.select_activity()
        elif user_input == 5:
            enabled_question_count = self.get_enabled_question_count()
            if enabled_question_count >= 5:
                session_number = int(input("Enter session number: "))
                session_date = datetime.date.today()
                session_time = datetime.datetime.now().strftime("%H:%M")
                test_mode = TestMode(learner_step, self.user_name)
                test_mode.start(
                    "questions.csv",
                    "questionstatus.csv",
                    session_number,
                    session_date,
                    session_time,
                    self.user_name,
                )

            else:
                print("You need to enable at least 5 questions.")
                self.select_activity()


class AddQuestions:
    def __init__(self, user_name):
        self.user_name = user_name

    def start(self, question_count, learner_step, user_name):
        print(
            "New session starting...\n",
            "Learner is ",
            user_name,
            "\n",
            "Remember you need to add at least 5 different questions - Good luck",
        )
        column_names = [
            "Question ID",
            "Question Type",
            "Question",
            "Choices",
            "Answer",
        ]
        file_exists = os.path.isfile("questions.csv")

        with open("questions.csv", mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(column_names)

            while True:
                question_type = input(
                    "Write Quiz or FFText to start adding questions of the relevant type: "
                ).title()

                if question_type == "Quiz":
                    quiz_id = random.randint(100, 999)
                    print("Your question ID is:", quiz_id)
                    quiz_question = input("Write a question: ")
                    quiz_question_choices = input("Write the question choices: ")
                    quiz_question_answer = input("Write the correct answer: ")

                    writer.writerow(
                        [
                            quiz_id,
                            "Quiz",
                            quiz_question,
                            quiz_question_choices,
                            quiz_question_answer,
                        ]
                    )

                    question_count += 1
                    print(
                        f"One Quiz question added - Total questions: {question_count}"
                    )

                elif question_type == "Fftext":
                    ff_id = random.randint(100, 999)
                    print("Your question ID is:", ff_id)
                    ff_question = input("Write the question: ")
                    ff_question_answer = input("Write the answer: ")

                    writer.writerow(
                        [
                            ff_id,
                            "FFText",
                            ff_question,
                            "",
                            ff_question_answer,
                        ]
                    )

                    question_count += 1
                    print(
                        f"One FFText question added - Total questions: {question_count}"
                    )

                else:
                    print("Invalid question type. Please enter Quiz or FFText.")

                add_more = input(
                    "Do you want to add more questions? (yes/no): "
                ).lower()
                if add_more == "no":
                    break

        learner_step.select_activity()
        return question_count


class QuestionsSetup:
    def __init__(self, learner_step):
        self.learner_step = learner_step

    def setup(self, input_file_path, output_file_path):
        print("You accessed the questions setup section")

        while True:
            user_input = input(
                "Please enter the ID of the question you would like to update (or 'return' to go back): "
            )

            if user_input.lower() == "return":
                self.learner_step.select_activity()
                return

            question_found = False
            question_status_data = []

            with open(output_file_path, mode="r") as file:
                reader = csv.reader(file)
                question_status_data = list(reader)

            with open(input_file_path, mode="r") as input_file:
                reader = csv.reader(input_file)
                data = list(reader)
                headers = data[0]
                data = data[1:]

                for row in data:
                    question_id = row[0]
                    question_text = row[2]
                    question_answer = row[4]

                    if user_input == question_id:
                        print("Question:", question_text)
                        print("Answer:", question_answer)
                        status = ""

                        while True:
                            user_choice = input(
                                "Please write 'Enable' or 'Disable': "
                            ).lower()
                            if user_choice == "enable":
                                status = "enabled"
                                print("Question status updated")
                                break
                            elif user_choice == "disable":
                                status = "disabled"
                                print("Question status updated")
                                break
                            else:
                                print("Invalid choice. Please try again.")

                        for i, row in enumerate(question_status_data):
                            if row and row[0] == question_id:
                                question_status_data[i][1] = status
                                break
                        else:
                            question_status_data.append([question_id, status])

                        question_found = True
                        break

            with open(output_file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(question_status_data)

            if question_found:
                continue

            user_input = input(
                "No question found with the specified ID. Please check the number and try again (or enter 'return'): "
            )
            if user_input.lower() == "return":
                self.learner_step.select_activity()
                return

            with open(output_file_path, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([question_id, status])


class PracticeMode:
    def __init__(self, learner_step, user_name):
        self.learner_step = learner_step
        self.user_name = user_name

    def start(self, file_path):
        print("Let's start learning!!!!")
        print(
            "Remember",
            self.user_name,
            "you can always exit the section by writing return\n",
        )
        student_score = []
        incorrect_questions = []
        question_status = {}

        with open("questionstatus.csv", "r") as status_file:
            status_reader = csv.reader(status_file)
            header = next(status_reader)
            question_status = {row[0]: row[1] for row in status_reader}

        with open(file_path, "r") as file:
            questions = list(csv.DictReader(file))
            while True:
                enabled_questions = [
                    q
                    for q in questions
                    if question_status.get(q["Question ID"], "") == "enabled"
                ]

                if incorrect_questions:
                    current_question = self.weighted_choice(
                        enabled_questions, incorrect_questions
                    )
                else:
                    unanswered_questions = [
                        q for q in enabled_questions if q not in student_score
                    ]
                    if not unanswered_questions:
                        print("You have answered all the questions!")
                        self.learner_step.select_activity()

                    current_question = random.choice(unanswered_questions)

                question_type = current_question["Question Type"]
                question_text = current_question["Question"]
                question_choices = current_question["Choices"]
                question_answer = current_question["Answer"]
                print("This question is of the type", question_type)
                print("Question:", question_text)
                if question_type == "Quiz":
                    print("Choices:", question_choices)

                response = input("Please enter your response:\n").lower()

                if response == question_answer:
                    print("That's correct! Well done")
                    student_score.append(current_question)
                    if current_question in incorrect_questions:
                        incorrect_questions.remove(current_question)
                elif response == "return":
                    print("Exiting the practice section...")
                    final_score = len(student_score)
                    learner_step = LearnerStep()
                    learner_step.question_count = final_score
                    learner_step.select_activity()
                    return
                else:
                    print("That's incorrect! The correct answer is", question_answer)
                    incorrect_questions.append(current_question)
                print()

    def weighted_choice(self, questions, incorrect_questions):
        weights = [1 if q in incorrect_questions else 0.2 for q in questions]
        return random.choices(questions, weights=weights)[0]




    def update_question_stats(self, student_score):
        stats_file_path = "questionstats.csv"
        fieldnames = ["ID", "Attempts", "Correct Attempts"]
        stats_data = []

        try:
            with open(stats_file_path, "r") as stats_file:
                reader = csv.DictReader(stats_file)
                stats_data = list(reader)

        except FileNotFoundError:
            print("Stats file not found.")

        for question in student_score:
            question_id = question["Question ID"]
            question_found = False

            for row in stats_data:
                if row["ID"] == question_id:
                    attempts = int(row["Attempts"])
                    correct_attempts = int(row["Correct Attempts"])
                    attempts += 1
                    if question_id in [q["Question ID"] for q in student_score]:
                        correct_attempts += 1
                    row["Attempts"] = str(attempts)
                    row["Correct Attempts"] = str(correct_attempts)
                    question_found = True
                    break

            if not question_found:
                stats_data.append(
                    {
                        "ID": question_id,
                        "Attempts": "1",
                        "Correct Attempts": "1"
                        if question_id in [q["Question ID"] for q in student_score]
                        else "0",
                    }
                )

        with open(stats_file_path, "w", newline="") as stats_file:
            writer = csv.DictWriter(stats_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(stats_data)

class TestMode:
    def __init__(self, learner_step, user_name):
        self.learner_step = learner_step
        self.user_name = user_name

    def start(
        self,
        file_path,
        status_file_path,
        session_number,
        session_date,
        session_time,
        user_name,
    ):
        print("Hello", self.user_name, "You accessed the testing section!")
        print("Remember you can always exit by writing return\n")
        num_questions = int(input("Enter the number of questions you would like to answer (5 is minimum): "))
        student_score = []
        session_terminated = False

        with open(file_path, "r") as file, open(status_file_path, "r") as status_file:
            questions = list(csv.DictReader(file))
            question_statuses = list(csv.DictReader(status_file))

            enabled_questions = []
            for question, status in zip(questions, question_statuses):
                current_question = question
                if status["status"] == "enabled":
                    enabled_questions.append(current_question)

            total_questions = min(len(enabled_questions), num_questions)
            questions_answered = 0

            while enabled_questions and questions_answered < total_questions:
                current_question = random.choice(enabled_questions)
                question_type = current_question["Question Type"]
                question_id = current_question["Question ID"]
                question_text = current_question["Question"]
                question_choices = current_question["Choices"]
                question_answer = current_question["Answer"]

                print("This question is of type", question_type)
                print("Question:", question_text)

                if question_type == "Quiz":
                    print("Choices:", question_choices)

                response = input("Please enter your response:\n").lower()

                if response == "return":
                    print("Test session terminated by student. Exiting the test section...")
                    session_terminated = True
                    break

                questions_answered += 1

                if response == question_answer:
                    print("That's correct! Well done")
                    student_score.append(current_question)
                    enabled_questions.remove(current_question)
                else:
                    print("Sorry, That's incorrect!")
                    enabled_questions.remove(current_question)

                print()

            correct_answers = len(student_score)
            final_score = round((correct_answers / total_questions) * 100, 2)

            self.update_question_stats(student_score)

        if session_terminated:
            return

        print("Test session completed. Your score is", final_score, "%")
        print("You can see your session details in the Results file")

        with open("results.txt", "a") as results_file:
            writer = csv.writer(results_file)
            if results_file.tell() == 0:
                writer.writerow(["final score", "round", "date", "time", "student"])
            writer.writerow(
                [
                    final_score,
                    session_number,
                    session_date,
                    session_time,
                    user_name,
                ]
            )

        learner_step = LearnerStep()
        learner_step.question_count = final_score
        self.learner_step.select_activity()

    def update_question_stats(self, student_score):
        stats_file_path = "questionstats.csv"
        fieldnames = ["ID", "Attempts", "Correct Attempts"]
        stats_data = []

        try:
            with open(stats_file_path, "r") as stats_file:
                reader = csv.DictReader(stats_file)
                stats_data = list(reader)

        except FileNotFoundError:
            print("Stats file not found.")

        for question in student_score:
            question_id = question["Question ID"]
            question_found = False

            for row in stats_data:
                if row["ID"] == question_id:
                    attempts = int(row["Attempts"])
                    correct_attempts = int(row["Correct Attempts"])
                    attempts += 1
                    if question_id in [q["Question ID"] for q in student_score]:
                        correct_attempts += 1
                    row["Attempts"] = str(attempts)
                    row["Correct Attempts"] = str(correct_attempts)
                    question_found = True
                    break

            if not question_found:
                stats_data.append(
                    {
                        "ID": question_id,
                        "Attempts": "1",
                        "Correct Attempts": "1"
                        if question_id in [q["Question ID"] for q in student_score]
                        else "0",
                    }
                )

        with open(stats_file_path, "w", newline="") as stats_file:
            writer = csv.DictWriter(stats_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(stats_data)


class ViewStatistics:
    def show(self):
        if not os.path.isfile("questions.csv"):
            print("No questions found.")
            return

        with open("questions.csv", "r") as questions_file, open(
            "questionstats.csv", "r"
        ) as stats_file, open("questionstatus.csv", "r") as status_file:
            questions_reader = csv.DictReader(questions_file)
            stats_reader = csv.DictReader(stats_file)
            status_reader = csv.DictReader(status_file)

            print("Question Statistics:")
            print("--------------------")

            question_status_dict = {row["id"]: row["status"] for row in status_reader}

            for question_row in questions_reader:
                question_id = question_row["Question ID"]
                question_text = question_row["Question"]
                question_answer = question_row["Answer"]


                question_status = question_status_dict.get(question_id, "disabled")

                question_stats = {}
                for stats_row in stats_reader:
                    if stats_row["ID"] == question_id:
                        question_stats = stats_row
                        break

                attempts = question_stats.get("Attempts", 0)
                correct_attempts = question_stats.get("Correct Attempts", 0)

                print("Question ID:", question_id)
                print("Status:", question_status)
                print("Question:", question_text)
                print("Answer:", question_answer)
                print("Attempts:", attempts)
                print("Correct Attempts:", correct_attempts)
                print("--------------------")


if __name__ == "__main__":
    learner_step = LearnerStep()
    learner_step.start()



# link to the part3 project below
# https://github.com/Emnamejeri/wargame
