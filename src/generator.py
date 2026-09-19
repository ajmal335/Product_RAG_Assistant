import torch

from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM
)


class RAGGenerator:

    def __init__(
        self,
        model_name="google/flan-t5-small"
    ):

        print("Loading LLM...")

        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name
        )

        # Load model
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name
        )

        # Select device
        self.device = (
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        # Move model to device
        self.model.to(
            self.device
        )

        # Evaluation mode
        self.model.eval()

        print(
            f"LLM loaded on {self.device}"
        )


    def generate(
        self,
        query,
        context
    ):

        # ==========================================
        # Build RAG prompt
        # ==========================================

        prompt = f"""
Answer the question using only the information
provided in the context.

Do not use outside knowledge.

Context:
{context}

Question:
{query}

Answer:
""".strip()


        # ==========================================
        # Tokenize prompt
        # ==========================================

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )


        # Move inputs to device
        inputs = {
            key: value.to(self.device)
            for key, value in inputs.items()
        }


        # ==========================================
        # Generate answer
        # ==========================================

        with torch.no_grad():

            outputs = self.model.generate(
                **inputs,
                max_new_tokens=100,
                do_sample=False
            )


        # ==========================================
        # Decode answer
        # ==========================================

        answer = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )


        return answer.strip()