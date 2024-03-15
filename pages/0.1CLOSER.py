import streamlit as st
import pandas as pd
import docx
import fitz  # PyMuPDF
from langchain.llms import openai
from langchain.chains import qa_generation  

from langchain_community.chat_models import ChatOpenAI
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain


# Initialize Langchain with OpenAI
with st.sidebar:
     openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
"[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    
def read_pdf(file):
    with fitz.open(stream=file, filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

def read_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def upload_business_process_document():
    uploaded_file = st.file_uploader("Upload your business process document", type=['txt', 'pdf', 'docx'])
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            content = read_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            content = read_docx(uploaded_file)
        else:  # Assuming text file
            content = uploaded_file.getvalue().decode("utf-8")
        return content
    return None

def upload_detailed_steps_documents():
    uploaded_files = st.file_uploader("Upload detailed steps documents for each activity", accept_multiple_files=True, type=['txt', 'pdf', 'docx'])
    detailed_docs = {}
    for uploaded_file in uploaded_files:
        if uploaded_file.type == "application/pdf":
            content = read_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            content = read_docx(uploaded_file)
        else:  # Assuming text file
            content = uploaded_file.getvalue().decode("utf-8")
        detailed_docs[uploaded_file.name] = content
    return detailed_docs

def process_documents(business_process_doc, detailed_steps_docs):
    
    business_process_document = Document(page_content=business_process_doc, title="Business Process Document")
    steps_documents = [Document(page_content=doc, title=name) for name, doc in detailed_steps_docs.items()]
    combined_document = Document.combine([business_process_document] + steps_documents, title="Combined Document")

    prompt = ChatPromptTemplate.from_messages(
    [("system", "Generate a test cases using the \n\n{context}")]
)
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo",openai_api_key=openai_api_key)
    chain = create_stuff_documents_chain(llm, prompt)

   # docs = [Document(page_content= business_process_doc),
   #         Document(content=doc, title=name) for name, doc in detailed_steps_docs.items()
   #         ]


    st.subheader("Generated Test Cases")
    st.write(chain.invoke({"context": combined_document}))

def main():

    st.title("Test Case Generator for Business Processes")

    business_process_doc = upload_business_process_document()
    detailed_steps_docs = upload_detailed_steps_documents()

    if st.button("Generate Test Cases") and business_process_doc and detailed_steps_docs:
        process_documents(business_process_doc, detailed_steps_docs)
        
if __name__ == "__main__":
    main()
