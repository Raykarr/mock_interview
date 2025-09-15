```mermaid
graph LR
    subgraph "User's Browser (Client)"
        A[HTML/CSS/JS] --> B{"MediaRecorder API"}
        B --> C["Audio Capture"]
        D["Audio Player"] --> E["Plays Bot's Speech"]
        A --> F["Displays Transcript & Feedback"]
    end

    subgraph "Backend Server (Flask on Python)"
        G["Flask App"]
        H["Interview State Management"]
        I["API Orchestration Logic"]
        G --- H
        G --- I
    end

    subgraph "External AI Services"
        J["Deepgram STT API<br><i>(nova-2)</i>"]
        K["Deepgram TTS API<br><i>(aura-asteria-en)</i>"]
        L["OpenRouter LLM API<br><i>(gpt-4o-mini)</i>"]
    end

    C -- "POST /respond<br>(Audio Blob)" --> G
    G -- "1. Transcribe" --> J
    J -- "User Text" --> G
    G -- "3. Get Feedback (Final Turn)" --> L
    L -- "Feedback Text" --> G
    G -- "2. Get Speech" --> K
    K -- "Audio" --> G
    G -- "Audio / JSON" --> D
    G -- "Transcripts" --> F
