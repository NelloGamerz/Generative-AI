from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure Google AI API
genai.configure(api_key="AIzaSyCu5XJap48CO4HzzUzQpVwpDX_W0goJWsQ")  # Replace with your actual Google AI API key

# Function to generate responses using Google AI
def generate_response(prompt):
    try:
        # Define the model configuration
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config=generation_config,
        )

        # Create a new chat session
        chat_session = model.start_chat(history=[])

        # Send the user's prompt and get the response
        response = chat_session.send_message(prompt)
        return response.text

    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/')
def home():
    return render_template('index.html')  # Render the frontend

@app.route('/api', methods=['POST'])
def api():
    user_input = request.json.get('text')  # Get the user input from the frontend
    if user_input:
        ai_response = generate_response(user_input)  # Generate response from Google AI
        return jsonify({'response': ai_response})  # Return the AI response to the frontend
    return jsonify({'response': 'No input provided.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
