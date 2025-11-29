import google.generativeai as genai
import os
from dotenv import load_dotenv
from report_generator import generate_competition_report
import mimetypes

# Load Gemini API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# -----------------------------------------------------
# GENERAL LLM CALL
# -----------------------------------------------------
def call_llm(prompt, model="gemini-2.5-flash"):
    try:
        response = genai.GenerativeModel(model).generate_content(prompt)
        return response.text
    except Exception as e:
        return f"LLM Error: {str(e)}"

# -----------------------------------------------------
# UNIVERSAL REPORT GENERATOR
# -----------------------------------------------------
def generate_report(file_type, analysis, metadata):
    prompt = f"""
    You are an AI analysis agent. Based on the following data,
    generate a clear, simple, human-friendly report.

    File Type: {file_type}
    Analysis Output: {analysis}
    Metadata: {metadata}

    Requirements:
    - Keep the report simple
    - Explain what the analysis means
    - Mention if the content is suspicious, harmful, fake, or normal
    - Add small recommendations
    """
    return call_llm(prompt)

# -----------------------------------------------------
# DETECT FILE TYPE
# -----------------------------------------------------
def detect_file_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type:
        if mime_type.startswith("video"):
            return "video"
        elif mime_type in ["application/pdf", "text/plain"]:
            return "text"  # PDFs will be converted to text in your report generator
    return "unknown"

# -----------------------------------------------------
# PROCESS MULTIPLE FILES
# -----------------------------------------------------
def process_files(file_list):
    reports = {}
    for file_path in file_list:
        file_type = detect_file_type(file_path)
        # Example: For real usage, you'll replace this with your analysis function
        if file_type == "video":
            analysis = {"deepfake_score": 68.2, "faces_detected": 1, "frames_analyzed": 120}
            metadata = {"file": file_path}
        elif file_type == "text":
            analysis = {"toxicity": 0.18, "sentiment": "slightly negative"}
            metadata = {"file": file_path, "words": 150}
        else:
            analysis = {}
            metadata = {"file": file_path}

        report = generate_report(file_type, analysis, metadata)
        reports[file_path] = report

    return reports

# -----------------------------------------------------
# LOCAL TESTING
# -----------------------------------------------------
if __name__ == "__main__":
    files_to_test = ["example.txt", "sample.pdf", "video.mp4"]
    all_reports = process_files(files_to_test)

    for f, r in all_reports.items():
        print(f"\nREPORT FOR {f}:\n")
        print(r)
        print("\n" + "-"*50 + "\n")
