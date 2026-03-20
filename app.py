import streamlit as st
from utils.rag import load_data, create_vector_db, search_docs
from models.llm import get_response
from utils.web_search import search_web

st.set_page_config(page_title="Interview Prep Bot", page_icon="")

st.title("AI Interview Preparation Bot")
mode = st.selectbox("Response Mode", ["Concise", "Detailed"])
data = load_data("data/interview_q&a.txt")
vector_db = create_vector_db(data)

st.write("Ask me anything about interviews, DSA, or HR questions!")

#Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

#Display previous messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

#Input box
user_input = st.chat_input("Type your question here...")

if user_input:
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    docs = search_docs(vector_db, user_input)

# Response style
    if mode == "Concise":
        style = "Give a short and crisp answer."
    else:
        style = "Explain in detail with examples."

    if docs:
        context = "\n".join([doc.page_content for doc in docs])
        prompt = f"{style}\n\nAnswer using this context:\n{context}\n\nQuestion: {user_input}"
    else:
        web_result = search_web(user_input)
        prompt = f"{style}\n\nUse this web info:\n{web_result}\n\nQuestion: {user_input}"

    response = get_response(prompt)

    st.chat_message("assistant").write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})