import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document
from langchain.prompts import ChatPromptTemplate
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from utils import read_pdf, read_docx, read_txt

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

def upload_document(label, file_types):
   uploaded_file = st.file_uploader(label, type=file_types)
   if uploaded_file is not None:
       if uploaded_file.type == "application/pdf":
           content = read_pdf(uploaded_file)
       elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
           content = read_docx(uploaded_file)
       else:  # Assuming text file
           content = read_txt(uploaded_file)
       return content
   return None

def process_documents(business_process_doc, detailed_steps_docs):
   business_process_document = Document(page_content=business_process_doc, metadata={"source": "Business Process Document"})
   steps_documents = [Document(page_content=doc, metadata={"source": name}) for name, doc in detailed_steps_docs.items()]
   combined_documents = [business_process_document] + steps_documents
   prompt = ChatPromptTemplate.from_messages(
       [("system", "Generate test cases using the following documents:\n\n{documents}")])
   llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)
   chain = StuffDocumentsChain(llm=llm, document_prompt=prompt)
   st.subheader("Generated Test Cases")
   st.write(chain.run(input_documents=combined_documents))

def main():
   st.title("Test Case Generator for Business Processes")
   
   business_process_doc = upload_document("Upload your business process document", ['txt', 'pdf', 'docx'])
   detailed_steps_docs = {}
   if business_process_doc:
       num_detailed_docs = st.number_input("Number of detailed steps documents", min_value=1, value=1, step=1)
       for i in range(num_detailed_docs):
           detailed_doc = upload_document(f"Upload detailed steps document {i+1}", ['txt', 'pdf', 'docx'])
           if detailed_doc:
               detailed_steps_docs[f"Detailed Steps Document {i+1}"] = detailed_doc
   if st.button("Generate Test Cases") and business_process_doc and detailed_steps_docs:
       process_documents(business_process_doc, detailed_steps_docs)
if __name__ == "__main__":
   main()