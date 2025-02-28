from flask import Flask, request, jsonify, render_template
import ollama
from duckduckgo_search import DDGS

app = Flask(__name__, template_folder="templates")

# Store chat history
chat_memory = []

def search_web(query):
    """Perform a DuckDuckGo search and return results."""
    with DDGS() as ddgs:
        results = [r["title"] + " - " + r["href"] for r in ddgs.text(query, max_results=3)]
    return "\n".join(results) if results else "No results found."

def chat_with_local_ai(prompt):
    # Check if user wants to search the web
    if "search for" in prompt.lower():
        query = prompt.lower().replace("search for", "").strip()
        return search_web(query)

    # Append user input to memory
    chat_memory.append({"role": "user", "content": prompt})

    # Generate AI response
    response = ollama.chat(model="mistral", messages=chat_memory)

    # Append AI response to memory
    chat_memory.append({"role": "assistant", "content": response['message']['content']})

    return response["message"]["content"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    response = chat_with_local_ai(user_message)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)