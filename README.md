# DocuJudge - AI-Powered Document Evaluation

DocuJudge is a Streamlit-based web application that uses large language models (LLMs) to evaluate documents against a golden standard. It provides a user-friendly interface for comparing multiple documents and generating detailed evaluation reports.

## Features

- **Multiple LLM Provider Support**: Choose between OpenAI and Groq LLM providers
- **Multiple Model Selection**: Various models available based on the selected provider
- **Batch Processing**: Evaluate multiple documents at once
- **Detailed Reports**: Get verdicts, confidence scores, and explanations for each document
- **Export Results**: Download evaluation results as CSV
- **Docker Support**: Easy deployment with Docker and Docker Compose
- **CI/CD Ready**: GitHub Actions workflows for testing and deployment
- **Type Checking**: Full type hints and mypy support
- **Code Quality**: Pre-configured with Black, Pylint, and other quality tools

## Quick Start

### Prerequisites

- Python 3.8+
- [Poetry](https://python-poetry.org/) (recommended) or pip
- API keys for your chosen LLM provider (OpenAI or Groq)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/docu-judge.git
   cd docu-judge
   ```

2. Install dependencies:
   ```bash
   # Using Poetry (recommended)
   poetry install
   
   # Or using pip
   pip install -r requirements.txt
   ```

3. Create a `.env` file:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and add your API keys.

### Running Locally

```bash
# Using Poetry
poetry run streamlit run app.py

# Or using pip
streamlit run app.py
```

### Using Docker

```bash
# Build the Docker image
docker build -t docu-judge .

# Run the container
docker run -p 8501:8501 --env-file .env docu-judge

# Or use Docker Compose
docker-compose up --build
```

## Development

### Setting Up Development Environment

1. Install development dependencies:
   ```bash
   poetry install --with dev
   # or
   pip install -r requirements-dev.txt
   ```

2. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=./ --cov-report=html

# Run specific test file
pytest tests/test_llm_service.py -v
```

### Code Quality

```bash
# Format code with Black
black .

# Run linter
pylint app.py config.py llm_service.py tests/

# Run type checking
mypy .
```

## LLM Configuration

DocuJudge supports multiple LLM providers. Configure your preferred provider in the `.env` file:

```ini
# For OpenAI
OPENAI_API_KEY=your_openai_api_key

# For Groq
GROQ_API_KEY=your_groq_api_key

# LLM Configuration
LLM_PROVIDER=openai  # or 'groq'
LLM_MODEL=gpt-4  # or other supported models
LLM_TEMPERATURE=0.3
MAX_TOKENS=1000
```

## Example Usage

1. **Upload Documents**:
   - Upload a Golden Standard document (your reference)
   - Upload one or more documents to evaluate

2. **Configure Settings** (optional):
   - Select LLM provider and model
   - Adjust temperature and max tokens as needed

3. **Evaluate**:
   - Click "Evaluate Documents" to start the analysis
   - View results in the table
   - Download results as CSV if needed

## Deployment

### Streamlit Cloud

1. Fork this repository
2. Go to [Streamlit Cloud](https://share.streamlit.io/)
3. Click "New app" and connect your repository
4. Set the following secrets in Streamlit Cloud:
   - `OPENAI_API_KEY`
   - `GROQ_API_KEY` (if using Groq)

### Other Cloud Providers

DocuJudge can be deployed to any cloud provider that supports Python applications or containers, such as:
- AWS Elastic Beanstalk
- Google Cloud Run
- Azure App Service
- Heroku
- Railway.app

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [LangChain](https://python.langchain.com/)
- LLM Providers: [OpenAI](https://openai.com/) and [Groq](https://groq.com/)
- Icons by [Feather Icons](https://feathericons.com/)
