import sqlite3
import datetime
from textblob import TextBlob
import geocoder
from geopy.geocoders import Nominatim
import schedule
import time
import random
import threading

def insert_prompts():
    prompts = [
        ("What made you feel joyful today?", "joyful"),
        ("What made you feel anxious today?", "anxiety"),
        ("What made you feel calm today?", "calmness"),
        ("What made you feel sad today?", "sadness"),
        ("What excited you today?", "excitement"),
        ("What was frustrating about today?", "frustration"),
        ("What filled you with pride today?", "pride"),
        ("What made you feel grateful today?", "gratitude"),
        ("What disappointed you today?", "disappointment"),
        ("What made you feel loved today?", "love"),
        ("What moment made you feel hopeful today?", "hope"),
        ("What made you feel relaxed today?", "calmness"),
        ("When did you feel angry today?", "anger"),
        ("What made you feel worried today?", "worry"),
        ("What surprised you today?", "surprise"),
        ("What gave you confidence today?", "self_confidence"),
        ("What moment today made you feel lonely?", "loneliness"),
        ("What encouraged you today?", "encouragement"),
        ("What filled you with energy today?", "energy"),
        ("What scared you today?", "fear"),
        ("What inspired you today?", "inspiration"),
        ("What made you feel guilty today?", "guilt"),
        ("What made you feel appreciated today?", "appreciation"),
        ("What relieved you today?", "relief"),
        ("What overwhelmed you today?", "overwhelm"),
        ("What made you laugh today?", "laughter"),
        ("What gave you peace of mind today?", "peace"),
        ("What made you curious today?", "curiosity"),
        ("What challenged you today?", "challenge"),
        ("What was a small victory for you today?", "success"),
    ]
    
    conn = sqlite3.connect('emotion_data.db')
    cursor = conn.cursor()

    for prompt, emotion in prompts:
        cursor.execute('INSERT INTO Prompts (text, emotion) VALUES (?, ?)', (prompt, emotion))

    conn.commit()
    conn.close()

    
    return prompts

# Getting a random prompt from the database
def get_random_prompt():
    conn = sqlite3.connect('emotion_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Prompts ORDER BY RANDOM() LIMIT 1')
    prompt = cursor.fetchone()

    conn.close()
    return prompt


def derive_emotion_based_on_prompt(prompt_text):
    # Define emotion_map as a dictionary
    emotion_map = {
        "What made you feel joyful today?": "joyful",
        "What made you feel anxious today?": "anxiety",
        "What made you feel calm today?": "calmness",
        "What made you feel sad today?": "sadness",
        "What excited you today?": "excitement",
        "What was frustrating about today?": "frustration",
        "What filled you with pride today?": "pride",
        "What made you feel grateful today?": "gratitude",
        "What disappointed you today?": "disappointment",
        "What made you feel loved today?": "love",
        "What moment made you feel hopeful today?": "hope",
        "What made you feel relaxed today?": "calmness",
        "When did you feel angry today?": "anger",
        "What made you feel worried today?": "worry",
        "What surprised you today?": "surprise",
        "What gave you confidence today?": "self_confidence",
        "What moment today made you feel lonely?": "loneliness",
        "What encouraged you today?": "encouragement",
        "What filled you with energy today?": "energy",
        "What scared you today?": "fear",
        "What inspired you today?": "inspiration",
        "What made you feel guilty today?": "guilt",
        "What made you feel appreciated today?": "appreciation",
        "What relieved you today?": "relief",
        "What overwhelmed you today?": "overwhelm",
        "What made you laugh today?": "laughter",
        "What gave you peace of mind today?": "peace",
        "What made you curious today?": "curiosity",
        "What challenged you today?": "challenge",
        "What was a small victory for you today?": "success",
    }
    
    # Default emotion is neutral if the prompt is not recognized
    return emotion_map.get(prompt_text, "neutral")

    # Default emotion is neutral if the prompt is not recognized
    return emotion_map.get(prompt_text, "neutral")



# Saving the user's response into the database
def save_response(prompt_id, response_text, emotion):
    conn = sqlite3.connect('emotion_data.db')
    cursor = conn.cursor()

    # Getting current date and time
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute('''
        INSERT INTO Responses (prompt_id, response_text, emotion, date)
        VALUES (?, ?, ?, ?)
    ''', (prompt_id, response_text, emotion, date))

    conn.commit()
    conn.close()
    
# Main function to collect and save responses
def collect_and_save_response():
    prompt = get_random_prompt()  # Fetching a random prompt from the database
    print(f"Prompt: {prompt[1]}")  # Displaying the prompt text

    response_text = input("Enter your response: ")  # Getting the response text from the user

    emotion = derive_emotion_based_on_prompt(prompt[1])  # Deriving emotion based on the prompt

    # Getting the user's location (latitude, longitude)
    location = get_user_location()
    if location:
        latitude, longitude = location
    else:
        latitude, longitude = None, None  # If location is not available, store None

    save_response(prompt[0], response_text, emotion, latitude, longitude)

    print(f"Emotion derived based on the prompt: {emotion}")
    print("Your response has been saved successfully.")
    print(f"Location: Latitude={latitude}, Longitude={longitude}")

# Function to view all data in the database
def view_database_contents():
    conn = sqlite3.connect('emotion_data.db')
    cursor = conn.cursor()

    # Querying to fetch all responses along with prompt, emotion, location, and date
    cursor.execute('''
        SELECT Prompts.text, Responses.response_text, Responses.emotion, Responses.latitude, Responses.longitude, Responses.date
        FROM Responses
        JOIN Prompts ON Responses.prompt_id = Prompts.id
    ''')

    responses = cursor.fetchall()

    if responses:
        print("\n--- Database Contents ---")
        for response in responses:
            print(f"Prompt: {response[0]}")
            print(f"Response: {response[1]}")
            print(f"Emotion: {response[2]}")
            print(f"Location: Latitude={response[3]}, Longitude={response[4]}")
            print(f"Date: {response[5]}")
            print("-" * 40)
    else:
        print("No responses found in the database.")

    conn.close()



# Main function to collect and save responses
def collect_and_save_response():
    prompt = get_random_prompt()  # Fetching a random prompt from the database

    if prompt is None:
        print("No prompts found in the database. Please add prompts first.")
        return

    print(f"Prompt: {prompt[1]}")  # Displaying the prompt text

    response_text = input("Enter your response: ")  # Getting the response text from the user
    emotion = derive_emotion_based_on_prompt(prompt[1])  # Deriving emotion based on the prompt

    # Saving the response and emotion to the database
    save_response(prompt[0], response_text, emotion)

    print(f"Emotion derived based on the prompt: {emotion}")
    print("Your response has been saved successfully.")
    
# Function to get the user's latitude and longitude based on their IP address
def get_user_location():
    g = geocoder.ip('me')  # This uses the user's IP address to get location
    return g.latlng  #Should return a list [latitude, longitude] or None if not available

    
def update_schema():
    conn = sqlite3.connect('emotion_data.db')
    cursor = conn.cursor()

    # Add latitude and longitude columns
    cursor.execute('''
        ALTER TABLE Responses ADD COLUMN latitude REAL
    ''')
    cursor.execute('''
        ALTER TABLE Responses ADD COLUMN longitude REAL
    ''')

    conn.commit()
    conn.close()
    

# Saving the daily prompt to the database
def save_daily_prompt(prompt_id):
    conn = sqlite3.connect('emotion_data.db')
    cursor = conn.cursor()

    # Getting the current date
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Check if a prompt has already been saved for today
    cursor.execute('SELECT * FROM DailyPrompt WHERE date = ?', (today_date,))
    existing_prompt = cursor.fetchone()

    if existing_prompt:
        print("A daily prompt has already been generated for today.")
    else:
        # Save the prompt for today
        cursor.execute('INSERT INTO DailyPrompt (prompt_id, date) VALUES (?, ?)', (prompt_id, today_date))
        print(f"New daily prompt saved for today: Prompt ID {prompt_id}")

    conn.commit()
    conn.close()

# Generate and save a daily prompt
def generate_daily_prompt():
    # Get a random prompt from the database
    prompt = get_random_prompt()
    
    if prompt:
        print(f"Today's prompt: {prompt[1]}")
        save_daily_prompt(prompt[0])
    else:
        print("No prompts found in the database.")

# Scheduling the task to run every 10 seconds (for testing)
def schedule_daily_prompt():
    # Scheduling every 10 seconds
    schedule.every(10).seconds.do(generate_daily_prompt)  

    print("Daily prompt scheduler initialized (testing mode).")
    while True:
        schedule.run_pending()
        time.sleep(1)

# Main function
if __name__ == "__main__":
    create_daily_prompt_table()  # Code for Ensuring the database and tables are set up

    # Scheduling the daily prompt generation
    schedule_daily_prompt()

# Create DailyPrompt table
def create_daily_prompt_table():
    conn = sqlite3.connect('emotion_data.db')
    cursor = conn.cursor()

    # Creating DailyPrompt table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS DailyPrompt (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt_id INTEGER NOT NULL,
            date TEXT NOT NULL UNIQUE,
            FOREIGN KEY (prompt_id) REFERENCES Prompts (id)
        )
    ''')

    conn.commit()
    conn.close()

def get_random_prompt():
    conn = sqlite3.connect('emotion_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Prompts ORDER BY RANDOM() LIMIT 1')
    prompt = cursor.fetchone()

    conn.close()
    return prompt

# Running the program
if __name__ == "__main__":
    initialize_database()  # Ensuring that the database and tables are set up
    collect_and_save_response()  # Collecting and saving a user response