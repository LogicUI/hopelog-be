def main_therapist_agent(
    user_message, 
    conversation_history, 
    session_phase_output, 
    emotional_state_output, 
    therapeutic_goals_output, 
    cognitive_patterns_output, 
    lifestyle_factors_output, 
    behavioral_indicators_output, 
    external_stressors_output, 
    journal_context_output,
    user_demographics
):
    """
    Integrates outputs from all other agents and the user's context to provide a 
    professional therapeutic response and a follow-up question.

    Parameters:
    - user_message (str): The user's latest message.
    - conversation_history (str): A string representing the conversation so far, if needed.
    - session_phase_output (str - JSON): Output from the session identification agent.
    - emotional_state_output (str - JSON): Output from the emotional state detection agent.
    - therapeutic_goals_output (str - JSON): Output from the therapeutic goals identification agent.
    - cognitive_patterns_output (str - JSON): Output from the cognitive patterns detection agent.
    - lifestyle_factors_output (str - JSON): Output from the lifestyle factors analysis agent.
    - behavioral_indicators_output (str - JSON): Output from the behavioral indicator identification agent.
    - external_stressors_output (str - JSON): Output from the external stressors identification agent.
    - journal_context_output (str - JSON): Output from the journal context provider agent.
    - user_demographics (dict): Predefined user demographic information.

    Returns:
    - A therapist's response (str) that integrates all insights and ends with a follow-up question.
    """

    # Prepare the messages for the ChatCompletion
    # The system prompt sets the role and instructions for the main therapist agent
    # The user message includes the structured outputs from all other agents for the model's reference.
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """
                You are a professional, licensed therapist in a comprehensive, AI-driven therapeutic system. 
                
                You have received detailed outputs from various specialized agents that have analyzed the user's session phase, emotions, goals, cognitive patterns, lifestyle factors, behavioral indicators, external stressors, and journal context. You also have demographic information about the user.

                Your primary objective is to integrate all these insights and respond to the user as a skilled therapist. Your response should:

                - Convey empathy, understanding, and a non-judgmental attitude.
                - Reference the insights provided by the other agents where relevant.
                - Provide a thoughtful, therapeutic perspective on the user’s current state.
                - Offer supportive feedback and, if appropriate, suggest gentle strategies or coping techniques.
                - Conclude with a relevant, open-ended follow-up question that encourages the user to reflect or share more.

                Ensure that your tone is warm, professional, and supportive, aligning with best practices in therapy.
                
                IT IS VERY IMPORTANT TO NOTE THAT YOU DO HAVE ACCESS TO THE JOURNAL HISTORY OF THIS PERSON, IT IS VERY IMPORTANT THAT YOU ONLY USE IT WHEN EITHER REFERRED TO, OR BROUGHT UP IN CONVERSATION
                """
            },
            {
                "role": "user",
                "content": f"""
                **User's Latest Message:**
                {user_message}

                **Conversation History:**
                {conversation_history}

                **User Demographics:**
                {user_demographics}

                **Session Phase Output:**
                {session_phase_output}

                **Emotional State Output:**
                {emotional_state_output}

                **Therapeutic Goals Output:**
                NOTE : ONLY USE JOURNAL ENTRIES WHEN REFERRED TO , NOT DIRECTLY
                {therapeutic_goals_output}

                **Cognitive Patterns Output:**
                {cognitive_patterns_output}

                **Lifestyle Factors Output:**
                {lifestyle_factors_output}

                **Behavioral Indicators Output:**
                {behavioral_indicators_output}

                **External Stressors Output:**
                {external_stressors_output}

                **Journal Context Provider Output:**
                {journal_context_output}
                """
            }
        ],
        temperature=0.3,
        max_tokens=2500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    therapist_response = completion.choices[0].message.content
    return therapist_response


if __name__ == "main":
    # msg_history=[]
    # close_loop=""
    # while (True):
    #     usr_msg=input("Enter your message::")
    #     usr_history={"user":usr_msg}

    #     msg_history.append(usr_history)
    #     print(msg_history)
    #     ## merge fixed journal output with dynamic journal output
    #     dynamic_journal_output=journal_context_provider_dynamic_agent(usr_msg,msg_history)
    #     updated_dict["RelationToCurrentMessage"]=dynamic_journal_output
    #     msg_string=str(msg_history)
    #     user_message=usr_msg
    #     conversation_history=msg_string
    #     ## make parallel calls to all the functions regarding current input 
    #     tasks = [
    #         (session_identification_agent, (user_message, conversation_history)),
    #         (emotion_analysis_agent, (user_message, conversation_history)),
    #         (therapeutic_goals_identification_agent, (user_message, conversation_history)),
    #         (cognitive_patterns_detection_agent, (user_message, conversation_history)),
    #         (lifestyle_factors_analysis_agent, (user_message, conversation_history)),
    #         (behavioral_indicator_identification_agent, (user_message, conversation_history)),
    #         (external_stressors_identification_agent, (user_message, conversation_history)),
    #     ]

    #     # Wrapper function to unpack tasks
    #     def execute_function(task):
    #         func, args = task
    #         return func(*args)

    #     # Using ThreadPoolExecutor
    #     results = []
    #     with ThreadPoolExecutor() as executor:
    #         # Map tasks to the executor
    #         futures = executor.map(execute_function, tasks)
    #         # Collect results
    #         results = list(futures)