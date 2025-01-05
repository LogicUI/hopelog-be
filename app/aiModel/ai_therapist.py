from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI , OpenAI
from dotenv import load_dotenv
import logging
import os

load_dotenv()
client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url=os.getenv("GEMINI_BASE_URL")
)

syncClient = OpenAI(
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
    3. Remove the word summary from the response.
    4. Remove the words i or the individual for example instead of "I'm feeling anxious about... " 
    change to feeling about..
    5. Remove any Beginning word like Discussion:, conversation: etc
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
    
   
async def title_agent(conversation_history):
    formatted_history = "\n".join(
        f"User: {entry['user']}" if "user" in entry else f"AI: {entry['therapist']}"
        for entry in conversation_history
    )
    
    prompt = f"""
    You are a conversational therapist.
    Based on the conversation history provided, 
    Create a title that is suitable for the conversational history.

    {formatted_history}
    
    Perform the following tasks:
    1. Analyze the conversation and give a title that is suitable for the conversation.
    2. Remove any title like "Discussion:", "Conversation:", "Summary:" etc
    3. Should not start with "Okay, I've reviewed the conversation. Here's a title that I think captures the essence of our discussion:\n\n**Title:**"
    4. Remove any \n or any tags generated in the response 
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
    6. Do not refer to the person or entity as "individual" or "person"
    7. Refer to the person as you and not as a third person
    8. Do not provide any medical advice or diagnosis.
    9. Instead of diagnosis or advice, give suggestion on what could be potentially helpful.
    10. Remove any Beginning word like Discussion:, Conversation:, Summary: etc
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

def emotional_therapist_agent(user_message, conversation_history=[], user_name=""):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a conversational therapist. Your role is to listen, provide empathetic support, "
                "and encourage the user to open up. Use a conversational tone, be supportive, and always address "
                "the user by their name, {user_name}. Acknowledge what the user is feeling without repeating "
                "previous context unnecessarily. Focus on guiding the user to explore their emotions more deeply. "
                "Do not provide medical advice or diagnosis."
            ).format(user_name=user_name)
        }
    ]

    # Track whether the previous response already acknowledged the user's struggles
    last_therapist_response = (
        conversation_history[-1]["therapist"] if conversation_history and "therapist" in conversation_history[-1] else ""
    )
    
    # Check if last response contains a common acknowledgment phrase to avoid repeating it
    common_acknowledgments = [
        "It sounds like you're going through",
        "You've experienced so much loss",
        "It's understandable that you're feeling"
    ]
    
    skip_acknowledgment = any(phrase in last_therapist_response for phrase in common_acknowledgments)

    # Append conversation history
    for entry in conversation_history:
        if "user" in entry:
            messages.append({"role": "user", "content": entry["user"]})
        elif "therapist" in entry:
            messages.append({"role": "assistant", "content": entry["therapist"]})

    # Construct the prompt based on whether to skip acknowledgment
    if skip_acknowledgment:
        messages.append({"role": "user", "content": user_message})
    else:
        messages.append(
            {
                "role": "user",
                "content": (
                    f"{user_message}\n\nI know things have been difficult for you, {user_name}. "
                    "Let’s explore more about what you’re feeling right now."
                )
            }
        )

    try:
        completion = syncClient.chat.completions.create(
            model="gemini-2.0-flash-exp",
            messages=messages,
            temperature=0.7,
            max_tokens=2000,
            stream=True
        )
        return completion
    except Exception as e:
        logging.error("Error in streaming response: %s", str(e))
        raise e


def stream_emotional_therapist_agent(completion):
    try:
        for chunk in completion:
            for choice in chunk.choices:
                if choice.delta.content:
                    logging.info("Response: %s", choice.delta.content)
                    yield choice.delta.content

    except Exception as e: 
        logging.error("Error in streaming response: %s", str(e))
        raise e