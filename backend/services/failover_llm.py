import os
import time
import asyncio
from groq import AsyncGroq
from google import genai
from cerebras.cloud.sdk import AsyncCerebras

# Model configuration — update these if models change
GROQ_MODEL = "qwen/qwen3-32b"
CEREBRAS_MODEL = "gpt-oss-120b"
GEMINI_MODEL = "gemini-2.5-flash"


def _api_key(name: str) -> str | None:
    """Read the configured key, accepting the project's numbered fallback keys."""
    for candidate in (name, f"{name}_2"):
        value = os.getenv(candidate, "").strip()
        # Do not treat JavaScript expressions copied into .env as credentials.
        if value and not value.startswith("process.env."):
            return value
    return None


async def call_llm(prompt: str):
    """Call LLM with 3-tier failover: Groq → Cerebras → Gemini.
    
    The prompt contains both system instructions and user context.
    We split it at '--- CONTEXT DATA ---' to separate system from user content,
    giving the LLM proper message structure.
    """
    start_time = time.time()

    # Split prompt into system and user parts for better LLM comprehension
    if "--- CONTEXT DATA ---" in prompt:
        parts = prompt.split("--- CONTEXT DATA ---", 1)
        system_msg = parts[0].strip()
        user_msg = "--- CONTEXT DATA ---" + parts[1]
    else:
        system_msg = "You are NirmaAI, a helpful FAQ assistant for Nirma University, Ahmedabad."
        user_msg = prompt

    # ── Tier 1: Groq (Qwen 3) ──────────────────────────────
    groq_key = _api_key("GROQ_API_KEY")
    if groq_key:
        try:
            groq_client = AsyncGroq(api_key=groq_key)
            response = await asyncio.wait_for(
                groq_client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": user_msg}
                    ],
                    model=GROQ_MODEL,
                    temperature=0.3,
                    max_tokens=1024,
                ),
                timeout=15.0
            )
            answer = response.choices[0].message.content
            # Qwen 3 thinking mode: strip <think>...</think> tags if present
            if answer and "<think>" in answer:
                import re
                answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL).strip()
            return {
                "answer": answer,
                "tier_used": f"Groq ({GROQ_MODEL})",
                "response_time_ms": (time.time() - start_time) * 1000
            }
        except Exception as e:
            print(f"⚠️  Groq failed: {e}")

    # ── Tier 2: Cerebras (GPT-OSS 120B) ────────────────────
    cerebras_key = _api_key("CEREBRAS_API_KEY")
    if cerebras_key:
        try:
            cerebras_client = AsyncCerebras(api_key=cerebras_key)
            response = await asyncio.wait_for(
                cerebras_client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": user_msg}
                    ],
                    model=CEREBRAS_MODEL,
                    temperature=0.3,
                    max_tokens=1024,
                ),
                timeout=15.0
            )
            return {
                "answer": response.choices[0].message.content,
                "tier_used": f"Cerebras ({CEREBRAS_MODEL})",
                "response_time_ms": (time.time() - start_time) * 1000
            }
        except Exception as e:
            print(f"⚠️  Cerebras failed: {e}")

    # ── Tier 3: Gemini (2.5 Flash) ──────────────────────────
    gemini_key = _api_key("GEMINI_API_KEY")
    if gemini_key:
        try:
            client = genai.Client(api_key=gemini_key)
            response = await asyncio.wait_for(
                asyncio.to_thread(
                    client.models.generate_content,
                    model=GEMINI_MODEL,
                    contents=user_msg,
                    config=genai.types.GenerateContentConfig(
                        system_instruction=system_msg,
                        temperature=0.3,
                        max_output_tokens=1024,
                    )
                ),
                timeout=15.0
            )
            return {
                "answer": response.text,
                "tier_used": f"Gemini ({GEMINI_MODEL})",
                "response_time_ms": (time.time() - start_time) * 1000
            }
        except Exception as e:
            print(f"⚠️  Gemini failed: {e}")

    # ── All tiers failed ────────────────────────────────────
    return {
        "answer": "I'm sorry, all my language model providers are currently unavailable. Please try again in a moment.",
        "tier_used": "None",
        "response_time_ms": (time.time() - start_time) * 1000
    }


async def stream_llm(prompt: str):
    """Stream LLM response for WebSocket. Tries Groq first, falls back to non-streaming."""
    
    if "--- CONTEXT DATA ---" in prompt:
        parts = prompt.split("--- CONTEXT DATA ---", 1)
        system_msg = parts[0].strip()
        user_msg = "--- CONTEXT DATA ---" + parts[1]
    else:
        system_msg = "You are NirmaAI, a helpful FAQ assistant for Nirma University, Ahmedabad."
        user_msg = prompt

    # Try streaming with Groq first
    groq_key = _api_key("GROQ_API_KEY")
    if groq_key:
        try:
            groq_client = AsyncGroq(api_key=groq_key)
            stream = await groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg}
                ],
                model=GROQ_MODEL,
                temperature=0.3,
                max_tokens=1024,
                stream=True
            )
            in_think = False
            async for chunk in stream:
                content = chunk.choices[0].delta.content
                if content is not None:
                    # Skip <think> blocks from Qwen 3
                    if "<think>" in content:
                        in_think = True
                        continue
                    if "</think>" in content:
                        in_think = False
                        continue
                    if not in_think:
                        yield content
            return
        except Exception as e:
            print(f"⚠️  Groq stream failed: {e}")

    # Fallback: non-streaming response
    result = await call_llm(prompt)
    yield result["answer"]
