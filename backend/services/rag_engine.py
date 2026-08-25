import re
from .data_ingester import get_collection, model

SYSTEM_PROMPT = """You are NirmaAI, the official FAQ assistant for Nirma University, Ahmedabad.
Answer only from CONTEXT DATA. Preserve exact names, numbers, currency, units, and years. If the context does not answer the question, say: I don't have that information in my current database. Please check the official website at nirmauni.ac.in or contact the relevant department.
Always cite the source file, such as Source: faculty.json. Never guess or mention internal implementation details."""

STOP = {"the", "is", "of", "a", "an", "what", "are", "was", "where", "who", "which", "from", "at", "in", "for", "does", "do", "and", "to"}
INTENTS = {
    "hod": ("faculty.json", ("hod", "head", "cse", "faculty")),
    "package": ("placements.json", ("highest", "package", "placement", "2025", "2026")),
    "fees": ("fees.json", ("fee", "fees", "btech", "tuition")),
    "library": ("campus_map.json", ("library", "central", "location")),
    "recruiters": ("placements.json", ("recruit", "companies", "google", "linkedin", "amazon", "microsoft")),
    "gate": ("fees.json", ("gate", "scholarship", "mtech")),
}

def tokens(text):
    return {x for x in re.findall(r"[a-z0-9]+", text.lower()) if x not in STOP and len(x) > 1}

def intent_for(question):
    q = question.lower()
    if "hod" in q or "head of" in q: return "hod"
    if "package" in q or ("placement" in q and "highest" in q): return "package"
    if "fee" in q or "tuition" in q: return "fees"
    if "library" in q: return "library"
    if any(x in q for x in ("recruit", "companies", "company")): return "recruiters"
    if "gate" in q and "scholar" in q: return "gate"
    return None

def query_rag(question: str):
    collection = get_collection()
    count = collection.count()
    raw = collection.query(query_embeddings=model.encode([question]).tolist(), n_results=min(12, count)) if count else {"documents": [[]], "metadatas": [[]]}
    docs, metas = raw.get("documents", [[]])[0] or [], raw.get("metadatas", [[]])[0] or []
    intent = intent_for(question)
    wanted_file, wanted_terms = INTENTS.get(intent, (None, ()))
    qtokens = tokens(question)
    ranked = []
    for index, (doc, meta) in enumerate(zip(docs, metas)):
        text = f"{doc} {meta.get('entity_name','')} {meta.get('department','')}".lower()
        overlap = len(qtokens & tokens(text))
        hits = sum(term in text for term in wanted_terms)
        score = overlap + hits * 2 + (8 if wanted_file and meta.get("source_file") == wanted_file else 0)
        if intent == "library" and "library" in text: score += 6
        ranked.append((score - index * 0.01, doc, meta))
    ranked.sort(reverse=True, key=lambda item: item[0])
    selected = ranked[:5]
    chunks = [x[1] for x in selected]
    sources, seen, context = [], set(), []
    for i, (chunk, meta) in enumerate(((x[1], x[2]) for x in selected), 1):
        source = meta.get("source_file", "unknown")
        key = (source, meta.get("entity_name", ""))
        if key not in seen:
            sources.append({"file": source, "section": meta.get("entity_name", meta.get("category", "")), "excerpt": chunk[:180] + ("..." if len(chunk) > 180 else "")})
            seen.add(key)
        context.append(f"[Source {i}: {source} → {meta.get('category','general')} → {meta.get('entity_name','')}]\n{chunk}")
    top_score = selected[0][0] if selected else 0
    confidence = round(min(0.99, max(0.05, 0.35 + top_score / 40)), 2) if selected else 0.05
    context_text = "\n\n---\n\n".join(context) or "No relevant context found."
    prompt = f"{SYSTEM_PROMPT}\n\n--- CONTEXT DATA ---\n{context_text}\n--- END CONTEXT ---\n\nStudent Question: {question}\nAnswer concisely using exact evidence and cite the source file."
    return chunks, prompt, sources, confidence

def get_retrieval_confidence(question):
    return query_rag(question)[3]
