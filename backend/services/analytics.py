import time
from .data_ingester import chroma_client

def get_analytics_collection():
    return chroma_client.get_or_create_collection("query_analytics")

def log_query(question: str, answer: str, tier_used: str, response_time_ms: float):
    try:
        collection = get_analytics_collection()
        topic = "general"
        if "faculty" in question.lower(): topic = "faculty"
        elif "placement" in question.lower(): topic = "placements"
        elif "fee" in question.lower(): topic = "fees"
        elif "campus" in question.lower() or "building" in question.lower(): topic = "campus"
        
        doc_id = f"query_{int(time.time() * 1000)}"
        collection.add(
            documents=[question],
            metadatas=[{
                "timestamp": time.time(),
                "answer_preview": answer[:100],
                "tier_used": tier_used,
                "response_time_ms": response_time_ms,
                "category": topic
            }],
            ids=[doc_id]
        )
    except Exception as e:
        print(f"Error logging analytics: {e}")

def get_summary():
    try:
        collection = get_analytics_collection()
        docs = collection.get()
        total_queries = len(docs['ids'])
        
        topic_counts = {}
        total_time = 0
        for meta in docs['metadatas']:
            topic = meta.get('category', 'general')
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
            total_time += meta.get('response_time_ms', 0)
            
        avg_time = total_time / total_queries if total_queries > 0 else 0
        popular_topics = [{"topic": k, "count": v} for k, v in topic_counts.items()]
        
        return {
            "total_queries": total_queries,
            "popular_topics": popular_topics,
            "avg_response_time_ms": avg_time
        }
    except Exception:
        return {
            "total_queries": 0,
            "popular_topics": [],
            "avg_response_time_ms": 0.0
        }
