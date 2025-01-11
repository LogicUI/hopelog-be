from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI, OpenAI
from dotenv import load_dotenv
from .filter_model import (
    is_greeting,
    check_toxic_words,
    is_goodbye,
    is_gibberish,
    is_affirmation,
    is_complaint,
    is_negation,
    is_thank_you,
    is_short_message,
    is_apology,
    therapist_reply,
    is_inappropriate_request,
)
import logging
import os
import re


load_dotenv()


client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"), base_url=os.getenv("GEMINI_BASE_URL")
)

syncClient = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"), base_url=os.getenv("GEMINI_BASE_URL")
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
                {
                    "role": "system",
                    "content": "You are a conversational therapist. Based on the conversation history provided, summarize the discussion and highlight key points that are important to the user. Ensure the response is concise and does not include any prefatory remarks, meta-statements, or instruction steps. Provide the summary and key points directly.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=2000,
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
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=2000,
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
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=2000,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


def emotional_therapist_agent(user_message, conversation_history=[], user_name=""):
    """
    A conversational therapist agent that provides empathetic support, encourages users to open up,
    and handles different types of user messages appropriately.
    """

    if is_greeting(user_message):
        logging.info("User provided a greeting: %s", user_message)
        return f"Hello {user_name}, it's great to hear from you! How are you feeling today?"
    elif check_toxic_words(user_message):
        logging.warning("User used toxic language: %s", user_message)
        return "I'm here to help, but please refrain from using such language."

    elif is_goodbye(user_message):
        logging.info("User provided a goodbye: %s", user_message)
        return therapist_reply(
            user_message,
            responses=[
                "Goodbye! Take care and have a great day!",
                "See you soon! Remember, I'm always here to listen.",
                "Take care! I'm here whenever you need to talk.",
            ],
        )

    elif is_thank_you(user_message):
        logging.info("User expressed gratitude: %s", user_message)
        return therapist_reply(
            user_message,
            responses=[
                "You're welcome! I'm glad I could help.",
                "No problem at all. I'm happy to support you.",
                "Anytime! Take care, and feel free to reach out if you need anything.",
            ],
        )

    elif is_apology(user_message):
        logging.info("User provided an apology: %s", user_message)
        return therapist_reply(
            user_message,
            responses=[
                "It's okay, you don't need to apologize.",
                "No need to say sorry. I'm here to support you.",
                "I understand. You don't need to feel bad about anything.",
                "There's nothing to apologize for. I'm here to listen.",
                "Don't worry about it. Let's focus on what matters to you.",
            ],
        )
    elif is_affirmation(user_message):
        logging.info("User provided affirmation: %s", user_message)
        return therapist_reply(
            user_message,
            responses=[
                f"I'm glad to hear that, {user_name}! What's making you feel that way?",
                "That's great to hear! What's been going well for you?",
                "I'm happy to hear that! What's been going on?",
                "That's wonderful! What's been happening in your life?",
            ],
        )

    elif is_complaint(user_message):
        logging.info("User expressed a complaint: %s", user_message)
        return therapist_reply(
            user_message,
            responses=[
                f"I'm here to listen, {user_name}. What's been bothering you?",
                "It sounds like there's something on your mind. Want to tell me more?",
                "I'd love to understand better. Could you share a bit more?",
                "Feel free to open up. I'm here to help.",
                "Sometimes sharing more can help. Would you like to talk more about it?",
                "I sense there's more to what you're feeling. Can you tell me more?",
                "Take your time. I'm here whenever you're ready to share.",
                "I'm listening. Can you help me understand better by sharing more?",
                "It's okay to take it slow. Tell me more whenever you feel comfortable.",
            ],
        )

    elif is_negation(user_message):
        logging.info("User provided negation: %s", user_message)
        return therapist_reply(
            user_message,
            responses=[
                "I understand. What's been on your mind?",
                "That's okay. Do you want to talk about it further?",
                f"It's alright, {user_name}. I'm here to listen whenever you're ready.",
            ],
        )

    elif is_short_message(user_message):
        logging.info("User provided a short message: %s", user_message)
        return therapist_reply(
            user_message,
            responses=[
                f"It seems like you have a lot on your mind, {user_name}. Would you like to share more?",
                "I'd love to understand better. Could you elaborate a bit?",
                "That’s a bit brief. Is there something you’d like to talk about in more detail?",
                "I sense there might be more you'd like to say. Could you share more about it?",
                "Sharing your thoughts can sometimes help. Would you like to tell me more?",
                "Take your time. Whenever you're ready, I'm here to listen.",
            ],
        )

    elif is_gibberish(user_message):
        logging.info("User provided gibberish or unclear input: %s", user_message)
        return therapist_reply(
            user_message,
            responses=[
                "I'm having trouble understanding. Could you clarify what you're trying to say?",
                "It looks like your message is unclear. Could you rephrase it?",
                "Hmm, I don't quite follow. Could you elaborate?",
            ],
        )

    elif is_inappropriate_request(user_message):
        logging.info("User made an inappropriate request: %s", user_message)
        return therapist_reply(
            user_message,
            responses=[
                "I'm sorry, but I can't help with that request. Could you tell me more about how you're feeling?",
                "That seems like a task I can't do, but I'm here to listen.",
                "I'm here to help with emotional support, not to perform tasks.",
            ],
        )

    else:
        logging.info("User provided a general message: %s", user_message)
        messages = [
            {
                "role": "system",
                "content": (
                    f"You are a conversational therapist. Your role is to listen, provide empathetic support, "
                    f"and encourage the user to open up. Use a conversational tone, be supportive, and always address "
                    f"the user by their name, {user_name}. Acknowledge what the user is feeling without repeating "
                    "previous context unnecessarily. Focus on guiding the user to explore their emotions more deeply. "
                    "Do not provide medical advice or diagnosis."
                ),
            }
        ]

        for entry in conversation_history:
            if "user" in entry:
                messages.append({"role": "user", "content": entry["user"]})
            elif "therapist" in entry:
                messages.append({"role": "assistant", "content": entry["therapist"]})

        last_therapist_response = (
            conversation_history[-1].get("therapist", "")
            if conversation_history
            else ""
        )

        common_acknowledgments = [
            "It sounds like you're going through",
            "You've experienced so much loss",
            "It's understandable that you're feeling",
        ]

        skip_acknowledgment = any(
            phrase in last_therapist_response for phrase in common_acknowledgments
        )

        if skip_acknowledgment:
            messages.append({"role": "user", "content": user_message})
        else:
            messages.append(
                {
                    "role": "user",
                    "content": (
                        f"{user_message}\n\nI know things have been difficult for you, {user_name}. "
                        "Let’s explore more about what you’re feeling right now."
                    ),
                }
            )

        try:
            completion = syncClient.chat.completions.create(
                model="gemini-2.0-flash-exp",
                messages=messages,
                temperature=0.7,
                max_tokens=2000,
                stream=True,
            )
            return completion
        except Exception as e:
            logging.error("Error in streaming response: %s", str(e))
            return "Sorry, something went wrong. Please try again in a moment."


def stream_emotional_therapist_agent(completion):
    try:
        if isinstance(completion, str):
            logging.info("Direct streaming response: %s", completion)
            yield completion
            return

        for chunk in completion:
            for choice in chunk.choices:
                if choice.delta.content:
                    logging.info("Streaming chunk: %s", choice.delta.content)
                    yield choice.delta.content

    except Exception as e:
        logging.error("Error in streaming response: %s", str(e))
        raise e
