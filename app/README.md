# Python LLM Learning

This project demonstrates setting up a local LLM model using [Ollama](https://ollama.com/) and managing dependencies with [UV](https://github.com/astral-sh/uv).

## Prerequisites

- Python (recommended: 3.10+)
- [UV package manager](https://github.com/astral-sh/uv)
- [Ollama](https://ollama.com/download) installed and running

## Setup

1. **Install dependencies using UV:**

    ```sh
    uv venv
    .venv\Scripts\activate
    ```

2. **Set up an LLM model with Ollama:**

    - Pull a model (e.g., llama2):

      ```sh
      ollama pull llama3.2
      ```

    - Run the model:

      ```sh
      ollama run llama3.2:latest
      ```

3. **Connect your Python code to Ollama's API as needed.**

## References

- [Ollama Documentation](https://github.com/jmorganca/ollama)
- [UV Documentation](https://github.com/astral-sh/uv)