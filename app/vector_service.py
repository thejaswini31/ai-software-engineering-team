import chromadb

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="documents"
)

def store_chunk(
    chunk,
    embedding,
    chunk_id
):

    collection.add(
        ids=[str(chunk_id)],
        documents=[chunk],
        embeddings=[embedding]
    )


def search_chunks(
    query_embedding,
    top_k=3
):

    results = collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=top_k
    )

    return results