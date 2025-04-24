import streamlit as st
import random
import time

# 💡 Encapsulation: All quiz data and logic inside this class
class Question:
    def __init__(self, question_text, options, answer):
        self.question_text = question_text
        self.options = options
        self.answer = answer

    def is_correct(self, selected_option):
        return selected_option == self.answer


# 💡 Encapsulation + Abstraction: QuizManager handles quiz logic
class QuizManager:
    def __init__(self):
        self.questions = self.load_questions()

    def load_questions(self):
        return [
            Question("What is the capital of Pakistan?", ["Lahore", "Karachi", "Islamabad", "Peshawar"], "Islamabad"),
            Question("Who is the founder of Pakistan?", ["Allama Iqbal", "Liaquat Ali Khan", "Muhammad Ali Jinnah", "Benazir Bhutto"], "Muhammad Ali Jinnah"),
            Question("Which is the national language of Pakistan?", ["Punjabi", "Urdu", "Sindhi", "Pashto"], "Urdu"),
            Question("What is the currency of Pakistan?", ["Rupee", "Dollar", "Taka", "Riyal"], "Rupee"),
            Question("Which city is known as the City of Lights in Pakistan?", ["Lahore", "Islamabad", "Faisalabad", "Karachi"], "Karachi"),
        ]

    def get_random_question(self):
        return random.choice(self.questions)


# 💡 Application Layer (Abstraction): Main Streamlit UI
class QuizApp:
    def __init__(self):
        self.quiz_manager = QuizManager()

    def run(self):
        st.title("📝 Quiz Application")

        if "current_question" not in st.session_state:
            st.session_state.current_question = self.quiz_manager.get_random_question()

        question = st.session_state.current_question

        st.subheader(question.question_text)

        selected_option = st.radio("Choose your answer", question.options, key="answer")

        if st.button("Submit Answer"):
            if question.is_correct(selected_option):
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Incorrect! The correct answer is: {question.answer}")

            time.sleep(3)
            st.session_state.current_question = self.quiz_manager.get_random_question()
            st.rerun()



if __name__ == "__main__":
    app = QuizApp()
    app.run()
