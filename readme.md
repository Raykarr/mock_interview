# AI-Powered Mock Interview Bot

This project is a web-based, voice-driven mock interview application designed to help students practice their interview skills in a real-time, conversational manner. It utilizes state-of-the-art AI services for speech-to-text, text-to-speech, and intelligent feedback generation.

## Features

- **Conversational Flow:** Real-time, turn-by-turn interaction with an AI interviewer.
- **Structured Interview:** Covers a predefined set of 8 common interview questions.
- **Voice I/O:** Users answer questions by speaking, and the bot responds with a natural-sounding voice.
- **Live Transcription:** The entire conversation is transcribed and displayed in a chat-like interface.
- **AI-Generated Feedback:** At the end of the interview, the AI provides personalized, encouraging, and actionable feedback based on the user's answers.
- **Formatted Feedback Display:** The final feedback is rendered with proper formatting (bold, lists) for enhanced readability.

---

## Technical Architecture

The application is built on a simple yet powerful 3-tier architecture:

1.  **Frontend (Client):** A vanilla HTML, CSS, and JavaScript interface that runs in the browser. It uses the `MediaRecorder` API to capture audio and the `fetch` API for server communication.
2.  **Backend (Server):** A **Flask** (Python) server that orchestrates the interview flow, manages state, and communicates with external AI services.
3.  **AI Services (APIs):**
    - **Deepgram:** For high-accuracy Speech-to-Text (`nova-2`) and natural Text-to-Speech (`aura-asteria-en`).
    - **OpenRouter:** As a gateway to the `openai/gpt-4o-mini` model for intelligent feedback generation.

---

## Getting Started

Follow these steps to set up and run the project locally.

### Prerequisites

- Python 3.8+
- A web browser that supports the `MediaRecorder` API (e.g., Chrome, Firefox).
- API keys from:
  - [Deepgram](https://deepgram.com/)
  - [OpenRouter.ai](https://openrouter.ai/)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Raykarr/mock_interview
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1.  **Start the Flask server:**
    ```bash
    python app.py
    ```

2.  **Open the application:**
    Open your web browser and navigate to `http://127.0.0.1:5003`.

3.  **Run the interview:**
    - Enter your Deepgram and OpenRouter API keys in the designated fields.
    - Click "Start Interview" to begin.
    - Use the "Record Answer" button to provide your spoken answers.

---
