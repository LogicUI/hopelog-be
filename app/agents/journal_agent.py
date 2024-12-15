from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor

client = OpenAI(api_key="")
def journal_context_provider_agent(query,journal_data=journal_data):
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are licensed therapist and have access to your patients journal . You need to infer it and respond to any queries. "
                },
                {
                    "role": "user",
                    "content": f"You are provided with a person's journal. : {journal_data} You need to answer accordingly the query that has been asked of you, which goes as follows :{query} . PLEASE NOTE : IF THE RESPONSE TO YOUR QUERY IS NOT FOUND  , SIMPLY RETURN : NA. NOTHING ELSE "
                }
            ],
            temperature=0.3,
            max_tokens=4000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
    
        guidelines = (completion.choices[0].message.content)
        return guidelines
    
def journal_context_provider_dynamic_agent(previous_context,current_msg):
    
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content":"You are licensed therapist and have access to your patients journal . You need to infer it and respond to any queries. "
            },
            {
                "role": "user",
                "content": f"""You are provided with a person's journal. This person is going through therapy and the context is provided as follows :
                    {previous_context}

                    with the most recent message being :
                    {current_msg}

                    you need to decide how do the themes and insights from the user's journal entries relate to their present concerns or topics of discussion? PLEASE NOTE : IF THE RESPONSE TO YOUR QUERY IS NOT FOUND  , SIMPLY RETURN : NA. NOTHING ELSE """
            }
        ],
        temperature=0.3,
        max_tokens=4000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        
    )

    guidelines = (completion.choices[0].message.content)
    return guidelines

if __name__ == "main": 
    journal_queries = [
    # Recent Activity
    "Can you provide a summary of the most recent entries in the user's journal, highlighting key activities, emotions, and experiences from the past week?",

    # Entry Themes
    "Identify and categorize the main themes present in the user's journal entries. What are the predominant topics or subjects the user frequently writes about?",

    # Self-Reported Progress
    "What insights can be drawn from the user's journal entries regarding their reported improvements, challenges faced, and personal realizations over time?",

    # Coping Strategies
    "What coping strategies has the user documented in their journal, and how effective do they describe these strategies—both healthy and unhealthy—in managing their stress or emotions?",

    # Recurring Patterns
    "What recurring emotional patterns or behavioral trends are evident in the user's journal entries, and what consistent triggers or situations do they frequently mention that affect their emotional state?",

    # Goals and Intentions
    "What short-term and long-term goals has the user set for themselves in their journal, and how has their focus on these goals evolved over time?",

    # Additional Parameters
     "What cultural, social, or environmental factors does the user mention in their journal that influence their mental well-being, and what motivational drivers or barriers to change have they identified?",

    # Summary and Synthesis
    "Provide a comprehensive summary that synthesizes the key insights from the user's entire journal, integrating information about their activities, emotions, progress, coping strategies, patterns, and goals."
]

fixed_response_list=[]

### for the main conversation agent, run the dynamic_Response that is the relevance query first, so that cache is created only once.

with ThreadPoolExecutor() as executor:
    results = executor.map(journal_context_provider_agent,journal_queries)
    for result in results:
        print(result)
        fixed_response_list.append(result)