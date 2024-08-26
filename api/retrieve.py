from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama 
from langchain_community.chat_message_histories import ChatMessageHistory

from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain_huggingface import HuggingFaceEmbeddings

from prompts import system_prompt, context_prompt

import uuid

persist_directory = '../chroma'

llm = Ollama(model="aya")

db = Chroma(
        persist_directory=persist_directory,
        embedding_function=HuggingFaceEmbeddings(
            model_name='intfloat/multilingual-e5-small',
            model_kwargs={'device': 'cpu'}
        )
    )

retriever = db.as_retriever()

compressor = LLMChainExtractor.from_llm(llm)
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=retriever
)

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def get_response(query):
    context_prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", context_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    
    history_retriever = create_history_aware_retriever(
        llm, retriever, context_prompt_template
    )
    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    chain = create_retrieval_chain(history_retriever, question_answer_chain)
    
    # response = chain.invoke({"input": query})
    
    rag_chain = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )
    
    response = rag_chain.invoke(
        {
        'input': query
        },
        config={
            'configurable': {
                'session_id' : uuid.uuid4()
            }
        },
    )['answer']
    
    return response