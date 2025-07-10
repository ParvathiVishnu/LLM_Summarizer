# LLM_Summarizer

```mermaid
flowchart TD
    A[User uploads document\n(.txt / .pdf / .docx)] --> B[Extract text using utils.py]
    B --> C[Split text into chunks\n(~1500 characters)]
    C --> D[Summarize each chunk\nvia llama3.2-summary model]
    D --> E[Clean summaries:\n- Remove markdown\n- Normalize bullets]
    E --> F[Join all chunk summaries]
    F --> G[Display in Streamlit\n+ Download option]
    F --> H[Save summary to\n test_results_llama3.2-summary/]
    H --> I[Compare with original document\nusing compare_results.py]
```
