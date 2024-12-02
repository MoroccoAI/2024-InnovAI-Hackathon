# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity

# def evaluate_user_responses(reference_answers, user_responses, model_name="all-MiniLM-L6-v2"):
#     """
#     Evaluate user responses against reference answers using cosine similarity.
#     :param reference_answers: List of correct answers.
#     :param user_responses: List of user-provided answers.
#     :param model_name: SentenceTransformer model for embeddings.
#     :return: List of similarity scores.
#     """
#     try:
#         if len(reference_answers) != len(user_responses):
#             raise ValueError("Mismatch in the number of reference answers and user responses.")

#         model = SentenceTransformer(model_name)
#         ref_embeddings = model.encode(reference_answers)
#         user_embeddings = model.encode(user_responses)

#         # Calculate cosine similarity scores
#         return [
#             cosine_similarity([ref_emb], [user_emb])[0][0]
#             for ref_emb, user_emb in zip(ref_embeddings, user_embeddings)
#         ]
#     except Exception as e:
#         print(f"Error during evaluation: {e}")
#         return []



from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

def evaluate_user_responses(reference_answers, user_responses, model_name="all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name)
    ref_embeddings = model.encode(reference_answers)
    user_embeddings = model.encode(user_responses)
    return [cosine_similarity([ref], [usr])[0][0] for ref, usr in zip(ref_embeddings, user_embeddings)]
