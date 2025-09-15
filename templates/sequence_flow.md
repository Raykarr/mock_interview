```mermaid
sequenceDiagram
    participant User
    participant Frontend as "Frontend (Browser)"
    participant Backend as "Backend (Flask App)"
    participant Deepgram as "Deepgram API"
    participant OpenRouter as "OpenRouter API"

    User->>Frontend: Clicks "Start Interview"
    Frontend->>Backend: POST /start
    Backend->>Deepgram: Synthesize 1st Question (TTS)
    Deepgram-->>Backend: Audio Stream
    Backend-->>Frontend: Returns Audio Stream
    Frontend->>User: Plays 1st Question Audio

    User->>Frontend: Clicks "Record", Speaks Answer, Clicks "Stop"
    Frontend->>Backend: POST /respond (with Audio Blob)
    Backend->>Deepgram: Transcribe Answer (STT)
    Deepgram-->>Backend: User's Text Transcript

    alt Interview NOT Over
        Backend->>Deepgram: Synthesize Next Question (TTS)
        Deepgram-->>Backend: Audio Stream
        Backend-->>Frontend: Returns Audio Stream & Transcripts
        Frontend->>User: Plays Next Question Audio
    else Interview IS Over
        Backend->>OpenRouter: Generate Feedback (LLM)
        OpenRouter-->>Backend: Feedback Text (Markdown)
        Backend->>Deepgram: Synthesize Feedback (TTS - Cleaned Text)
        Deepgram-->>Backend: Audio Stream
        Backend-->>Frontend: Returns JSON (Transcripts + Base64 Audio)
        Frontend->>User: Plays Final Feedback Audio & Displays Formatted Text
    end
