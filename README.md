# LLM POCs (Proof of Concepts)

This repository contains various proof of concepts and experiments with Large Language Models (LLMs) and related technologies. The project is organized into different modules, each focusing on specific aspects of LLM applications.

## Project Structure

```
.
├── src/
│   ├── huggingface/         # Hugging Face model experiments
│   ├── groq/                # Groq API integration
│   ├── agents/              # LLM agent implementations
│   ├── rag/                 # Retrieval Augmented Generation examples
│   ├── llm_apis/           # Various LLM API integrations
│   ├── langchain_llm_app/   # LangChain-based applications
│   └── weviate_study/       # Weaviate vector database experiments
├── data/                    # Data files and resources
├── requirements.txt         # Python dependencies
└── .env                     # Environment variables
```

## Components

### Hugging Face Experiments
- `huggingface_bot.ipynb`: Jupyter notebook demonstrating Hugging Face model integration

### Groq Integration
- `app.py`: Application demonstrating Groq API usage

### LLM Agents
- `agents.ipynb`: Jupyter notebook showcasing LLM agent implementations

### RAG (Retrieval Augmented Generation)
- `rag_basics.ipynb`: Basic RAG implementation
- `retriver.ipynb`: Advanced retrieval techniques

### LLM APIs
- `client.py`: Generic LLM API client
- `app.py`: Example application using various LLM APIs

### LangChain Applications
- `app.py`: LangChain-based application
- `basic_open_ai.py`: Basic OpenAI integration with LangChain

### Weaviate Studies
- `poc_weviate.py`: Proof of concept for Weaviate vector database integration

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
- Copy `.env.example` to `.env`
- Fill in the required API keys and configuration values

## Usage

Each component can be run independently. Navigate to the specific directory and run the corresponding Python file or Jupyter notebook.

For example:
```bash
# Run Groq application
cd src/groq
python app.py

# Run Weaviate POC
cd src/weviate_study
python poc_weviate.py
```

## Requirements

See `requirements.txt` for the complete list of dependencies. Key dependencies include:
- Python 3.8+
- Various LLM-related packages
- Jupyter for notebook-based experiments

## Notes

- This is a collection of proof of concepts and experiments
- Each component is designed to be self-contained
- Some components may require specific API keys or credentials
- Check individual component directories for specific setup instructions

## License

[Add your license information here] 