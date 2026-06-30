# scripts/benchmark.py

import asyncio
import statistics
import time

import httpx

BASE_URL = "http://127.0.0.1:8000/query/"

BENCHMARK_QUERIES = [
    "What is FastAPI?",
    "How are path parameters used?",
    "What is a ResponseModel?",
    "How to handle errors?",
    "Explain dependency injection.",
    "What are Pydantic models?",
    "How does middleware work?",
    "How authentication is implemented?",
    "How to upload files?",
    "Explain background tasks.",
]


async def benchmark():
    retrieval_times = []
    generation_times = []
    evaluation_times = []
    total_times = []

    confidence_scores = []
    answer_scores = []

    async with httpx.AsyncClient(timeout=120) as client:
        for query in BENCHMARK_QUERIES:
            print(f"Running: {query}")

            start = time.perf_counter()

            response = await client.post(
                BASE_URL,
                json={
                    "question": query,
                    "top_k": 5,
                },
            )

            elapsed = (time.perf_counter() - start) * 1000

            response.raise_for_status()

            data = response.json()

            latency = data["latency"]

            retrieval_times.append(latency["retrieval_ms"])
            generation_times.append(latency["generation_ms"])
            evaluation_times.append(latency["evaluation_ms"])
            total_times.append(latency["total_ms"])

            evaluation = data.get("evaluation")

            if evaluation:
                confidence_scores.append(
                    evaluation["retrieval"]["confidence"]["score"]
                )

                answer_scores.append(
                    evaluation["answer"]["overall_score"]
                )

            print(f"Completed in {elapsed:.2f} ms")

    print()
    print("=" * 70)
    print("SentinelRAG Benchmark")
    print("=" * 70)

    print(f"Queries Tested       : {len(BENCHMARK_QUERIES)}")
    print()

    print(
        f"Average Retrieval    : {statistics.mean(retrieval_times):.2f} ms"
    )

    print(
        f"Average Generation   : {statistics.mean(generation_times):.2f} ms"
    )

    print(
        f"Average Evaluation   : {statistics.mean(evaluation_times):.2f} ms"
    )

    print(
        f"Average Total        : {statistics.mean(total_times):.2f} ms"
    )

    if confidence_scores:
        print()

        print(
            f"Average Confidence   : {statistics.mean(confidence_scores):.2f}"
        )

    if answer_scores:
        print(
            f"Average Answer Score : {statistics.mean(answer_scores):.2f}"
        )

    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(benchmark())