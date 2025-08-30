import streamlit as st
import os
import subprocess

# Quiz data for 3 levels (each level has 2 questions)
quiz_data = {
    "Level 1": {
        "learn": "What is a Stock?\n"
        "\n A stock represents a share in the ownership of a company.\n"
        "\n It gives you a claim on part of the company's assets and earnings.\n"
        "\n Stocks are traded on exchanges like the NYSE or NASDAQ.\n"
        "\n Owning stocks makes you a partial owner of the company.\n",
        "questions": [
            {
                "question": "What does owning a stock represent?",
                "options": ["Debt", "Ownership", "Rent", "Loan"],
                "answer": "Ownership"
            },
            {
                "question": "Where are stocks traded?",
                "options": ["Banks", "Exchanges", "Malls", "Airports"],
                "answer": "Exchanges"
            }
        ]
    },
    "Level 2": {
        "learn": "What is a Stock Market?\n"
        "\nThe stock market is where buyers and sellers trade stocks.\n"
        "\n It allows companies to raise funds by issuing shares.\n"
        "\n Investors can earn profits or losses based on price changes.\n"
        "\n Examples include the NYSE, NASDAQ, and BSE.\n",
        "questions": [
            {
                "question": "What is the purpose of the stock market?",
                "options": ["To sell products", "To trade stocks", "To create ads", "To build apps"],
                "answer": "To trade stocks"
            },
            {
                "question": "How can investors profit in the stock market?",
                "options": ["By trading goods", "By changing prices", "By price changes in stocks", "By owning malls"],
                "answer": "By price changes in stocks"
            }
        ]
    },
    "Level 3": {
        "learn": "\n Stock Prices\n"
        "\nStock prices are influenced by demand and supply.\n"
        "\n Positive news increases demand, raising prices.\n"
        "\n Negative news decreases demand, lowering prices.\n"
        "\n Other factors include earnings reports, economic conditions, and market sentiment.\n",
        "questions": [
            {
                "question": "What happens to stock prices when demand increases?",
                "options": ["They decrease", "They remain constant", "They increase", "They become zero"],
                "answer": "They increase"
            },
            {
                "question": "Which factor affects stock prices the most?",
                "options": ["Company profits", "Market sentiment", "Earnings reports", "All of the above"],
                "answer": "All of the above"
            }
        ]
    }
}

# Initialize session state to track progress
def init_session_state():
    if 'level' not in st.session_state:
        st.session_state.level = 1
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'answered_current_question' not in st.session_state:
        st.session_state.answered_current_question = False
    if 'unlocked_levels' not in st.session_state:
        st.session_state.unlocked_levels = [1]  # Level 1 is unlocked by default

def reset_level():
    """Resets progress to start a new level."""
    st.session_state.current_question_index = 0
    st.session_state.score = 0
    st.session_state.answered_current_question = False

def main():
    # Initialize session state
    init_session_state()

    # Sidebar Navigation
    st.sidebar.title("Levels")
    for i in range(1, len(quiz_data) + 1):
        if i in st.session_state.unlocked_levels:
            st.sidebar.markdown(f"✅ *Level {i} - Unlocked*")
        else:
            st.sidebar.markdown(f"🔒 *Level {i} - Locked*")

    # Main content
    current_level = f"Level {st.session_state.level}"
    st.title(f"🌟 Financial Market Simulator - {current_level} 🌟")

    # Learning content
    st.subheader("📘 Learn")
    st.info(quiz_data[current_level]["learn"])

    # Quiz content
    questions = quiz_data[current_level]["questions"]

    if st.session_state.current_question_index < len(questions):
        current_question = questions[st.session_state.current_question_index]

        st.subheader(f"❓ Question {st.session_state.current_question_index + 1}")
        st.write(current_question["question"])

        # Radio button for answer selection
        selected_option = st.radio(
            "Choose your answer:",
            current_question["options"],
            key=f"question_{st.session_state.current_question_index}",
            disabled=st.session_state.answered_current_question
        )

        # Submit button logic
        if not st.session_state.answered_current_question:
            if st.button("Submit"):
                if selected_option == current_question["answer"]:
                    st.success("🎉 Correct!")
                    st.session_state.score += 1
                else:
                    st.error(f"❌ Incorrect. The correct answer is: {current_question['answer']}")
                st.session_state.answered_current_question = True

        # Next question logic
        if st.session_state.answered_current_question:
            if st.button("Next Question"):
                st.session_state.current_question_index += 1
                st.session_state.answered_current_question = False
                st.rerun()  # Re-run to update the question

    else:
        st.subheader("🎉 Level Complete!")
        st.write(f"Your score: {st.session_state.score}/{len(questions)}")

        # Automatically move to the next level if the score is full
        if st.session_state.score == len(questions):
            st.success("👏 Congratulations! You've unlocked the next level.")
            if st.session_state.level < len(quiz_data):
                st.session_state.level += 1
                if st.session_state.level not in st.session_state.unlocked_levels:
                    st.session_state.unlocked_levels.append(st.session_state.level)
            reset_level()
            st.rerun()  # Move to next level immediately
        else:
            st.error("❌ You need to score full points to unlock the next level.")
            reset_level()

    # Restart Level button
    if st.button("Restart Level"):
        reset_level()
        st.rerun()  # Re-run to restart the level

    # Add Let's Trade Now button
    st.markdown("---")

    # Check if all levels are completed
    if len(st.session_state.unlocked_levels) == len(quiz_data):
        st.success("🎉 All levels completed!")
        
        # Display the "Let's Trade Now" button
        if st.button("Let's Trade Now! 🚀"):
            try:
                # Specify the full path to the Streamlit app
                app_path = r"C:\Users\vijay\Desktop\exp\New folder\stremlit_app\app.py"
                
                # Ensure the path exists
                if not os.path.exists(app_path):
                    st.error(f"Error: The file {app_path} does not exist.")
                else:
                    # Run the Streamlit app using subprocess
                    subprocess.Popen(
                        ["streamlit", "run", app_path], 
                        creationflags=subprocess.CREATE_NEW_CONSOLE
                    )
                    st.success("Trading platform is launching in a new window!")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.info("Complete all levels to unlock the trading platform!")

if __name__ == "__main__":
    main()
