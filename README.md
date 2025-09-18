# **AI-Powered Customer Call Transcript Analyzer**

This project is a Python-based web application that leverages the Groq API to perform intelligent analysis on customer call transcripts. The application provides a concise summary and a nuanced sentiment analysis (Positive, Neutral, or Negative) for any given transcript, saving the results in a structured log file for record-keeping.

# Features

- Simple Web Interface: An easy-to-use UI for pasting and submitting call transcripts.

- AI-Powered Summarization: Generates a 2-3 sentence summary of the conversation's key points.

- Sophisticated Sentiment Analysis: Accurately identifies the customer's sentiment by analyzing the context, not just keywords.

- Data Persistence: Automatically saves each analysis (transcript, summary, sentiment) with a timestamp to a structured .txt file.

# Technology Stack

- Backend: Python

- Web Framework: Flask

- AI / LLM: Groq API (using the LLaMA 3 model)

- Frontend: Standard HTML & CSS

# Project Structure
```
call-analyzer/
│
├── app.py              # Main Flask application script
├── requirements.txt    # Required Python packages
├── call_analysis.txt   # Generated log file for analysis results
└── templates/
    ├── index.html      # Home page with the input form
    └── result.html     # Page to display the analysis results
```

# Setup and Installation

Follow these steps to get the application running on your local machine.

**1. Clone the Repository**

First, clone this project's repository to your local machine (or simply download and place the files in a folder).

**2. Create a Virtual Environment**

It is highly recommended to use a virtual environment to manage project dependencies.

```Bash

# Navigate into your project directory
cd call-analyzer

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

**3. Install Dependencies**

Install the required Python packages using the requirements.txt file.

```Bash
pip install -r requirements.txt
```

**4. Set Up the Groq API Key**

This project requires a Groq API key to function.

- Get a Key: Visit GroqCloud to create a free account and generate an API key.

- Set Environment Variable: For security, the application reads the key from an environment variable named GROQ_API_KEY.

  - On Windows (Command Prompt):

```Bash
setx GROQ_API_KEY "YOUR_API_KEY_HERE"
```

(You must restart your terminal after running this command for the change to take effect.)

  - On macOS / Linux:

```Bash
export GROQ_API_KEY="YOUR_API_KEY_HERE"
```

(To make this permanent, add this line to your ~/.bashrc or ~/.zshrc file.)

# How to Run the Application

With your virtual environment activated and the API key set, start the Flask server with this simple command:

```Bash
python app.py
```
You will see output in your terminal indicating that the server is running. Now, open your web browser and navigate to:

**http://127.0.0.1:5000**

# How to Use

- Paste Transcript: Copy any customer call transcript and paste it into the text area on the home page.

- Analyze: Click the "Analyze Transcript" button.

- View Results: The application will process the transcript and display the summary and sentiment on the results page.

- Check Log File: A new entry will be appended to the call_analysis.txt file in your project directory, containing the full transcript, summary, sentiment, and a timestamp

