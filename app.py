from flask import Flask, render_template, request, jsonify, Response
import requests
import json
import os
import base64 

app = Flask(__name__)

# Interview config
INTERVIEW_QUESTIONS = [
    "To start, please tell me something about yourself. Include your name, family background, educational background, and whether you are an earning member of the family.",
    "What motivated you to pursue a career in this particular field?",
    "How many internships or industrial training programs have you completed so far? Please include the names, durations, and the departments where you were trained.",
    "Tell me five things you have learned from your internships.",
    "Tell me two positive qualities about yourself and two areas where you think you need improvement.",
    "Where do you see yourself in five years from now?",
    "Give me a strong reason why we should hire you and how you are different from other candidates.",
    "Finally, are you available to start work immediately, or do you need time to complete other commitments?"
]

interview_state = {
    "current_question_index": 0,
    "answers": [],
    "interview_over": False
}

# API helper functions

def transcribe_audio(api_key, audio_bytes):
    headers = {"Authorization": f"Token {api_key}", "Content-Type": "audio/wav"}
    url = "https://api.deepgram.com/v1/listen?model=nova-2&punctuate=true"
    response = requests.post(url, headers=headers, data=audio_bytes)
    response.raise_for_status()
    return response.json()["results"]["channels"][0]["alternatives"][0]["transcript"]

def synthesize_speech(api_key, text):
    headers = {"Authorization": f"Token {api_key}", "Content-Type": "application/json"}
    payload = {"text": text}
    url = "https://api.deepgram.com/v1/speak?model=aura-asteria-en"
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.content

def generate_feedback(api_key, answers):
    full_interview = ""
    for i, answer in enumerate(answers):
        full_interview += f"Question: {INTERVIEW_QUESTIONS[i]}\nAnswer: {answer}\n\n"
    system_prompt = (
        "You are an encouraging interview coach for students. "
        "Your task is to provide feedback on the user's mock interview answers. "
        "The feedback must be brief (under 150 words), encouraging, and provide two or three actionable tips for improvement. "
        "Address the student directly. Always start with something positive. Use markdown for formatting if needed (e.g., bullet points)."
    )
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={ "Authorization": f"Bearer {api_key}", "Content-Type": "application/json" },
            data=json.dumps({
                "model": "openai/gpt-oss-20b:free",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": full_interview}
                ]
            })
        )
        response.raise_for_status()
        response_data = response.json()
        return response_data['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error generating feedback: {e}")
        return "I encountered an error while generating your feedback. Please ensure your OpenRouter API key is correct and has funds."

# Flask routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_interview():
    global interview_state
    interview_state = { "current_question_index": 0, "answers": [], "interview_over": False }
    api_key = request.form.get('deepgramApiKey')
    first_question_text = INTERVIEW_QUESTIONS[0]
    try:
        audio_content = synthesize_speech(api_key, first_question_text)
        response = Response(audio_content, mimetype='audio/mpeg')
        response.headers['X-Bot-Transcript'] = first_question_text
        return response
    except Exception as e:
        return jsonify({"error": f"Failed to synthesize first question: {str(e)}"}), 500

@app.route('/respond', methods=['POST'])
def respond():
    global interview_state
    if interview_state["interview_over"]:
        return jsonify({"error": "Interview has already ended."}), 400

    deepgram_api_key = request.form.get('deepgramApiKey')
    openrouter_api_key = request.form.get('openrouterApiKey')
    audio_file = request.files.get('audio')

    if not all([deepgram_api_key, openrouter_api_key, audio_file]):
        return jsonify({"error": "Missing API keys or audio file."}), 400

    try:
        user_answer_text = transcribe_audio(deepgram_api_key, audio_file.read())
        interview_state["answers"].append(user_answer_text)
        interview_state["current_question_index"] += 1

        if interview_state["current_question_index"] < len(INTERVIEW_QUESTIONS):
            # This is a normal question turn
            bot_response_text = INTERVIEW_QUESTIONS[interview_state["current_question_index"]]
            audio_content = synthesize_speech(deepgram_api_key, bot_response_text)
            response = Response(audio_content, mimetype='audio/mpeg')
            response.headers['X-User-Transcript'] = user_answer_text
            response.headers['X-Bot-Transcript'] = bot_response_text
            response.headers['X-Interview-Over'] = 'false'
            return response
        else:
            # This is the FINALLLL feedback turn
            interview_state["interview_over"] = True
            feedback_with_markdown = generate_feedback(openrouter_api_key, interview_state["answers"])
            bot_response_text_for_display = f"Thank you for completing the interview. Here is your feedback. {feedback_with_markdown}"
            
            clean_feedback_for_speech = feedback_with_markdown.replace('**', '').replace('*', '').replace('#', '')
            bot_response_text_for_speech = f"Thank you for completing the interview. Here is your feedback. {clean_feedback_for_speech}"

            # Synthesize the clean text
            audio_content = synthesize_speech(deepgram_api_key, bot_response_text_for_speech)
            
            # Encode audio and send the version with markdown to the frontend for display.
            audio_base64 = base64.b64encode(audio_content).decode('utf-8')
            
            return jsonify({
                "user_transcript": user_answer_text,
                "bot_transcript": bot_response_text_for_display, 
                "audio_base64": audio_base64,
                "interview_over": True
            })

    except Exception as e:
        print(f"Error in /respond: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5003)