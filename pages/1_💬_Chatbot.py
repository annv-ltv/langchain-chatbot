import os
import time
import utils
import streamlit as st
from streaming import StreamHandler

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

st.set_page_config(page_title="Chatbot", page_icon="💬")
st.header('Chatbot')

class ContextChatbot:
    """
    ContextChatbot class represents a chatbot that interacts with users through a Streamlit interface.
    Attributes:
        llm (LLM): The language model used by the chatbot.
    Methods:
        __init__(): Initializes the ContextChatbot object.
        setup_chain(): Sets up the conversation chain for the chatbot.
        main(): The main function that handles user queries and generates responses.
    """
    def __init__(self):
        utils.sync_st_session()
        self.llm = utils.configure_llm()

    def setup_chain(self):
        memory = ConversationBufferMemory()
        chain = ConversationChain(llm=self.llm, memory=memory, verbose=True)
        return chain

    @utils.enable_chat_history
    def main(self):
        chain = self.setup_chain()
        user_query = st.chat_input(placeholder="Ask me anything!")
        if user_query:
            utils.display_msg(user_query, 'user')
            with st.chat_message("assistant"):
                st_cb = StreamHandler(st.empty())
                # Start measuring time
                start = time.time()
                try:
                    result = chain.invoke(
                        {"input": user_query},
                        {"callbacks": [st_cb]}
                    )
                    response = result["response"]
                except Exception as e:
                    response = f"An error occurred: {str(e)}"
                # End measuring time
                elapsed_time = time.time() - start
                st.write(f"Execution time: {elapsed_time:.2f}s")
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    obj = ContextChatbot()
    obj.main()