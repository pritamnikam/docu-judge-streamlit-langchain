import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv
from typing import List, Dict, Any
import pandas as pd

# Load environment variables
load_dotenv()

# Initialize OpenAI client
llm = ChatOpenAI(
    model_name="gpt-4",
    temperature=0.3,
    api_key=os.getenv("OPENAI_API_KEY")
)

def evaluate_document(golden_standard: str, document: str, filename: str) -> Dict[str, Any]:
    """
    Evaluate a document against the golden standard using LLM
    """
    system_prompt = """You are a judge and your task is to evaluate documents based on the provided golden standard.
    Analyze the content thoroughly and provide a verdict with confidence score.
    """
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"""
        GOLDEN STANDARD:
        {golden_standard}
        
        DOCUMENT TO EVALUATE:
        {document}
        
        Please provide:
        1. A verdict (Pass/Fail) based on the document's alignment with the golden standard
        2. A confidence score between 0 and 1 (1 being most confident)
        3. A brief explanation for your verdict
        
        Format your response as:
        VERDICT: [Pass/Fail]
        CONFIDENCE: [0-1]
        EXPLANATION: [Your explanation]
        """)
    ]
    
    response = llm.invoke(messages)
    result = {"Document": filename, "Verdict": "", "Confidence": 0, "Explanation": ""}
    
    # Parse the response
    for line in response.content.split('\n'):
        if line.startswith("VERDICT:"):
            result["Verdict"] = line.split(":")[1].strip()
        elif line.startswith("CONFIDENCE:"):
            try:
                result["Confidence"] = float(line.split(":")[1].strip())
            except (ValueError, IndexError):
                result["Confidence"] = 0.0
        elif line.startswith("EXPLANATION:"):
            result["Explanation"] = line.split(":", 1)[1].strip()
    
    return result

def main():
    st.set_page_config(page_title="Document Evaluator", layout="wide")
    st.title("📝 LLM Document Evaluator")
    
    # File upload section
    st.header("Upload Documents")
    
    # Golden standard upload
    st.subheader("1. Upload Golden Standard (Markdown)")
    golden_standard_file = st.file_uploader(
        "Upload Golden Standard", 
        type=["md", "markdown"],
        key="golden_standard"
    )
    
    # Documents to evaluate upload
    st.subheader("2. Upload Documents to Evaluate (Markdown)")
    eval_docs = st.file_uploader(
        "Upload Documents to Evaluate", 
        type=["md", "markdown"],
        accept_multiple_files=True,
        key="eval_docs"
    )
    
    # Evaluation button
    if st.button("Evaluate Documents") and golden_standard_file and eval_docs:
        with st.spinner("Evaluating documents..."):
            # Read golden standard
            golden_standard = golden_standard_file.read().decode()
            
            # Process each document
            results = []
            for doc in eval_docs:
                document_content = doc.read().decode()
                result = evaluate_document(golden_standard, document_content, doc.name)
                results.append(result)
            
            # Display results
            if results:
                st.success("Evaluation complete!")
                df = pd.DataFrame(results)
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
                
                # Add download button for results
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "Download Results",
                    data=csv,
                    file_name="document_evaluation_results.csv",
                    mime="text/csv"
                )
    
    # Add some instructions
    with st.expander("ℹ️ How to use"):
        st.markdown("""
        1. Upload a Golden Standard document (Markdown format)
        2. Upload one or more documents to evaluate (Markdown format)
        3. Click 'Evaluate Documents' to get the evaluation results
        
        The evaluation will check each document against the Golden Standard and provide:
        - A verdict (Pass/Fail)
        - A confidence score (0-1)
        - An explanation for the verdict
        """)

if __name__ == "__main__":
    main()
