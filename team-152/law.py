from langchain.chains.question_answering import load_qa_chain
from langchain_community.vectorstores import Pinecone
import os
from dotenv import load_dotenv
from langchain_community.llms import OpenAI
from pinecone import Pinecone, ServerlessSpec
from langchain_community.vectorstores import Pinecone as LangChainPinecone
from langchain_openai import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI


class Law:
    def __init__(self):
        # Load environment variables
        load_dotenv()

        # Initialize Pinecone
        self.pc = Pinecone(
            api_key=os.environ.get("PINECONE_API_KEY")
        )

        self.index_name = 'low2'
        # Connect to the index
        self.index = self.pc.Index(self.index_name)

        # Set up embeddings
        self.openAiKey = os.environ["OPENAI_API_KEY"]
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.openAiKey)

        # LangChain Pinecone wrapper
        self.book_docsearch = LangChainPinecone(
            index=self.index,
            embedding=self.embeddings,
            text_key="text"  # Ensure documents use this key for storing text
        )

        # LLM setup
        self.llm = ChatOpenAI(model_name="gpt-4", temperature=0.3, openai_api_key=self.openAiKey)

    def getLaw(self, prompt, chat_hist):
        # Prompt templates
        from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate

        template = """
        You are a knowledgeable legal assistant specializing in providing accurate and concise information about laws and legal frameworks. Your role is to assist users by interpreting their queries, offering reliable legal insights, and guiding them to the most relevant legal resources or concepts. You do not offer legal advice but provide general information and clarifications based on the user's questions.

        Your communication style is professional, clear, and neutral. Respond using appropriate legal terminology and explain concepts in a way that is easy to understand. If additional details are needed to address the query, ask specific and targeted follow-up questions.

        Focus on delivering precise and relevant responses, ensuring the user understands the legal principles or frameworks related to their inquiry. 

        {document}

        Here is the chat history:
        """ + str(chat_hist) + """
        """
        docs = self.book_docsearch.similarity_search(prompt)

        # LLM chain
        llm = OpenAI(temperature=0.3, openai_api_key=self.openAiKey)
        chain = load_qa_chain(llm, chain_type="stuff")
        # Perform similarity search


        # Run the chain with the required inputs
        response = chain.run(
            input_documents= docs,  # Pass the combined document text
            question= prompt  # Pass the user query
        )

        return response