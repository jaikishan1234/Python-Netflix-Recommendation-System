
from src.embedding_model import EmbeddingModel

embedding_model = EmbeddingModel()

text = "A space adventure about saving humanity."
embedding = embedding_model.embed(text)

print("Text:", text)
print("Embedding dimensions:", len(embedding))
print("First five values:", embedding[:5])
