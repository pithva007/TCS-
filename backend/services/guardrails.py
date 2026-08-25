import re

# Prompt injection patterns
INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+(instructions|prompts|context)",
    r"you\s+are\s+no\s+longer",
    r"forget\s+(everything|all|your)\s+(you|instructions|rules)",
    r"(disregard|override|bypass)\s+(your|all|the)\s+(rules|instructions|guardrails|safety)",
    r"system\s*prompt",
    r"act\s+as\s+(a\s+)?different",
    r"pretend\s+(to\s+be|you\s+are)",
    r"jailbreak",
    r"DAN\s+mode",
    r"developer\s+mode",
    r"reveal\s+(your|the)\s+(prompt|instructions|system)",
]

# Profanity list (basic set)
PROFANITY_WORDS = {
    "fuck", "shit", "bitch", "asshole", "bastard", "dick", "cunt",
    "motherfucker", "bullshit", "damn", "piss", "slut", "whore",
}

# Keywords that indicate university/education relevance
UNIVERSITY_KEYWORDS = {
    "nirma", "university", "college", "faculty", "professor", "hod",
    "department", "placement", "package", "salary", "company", "recruit",
    "fee", "tuition", "admission", "course", "syllabus", "semester",
    "campus", "hostel", "library", "lab", "building", "canteen",
    "sports", "club", "event", "exam", "result", "scholarship",
    "btech", "mtech", "mba", "mca", "phd", "engineering",
    "cse", "ece", "mechanical", "civil", "electrical", "chemical",
    "itnu", "imnu", "iop", "ios", "iol", "ahmedabad", "gujarat",
    "gate", "jee", "gujcet", "acpc", "nri", "student", "academic",
    "research", "specialization", "qualification", "degree",
    "internship", "career", "industry", "tcs", "google", "amazon",
    "infosys", "microsoft", "linkedin", "nvidia", "atlassian",
    "parking", "bus", "brts", "metro", "canteen", "food",
    "auditorium", "gym", "swimming", "cricket", "director", "dean",
    "principal", "registrar", "contact", "email", "phone",
    "hi", "hello", "hey", "help", "what", "who", "where", "when",
    "how", "which", "tell", "list", "show", "find", "search",
}


def check_input(query: str) -> dict:
    """Validate and sanitize user input. Returns safety status and sanitized query."""

    # Length check
    if not query or not query.strip():
        return {"is_safe": False, "sanitized_query": None,
                "rejection_reason": "Please enter a question to get started!"}

    if len(query) > 500:
        return {"is_safe": False, "sanitized_query": None,
                "rejection_reason": "Your question is too long. Please keep it under 500 characters."}

    sanitized = query.strip()
    lower_query = sanitized.lower()

    # Prompt injection check
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, lower_query, re.IGNORECASE):
            return {"is_safe": False, "sanitized_query": None,
                    "rejection_reason": "I'm designed to answer questions about Nirma University. Let me know how I can help!"}

    # Profanity check
    words = set(re.findall(r'\b\w+\b', lower_query))
    if words & PROFANITY_WORDS:
        return {"is_safe": False, "sanitized_query": None,
                "rejection_reason": "Please keep the conversation respectful. How can I help you with Nirma University information?"}

    # Relevance check — allow short/greeting queries, but flag clearly off-topic long queries
    if len(sanitized) > 20:
        query_words = set(re.findall(r'\b\w+\b', lower_query))
        relevance_score = len(query_words & UNIVERSITY_KEYWORDS) / max(len(query_words), 1)
        if relevance_score < 0.05 and len(query_words) > 8:
            return {"is_safe": False, "sanitized_query": None,
                    "rejection_reason": "I specialize in Nirma University information — placements, faculty, fees, campus facilities, and more. Could you rephrase your question about Nirma?"}

    return {"is_safe": True, "sanitized_query": sanitized, "rejection_reason": None}


def verify_output(answer: str, context_chunks: list) -> str:
    """Post-process the LLM output for safety and quality."""
    if not answer:
        return "I apologize, but I couldn't generate a response. Please try rephrasing your question."

    # Strip any leaked system prompt or internal references
    leak_patterns = [
        r"(system\s*prompt|SYSTEM_PROMPT|api[_\s]*key|API_KEY|GROQ|CEREBRAS|\.env)",
        r"(chromadb|sentence.transformers|embedding|vector.store)",
    ]
    for pattern in leak_patterns:
        if re.search(pattern, answer, re.IGNORECASE):
            # Remove the offending section rather than blocking the whole answer
            answer = re.sub(pattern, "[redacted]", answer, flags=re.IGNORECASE)

    # Add disclaimer if answer seems uncertain
    uncertainty_markers = [
        "i don't have", "not available", "no information",
        "cannot find", "not in my", "i'm not sure",
    ]
    if any(marker in answer.lower() for marker in uncertainty_markers):
        if "nirmauni.ac.in" not in answer:
            answer += "\n\n_For the latest information, please visit [nirmauni.ac.in](https://nirmauni.ac.in)._"

    return answer
