# LLM_Summarizer

```mermaid
flowchart TD
    A[User uploads document:\n.txt / .pdf / .docx] --> B[Extract text using utils.py]
    B --> C[Split text into chunks\n(~1500 characters)]
    C --> D[Summarize each chunk\nvia llama3.2-summary model]
    D --> E[Clean summaries:\nremove markdown + normalize bullets]
    E --> F[Join all chunk summaries]
    F --> G[Display in Streamlit UI\n+ download option]
    F --> H[Save summary to folder:\n test_results_llama3.2-summary/]
    H --> I[Compare summary vs original\nusing compare_results.py]
```
