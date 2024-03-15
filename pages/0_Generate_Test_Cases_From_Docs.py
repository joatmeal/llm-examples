import streamlit as st
from langchain.llms import openai
import pandas as pd
import os

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
    # Here, you would analyze the documents using Langchain and generate test cases
    # For demonstration, let's assume we're simply returning a list of test cases
    test_cases = ["Test Case 1: Verify X", "Test Case 2: Validate Y"]  # Placeholder test cases
    return test_cases

def display_test_cases(test_cases):
    st.subheader("Generated Test Cases")
    for i, test_case in enumerate(test_cases, start=1):
        st.text(f"{i}. {test_case}")

    # Optionally, allow users to download the test cases as a file
    if st.button('Download Test Cases'):
        test_cases_df = pd.DataFrame(test_cases, columns=["Test Cases"])
        csv = test_cases_df.to_csv(index=False)
        st.download_button(label="Download test cases as CSV", data=csv, file_name='test_cases.csv', mime='text/csv')

def main():

    with st.sidebar:
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

    st.title("Test Case Generator for Business Processes")

    business_process_doc = upload_business_process_document()
    detailed_steps_docs = upload_detailed_steps_documents()

    if st.button("Generate Test Cases") and business_process_doc and detailed_steps_docs:
        test_cases = process_documents(business_process_doc, detailed_steps_docs)
        display_test_cases(test_cases)

if __name__ == "__main__":
    main()
