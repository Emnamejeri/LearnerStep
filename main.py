import csv
import random
import os

print("Welcome to LearnerStep\n\nYour pathway for a better learning experience.\n")
user_name = input("Enter your name: ")
question_count = 0
def select_activity():
    print(
        "Start by selecting the action you would like to perform and press the corresponding number:\n\n1.Add questions\n\n2.View Statistics\n\n3.Disable/enable questions\n\n4.Practice mode\n\n5.Test mode\n\n6.View profile\n"
    )
    user_input = int(input("Enter choice: "))
    if user_input == 1:
        add_questions()
    elif user_input == 2:
        view_statstics()
    elif user_input == 3:
        disable_enable_questions("questions.csv", "questionstatus.csv")
    elif user_input == 4:
        if question_count >= 5:  # Check if question_count is at least 5
            practice_mode("questions.csv")
        else:
            print("You need to add at least 5 questions.")
            select_activity()
    elif user_input == 5:
        if question_count >= 5:  # Check if question_count is at least 5
            session_number = int(input("Enter session number: "))
            test_mode("questions.csv", session_number)
        else:
            print("You need to add at least 5 questions. Your current count is: ", question_count)
            select_activity()
    # elif user_input == 6:
    #     profile()
    else:
        print("Invalid input. Please enter correct number.Your current count is: ", question_count)


def add_questions():
    global question_count
    print("New session starting... \n", "Remember you need to add at least 5 different questions - So good luck", user_name)
    column_names = ["Question ID", "Question Type", "Question", "Choices", "Answer", "Question Status"]
    file_exists = False
    

    with open("questions.csv", mode="a", newline="") as file:
        writer = csv.writer(file)

        # Check if questions file already exists
        file_exists = os.path.isfile("questions.csv")

        if not file_exists:
            writer.writerow(column_names)
        if file_exists:
            with open("questions.csv", mode="r") as file:
                reader = csv.reader(file)
                question_count = sum(1 for _ in reader) - 1  # Subtract 1 to exclude header
        while True:
            question_type = input(
                "Write Quiz or FFText to start adding questions of the relevant type: "
            ).title()

            if question_type == "Quiz":
                quiz_question = input("Write a question: ")
                quiz_id = random.randint(100, 999)
                print("Your question ID is: ", quiz_id)
                quiz_question_choices = input("Write the question choices: ")
                quiz_question_answer = input("Write the correct answer: ")

                writer.writerow(
                    ["Quiz", quiz_id, quiz_question, quiz_question_choices, quiz_question_answer]
                )

                question_count += 1  
                print(
                    f"One Quiz question added - Total questions: {question_count}"
                )

            elif question_type == "Fftext":
                ff_question = input("Write the question: ")
                ff_id = random.randint(100, 999)
                print("Your question ID is: ", ff_id)
                ff_question_answer = input("Write the answer: ")

                writer.writerow(["FFText", ff_id, ff_question, "", ff_question_answer])

                question_count += 1 
                print(
                    f"One FreeForm question added - Total questions: {question_count}"
                )

            elif question_type == "Quit":
                print("Saving questions...")
                print("Exiting the program...")
                select_activity()
                return

            else:
                print("That's not a valid question form - Please write Quiz or FFText")
            

def practice_mode(file_path):
    global question_count
    global user_name
    print("Let's start learning", user_name, "!!!!")
    print("Remember you can always exit the section by writing quit \n")
    student_score = []
    incorrect_questions = []

    with open(file_path, "r") as file:
        questions = list(csv.DictReader(file))
        while True:
            # Check if there are any unanswered incorrect questions
            if incorrect_questions:
                current_question = weighted_choice(questions, incorrect_questions)
            else:
                # If no incorrect questions, select a random unanswered question
                unanswered_questions = [q for q in questions if q not in student_score]
                if not unanswered_questions:
                    print("You have answered all the questions!")
                    break
                current_question = random.choice(unanswered_questions)

            question_type = current_question["Question Type"]
            question_text = current_question["Question"]
            question_choices = current_question["Choices"]
            question_answer = current_question["Answer"]
            print("This question is of the type", question_type)
            print("Question: ", question_text)
            if question_type == "Quiz":
                print("Choices: ", question_choices)

            response = input("Please enter your response: \n").lower()

            if response == question_answer:
                print("That's correct! Well done")
                student_score.append(current_question)
                if current_question in incorrect_questions:
                    incorrect_questions.remove(current_question)
            elif response == "quit":
                print("Saving answers...")
                print("Exiting the practice section...")
                final_score = len(student_score)
                print("Your Score is ", final_score, "points")
                select_activity()
                return
            else:
                print("That's incorrect! The correct answer is", question_answer)
                incorrect_questions.append(current_question)
            print()


def weighted_choice(questions, incorrect_questions):
    weights = [1 if q in incorrect_questions else 0.2 for q in questions]
    return random.choices(questions, weights=weights)[0]


def test_mode(file_path, session_number):
    print("You accessed the testing section!")
    student_score = []
    global question_count

    with open(file_path, "r") as file:
        questions = list(csv.DictReader(file))
        total_questions = len(questions)
        
        while questions:
            current_question = random.choice(questions)
            question_type = current_question["Question Type"]
            question_text = current_question["Question"]
            question_choices = current_question["Choices"]
            question_answer = current_question["Answer"]

            print("This question is of type", question_type)
            print("Question:", question_text)

            if question_type == "Quiz":
                print("Choices:", question_choices)

            response = input("Please enter your response:\n").lower()
            if len(student_score) == total_questions:
                print("You answered all questions.")

            final_score = round((len(student_score) / total_questions) * 100, 2)
            if response == question_answer:
                print("That's correct! Well done", user_name)
                student_score.append(current_question)
                questions.remove(current_question)
            elif response == "quit":
                print("Saving your answers...")
                print(
                    "Test session terminated. Your score is",
                    final_score,
                    "%, and results are saved in results.txt file.",
                )
                print("Exiting the test section...")
                select_activity()
                return
            else:
                print("Sorry,", user_name, "That's incorrect!")
                questions.remove(current_question)
            print()

    # Save user scores in results.txt file
    with open("results.txt", "a") as results_file:
        writer = csv.writer(results_file)
        writer.writerow(["final score", "round"])
        writer.writerow([final_score, session_number])

    print("Test session completed. Your score is", final_score, "%")
    print("Results saved in results.txt.")



def disable_enable_questions(input_file_path, output_file_path):
    print("You accessed the questions setup section")
    user_input = int(input("Please enter the ID of the question you would like to update: "))
    column_names = ["QuestionId", "Question status"]
    file_exists = False

    # Check if questionstatus.csv file already exists
    with open(output_file_path, mode="a", newline="") as file:
        writer = csv.writer(file)

        # Check if the file is empty
        file_exists = file.tell() != 0

        if not file_exists:
            writer.writerow(column_names)

        # Read the questions.csv file
        with open(input_file_path, mode='r') as input_file:
            reader = csv.reader(input_file)
            data = list(reader)

            # Search for the user_input question ID in questions.csv
            question_found = False
            for row in data:
                question_id = int(row[0])
                question_text = row[2]
                question_answer = row[4]
                if user_input == question_id:
                    print("Question:", question_text)
                    print("Answer:", question_answer)
                    user_choice = input("Please write 'Enable' or 'Disable': ").lower()
                    if user_choice == "enable":
                        status = "active"
                    elif user_choice == "disable":
                        status = "inactive"
                    else:
                        print("Invalid choice. Please try again.")
                        return

                    writer.writerow([question_id, status])
                    question_found = True
                    break

            if not question_found:
                print("Are you sure the ID is correct?")

def view_statstics():
    print("Your statistics are displayed below:")

select_activity()





