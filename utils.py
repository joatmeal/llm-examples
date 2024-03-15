import docx
import fitz  # PyMuPDF
def read_pdf(file):
   with fitz.open(stream=file.read(), filetype="pdf") as doc:
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
def read_txt(file):
   return file.read().decode("utf-8")
