import subprocess

# Use your fine-tuned model by default
DEFAULT_MODEL = "llama3.2-summary"

def ask_ollama(prompt: str, model: str = DEFAULT_MODEL) -> str:
    """
    Sends a prompt to the local Ollama model and returns the response.
    Defaults to the custom summarization model.
    """
    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=180,
            check=True
        )
        output = result.stdout.decode("utf-8", errors="ignore")
        return extract_response(output)

    except subprocess.TimeoutExpired:
        return "❌ Timeout: The model took too long to respond."

    except subprocess.CalledProcessError as e:
        err = e.stderr.decode("utf-8", errors="ignore")
        return f"❌ Ollama CLI error: {err}"

    except Exception as e:
        return f"❌ Error: {str(e)}"

def extract_response(full_output: str) -> str:
    """
    Cleans up the raw Ollama CLI output by removing prompts and noise.
    """
    lines = full_output.strip().splitlines()
    response_lines = [line for line in lines if line.strip() and not line.strip().startswith(">>>")]
    return "\n".join(response_lines).strip()

