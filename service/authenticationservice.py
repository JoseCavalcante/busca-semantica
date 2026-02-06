from pinecone import Pinecone
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def authentication_pinecone():
   api_key = os.getenv("PINECONE_API_KEY")

   if not api_key:
       raise RuntimeError("PINECONE_API_KEY não encontrada no ambiente")

   pc = Pinecone(api_key=api_key)
   return pc

def authentication_openai():

   api_key = os.getenv("OPENAI_API_KEY")

   if not api_key:
       raise RuntimeError("OPENAI_API_KEY não encontrada no ambiente")

   clientOpenAI = OpenAI(api_key=api_key)
   return clientOpenAI