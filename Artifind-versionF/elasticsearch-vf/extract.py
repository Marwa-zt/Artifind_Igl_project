import json
import requests
import fitz
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from langchain_openai import ChatOpenAI
from langchain.chains import create_extraction_chain
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.schema.document import Document
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain  



router = APIRouter(
    prefix='/extract',
    tags=['extract']
)

api_key = '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'

if api_key is None:
    raise EnvironmentError("OpenAI API key is not provided.")

# Create schema
schema = {
    "properties": {
        "titre": {"type": "string"},
        "auteur": {"type": "array", "items": {"type": "string"}},
        "institutions": {"type": "array", "items": {"type": "string"}},
        "resume": {"type": "string"},
        "motscles": {"type": "array", "items": {"type": "string"}},
        "date": {"type": "string", "format": "date"},
        "url": {"type": "string"}
    },
}

# Run chain
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", api_key=api_key)
chain = create_extraction_chain(schema, llm)

@router.post("/articles/upload")
async def extract(request: Request):
    try:
        data = await request.json()
        url = data.get("url")
        if not url:
            raise HTTPException(status_code=400, detail="URL not provided in the request.")

        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch PDF from the provided URL.")

        # Extract text from PDF
        pdf_content = response.content
        pdf_document = fitz.open("pdf", pdf_content)
        num_pages = pdf_document.page_count
        text = ''.join(pdf_document[i].get_text() for i in range(num_pages))
        first_part = ''.join(pdf_document[i].get_text() for i in range(2))  # Extracting text from first 2 pages
        second_part = [
            Document(page_content=pdf_document[-1].get_text(), metadata={'source': 'file_name', 'page': num_pages - 1}),
        ]

        extracted_data = chain.invoke(first_part)

        extracted_data["url"] = url

        # FAISS Vector Store and Conversational Retrieval Chain
        db = FAISS.from_documents(second_part, OpenAIEmbeddings(openai_api_key=api_key))
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        qa = ConversationalRetrievalChain.from_llm(OpenAI(openai_api_key=api_key, temperature=0), db.as_retriever(), memory=memory)

        # Ask a question
        query = "write the first 3 references. Generally, there is a keyword 'References' before them. Write all the reference (writers + articles). Separate them by a '|'."
        result = qa({"question": query})
        references_string = result['answer']

        if isinstance(extracted_data, list):
            extracted_data = extracted_data[0]

        references = references_string.split('|')
        extracted_data['references'] = references
        extracted_data['text'] = text

        return {"data": extracted_data}

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
