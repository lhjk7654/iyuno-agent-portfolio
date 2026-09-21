from app.retriever import search


def search_documents(query: str, top_k: int = 5) -> dict:
    """
    Search the cybersecurity and AI document collection.
    """

    results = search(query, top_k=top_k)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    sources = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances,
    ):
        sources.append(
            {
                "source": metadata["source"],
                "chunk": metadata["chunk_index"],
                "distance": distance,
                "text": document,
            }
        )

    return {
        "query": query,
        "results": sources,
    }


def get_document_stats() -> dict:
    """
    Return basic statistics about the document collection.
    """

    result = search_documents(
        "cybersecurity",
        top_k=5,
    )

    unique_sources = {
        item["source"]
        for item in result["results"]
    }

    return {
        "documents_in_search_results": len(unique_sources),
        "top_k": 5,
    }