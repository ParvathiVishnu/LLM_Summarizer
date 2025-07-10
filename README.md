# LLM_Summarizer

```mermaid
flowchart TD
    A[User uploads document<br>(.txt / .pdf / .docx)] --> B[Extract text using utils.py]
    B --> C[Split large text into chunks<br>(~1500 characters)]
    C --> D[Call LLM (llama3.2-summary)<br>Generate summaries for each chunk]
    D --> E[Clean summary text:<br>- Normalize bullets<br>- Remove markdown<br>- Trim noise]
    E --> F[Combine all cleaned summaries]
    F --> G[Display final summary in Streamlit<br>+ Provide download option]
    F --> H[Save summary in folder:<br>test_results_llama3.2-summary/]
    H --> I[Compare summaries with original<br>via compare_results.py UI]
```
