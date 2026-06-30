from textwrap import dedent

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

        return dedent(
            f"""
            You are detecting hallucinations in a Retrieval-Augmented Generation (RAG) answer.

            Compare the generated answer against the retrieved context.

            Return a hallucination_score between 0.0 and 1.0.

            0.0 = Every statement is fully supported by the retrieved context.

            1.0 = Most statements are unsupported or fabricated.

            Retrieved Context:
            {context}

            Generated Answer:
            {answer}

            Return only the structured response.
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

        return dedent(
            f"""
            You are evaluating a Retrieval-Augmented Generation (RAG) response.

            Evaluate the answer using ONLY the retrieved context.

            Score each metric between 0.0 and 1.0:

            - faithfulness
            - answer_relevancy
            - context_utilization
            - completeness

            Question:
            {question}

            Retrieved Context:
            {context}

            Generated Answer:
            {answer}

            Return only the structured response.
            """
        ).strip()