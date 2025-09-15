### Project Assessment & Analysis

## What is the technical architecture of your implementation? What models did you use? Why did you choose this architecture?

POC is built on a **3-Tier Client-Server Architecture** for simplicity and rapid development.

  * **1. Frontend (Client):** A single HTML page with vanilla JavaScript

      * **Responsibility:** It captures microphone audio using the browser's `MediaRecorder` API, sends it to the server, receives audio back, plays it automatically, and displays the conversation transcript

  * **2. Backend (Server):** A lightweight **Flask** server written in Python

      * **Responsibility:** It acts as the central orchestrator. It receives audio from the client, manages the interview state (which question to ask next), and communicates with the external AI services.

  * **3. External APIs (Services):**

      * **Deepgram:** Used for both Speech-to-Text (STT) and Text-to-Speech (TTS)
          * **STT Model:** `nova-2` (for high-accuracy transcription)
          * **TTS Model:** `aura-asteria-en` (for a natural-sounding voice)
      * **OpenRouter:** Used as a gateway to access a powerful Large Language Model (LLM) for generating feedback
          * **LLM Model:** `openai/gpt-oss-20b:free` (chosen for its excellent balance of being open-source, intelligent, and free)

**Why this architecture?** 💡
This architecture was chosen because it's **ideal for a POC**. It allows to leverage best-in-class, specialized AI models for each task (speech, text, and reasoning) without building them from scratch. The simple HTTP request-response model was easy to implement and debug, providing a "real-time" feel that is perfectly adequate for a turn-based interview

-----

## What challenges did you encounter while implementing the solution?

1.  **Browser Audio Handling:** Capturing microphone audio reliably in a web browser using the `MediaRecorder` API requires careful management of data chunks and formats to ensure compatibility with the STT API
2.  **Handling Multi-line Text in Headers:** The initial design crashed on the final question because the AI's multi-line feedback (with Markdown) couldn't be placed in a single-line HTTP header. The solution was to send the final response as a more structured JSON package
3.  **TTS Reading Out Markdown:** The TTS engine was reading "star star" aloud , simply speaking BOLD formatting options. This required creating two versions of the final text: a clean one for speech and a formatted one for display.
4.  **Prompt Engineering:** Designing the right prompt for the OpenRouter LLM was crucial. It took refinement to ensure the feedback was consistently brief, encouraging, actionable, and in the right tone for the target audience

-----

## Do you think the application can be readily used on the field for testing? If not, what changes need to be made?

Nope, this application is a **functional POC and is not ready for field testing**. Before it can be used by students , many changes are needed:

1.  **Handling Multiple Users:** The current app uses a single global variable to track interview progress, meaning it can only handle **one user at a time**. This must be replaced with a proper **session management** system, likely backed by a databeas, to give each user their own private interview state
2.  **Robust Error Handling:** The application needs much more robust error handling to gracefully manage situations like API keys being invalid, network failures, or the AI services being temporarily down
3.  **Deployment:** It's currently running on a local Flask development server. For real-world use, it must be deployed on a better production-grade server

-----

## What are the limitations of your application? How can they be addressed?

  * **Limitation 1: High Latency:** There is a noticeable delay between speaking and getting a response due to the sequential API calls (STT → LLM → TTS).

      * **Solution:** For a truly seamless experience, the architecture could be upgraded to use **WebSockets for real-time streaming**. Audio could be streamed to Deepgram as the user speaks, reducing perceived latency

  * **Limitation 2: No User Accounts or History:** Users cannot save their interview history to track their progress over time

      * **Solution:** Add a simple user authentication system and a **database (like SQLite or PostgreSQL)** to store user data and past interview transcripts and feedback

-----

## What challenges do you anticipate in building the same for an Indian language, say Hindi or Marathi?

Building this for an Indian language presents significant and fascinating challenges:

1.  **Model Quality and Availability:** The biggest hurdle is the availability of high-quality, low-latency STT and TTS models for Hindi or Marathi that are as good as the English ones. While models exist, their accuracy with diverse Indian accents is a major concern
2.  **Code-Switching (Hinglish/Marathi-English):** This is a massive challenge. Users will naturally mix English words with Hindi/Marathi (e.g., "Mera first internship *experience* bahut *learning wala* tha"). Most STT models are very poor at transcribing this common speech pattern, leading to major errors
3.  **Cultural and Contextual Nuance:** The LLM must be able to generate feedback that is not just a literal translation but is also **culturally relevant** to our Indian job market. A generic prompt might produce feedback that doesn't resonate or is not applicable
4.  **Dialectal Variation:** Both Hindi and Marathi have numerous regional dialects. An STT model trained on one may perform poorly on another, requiring either very robust models or region-specific ones