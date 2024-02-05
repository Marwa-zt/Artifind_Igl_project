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
    prefix='/articles',
    tags=['articles']
)


api_key = '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'

if api_key is None:
    raise EnvironmentError("OpenAI API key is not provided.")

# Create schema
schema = {
    "properties": {
        "title": {"type": "string"},
        "authors": {"type": "array", "items": {"type": "string"}},
        "institutes": {"type": "array", "items": {"type": "string"}},
        "abstract": {"type": "string"},
        "keywords": {"type": "array", "items": {"type": "string"}},
        "publication date": {"type": "string", "format": "date"}
    },
}

# Run chain
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", api_key=api_key)
chain = create_extraction_chain(schema, llm)

@router.post("/upload")
async def extract(request: Request, file: UploadFile = File(...)):
    try:
        # PDF Text Extraction
        file_content = await file.read()
        with open('pdf_file.pdf', 'wb') as f:
            f.write(file_content)

        with open('pdf_file.pdf', 'rb') as pdf_file:
            # Create a PDF reader object
            pdf_document = fitz.open(pdf_file)
            num_pages = pdf_document.page_count
            text = ''.join(pdf_document[i].get_text() for i in range(num_pages))

            first_part = ''.join(pdf_document[i].get_text() for i in range(2))
            second_part = [
                Document(page_content=pdf_document[-3].get_text(), metadata={'source': 'file_name', 'page': num_pages - 2}),
                Document(page_content=pdf_document[-2].get_text(), metadata={'source': 'file_name', 'page': num_pages - 1}),
            ]

        extracted_data = chain.invoke(first_part)

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

    except Exception as e:
        # Handle exceptions and return an appropriate response
        return HTTPException(status_code=500, detail=str(e))
