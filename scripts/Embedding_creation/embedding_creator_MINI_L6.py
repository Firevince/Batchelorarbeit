from sentence_transformers import SentenceTransformer

def document_embedding(doc_text):
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    doc_embedding = model.encode(doc_text, show_progress_bar=True)
    return doc_embedding