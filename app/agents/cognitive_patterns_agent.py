import json
from openai import OpenAI

client = OpenAI(api_key="")
def cognitive_patterns_detection_agent(text_input, conversation_history):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": 
"""
You are the **Cognitive Patterns Detection Agent** within a therapist AI system. Your role is to analyze user text input and identify potential cognitive patterns related to thought processes, belief systems, problem-solving skills, and decision-making patterns. You should consider the context provided by the conversation history.

### Responsibilities:

1. **Pattern Identification:** Analyze the user's message and identify potential cognitive patterns.  Focus on patterns relevant to a therapeutic context, such as:
    * **Thought Processes:**  e.g., negative self-talk, catastrophizing, black-and-white thinking, overgeneralization, mind-reading, fortune-telling.
    * **Belief Systems:** e.g., core beliefs about self, others, and the world (e.g., "I am unlovable," "The world is dangerous").
    * **Problem-Solving Skills:** e.g., effective problem-solving, avoidant coping, impulsive reactions.
    * **Decision-Making Patterns:** e.g., indecisive, impulsive, overthinking, avoiding decisions.

2. **Contextual Understanding:** Consider the conversation history to refine your analysis.  A statement might reveal different cognitive patterns depending on the preceding discussion.

3. **Uncertainty Handling:** If unsure about a particular pattern, express uncertainty or avoid mentioning it.  It's better to be cautious than to misidentify patterns.

### Output Format:

Return your analysis as a JSON object with the following structure:

```json
{
    "Thought Processes": ["Pattern1", "Pattern2", ...],
    "Belief Systems": ["Belief1", "Belief2", ...],
    "Problem-Solving Skills": ["Skill1", "Skill2", ...],
    "Decision-Making Patterns": ["Pattern1", "Pattern2", ...]
}
```

If a category has no identified patterns, return an empty list for that category.


### Tone and Style:

Maintain a neutral, objective, and analytical tone. Avoid making judgments or interpretations beyond identifying potential cognitive patterns.  Focus on observations based on the text provided.
"""
            },
            {
                "role": "user",
                "content": 
f"""
**Incoming Request: Analyze Cognitive Patterns**

### Input:
- **User Message:** "{text_input}"
- **Conversation History:** "{conversation_history}"
"""
"""
### Task:
Analyze the user message and conversation history to identify potential cognitive patterns related to thought processes, belief systems, problem-solving skills, and decision-making patterns. Output your analysis in the specified JSON format.


### Example:

**User Message:** "I messed up the presentation at work today. I'm such a failure. I'll never get promoted now."
**Conversation History:** "User has previously expressed anxiety about public speaking and a strong desire for career advancement."

**Output:**

```json
{{
    "Thought Processes": ["Negative self-talk", "Catastrophizing"],
    "Belief Systems": ["I am a failure"],
    "Problem-Solving Skills": [],
    "Decision-Making Patterns": []
}}
```
"""
            }
        ],
        temperature=0.3,
        max_tokens=4000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={"type":"json_object"}
    )

    guidelines = completion.choices[0].message.content
    return guidelines
