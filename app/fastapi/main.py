from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.document_loaders import UnstructuredURLLoader
from langchain.indexes import VectorstoreIndexCreator
import os
from apikey import OPENAI_API_KEY

os.environb[b"OPEN_AI_KEY"] = OPENAI_API_KEY.encode()

urls = [
    "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-february-8-2023",
    "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-february-9-2023"
]
loader = UnstructuredURLLoader(urls=urls)
index = VectorstoreIndexCreator().from_loaders([loader])

app = FastAPI()

class Item(BaseModel):
    query: str

@app.get('/')
def read_root():
    return {"Hello": "WORLD"}

@app.post('/')
def reply(item: Item):
    try:
        response = index.query(item.query)
        return response
    except:
        return {"message": "Some Error Occurred"}
