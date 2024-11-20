from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
assistant_id = os.getenv('ASSISTANT_ID')  # Your trained assistant ID

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json['message']
        
        # Create a thread
        thread = client.beta.threads.create()
        
        # Add the user's message to the thread
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_message
        )
        
        # Run the assistant
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )
        
        # Wait for the completion
        while run.status not in ["completed", "failed"]:
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            time.sleep(0.5)  # Add a small delay to prevent too many API calls
            
        if run.status == "failed":
            return jsonify({'error': 'Assistant failed to respond'}), 500
            
        # Get the assistant's response
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        assistant_response = messages.data[0].content[0].text.value
        
        return jsonify({'response': assistant_response})
    
    except Exception as e:
        print(f"Error: {str(e)}")  # Add this for debugging
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)