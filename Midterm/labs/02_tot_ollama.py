"""
Lab 02 — Mini Tree-of-Thought (ToT) with Ollama
=================================================
Implements a lightweight beam-search style Tree-of-Thought:
  1. At each depth, propose candidate next-reasoning steps (model call).
  2. Score each candidate 0-10 (model call).
  3. Keep the top `beam_width` candidates and repeat.
  4. Produce a final answer from the best beam.

Usage:
    python labs/02_tot_ollama.py --model qwen2.5:3b-instruct --depth 2 --beam-width 2
"""

import argparse
from dataclasses import dataclass, field
from typing import List

import requests

# ---------------------------------------------------------------------------
# Ollama helper
# ---------------------------------------------------------------------------

OLLAMA_URL = "http://localhost:11434/api/generate"


def ollama_generate(
    model: str,
    prompt: str,
    temperature: float = 0.4,
    num_predict: int = 160,
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
# Beam state
# ---------------------------------------------------------------------------

@dataclass
class Beam:
    thought: str          # accumulated reasoning path so far
    score: float = 0.0    # cumulative score


# ---------------------------------------------------------------------------
# ToT operations
# ---------------------------------------------------------------------------

def propose_candidates(
    model: str, problem: str, partial_thought: str, k: int = 3
) -> List[str]:
    """Ask the model to propose k distinct next reasoning steps."""
    prompt = (
        "You are solving a problem using a tree-of-thought approach.\n"
        f"Problem: {problem}\n"
        f"Current reasoning so far: {partial_thought}\n\n"
        f"Propose {k} distinct next reasoning steps.\n"
        f"Return exactly {k} lines, each starting with '- '.\n"
    )
    output = ollama_generate(model, prompt, temperature=0.7, num_predict=200)
    # Parse lines starting with '- '
    lines = [
        line.strip()[2:].strip()
        for line in output.splitlines()
        if line.strip().startswith("- ")
    ]
    candidates = lines[:k]
    # Fallback: if parsing failed, treat whole output as one candidate
    if not candidates:
        candidates = [output[:120]]
    return candidates


def score_candidate(model: str, problem: str, candidate: str) -> float:
    """Ask the model to rate a reasoning step from 0 to 10."""
    prompt = (
        f"Problem: {problem}\n"
        f"Reasoning step: {candidate}\n\n"
        "Rate how useful this step is for solving the problem.\n"
        "Reply with a single number between 0 and 10. Nothing else.\n"
    )
    output = ollama_generate(model, prompt, temperature=0.0, num_predict=8)
    try:
        return float(output.strip().split()[0])
    except (ValueError, IndexError):
        return 0.0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Mini Tree-of-Thought lab with local Ollama"
    )
    parser.add_argument(
        "--model", default="qwen2.5:3b-instruct", help="Ollama model name"
    )
    parser.add_argument(
        "--depth", type=int, default=2, help="Number of ToT expansion steps"
    )
    parser.add_argument(
        "--beam-width", type=int, default=2, help="Beams to keep per depth level"
    )
    args = parser.parse_args()

    problem = (
        "A store had 120 apples. It sold 35, then received a shipment of 20, "
        "then sold 18 more. How many apples does it have now?"
    )

    print(f"Problem: {problem}\n")
    print(f"Config: depth={args.depth}, beam_width={args.beam_width}, model={args.model}\n")

    # Initialise beams with an empty starting thought
    beams: List[Beam] = [Beam(thought="Start reasoning about the problem.", score=0.0)]

    for depth in range(args.depth):
        expanded: List[Beam] = []

        for beam in beams:
            # Generate candidate next steps
            candidates = propose_candidates(
                args.model, problem, beam.thought, k=3
            )
            for candidate in candidates:
                step_score = score_candidate(args.model, problem, candidate)
                expanded.append(
                    Beam(
                        thought=beam.thought + "\n  -> " + candidate,
                        score=beam.score + step_score,
                    )
                )

        # Keep only the top beam_width beams
        expanded.sort(key=lambda b: b.score, reverse=True)
        beams = expanded[: args.beam_width]

        print(f"[Depth {depth + 1}] Top {args.beam_width} beam(s):")
        for i, b in enumerate(beams, 1):
            print(f"  {i}. cumulative_score={b.score:.2f}")
            for line in b.thought.splitlines():
                print(f"     {line}")

    if not beams:
        print("\nNo beams survived — try increasing --beam-width or --depth.")
        return

    # Produce final answer from the best beam
    best = beams[0]
    final_prompt = (
        f"Problem: {problem}\n\n"
        f"Reasoning path:\n{best.thought}\n\n"
        "Based on the reasoning above, state the final answer.\n"
        "End with exactly: Final: <number>\n"
    )
    final_output = ollama_generate(args.model, final_prompt, temperature=0.2, num_predict=64)

    print("\n=== Final Answer ===")
    print(final_output)


if __name__ == "__main__":
    main()
