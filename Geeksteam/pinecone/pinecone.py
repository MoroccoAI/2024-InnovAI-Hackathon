from pinecone import Pinecone
from dotenv import load_dotenv
import os
import jsonlines
import torch


load_dotenv(override=True)

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")


pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX)


def load_and_clean_json(file_path):
    try:
        with jsonlines.open(file_path, "r") as reader:
            # Read each line separately
            lines = [line for line in reader]

            return lines

    except Exception as e:
        print(f"Error: {e}")
        return None


def batch_insert(batch_size, corpus_embeddings):
    batch = 0
    vectors = []
    i = 0
    for data, encoding in zip(DATA, corpus_embeddings):
        # print(data, encoding)
        # break
        i += 1
        vector = {"id": f"id{i}", "values": "", "metadata": {"class_violation": ""}}
        vector["metadata"]["class_violation"] = str(data["feature_class"])
        vector["values"] = encoding
        vectors.append(vector)
        batch += 1
        if batch >= batch_size:
            index.upsert(vectors=vectors)
            vectors = []
            batch = 0
    # Insert any remaining vectors if the total is not a perfect multiple of batch_size
    if vectors:
        index.upsert(vectors=vectors)


if __name__ == "__main__":
    DATA = load_and_clean_json("finaldata/DATA_final.json")
    corpus_embeddings = torch.load("corpus_embeddings.pth")

    batch_insert(100, corpus_embeddings)
    print(index.describe_index_stats())
