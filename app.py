import os
import json
from datetime import datetime
from flask import Flask, render_template, request
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# --- Initialization ---
app = Flask(__name__)

# --- Configuration ---
# Ensure you have set your GROQ_API_KEY in your environment variables
try:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
except Exception as e:
    print(f"Error initializing Groq client: {e}")
    print("Please make sure the GROQ_API_KEY environment variable is set correctly.")
    client = None

# CHANGED: The output file is now a .txt file
TXT_FILE = 'call_analysis.txt'

# --- Helper Functions ---
def save_to_txt(data):
    """Appends a dictionary of data to a structured text file."""
    # Get the current time for the log entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Define the structured format for the text file entry
    formatted_entry = f"""
==================================================
Log Entry: {timestamp}
==================================================

[Transcript]
{data['Transcript']}

--------------------------------------------------

[Summary]
{data['Summary']}

--------------------------------------------------

[Sentiment]
{data['Sentiment']}

==================================================\n\n
"""
    # Append the formatted entry to the file
    with open(TXT_FILE, 'a', encoding='utf-8') as txtfile:
        txtfile.write(formatted_entry)


def analyze_transcript(transcript):
    """
    Analyzes the transcript using the Groq API to get a summary and sentiment.
    This function contains the final, definitive prompt logic.
    """
    if not client:
        raise ConnectionError("Groq client is not initialized. Check API key.")

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a sophisticated AI assistant for analyzing customer call transcripts. Your goal is to determine the sentiment, considering both the initial problem and the final resolution."
                    "\n\n**CRITICAL SENTIMENT RULES:**"
                    "\n1. **Problem/Complaint = Negative:** If a customer calls about a company error (e.g., broken product, billing mistake), their sentiment starts as **Negative**. If the resolution is standard, the sentiment remains Negative."
                    "\n2. **The 'Exceptional Resolution' Exception:** However, if the agent provides a resolution that is far above and beyond a standard fix, causing the customer to express genuine delight or surprise (e.g., 'Wow, that's amazing!', 'You've really turned this around', 'That's perfect!'), you should classify the final sentiment as **Positive**."
                    "\n3. **Information/Question = Neutral:** If the customer's main purpose is to ask questions or get information (e.g., product details, order status), the sentiment is **Neutral**. Standard politeness ('thank you') does not make it positive."
                    "\n4. **Praise/Compliment = Positive:** If the customer's primary reason for calling is to give a compliment, the sentiment is **Positive**."
                    "\n\nProvide your output in a clean JSON format with 'summary' and 'sentiment' keys."
                )
            },
            {
                "role": "user",
                "content": f"Please analyze the following transcript:\n\n---START OF TRANSCRIPT---\n{transcript}\n---END OF TRANSCRIPT---",
            }
        ],
        model="llama-3.1-8b-instant",
        temperature=0.1,
        max_tokens=200,
        response_format={"type": "json_object"},
    )
    
    response_content = chat_completion.choices[0].message.content
    try:
        analysis_result = json.loads(response_content)
        analysis_result['sentiment'] = analysis_result.get('sentiment', 'Unknown').capitalize()
        return analysis_result
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error parsing Groq API response: {e}")
        return {
            "summary": "Failed to generate summary.",
            "sentiment": "Unknown"
        }

# --- Flask Routes ---
@app.route('/')
def index():
    """Renders the main page with the input form."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Handles the form submission, analyzes the transcript, and displays the result.
    """
    transcript = request.form.get('transcript', '').strip()

    if not transcript:
        return render_template('index.html', error="Please provide a transcript.")
    
    if not client:
        return render_template('index.html', error="Groq client is not configured. Please check your API key.")

    try:
        result = analyze_transcript(transcript)
        summary = result.get('summary', 'Not available')
        sentiment = result.get('sentiment', 'Not available')

        output_data = {
            'Transcript': transcript,
            'Summary': summary,
            'Sentiment': sentiment
        }

        # CHANGED: Call the new function to save to a .txt file
        save_to_txt(output_data)

        return render_template(
            'result.html',
            transcript=transcript,
            summary=summary,
            sentiment=sentiment
        )
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return render_template('index.html', error=f"An error occurred during analysis: {e}")

# --- Main Execution ---
if __name__ == '__main__':
    app.run(debug=True)