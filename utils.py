import os
import openai
import streamlit as st
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_google_vertexai import ChatVertexAI


#decorator
def enable_chat_history(func):
    if os.environ.get("OPENAI_API_KEY"):

        # to clear chat history after swtching chatbot
        current_page = func.__qualname__
        if "current_page" not in st.session_state:
            st.session_state["current_page"] = current_page
        if st.session_state["current_page"] != current_page:
            try:
                st.cache_resource.clear()
                del st.session_state["current_page"]
                del st.session_state["messages"]
            except:
                pass

        # to show chat history on ui
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
        for msg in st.session_state["messages"]:
            st.chat_message(msg["role"]).write(msg["content"])

    def execute(*args, **kwargs):
        func(*args, **kwargs)

    return execute


def display_msg(msg, author):
    """Method to display message on the UI

    Args:
        msg (str): message to display
        author (str): author of the message -user/assistant
    """
    st.session_state.messages.append({"role": author, "content": msg})
    st.chat_message(author).write(msg)


def configure_llm():
    available_llms = {
        "gpt-4o": "GPT-4o",
        "gpt-4o-mini": "GPT-4o Mini",
        "gemini-1.5-pro-001": "Gemini 1.5 Pro",
        "gemini-1.5-flash-001": "Gemini 1.5 Flash",
    }
    llm_opt = st.sidebar.radio(
        label="Models",
        options=available_llms.values(),
        key="SELECTED_LLM"
    )
    selected_llm = next(key for key, value in available_llms.items() if value == llm_opt)
    if selected_llm == "gpt-4o" or selected_llm == "gpt-4o-mini":
        llm = ChatOpenAI(model_name=selected_llm, temperature=0, streaming=True)
    else:
        llm = ChatVertexAI(model_name=selected_llm, temperature=0, streaming=True)
    return llm


def sync_st_session():
    for k, v in st.session_state.items():
        st.session_state[k] = v
