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

# 'cbaiabfkafbef bsfsfbsfsf'

# from flask import Flask, render_template, request, jsonify
# import google.generativeai as genai
# import json
# import os
# import logging

# app = Flask(__name__)

# logging.basicConfig(filename='app.log', level=logging.ERROR)
# genai.configure(api_key="AIzaSyCu5XJap48CO4HzzUzQpVwpDX_W0goJWsQ")

# def save_chat_history(user_input, ai_response, file_path="chat_history.json"):
#     chat_data = []
    
#     if os.path.exists(file_path):
#         with open(file_path, 'r') as f:
#             chat_data = json.load(f)
    
#     chat_data.append({"user": user_input, "ai": ai_response})
    
#     with open(file_path, 'w') as f:
#         json.dump(chat_data, f)

# def load_chat_history(file_path="chat_history.json"):
#     if os.path.exists(file_path):
#         with open(file_path, 'r') as f:
#             return json.load(f)
#     return []

# def generate_response(prompt, history):
#     try:
#         generation_config = {
#             "temperature": 1,
#             "top_p": 0.95,
#             "top_k": 64,
#             "max_output_tokens": 8192,
#         }

#         history_prompt = "\n".join([f"User: {entry['user']}\nAI: {entry['ai']}" for entry in history])
#         full_prompt = f"{history_prompt}\nUser: {prompt}"

#         response = genai.generate_text(prompt=full_prompt, **generation_config)

#         if response.generations:
#             return response.generations[0].text
#         else:
#             logging.error("No generations returned from the AI API.")
#             return "No response generated from AI."

#     except Exception as e:
#         logging.error(f"An error occurred: {str(e)}") 
#         return "An error occurred while generating a response. Please try again."

# @app.route('/')
# def home():
#     return render_template('index.html') 

# @app.route('/api', methods=['POST'])
# def api():
#     user_input = request.json.get('text') 

#     if user_input:
#         history = load_chat_history()
#         ai_response = generate_response(user_input, history)
#         save_chat_history(user_input, ai_response)
#         return jsonify({'response': ai_response})
    
#     return jsonify({'response': 'No input provided.'}), 400

# if __name__ == '__main__':
#     app.run(debug=True)


