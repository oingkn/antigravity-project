"""
Lab 01 — Self-Consistency with Ollama
======================================
Demonstrates how sampling the same question multiple times and taking
the majority vote (self-consistency) can improve accuracy over a single shot.

Usage:
    python labs/01_self_consistency_ollama.py --model qwen2.5:3b-instruct --num-samples 5
"""

import argparse
import re
from collections import Counter

import requests

# ---------------------------------------------------------------------------
# Ollama helper
# ---------------------------------------------------------------------------

OLLAMA_URL = "http://localhost:11434/api/generate"


def ollama_generate(
    model: str,
    prompt: str,
    temperature: float = 0.7,
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
    return response.json()["response"]


# ---------------------------------------------------------------------------
# Answer extraction
# ---------------------------------------------------------------------------

def extract_final_number(text: str):
    """Parse 'Final: <integer>' from model output."""
    match = re.search(r"Final:\s*(-?\d+)", text)
    return int(match.group(1)) if match else None


# ---------------------------------------------------------------------------
# Answering strategies
# ---------------------------------------------------------------------------

def ask_once(model: str, question: str, temperature: float):
    """Ask the model a single arithmetic question at a given temperature."""
    prompt = (
        "Solve the math problem step by step.\n"
        "End your answer with exactly one line: Final: <integer>\n\n"
        f"Question: {question}\n"
    )
    output = ollama_generate(model, prompt, temperature=temperature, num_predict=128)
    return output, extract_final_number(output)


def majority_vote(answers: list):
    """Return the most common non-None answer."""
    valid = [a for a in answers if a is not None]
    if not valid:
        return None
    return Counter(valid).most_common(1)[0][0]


# ---------------------------------------------------------------------------
# Dataset & gold answers
# ---------------------------------------------------------------------------

DATASET = [
    "What is 12 + 7 + 5?",
    "Compute 20 + 11 - 3.",
    "Find 9 + 9 + 9.",
    "Calculate 100 - 40 + 6.",
    "What is 3 + 14 + 15?",
]


def gold_answer(question: str) -> int:
    """Evaluate the arithmetic expression embedded in the question string."""
    # Match a multi-term arithmetic expression (e.g. '12 + 7 + 5' or '100 - 40 + 6')
    match = re.search(r"-?\d+(?:\s*[\+\-\*\/]\s*-?\d+)+", question)
    if not match:
        return 0
    # Allow only digits, operators, and spaces before eval
    expr = re.sub(r"[^\d\+\-\*\/\s]", "", match.group()).strip()
    try:
        return int(eval(expr))  # noqa: S307 — expression sanitized above
    except Exception:
        return 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Self-consistency lab with local Ollama"
    )
    parser.add_argument(
        "--model", default="qwen2.5:3b-instruct", help="Ollama model name"
    )
    parser.add_argument(
        "--num-samples", type=int, default=5, help="Number of samples for majority vote"
    )
    args = parser.parse_args()

    # Vary temperatures across samples so we get diverse reasoning paths
    temperatures = [0.2, 0.4, 0.6, 0.8, 1.0]

    single_correct = 0
    sc_correct = 0

    for question in DATASET:
        gold = gold_answer(question)

        # --- Single-shot answer (temperature 0.7) ---
        _, single_pred = ask_once(args.model, question, temperature=0.7)
        single_correct += int(single_pred == gold)

        # --- Multi-sample majority vote ---
        samples = []
        for i in range(args.num_samples):
            temp = temperatures[i % len(temperatures)]
            _, pred = ask_once(args.model, question, temperature=temp)
            samples.append(pred)
        sc_pred = majority_vote(samples)
        sc_correct += int(sc_pred == gold)

        print(f"\nQ: {question}")
        print(f"Gold={gold} | Single={single_pred} | SC(majority)={sc_pred}")
        print(f"All samples: {samples}")

    n = len(DATASET)
    print("\n=== Summary ===")
    print(f"Single-shot accuracy : {single_correct}/{n} ({100*single_correct/n:.0f}%)")
    print(f"Self-consistency acc : {sc_correct}/{n} ({100*sc_correct/n:.0f}%)")


if __name__ == "__main__":
    main()
