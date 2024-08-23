import os
import sys
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_google_vertexai import ChatVertexAI

def enable_chat_history(func):
    """
    Decorator function that enables chat history functionality.
    Args:
        func (callable): The function to be decorated.
    Returns:
        callable: The decorated function.
    """
    def wrapper(*args, **kwargs):
        if os.environ.get("OPENAI_API_KEY"):
            # To clear chat history when switching between pages
            current_page = func.__qualname__
            if "current_page" not in st.session_state:
                st.session_state["current_page"] = current_page
            if st.session_state["current_page"] != current_page:
                try:
                    st.cache_resource.clear()
                    del st.session_state["current_page"]
                    del st.session_state["messages"]
                except KeyError:
                    pass
            # to show chat history on ui
            if "messages" not in st.session_state:
                st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
            for msg in st.session_state["messages"]:
                st.chat_message(msg["role"]).write(msg["content"])

        return func(*args, **kwargs)

    return wrapper

def display_msg(msg, author):
    """Method to display message on the UI

    Args:
        msg (str): message to display
        author (str): author of the message - user/assistant
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

    try:
        if selected_llm in ["gpt-4o", "gpt-4o-mini"]:
            llm = ChatOpenAI(model_name=selected_llm, temperature=0, streaming=True)
        else:
            llm = ChatVertexAI(model_name=selected_llm, temperature=0, streaming=True)
        return llm
    except Exception as e:
        st.write(f"An error occurred: {str(e)}")
        sys.exit(1)

def sync_st_session():
    for k, v in st.session_state.items():
        st.session_state[k] = v