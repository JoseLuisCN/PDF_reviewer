import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from dotenv import load_dotenv
import os
from neuro_san.interfaces.coded_tool import CodedTool
from typing import Any
from typing import Dict
from typing import List
# ----------------------------
# 1. Configure Gemini API
# ----------------------------

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

EMBED_MODEL = "models/text-embedding-004"  # gemini-embedding-001 alias

script_dir = os.path.dirname(os.path.abspath(__file__))

pdf_path = os.path.join(script_dir, "airline_faq.pdf")

# 2. Embedding function for Chroma
# ----------------------------
class GeminiEmbeddingFunction:
    def embed_documents(self, texts):
        embeddings = []
        for text in texts:
            result = genai.embed_content(
                model=EMBED_MODEL,
                content=text,
                task_type="retrieval_document"
            )
            embeddings.append(result["embedding"])
        return embeddings

    def embed_query(self, text):
        result = genai.embed_content(
            model=EMBED_MODEL,
            content=text,
            task_type="retrieval_query"
        )
        return result["embedding"]

embedding_fn = GeminiEmbeddingFunction()

# ----------------------------
# 3. Load document from same folder as script
# ----------------------------


loader = PyPDFLoader(pdf_path)
documents = loader.load()

# ----------------------------
# 4. Split into chunks
# ----------------------------
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(documents)

# ----------------------------
# 5. Store in Chroma
# ----------------------------
vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_fn,
    persist_directory=os.path.join(script_dir, "chroma_store")
)
vectordb.persist()

# ----------------------------
# 6. Retrieval + Gemini 2.5 Flash
# ----------------------------

class RagTool(CodedTool):

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> str:
        retriever = vectordb.as_retriever(search_kwargs={"k": 5})
        user_query = args.get("user_query")
        relevant_docs = retriever.get_relevant_documents(user_query)

        # Build context for prompt
        context_text = "\n\n".join([doc.page_content for doc in relevant_docs])

        prompt = f"""
        You are an assistant with access to retrieved context.
        Use only the provided context to answer the question.
        
        Context:
        {context_text}

        Question:
        {user_query}
        """

        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text




