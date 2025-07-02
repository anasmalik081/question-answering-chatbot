import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Loading Environments
load_dotenv()

# LangSmith Tracking
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "QA Chatbot"

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please response to the user queries."),
        ("user", "Question: {question}")
    ]
)

def generate_response(
        query: str,
        api_key: str,
        model_name: str,
        temperature: float,
        max_tokens: int     
) -> str:
    """
    This function is responsible to generate response to the query
    """
    # Loading Model
    os.environ["GOOGLE_API_KEY"] = api_key
    model = ChatGoogleGenerativeAI(model=model_name)

    # Creating Chain
    chain = prompt | model | StrOutputParser()

    # Generating response
    response = chain.invoke({"question": query})
    return response

# Title of the app
st.title("Enhanced Q&A Chatbot")

# Sidebar Settings
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your Google API Key: ", type="password")

# Dropdown to Select Various Google Models
model_name = st.sidebar.selectbox("Select an Google Model", [
    "gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"
])

# Adjust response parameter
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=300, value=150)

# Main Interface for User Input
st.write("Go ahead and ask any question")
user_input = st.text_input("You: ")

if user_input:
    response = generate_response(
        query=user_input,
        api_key=api_key,
        model_name=model_name,
        temperature=temperature,
        max_tokens=max_tokens
    )
    st.write(response)
else:
    st.write("Please provide the query")