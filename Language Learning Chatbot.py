import openai
import sqlite3
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

# Initialize OpenAI model
client = openai.OpenAI(api_key="")  # Use your real API key

response = client.chat.completions.create(
    model="gpt-4o",  e
    messages=[
        {"role": "system", "content": "You are a language tutor."},
        {"role": "user", "content": "How do I say 'hello' in Spanish?"}
    ]
)

print(response.choices[0].message.content)


print(response.choices[0].message.content)



def setup_database():
    """Creates an SQLite database to track user mistakes."""
    conn = sqlite3.connect("mistakes.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mistakes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            mistake TEXT,
            correction TEXT
        )
    """)
    conn.commit()
    conn.close()

def store_mistake(user, mistake, correction):
    """Stores user mistakes in SQLite."""
    conn = sqlite3.connect("mistakes.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO mistakes (user, mistake, correction) VALUES (?, ?, ?)",
                   (user, mistake, correction))
    conn.commit()
    conn.close()

def generate_prompt(user_lang, learning_lang, level):
    """Creates an initial system prompt for conversation."""
    return f"You are a language tutor. The user speaks {user_lang} and is learning {learning_lang} at {level} level. " \
           f"Create a conversation in {learning_lang}, correct their mistakes, and track them."

def get_feedback(user):
    """Fetches all mistakes for a user and provides feedback."""
    conn = sqlite3.connect("mistakes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT mistake, correction FROM mistakes WHERE user = ?", (user,))
    mistakes = cursor.fetchall()
    conn.close()
    
    if not mistakes:
        return "No mistakes recorded! Great job!"
    
    feedback = "Here are the mistakes you made and their corrections:\n"
    for mistake, correction in mistakes:
        feedback += f"- {mistake} → {correction}\n"
    
    return feedback

def chat_with_bot(user, user_lang, learning_lang, level):
    """Handles the chatbot conversation."""
    messages = [SystemMessage(content=generate_prompt(user_lang, learning_lang, level))]
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print(get_feedback(user))
            break
        
        messages.append(HumanMessage(content=user_input))
        response = llm(messages)
        ai_reply = response.content
        print("Bot:", ai_reply)
        
        # (Assuming we can detect mistakes in future expansion)
        messages.append(AIMessage(content=ai_reply))

# Setup database
setup_database()

# Example: Start chat
if __name__ == "__main__":
    user = "User1"
    user_lang = input("Enter your native language: ")
    learning_lang = input("Enter the language you want to learn: ")
    level = input("Enter your proficiency level (beginner, intermediate, advanced): ")
    chat_with_bot(user, user_lang, learning_lang, level)
