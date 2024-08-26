# Chatbot Implementations with Langchain + Streamlit

Langchain is a powerful framework designed to streamline the development of applications using Language Models (LLMs). \
It provides a comprehensive integration of various components, simplifying the process of assembling them to create robust applications.


## <img src="https://streamlit.io/images/brand/streamlit-mark-color.png" width="40" height="22"> Streamlit App
Chatbot run on Streamlit.

## 🖥️ Running locally
```shell
# Run main streamlit app
$ streamlit run Home.py
```

## 📦 Running with Docker
```shell
# To generate image
$ docker build -t langchain-chatbot .

# To run the docker container
$ docker run -p 8501:8501 langchain-chatbot

# Go
http://localhost:8501/
```