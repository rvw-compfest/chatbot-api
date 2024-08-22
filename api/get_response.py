from langchain.prompts import ChatPromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain_community.llms import Ollama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


persist_directory = "./chroma"

PROMPT_TEMPLATE = """
Anda adalah seorang paralegal hukum AI. Anda akan diberikan konteks
untuk menjawab pertanyaan yang diberikan. Jika jawaban dari pertanyaan yang diberikan
tidak ada pada konteks, cukup jawab dengan "Maaf, saya tidak tahu tentang hal itu" dan jangan membuat
jawaban sendiri. Jawaban yang anda berikan harus jelas dan minimal terdiri dari 2 paragraf.
Jawab pertanyaan yang diberikan hanya berdasarkan konteks berikut:

{context}

---

Jawab pertanyaan berikut berdasarkan konteks: {question}
"""

db = Chroma(
        collection_name="law_db",
        persist_directory=persist_directory,
        embedding_function=HuggingFaceEmbeddings(
            model_name="intfloat/multilingual-e5-small",
            model_kwargs={'device': 'cpu'}
        )
    )

retriever = db.as_retriever()

def create_agent_chain():
    model_name = "aya"
    llm = Ollama(model=model_name)
    chain = load_qa_chain(llm, chain_type="stuff")
    return chain

def get_llm_response(query):
    chain = create_agent_chain()
    result = db.similarity_search(query, k=5)

    context = "\n\n---\n\n".join([doc.page_content for doc in result])

    template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    prompt = template.format(context=context, question=query)

    answer = chain.invoke({
        "input_documents": result,
        "question": prompt
    })
    
    response = {
        "response": answer['output_text'],
    }

    return response