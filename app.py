import streamlit as st

from src.rag_pipeline import RAGPipeline


# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="Product RAG Assistant",
    page_icon="🤖",
    layout="wide"
)


# ==========================================
# Application Header
# ==========================================

st.title("🤖 Product RAG Assistant")

st.write(
    "Ask questions about the product catalog "
    "using semantic search and "
    "retrieval-augmented generation."
)


# ==========================================
# Load RAG Pipeline
# ==========================================

@st.cache_resource
def load_pipeline():

    return RAGPipeline()


pipeline = load_pipeline()


# ==========================================
# Example Questions
# ==========================================

st.subheader("Example Questions")

example_questions = [
    "Which product is the cheapest laptop?",
    "Which is the most expensive laptop?",
    "Show me smartphones",
    "Which laptop is good for programming?",
    "Which headphones are available?"
]


selected_example = st.selectbox(
    "Choose an example:",
    [""] + example_questions
)


# ==========================================
# User Query
# ==========================================

query = st.text_input(
    "Ask a question",
    value=selected_example,
    placeholder="Example: Which product is the cheapest laptop?"
)


# ==========================================
# Search Button
# ==========================================

if st.button(
    "🔍 Search",
    use_container_width=True
):

    if not query.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "Searching product knowledge..."
        ):

            result = pipeline.run(
                query
            )


        # ======================================
        # Final Answer
        # ======================================

        st.subheader("Answer")

        st.success(
            result["answer"]
        )


        # ======================================
        # Query Analysis
        # ======================================

        with st.expander(
            "🔎 Query Analysis"
        ):

            st.write(
                "**Intent:**",
                result["intent"]
            )

            st.write(
                "**Filters:**",
                result["filters"]
            )


        # ======================================
        # Retrieved Products
        # ======================================

        with st.expander(
            "📚 Retrieved Products"
        ):

            if result["results"]:

                for rank, item in enumerate(
                    result["results"],
                    start=1
                ):

                    st.markdown(
                        f"### Result {rank}"
                    )

                    st.code(
                        item["document"]
                    )

                    if item["score"] is not None:

                        st.write(
                            f"Similarity Score: "
                            f"{item['score']:.4f}"
                        )

                    st.divider()

            else:

                st.write(
                    "No relevant products found."
                )


# ==========================================
# Footer
# ==========================================

st.divider()

st.caption(
    "Product RAG Assistant | "
    "Sentence Transformers + FAISS + "
    "Hugging Face Transformers"
)