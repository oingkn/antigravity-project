"""
Lab 03 — Pseudo-MoE Router with Ollama
========================================
Implements a simple rule-based router that directs each query to the most
appropriate "expert" prompt, then calls the local Ollama model.

Routes:
  - math    : arithmetic / calculation questions
  - code    : programming / debugging questions
  - summary : everything else → summarise / explain

Usage:
    python labs/03_router_moe_ollama.py --model qwen2.5:3b-instruct
"""

import argparse

import requests

# ---------------------------------------------------------------------------
# Ollama helper
# ---------------------------------------------------------------------------

OLLAMA_URL = "http://localhost:11434/api/generate"


def ollama_generate(
    model: str,
    prompt: str,
    temperature: float = 0.2,
    num_predict: int = 128,
) -> str:
    """Call the local Ollama /api/generate endpoint and return the response text."""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": num_predict,
        },
    }
    response = requests.post(OLLAMA_URL, json=payload, timeout=120)
    response.raise_for_status()
    return response.json()["response"].strip()


# ---------------------------------------------------------------------------
# Router: rule-based keyword matching
# ---------------------------------------------------------------------------

_MATH_KEYWORDS = {"calculate", "compute", "sum", "subtract", "multiply", "+", "-", "*", "/", "how many", "what is"}
_CODE_KEYWORDS = {"python", "bug", "function", "class", "code", "error", "debug", "syntax"}


def route(query: str) -> str:
    """Return one of: 'math', 'code', 'summary'."""
    ql = query.lower()
    if any(kw in ql for kw in _MATH_KEYWORDS):
        return "math"
    if any(kw in ql for kw in _CODE_KEYWORDS):
        return "code"
    return "summary"


# ---------------------------------------------------------------------------
# Expert prompt builders
# ---------------------------------------------------------------------------

def build_prompt(route_name: str, query: str) -> str:
    """Return a specialised system+user prompt for the given route."""
    if route_name == "math":
        return (
            "You are a precise math tutor.\n"
            "Solve the following problem step by step.\n"
            "End your answer with: Final: <answer>\n\n"
            f"Problem: {query}\n"
        )
    if route_name == "code":
        return (
            "You are an expert programming tutor.\n"
            "Identify the issue, explain the cause, and show a minimal fix.\n\n"
            f"Question: {query}\n"
        )
    # summary / general
    return (
        "You are a clear and concise teaching assistant.\n"
        "Summarise the following in 3 bullet points (Korean is fine).\n\n"
        f"Text or question: {query}\n"
    )


# ---------------------------------------------------------------------------
# Sample queries
# ---------------------------------------------------------------------------

SAMPLE_QUERIES = [
    "Calculate 15 + 27 - 4.",
    "My python function throws a NoneType error. How do I debug it?",
    "트랜스포머의 어텐션 메커니즘을 초보자용으로 설명해줘.",
]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Pseudo-MoE router lab with local Ollama"
    )
    parser.add_argument(
        "--model", default="qwen2.5:3b-instruct", help="Ollama model name"
    )
    args = parser.parse_args()

    for query in SAMPLE_QUERIES:
        route_name = route(query)
        prompt = build_prompt(route_name, query)
        answer = ollama_generate(args.model, prompt, temperature=0.2, num_predict=128)

        print(f"\n{'='*60}")
        print(f"Query : {query}")
        print(f"Route : {route_name}")
        print(f"Answer: {answer}")

    print(f"\n{'='*60}")


if __name__ == "__main__":
    main()
