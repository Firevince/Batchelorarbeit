from sentence_transformers import SentenceTransformer

def document_embedding_MINI_LM(doc_text):
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    doc_embedding = model.encode(doc_text)
    return doc_embedding