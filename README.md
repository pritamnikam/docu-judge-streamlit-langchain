# DocuJudge: AI-Powered Document Evaluation Tool

A Streamlit-based web application that uses OpenAI's GPT-4 model to evaluate documents against a golden standard. The application provides a verdict, confidence score, and detailed explanation for each document's alignment with the golden standard.

## Features

- **Intuitive Interface**: Simple drag-and-drop interface for uploading documents
- **AI-Powered Analysis**: Utilizes GPT-4 for comprehensive document evaluation
- **Detailed Reports**: Get verdicts with confidence scores and explanations
- **Batch Processing**: Evaluate multiple documents at once
- **Export Results**: Download evaluation results as CSV
- **Example Included**: Comes with sample documents to get started quickly

## Prerequisites

- Python 3.8 or higher
- OpenAI API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/docujudge.git
   cd docujudge
   ```

2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your OpenAI API key:
   ```bash
   # Copy the example environment file
   copy .env.example .env  # Windows
   # or
   cp .env.example .env    # macOS/Linux
   ```
   Then edit `.env` and add your OpenAI API key.

## Usage

1. Start the application:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to `http://localhost:8501`

3. In the application:
   - Upload your golden standard document (Markdown format)
   - Upload one or more documents to evaluate
   - Click "Evaluate Documents" to start the analysis
   - View and download the results

## Example Documents

### Golden Standard Example (`examples/golden_standard.md`)
```markdown
# Project Requirements

## Core Features
- User authentication
- Document upload
- Real-time processing

## Security Requirements
- Password hashing
- Input validation
- Rate limiting

## Performance
- Page load time < 2s
- Support for 1000+ concurrent users
```

### Document to Evaluate (`examples/document1.md`)
```markdown
# Project Specs

## Main Features
- User login system
- File upload functionality
- Live updates

## Security
- Passwords are hashed
- Input is validated
- DDoS protection

## Performance Targets
- Fast page loads
- Handles many users
```

## How It Works

1. The application uses LangChain to interact with OpenAI's GPT-4 model
2. Each document is evaluated against the golden standard using a predefined prompt
3. The LLM provides a verdict (Pass/Fail), confidence score, and explanation
4. Results are displayed in an interactive table and can be exported to CSV

## Customization

You can modify the evaluation criteria by editing the `evaluate_document` function in `app.py`. The current prompt can be adjusted to better suit your specific evaluation needs.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [OpenAI](https://openai.com/)
- Uses [LangChain](https://python.langchain.com/) for LLM integration
