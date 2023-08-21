import os
import logging
from dotenv import load_dotenv
from flask import Flask, request, render_template, jsonify
import pinecone
from langchain.llms import OpenAI
from langchain.vectorstores import Pinecone
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts.prompt import PromptTemplate

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
app = Flask(__name__)

llm_model = os.environ.get("LLM_MODEL")
open_api_key = os.environ.get("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_env = os.getenv("PINECONE_ENV")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")

# Validate environment variables
if not all([llm_model, open_api_key, pinecone_api_key, pinecone_env, pinecone_index_name]):
    logger.error("Missing required environment variables.")
    exit(1)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
custom_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question. At the end of standalone question add this 'Answer the question in English(USA) language.' If you do not know the answer reply with 'I am sorry'.
Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
CUSTOM_QUESTION_PROMPT = PromptTemplate.from_template(custom_template)

try:
    llm = OpenAI(openai_api_key=open_api_key, temperature=0)
    embeddings = OpenAIEmbeddings(openai_api_key=open_api_key)
    pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)
    vector_db = Pinecone.from_existing_index(pinecone_index_name, embeddings)
    qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        chain_type="stuff",
        retriever=vector_db.as_retriever(),
        condense_question_prompt=CUSTOM_QUESTION_PROMPT,
        return_source_documents=False,
        memory=memory,
    )
except Exception as e:
    logger.error(f"Failed to initialize services: {e}")
    exit(1)

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        question = data.get("question")
        question = question.strip()

        if not question:
            return jsonify({"error": "Please enter your question."})

        ai_response = qa({"question": question})
        return jsonify({"answer": ai_response["answer"]})
    except Exception as e:
        logger.error(f"Failed to process question: {e}")
        return jsonify({"error": "An error occurred while processing your question."})

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
