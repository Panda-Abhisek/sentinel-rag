from textwrap import dedent

from app.evaluation.models import AnswerEvaluation, HallucinationEvaluation
from app.evaluation.json_contract import build_json_contract

class EvaluationPromptBuilder:
    """
    Builds prompts for LLM-based evaluation tasks.
    """
    
    @staticmethod
    def build_hallucination_prompt(
        contexts: list[str],
        answer: str,
    ) -> str:
        """
        Build prompt for hallucination detection.
        """

        context = "\n\n".join(contexts)

        contract = build_json_contract(HallucinationEvaluation)

        return dedent(
            f"""
            You are detecting hallucinations in a Retrieval-Augmented Generation (RAG) answer.

            Identify every factual claim made in the generated answer.

            Verify each claim against the retrieved context.

            A claim is hallucinated if it cannot be fully supported by the retrieved context.

            Compute the hallucination score based on the proportion and severity of unsupported claims.

            Retrieved Context:
            {context}

            Generated Answer:
            {answer}

            {contract}
            First, internally evaluate the answer against the retrieved context.

            Then return ONLY the final JSON object.

            Do not reveal your reasoning.
            """
        ).strip()

    @staticmethod
    def build_answer_evaluation_prompt(
        question: str,
        contexts: list[str],
        answer: str,
    ) -> str:
        """
        Build the evaluation prompt for answer quality assessment.
        """

        context = "\n\n".join(contexts)

        contract = build_json_contract(AnswerEvaluation)

        return dedent(
            f"""
            You are an expert evaluator for a Retrieval-Augmented Generation (RAG) system.

            Your task is to objectively evaluate the generated answer using ONLY the retrieved context.

            Evaluation Criteria

            1. Faithfulness
            Score how well every factual statement in the answer is supported by the retrieved context.

            2. Answer Relevancy
            Score how directly and completely the answer addresses the user's question.

            3. Context Utilization
            Score how effectively the retrieved context is used to construct the answer.

            4. Completeness
            Score whether the answer covers all important aspects that can be answered from the retrieved context.

            Scoring Rules

            - Every score must be between 0.0 and 1.0.
            - Evaluate every metric independently.
            - Different metrics should receive different scores whenever appropriate.
            - Do NOT automatically assign 0.0 or 1.0.
            - Reserve 1.0 only for nearly perfect performance.
            - Reserve 0.0 only for complete failure.
            - If uncertain, assign an intermediate value.

            Question:
            {question}

            Retrieved Context:
            {context}

            Generated Answer:
            {answer}

            {contract}

            Think carefully before scoring.

            Return ONLY the JSON object.

            Do not include explanations, markdown, code fences, or additional text.
            """
        ).strip()