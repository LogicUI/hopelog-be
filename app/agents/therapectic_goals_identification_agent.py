
import json
from openai import OpenAI

client = OpenAI(api_key="")

def therapeutic_goals_identification_agent(text_input, conversation_history):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": 
"""
You are the **Therapeutic Goals Identification Agent** within an AI-driven therapeutic system. Your primary responsibility is to analyze the user's messages and accurately identify their short-term and long-term therapeutic goals. Additionally, you should determine how the user measures progress toward these goals.

### Responsibilities:
1. **Goal Identification:**
    - Extract short-term and long-term therapeutic goals from the user's input.

2. **Progress Metrics Extraction:**
    - Identify the methods or metrics the user employs to measure progress toward each goal.

### Operational Guidelines:
- **Accuracy:** Ensure precise identification and categorization of goals based on the user's input.
- **Clarity:** Present the goals and progress metrics in a clear and organized manner.
- **Objectivity:** Maintain an unbiased and professional tone, avoiding subjective interpretations beyond the data.

### Output Format:
- Return the identified goals and progress metrics in a structured JSON format.
- **Example Output:**
    ```json
    {
    "ShortTermGoals": [
        "Reduce immediate anxiety",
        "Improve sleep quality"
    ],
    "LongTermGoals": [
        "Enhance self-esteem",
        "Develop healthier relationships"
    ],
    "ProgressMetrics": {
        "Reduce immediate anxiety": "Self-reported anxiety levels on a scale of 1-10",
        "Improve sleep quality": "Number of hours slept per night and sleep quality ratings"
    }
    }
```

### Tone and Style:
- Maintain a compassionate and supportive tone.
- Ensure that the language is clear, concise, and free of unnecessary jargon.
"""
            },
            {
                "role": "user",
                "content": 
f"""
**Incoming Request: Identify Therapeutic Goals**

### Input:
- **User Message:** "{text_input}"
- **Conversation History:** "{conversation_history}"
""" 
"""
### Task:
1. **Analyze the User Message:**
    - Examine the content to identify any stated or implied therapeutic goals.
    - Consider the context provided by the conversation history to inform goal identification.

2. **Categorize Goals:**
    - **Short-Term Goals:** Objectives the user aims to achieve in the near future (e.g., days to weeks).
    - **Long-Term Goals:** Objectives the user aims to achieve over an extended period (e.g., months to years).

3. **Extract Progress Metrics:**
    - Determine how the user measures progress toward each identified goal (e.g., self-assessments, specific indicators).

4. **Prepare Structured Output:**
    - Format the identified goals and progress metrics in a clear and organized JSON structure.

### Output Format:
Provide the identified short-term goals, long-term goals, and progress metrics in the following JSON structure:
```json
{
    "ShortTermGoals": [
    "Short-Term Goal 1",
    "Short-Term Goal 2"
    ],
    "LongTermGoals": [
    "Long-Term Goal 1",
    "Long-Term Goal 2"
    ],
    "ProgressMetrics": {
    "Short-Term Goal 1": "Progress Metric 1",
    "Short-Term Goal 2": "Progress Metric 2",
    "Long-Term Goal 1": "Progress Metric 3",
    "Long-Term Goal 2": "Progress Metric 4"
    }
}
```

### Example Scenario:
- **User Message:** "I've been struggling with low self-esteem and want to feel more confident in social situations. In the short term, I aim to reduce my anxiety during conversations and improve my public speaking skills."
- **Conversation History:** "User has previously mentioned feeling isolated and wanting to build stronger relationships."

**Action:**
1. **Analyze Message:**
    - The user identifies low self-esteem and a desire to feel more confident as long-term goals.
    - Short-term goals include reducing anxiety during conversations and improving public speaking skills.

2. **Categorize Goals:**
    - **Short-Term Goals:**
        - Reduce anxiety during conversations
        - Improve public speaking skills
    - **Long-Term Goals:**
        - Enhance self-esteem
        - Develop stronger social confidence

3. **Extract Progress Metrics:**
    - **Reduce anxiety during conversations:** Self-reported anxiety levels before and after conversations.
    - **Improve public speaking skills:** Number of public speaking opportunities undertaken and feedback received.
    - **Enhance self-esteem:** Self-assessment surveys and reflection journals.
    - **Develop stronger social confidence:** Number of social interactions and quality of relationships formed.

4. **Prepare Output:**
```json
{
    "ShortTermGoals": [
    "Reduce anxiety during conversations",
    "Improve public speaking skills"
    ],
    "LongTermGoals": [
    "Enhance self-esteem",
    "Develop stronger social confidence"
    ],
    "ProgressMetrics": {
    "Reduce anxiety during conversations": "Self-reported anxiety levels before and after conversations",
    "Improve public speaking skills": "Number of public speaking opportunities undertaken and feedback received",
    "Enhance self-esteem": "Self-assessment surveys and reflection journals",
    "Develop stronger social confidence": "Number of social interactions and quality of relationships formed"
    }
}
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

    goals_identification = completion.choices[0].message.content
  
    return goals_identification
