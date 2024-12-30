from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI
from dotenv import load_dotenv
import logging
import os

load_dotenv()
client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url=os.getenv("GEMINI_BASE_URL")
)

async def summary_agent(conversation_history):
    formatted_history = "\n".join(
        f"User: {entry['user']}" if "user" in entry else f"AI: {entry['therapist']}"
        for entry in conversation_history
    )
    
    prompt = f"""
    You are a conversational therapist.
    Based on the conversation history provided, 
    summarize the discussion and highlight key points that are important to the user. Ensure the response is concise and does not include any prefatory remarks,
    meta-statements, or instruction steps. Provide the summary and key points directly.

    {formatted_history}
    
    Perform the following tasks:
    1. Create a summary of the conversation history based on what was discussed. 
    2. Highlight key points of the conversations that are important to the user.
    3. It should refer to the person by name and express in first person view.
    4. Remove the word summary from the response.
    """
    
    try:
        response = await client.chat.completions.create(
            model="gemini-2.0-flash-exp",
            messages=[
                {"role": "system", "content": "You are a conversational therapist. Based on the conversation history provided, summarize the discussion and highlight key points that are important to the user. Ensure the response is concise and does not include any prefatory remarks, meta-statements, or instruction steps. Provide the summary and key points directly."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


async def analyze_agent(conversation_history):
    formatted_history = "\n".join(
        f"User: {entry['user']}" if "user" in entry else f"AI: {entry['therapist']}"
        for entry in conversation_history
    )
    
    prompt = f"""
    You are a conversational therapist.
    Based on the conversation history provided, 
    summarize the discussion and highlight key points that are important to the user. Ensure the response is concise and does not include any prefatory remarks,
    meta-statements, or instruction steps. Provide the summary and key points directly.

    {formatted_history}
    
    Perform the following tasks:
    1. Analyze the conversation on what was discussed and provide insights on the user's emotions
    2. Highlight key points of the conversations that are important to the user.
    3. Give a brief overview in one paragraph
    4. Do not say user, should be something like "feeling of axiety, anger, fear etc"
    5. Do not refer the person and call them by "user" just state the emotion and expression concisely 
    6. Do not refer to the person or entity, it should be formatted like hashtags 
    7. Refer to the person as you and not as a third person
    """
    try:
        response = await client.chat.completions.create(
            model="gemini-2.0-flash-exp",
            messages=[
                {"role": "system", "content": "You are a conversational therapist."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error occurred: {e}")
        return None



async def stream_emotion_analysis_response(user_message, conversation_history=[], user_name=""):
    """
    Construct the prompt and stream the response from the AI model.
    """
    # Format conversation history for the prompt
    formatted_history = "\n".join(
        f"User: {entry['user']}" if "user" in entry else f"AI: {entry['therapist']}"
        for entry in conversation_history
    )
    
    # Construct the system prompt
    system_prompt = f"""
    You are a conversational therapist. 
    Your primary role is to analyze the user's messages to identify emotions and provide therapeutic support.
    
    Conversation history:
    {formatted_history}
    
    Current user message:
    {user_message}
    
    User name: {user_name}
    
    Perform the following tasks:
    1. Identify and list the emotions expressed by the user in their latest message.
    2. It should return back a text in a chat format as if i'm talking to a real person
    3. Keep the response empathetic and supportive.
    4. The response should not be robotic, it should be more human like with emotions expressed and being a good listener while implying and prompt the user to talk more
    5. It should be more expressive and engaging like "hey john!, im so sorry about what you feel !, you are not alone in this and im here to listen to you"
    6. Should address by name and should be more personal
    7. Do not provide any medical advice or diagnosis.
    8. Do not repeat saying that you will be listening without judgement. 
    """

    # Generator to stream response
    async def response_generator():
        logging.info("Streaming AI response...")
        logging.info("Prompt: %s", system_prompt)
        
        try:
            completion = client.chat.completions.create(
                model="gemini-2.0-flash-exp",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,
                max_tokens=2000,
                stream=True  # Enable streaming
            )
            for chunk in completion:
                for choice in chunk.choices:
                    if choice.delta.content:  
                         yield choice.delta.content
                    
        except Exception as e:
            logging.error("Error in streaming response: %s", str(e))
            raise e

    return response_generator()
