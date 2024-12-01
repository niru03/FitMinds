import streamlit as st
import openai
from textblob import TextBlob
import pandas as pd
# Set OpenAI API key directly (less secure)
openai.api_key = "QWdBDAfPTeAk0_h3txkx9aYpRv0pyRuqCFxhnkgKuG3QJgYzaMrguisPh4ziwzDDl2fD9xD8epT3BlbkFJ88y5zkpiuU46a4_cEVQT9QsdoaqJDd6eayahLZeMTmEUm4sEcZkb6oYaeEstYR3_1ddie2vAsA"

    
# --- GPT Response Generator ---
def generate_gpt_response(user_input):
    """
    Generates a response using OpenAI's GPT-3.5 Turbo.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are FitMinds, a friendly AI mental health assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        return response['choices'][0]['message']['content']
    except openai.error.AuthenticationError:
        return "Invalid API key. Please check your OpenAI API key."
    except Exception as e:
        return f"An error occurred: {e}"

# --- Sentiment Analysis ---
def analyze_user_sentiment(text):
    """
    Analyzes the user's sentiment using TextBlob and returns sentiment type and polarity score.
    """
    sentiment_analysis = TextBlob(text)
    polarity = sentiment_analysis.sentiment.polarity
    if polarity > 0.5:
        return "Very Positive", polarity
    elif 0.1 < polarity <= 0.5:
        return "Positive", polarity
    elif -0.1 <= polarity <= 0.1:
        return "Neutral", polarity
    elif -0.5 < polarity < -0.1:
        return "Negative", polarity
    else:
        return "Very Negative", polarity

# --- Main Application ---
def main():
    """
    Main Streamlit app function for user interaction, sentiment analysis, and chatbot responses.
    """
    st.title("FitMinds: AI Mental Health App")
    st.write("Share your thoughts and receive support and guidance!")

    # Initialize chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # User input
    user_input = st.text_input("How are you feeling today?")
    if user_input:
        # Sentiment analysis
        sentiment, polarity = analyze_user_sentiment(user_input)
        
        # GPT-generated response
        response = generate_gpt_response(user_input)

        # Save conversation to chat history
        st.session_state["chat_history"].append({"user": user_input, "bot": response, "sentiment": sentiment})

        # Display conversation
        st.markdown(f"**You:** {user_input}")
        st.markdown(f"**FitMinds:** {response}")
        st.markdown(f"**Sentiment:** {sentiment} (Polarity: {polarity})")

    # Display chat history
    if st.session_state["chat_history"]:
        st.subheader("Chat History")
        for chat in st.session_state["chat_history"]:
            st.markdown(f"**You:** {chat['user']}")
            st.markdown(f"**FitMinds:** {chat['bot']}")
            st.markdown(f"**Sentiment:** {chat['sentiment']}")

# Run the Streamlit app
if __name__ == "__main__":
    main()
