import os
import streamlit as st
import pandas as pd
from typing import List, Dict, Any
import asyncio
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()  # This loads the .env file

from config import config, LLMProvider
from llm_service import llm_service

# Set page config
st.set_page_config(
    page_title="DocuJudge - AI Document Evaluation",
    page_icon="📝",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main .block-container {
        max-width: 1200px;
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .success-msg {
        color: #28a745;
        font-weight: bold;
    }
    .error-msg {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def read_file(file) -> str:
    """Read file content with proper encoding handling."""
    try:
        return file.getvalue().decode("utf-8")
    except UnicodeDecodeError:
        try:
            return file.getvalue().decode("latin-1")
        except Exception as e:
            st.error(f"Error reading file {file.name}: {str(e)}")
            return ""

def update_llm_config(provider: str, model: str, temperature: float, max_tokens: int):
    """Update the LLM service with the latest configuration."""
    api_key = os.getenv("OPENAI_API_KEY") if provider == LLMProvider.OPENAI else os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error(f"API key not found. Please set the {'OPENAI_API_KEY' if provider == LLMProvider.OPENAI else 'GROQ_API_KEY'} in your .env file.")
        return False
    
    llm_service.update_config(
        provider=provider,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        api_key=api_key
    )
    return True

def main():
    st.title("📝 DocuJudge - AI Document Evaluation")
    st.markdown("Evaluate documents against a golden standard using AI")
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # LLM Provider Selection
        provider = st.selectbox(
            "LLM Provider",
            [p.value for p in LLMProvider],
            index=0
        )
        
        # Model selection based on provider
        if provider == LLMProvider.OPENAI:
            model = st.selectbox(
                "Model",
                ["gpt-4", "gpt-3.5-turbo"],
                index=0
            )
        else:  # GROQ
            model = st.selectbox(
                "Model",
                ["mixtral-8x7b-32768", "llama3-8b-8192"],
                index=0
            )
        
        # Advanced settings
        with st.expander("Advanced Settings"):
            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=float(config.temperature),
                step=0.1,
                help="Controls randomness in the model's responses. Lower values make the output more deterministic."
            )
            
            max_tokens = st.number_input(
                "Max Tokens",
                min_value=100,
                max_value=4000,
                value=config.max_tokens,
                step=100,
                help="Maximum number of tokens to generate in the response."
            )
            
            # Update LLM config when settings change
            if st.button("Update Settings"):
                # Update LLM service with initial config
                if not update_llm_config(provider, model, temperature, max_tokens):
                    st.error("Failed to initialize LLM service. Please check your API key configuration.")
                    st.stop()  # Stop execution if API key is not configured
                st.success("LLM settings updated successfully!")
    
    # Update config with user selections
    config.llm_provider = provider
    config.llm_model = model
    config.temperature = temperature
    config.max_tokens = max_tokens
    
    # Update LLM service with initial config
    if not update_llm_config(provider, model, temperature, max_tokens):
        st.error("Failed to initialize LLM service. Please check your API key configuration.")
        st.stop()  # Stop execution if API key is not configured
    
    # Main content
    st.header("📤 Upload Documents")
    
    # File upload section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Golden Standard")
        golden_standard_file = st.file_uploader(
            "Upload Golden Standard (Markdown)",
            type=["md", "markdown", "txt"],
            key="golden_standard"
        )
    
    with col2:
        st.subheader("Documents to Evaluate")
        eval_docs = st.file_uploader(
            "Upload Documents to Evaluate",
            type=["md", "markdown", "txt"],
            accept_multiple_files=True,
            key="eval_docs"
        )
    
    # Evaluation button
    if st.button("🚀 Evaluate Documents", type="primary"):
        if not golden_standard_file:
            st.error("Please upload a golden standard document")
            return
            
        if not eval_docs:
            st.error("Please upload at least one document to evaluate")
            return
        
        # Process evaluation
        with st.spinner("Evaluating documents..."):
            golden_standard = read_file(golden_standard_file)
            if not golden_standard:
                st.error("Failed to read golden standard file")
                return
            
            results = []
            progress_bar = st.progress(0)
            total_docs = len(eval_docs)
            
            for i, doc in enumerate(eval_docs):
                try:
                    doc_content = read_file(doc)
                    if not doc_content:
                        st.warning(f"Skipping empty or unreadable file: {doc.name}")
                        continue
                        
                    # Show progress
                    progress = (i + 1) / total_docs
                    progress_bar.progress(progress, text=f"Evaluating {i+1} of {total_docs}: {doc.name}")
                    
                    # Evaluate document
                    result = asyncio.run(
                        llm_service.evaluate_document(golden_standard, doc_content)
                    )
                    
                    if result["success"]:
                        results.append({
                            "Document": doc.name,
                            "Verdict": result["verdict"],
                            "Confidence": result["confidence"],
                            "Explanation": result["explanation"]
                        })
                    else:
                        st.error(f"Error evaluating {doc.name}: {result['error']}")
                        
                except Exception as e:
                    st.error(f"Error processing {doc.name}: {str(e)}")
            
            # Display results
            if results:
                st.success("✅ Evaluation complete!")
                
                # Create results dataframe
                df = pd.DataFrame(results)
                
                # Display results table
                st.subheader("📊 Results")
                st.dataframe(
                    df,
                    column_config={
                        "Document": "Document",
                        "Verdict": st.column_config.TextColumn("Verdict"),
                        "Confidence": st.column_config.ProgressColumn(
                            "Confidence",
                            min_value=0,
                            max_value=1,
                            format="%.2f"
                        ),
                        "Explanation": "Explanation"
                    },
                    hide_index=True,
                    use_container_width=True
                )
                
                # Add download button
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "💾 Download Results",
                    data=csv,
                    file_name="document_evaluation_results.csv",
                    mime="text/csv"
                )

    # Add usage instructions
    with st.expander("ℹ️ How to use"):
        st.markdown("""
        1. **Upload Documents**:
           - Golden Standard: Your reference document (Markdown format)
           - Documents to Evaluate: One or more documents to compare against the standard
        
        2. **Configure Settings** (optional):
           - Choose LLM provider (OpenAI or Groq)
           - Select model based on your provider
           - Adjust temperature and max tokens as needed
        
        3. **Evaluate**:
           - Click "Evaluate Documents" to start the analysis
           - View results in the table below
           - Download results as CSV if needed
        
        **Note**: The evaluation checks each document against the Golden Standard and provides:
        - A verdict (Pass/Fail)
        - A confidence score (0-1)
        - An explanation for the verdict
        """)

if __name__ == "__main__":
    main()
