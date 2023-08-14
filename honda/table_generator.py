import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.schema import Document
import csv
import os
import openai
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
)
from langchain.document_loaders import PyPDFDirectoryLoader, PyPDFLoader
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains.question_answering import load_qa_chain
import pickle
import PyPDF2
from langchain.chains import RetrievalQAWithSourcesChain

load_dotenv()
openai.api_type = "azure"
openai.api_version = "2023-05-15"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")
specifications = [
    "Year",
    "Engine Type",
    "Engine Displacement",
    "Horsepower (HP)",
    "Torque",
    "Transmission Type",
    "Fuel Efficiency",
    "Drive Type",
    "Seating Capacity",
    "Cargo Capacity",
    "Safety Features",
    "Infotainment System",
    "Advanced Driver Assistance Systems (ADAS)",
    "Dimensions",
    "Suspension Type",
    "Brake Type",
    "Top Speed",
    "Acceleration (0-60 mph or 0-100 km/h)",
    "Towing Capacity",
    "Warranty",
    "Price",
]

# models = {
#     "IGNIS": "IGNIS GL, IGNIS GLX",
#     "Jimny": "Jimny Lite, Jimny",
#     "Swift Sport": "Swift Sport",
#     "Swift": "Swift GL, Swift GL Plus, Swift GLX Turbo",
#     "Vitara": "Vitara, Vitara Turbo, Vitara Turbo Allgrip",
# }
models = {
    "Civic": "Civic VTi LX, Civic e:HEV LX",
    "Accord": "Accord VTi-LX Petrol, Accord VTi-LX Hybrid",
    "HR-V": "HR-V Vi X Petrol, HR-V e:HEV L Hybrid",
    "ZR-V": "ZR-V VTi X, ZR-V VTi L, ZR-V VTi LX, ZR-V e:HEV LX",
    "CR-V": "CR-V Vi, CR-V VTi, CR-V VTi L AWD, CR-V VTi L7, CR-V VTi LX AWD, CR-V VTi 7 + Luxe, CR-V VTi 7, CR-V VTi X",
}
llm = AzureChatOpenAI(
    deployment_name="GPT3-5",
    temperature=0.0,
    openai_api_type="azure",
    openai_api_version="2023-05-15",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_API_BASE"),
)


class VectorDB:
    def __init__(self):
        pass

    def get_pdf_text(self, pdf_path):
        data = []
        with open(pdf_path, "rb") as pdf_docs:
            pdf_reader = PyPDF2.PdfReader(pdf_docs)
            page_num = 0
            num_pages = len(pdf_reader.pages)
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                page_num += 1
                data.append(Document(page_content=text, metadata={"page": page_num}))
        return data

    def get_text_chunks(self, text):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, length_function=len
        )
        chunks = text_splitter.split_documents(text)
        print(f"Total number of chunks: {len(chunks)}")
        return chunks

    def create_pickles(self, chunks, name):
        store_name = name
        if os.path.exists(f"{store_name}.pkl"):
            with open(f"pickles/{store_name}.pkl", "rb") as f:
                VectorStore = pickle.load(f)

        else:
            embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
            VectorStore = FAISS.from_documents(chunks, embedding=embeddings)

            with open(f"{store_name}.pkl", "wb") as f:
                pickle.dump(VectorStore, f)
        return VectorStore


class TableGenerator:
    def generate_table(self, VectorStore, query):
        docs = VectorStore.similarity_search(query=query,k=2)
        # for doc in docs:
        #     print(doc)
        #     print("\n")
        print(len(docs))
        chain = load_qa_chain(llm=llm, chain_type="stuff", verbose=False)
        with get_openai_callback() as cb:
            response = chain.run(input_documents=docs, question=query)
        print(cb)
        return response

    def save_to_csv(self, data, file_path):
        with open(file_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)

            lines = data.split("\n")

            for line in lines:
                writer.writerow(line.split("|")[1:-1])


def main():
    year = "2023"

    for model, model_names in models.items():
        query = f"""Generate a table of specifications of {model} variants like {model_names}.
        Specifications : {specifications}
        If any specifications like Engine Displacement, Drive Type is not available in the given context, just give NULL.
        Use specifications as columns and model names as rows. In the Year column print {year} only and nothing else.
        [ONLY USE THE GIVEN CONTEXT AND NOTHING ELSE.]
        """

        path = f"{year}-Test/Honda-{model}-{year}.pdf"
        # path = f"Suzuki/Suzuki-{model}.pdf"
        if path:
            db = VectorDB()
            raw_text = db.get_pdf_text(path)
            text_chunks = db.get_text_chunks(raw_text)
            store = db.create_pickles(text_chunks, model)
            q = TableGenerator()
            table = q.generate_table(store, query)
            q.save_to_csv(table, f"Tables/{model}-{year}.csv")


if __name__ == "__main__":
    main()
