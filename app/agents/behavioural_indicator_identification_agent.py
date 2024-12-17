import os 
from google import genai
from dotenv import load_dotenv

load_dotenv()

def behavioral_indicator_identification_agent(text_input, conversation_history):
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    
    prompt = f"""
        ### Role: Behavioral Indicator Identification Agent

        **System Instructions:**
        You are the **Behavioral Indicator Identification Agent** within an AI-driven therapeutic system. Your primary role is to analyze user messages and identify behavioral indicators, including:
        - Daily Activities
        - Avoidance Behaviors
        - Engagement Levels
        - Changes in Behavior
        
        Follow these guidelines:
        - Accuracy: Provide precise and structured categorization.
        - Output Format: Return JSON with clear categories.

        **User Input:**
        - User Message: "{text_input}"
        - Conversation History: "{conversation_history}"

        **Task:**
        1. Analyze the user message for behavioral indicators.
        2. Categorize findings into the following format:
        ```json
        {{
            "DailyActivities": {{
                "Routine": "Description of daily routine",
                "EngagementInHobbies": "Description of engagement in hobbies"
            }},
            "AvoidanceBehaviors": {{
                "Tasks": "Description of avoidance related to tasks",
                "People": "Description of avoidance related to people"
            }},
            "EngagementLevels": {{
                "Participation": "Level of participation in activities",
                "Involvement": "Level of involvement in other areas"
            }},
            "ChangesInBehavior": {{
                "Irritability": "Description of irritability changes",
                "Withdrawal": "Description of withdrawal from activities"
            }}
        }}
        ```

        **Example Scenario:**
        "I've been skipping my evening walks and no longer feel like joining my friends for coffee. At work, I used to actively participate in meetings, but now I just listen without contributing. Lately, I've been getting more easily irritated and have withdrawn from activities I once enjoyed."

        **Expected Analysis:**
        ```json
        {{
            "DailyActivities": {{
                "Routine": "Skipping evening walks",
                "EngagementInHobbies": "No longer feels like joining friends for coffee"
            }},
            "AvoidanceBehaviors": {{
                "Tasks": "Skipping evening walks",
                "People": "Avoids joining friends for coffee"
            }},
            "EngagementLevels": {{
                "Participation": "Passively listens in meetings without contributing",
                "Involvement": "Withdrawn from social activities"
            }},
            "ChangesInBehavior": {{
                "Irritability": "Increased irritability lately",
                "Withdrawal": "Withdrawal from activities once enjoyed"
            }}
        }}
        ```

        Now analyze the user's message and return the structured output in JSON.
        """
    response = client.models.generate_content(
        config={
            "temperature": 0.3,
            "max_output_tokens": 4000,
            "top_p": 1,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0
        },
        model="gemini-2.0-flash-exp",
        contents=[{"text": prompt}]
    )
    return response.text
    
if __name__ == "__main__":
        behaviour_indicator = behavioral_indicator_identification_agent('i feel v tired recently even though i try to do my daily exercise through gym', "none")
        print(behaviour_indicator)
