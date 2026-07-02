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
            You are evaluating a Retrieval-Augmented Generation (RAG) response.

            Evaluate the generated answer using ONLY the retrieved context.

            Evaluation Guidelines

            - Faithfulness:
            Measure whether every factual claim is supported by the retrieved context.

            - Answer Relevancy:
            Measure how directly the answer addresses the user's question.

            - Context Utilization:
            Measure how effectively the retrieved context is used.

            - Completeness:
            Measure whether the answer covers all important aspects of the question.

            Each metric should be evaluated independently.
            Do not assign identical scores unless they genuinely deserve the same value.

            Question:
            {question}

            Retrieved Context:
            {context}

            Generated Answer:
            {answer}

            {contract}
            Evaluate the answer carefully before producing the output. 
            First, internally evaluate the answer against the retrieved context.

            Then return ONLY the final JSON object.

            Reason privately about the evaluation.

            Return ONLY the final JSON object.

            Do not reveal your reasoning.
            """
        ).strip()