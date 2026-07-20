import pandas as pd
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DataFrameLoader
import tiktoken
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import List, Literal, Optional, Any
from langchain_core.messages import HumanMessage

from langchain_milvus import Milvus
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
import torch

from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
import pickle
from typing import Callable, List, Optional
import os
import json

from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document

from typing import List

import nltk
from langdetect import LangDetectException, detect
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")
import os

from dotenv import load_dotenv
from langchain_core.language_models import BaseLanguageModel
from langchain_openai import AzureChatOpenAI, AzureOpenAI, AzureOpenAIEmbeddings

load_dotenv()

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", None)
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION", None)
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", None)


def capture_value_error(*args: List[Any]) -> None:
    for value in args:
        if value is None:
            raise ValueError(
                f"{value.__name__} environment variable is missing or empty."
            )


def load_openai_llm(
    ask_or_chat: Literal["chat", "ask"], **llm_kwargs: Any
) -> BaseLanguageModel:
    capture_value_error(AZURE_OPENAI_API_KEY, OPENAI_API_VERSION, AZURE_OPENAI_ENDPOINT)
    if ask_or_chat == "ask":
        return AzureOpenAI(
            api_key=AZURE_OPENAI_API_KEY,
            api_version=OPENAI_API_VERSION,
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            deployment_name="davinci",
            **llm_kwargs,
        )
    elif ask_or_chat == "chat":
        return AzureChatOpenAI(
            openai_api_version=OPENAI_API_VERSION,
            openai_api_key=AZURE_OPENAI_API_KEY,
            deployment_name="chat",
            **llm_kwargs,
        )
    else:
        raise ValueError("Invalid value for 'ask_or_chat'. Expected 'ask' or 'chat'.")


stemmer = PorterStemmer()


def detect_language(sentence: str) -> str:
    try:
        language = detect(sentence)
    except LangDetectException:
        language = None
    return language


def preprocess_text(sentence: str) -> List[str]:
    language = detect_language(sentence)
    if language == "en":
        stop_words = set(stopwords.words("english"))
    elif language == "fr":
        stop_words = set(stopwords.words("french"))
    else:
        stop_words = set(stopwords.words("english")) | set(stopwords.words("french"))
    return [
        stemmer.stem(word.lower())
        for word in word_tokenize(sentence)
        if word.isalnum() and word.lower() not in stop_words
    ]


class Vectorstore(ABC):
    @abstractmethod
    def transform(self):
        ...

    @abstractmethod
    def load(self):
        ...


@dataclass
class BM25Config:
    path: Optional[str] = None
    b: float = 0.75
    k1: float = 1.2


def load_config(path: str) -> BM25Config:
    with open(os.path.join(path, "config.json"), "r") as f:
        config = BM25Config(**json.load(f))
    return config


def save_config(path: str, config: BM25Config):
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, "config.json"), "w") as f:
        json.dump(asdict(config), f)


class BM25(Vectorstore):
    def __init__(
        self,
        config: Optional[BM25Config] = None,
        preprocess_func: Callable[[str], List[str]] = preprocess_text,
        path: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.preprocess_func = preprocess_func

        if config is not None:
            save_config(path=config.path, config=config)
        elif path is not None:
            config = load_config(path)
        else:
            raise ValueError()
        self.config = config

    def transform(self, documents: List[Document]):
        bm25_retriever = BM25Retriever.from_documents(
            documents=documents,
            preprocess_func=self.preprocess_func,
            bm25_params={"b": self.config.b, "k1": self.config.k1},
            k=20,
        )

        save_path = os.path.join(self.config.path, "db.index")
        with open(save_path, "wb") as f:
            pickle.dump(bm25_retriever, f, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self):
        load_path = os.path.join(self.config.path, "db.index")
        with open(load_path, "rb") as f:
            bm25_retriever = pickle.load(f)
        return bm25_retriever




def torch_device(device_id: int = 0) -> str:
    if torch.cuda.is_available():
        return f"cuda:{device_id}"
    return "cpu"


@dataclass
class MilvusConfig:
    embedding_model_name: str
    path: Optional[str] = None
    metric_type: Literal["COSINE"] = "COSINE"
    index_type: Literal["HNSW"] = "HNSW"
    M: int = 4
    ef: int = 500
    efConstruction: int = 400


def load_config(path: str) -> MilvusConfig:
    with open(os.path.join(path, "config.json"), "r") as f:
        config = MilvusConfig(**json.load(f))
    return config


def save_config(path: str, config: MilvusConfig):
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, "config.json"), "w") as f:
        json.dump(asdict(config), f)


class MilvusVectorstore(Vectorstore):
    def __init__(
        self, config: Optional[MilvusConfig] = None, path: Optional[str] = None
    ) -> None:
        super().__init__()
        if config is not None:
            save_config(path=config.path, config=config)
        elif path is not None:
            config = load_config(path)
        else:
            raise ValueError()
        self.config = config

        self.embedding = HuggingFaceEmbeddings(
            model_name=config.embedding_model_name,
            model_kwargs={"device": torch_device(), "trust_remote_code": True},
        )
        self.index_params = {
            "metric_type": config.metric_type,
            "index_type": config.index_type,
            "params": {"M": config.M, "efConstruction": config.efConstruction},
        }
        self.search_params = {
            "metric_type": config.metric_type,
            "params": {"ef": config.ef},
        }

    def transform(self, documents: List[Document]):
        return Milvus.from_documents(
            documents=documents,
            embedding=self.embedding,
            collection_name="vectorstore",
            connection_args={"uri": os.path.join(self.config.path, "index.db")},
            index_params=self.index_params,
            search_params=self.search_params,
        )

    def load(self):
        return Milvus(
            embedding_function=self.embedding,
            collection_name="vectorstore",
            connection_args={"uri": os.path.join(self.config.path, "index.db")},
            index_params=self.index_params,
            search_params=self.search_params,
        )


encoder = tiktoken.get_encoding("cl100k_base")


def num_tokens_text(text: str) -> int:
    return len(encoder.encode(text))


def create_vectorstore_vector_search(
    dataframe_path: str,
    embedding_model_name: str,
    path: str,    
    metric_type: Literal["COSINE"] = "COSINE",
    index_type: Literal["HNSW"] = "HNSW",
    M: int = 4,
    ef: int = 500,
    efConstruction: int = 400,
    chunk_size: int = 512,
    chunk_overlap: int = 20,
) -> MilvusVectorstore:
    data = pd.read_csv(dataframe_path)
    data = data[data["content"].notna()]

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n"],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=num_tokens_text,
    )
    loader = DataFrameLoader(data, page_content_column="content")
    documents = loader.load_and_split(text_splitter=text_splitter)

    config = MilvusConfig(
        embedding_model_name=embedding_model_name,
        path=path,
        metric_type=metric_type,
        index_type=index_type,
        M=M,
        ef=ef,
        efConstruction=efConstruction,
    )
    vs = MilvusVectorstore(config=config)
    vs.transform(documents=documents)
    return vs


def create_vectorstore_keyword_search(
    dataframe_path: str,
    path: str,
    b: float,
    k1: float,
):
    data = pd.read_csv(dataframe_path)
    data = data[data["content"].notna()]

    loader = DataFrameLoader(data, page_content_column="content")
    documents = loader.load()

    config = BM25Config(path=path, b=b, k1=k1)

    r = BM25(config=config, preprocess_func=preprocess_text)
    r.transform(documents=documents)


if __name__ == "__main__":


    SYSTEM_TEMPLATE = """
    <context>
    {context}
    </context>
    """

    question_answering_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                SYSTEM_TEMPLATE,
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    retriever = create_vectorstore_vector_search(dataframe_path=dataframe_path, embedding_model_name="dunzhang/stella_en_400M_v5")
    docs = retriever.invoke("Can LangSmith help test my LLM applications?")
    docs
    
    chat = load_openai_llm(ask_or_chat="chat", temperature=0.0)
    document_chain = create_stuff_documents_chain(chat, question_answering_prompt)
    document_chain.invoke(
        {
            "context": docs,
            "messages": [
                HumanMessage(content="Can LangSmith help test my LLM applications?")
            ],
        }
    )
