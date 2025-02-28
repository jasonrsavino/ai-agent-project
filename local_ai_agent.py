import ollama
from duckduckgo_search import DDGS

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

print("AI Agent with Memory & Web Search is ready! Type 'exit' to quit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Goodbye!")
        break
    response = chat_with_local_ai(user_input)
    print("AI:", response)