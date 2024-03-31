from flask import Flask, render_template, request
from llm import customizable_llm_rag, simple_llm
from werkzeug.utils import secure_filename
import os
import uuid  # for generating unique identifiers
from config import UPLOAD_FOLDER

app = Flask(__name__)

chat_history = []
chat_history_rag = []

# Set upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def generate_unique_filename(filename):
    # Get file extension
    _, file_extension = os.path.splitext(filename)
    # Generate a unique identifier (UUID)
    unique_id = str(uuid.uuid4())
    # Combine the unique identifier and the original file extension
    unique_filename = f"{unique_id}{file_extension}"
    return unique_filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simple-chatbot', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        user_input = request.form['user_input']
        bot_response = simple_llm.simple_llm_chat(user_input) 
        chat_history.append({'text': user_input, 'sender': 'user'})
        chat_history.append({'text': bot_response, 'sender': 'bot'})
        return bot_response

    return render_template('simple-chatbot.html', chat_history=chat_history)

@app.route('/customizable-llm', methods=['POST'])
def upload_files():
    file_paths = []
    if 'files[]' not in request.files:
        return "No file part"

    files = request.files.getlist('files[]')

    if not all(files):
        return "No selected file or topic or query"

    for file in files:
        if file:
            filename = secure_filename(file.filename)
            unique_filename = generate_unique_filename(filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file_paths.append(file_path)
            file.save(file_path)

    result = customizable_llm_rag.embeddingsCreationStoring(file_paths)
    return render_template('rag-chatbot.html', result=result)

@app.route('/rag-chatbot', methods=['GET', 'POST'])
def rag_chatbot():
    if request.method == 'POST':
        user_input = request.form['user_input']
        bot_response = customizable_llm_rag.rag(user_input) 
        chat_history_rag.append({'text': user_input, 'sender': 'user'})
        chat_history_rag.append({'text': bot_response, 'sender': 'bot'})
        return bot_response

    return render_template('rag-chatbot.html', chat_history_rag=chat_history_rag)
    
if __name__ == '__main__':
    app.run(debug=True)