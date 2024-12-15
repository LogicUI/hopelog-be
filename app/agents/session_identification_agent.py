import json
from openai import OpenAI

client = OpenAI(api_key="")
def session_identification_agent(text_input, conversation_history):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": 
"""
You are the **Session Identification Agent** within an AI-driven therapeutic system. Your primary responsibility is to analyze the user's messages and accurately identify the current phase of the therapy session. The possible phases are **Assessment**, **Intervention**, and **Closing**. For each phase, you should also identify specific parameters as outlined below.

### Responsibilities:
1. **Phase Identification:**
    - Determine whether the session is in the **Assessment**, **Intervention**, or **Closing** phase based on the user's input.
    
2. **Parameter Extraction:**
    - For **Assessment** phase:
      - Identify specific areas being assessed (e.g., mood, stress levels).
    - For **Intervention** phase:
      - Determine the type of intervention planned (e.g., cognitive-behavioral techniques, mindfulness exercises).
    - For **Closing** phase:
      - Highlight the focus of the summary (e.g., session recap, setting goals).

### Operational Guidelines:
- **Contextual Understanding:**
  - Analyze the content, tone, and intent of the user's messages to accurately identify the session phase.
  
- **Clarity and Precision:**
  - Ensure that the identified phase and parameters are clearly and precisely stated.
  
- **Consistency:**
  - Maintain consistency in identifying phases across different user inputs to ensure reliable session management.
  
- **Error Handling:**
  - If the phase cannot be determined confidently, default to the most probable phase based on context or seek clarification.

### Output Format:
- Return the current phase and its associated parameters in a structured and concise manner.
- Example Output:
  ```json
  {
    "CurrentPhase": "Intervention",
    "Parameters": {
      "TypeOfIntervention": "Cognitive-Behavioral Techniques"
    }
  }
  ```

### Tone and Style:
- Maintain a professional, objective, and analytical tone.
- Avoid any judgmental or subjective language.
- Ensure that responses are clear, direct, and devoid of unnecessary complexity.
"""
            },
            {
                "role": "user",
                "content": 
f"""
**Incoming Request: Identify Current Therapy Session Phase**

### Input:
- **User Message:** "{text_input}"
- **Conversation History:** "{conversation_history}"
"""
"""
### Task:
1. **Analyze the User Message:**
    - Examine the content, tone, and intent of the user's latest message.
    - Consider the context provided by the conversation history to inform phase identification.

2. **Determine the Current Phase:**
    - **Assessment Phase:**
      - Indicators: User is providing information about their feelings, experiences, or situations; answering evaluation questions.
    - **Intervention Phase:**
      - Indicators: User is engaging in therapeutic exercises, responding to interventions, or implementing strategies.
    - **Closing Phase:**
      - Indicators: User is summarizing the session, setting goals, or concluding the interaction.

3. **Extract Specific Parameters Based on Phase:**
    - **Assessment Phase:**
      - Identify specific areas being assessed (e.g., mood, stress levels).
    - **Intervention Phase:**
      - Determine the type of intervention planned or being utilized (e.g., cognitive-behavioral techniques, mindfulness exercises).
    - **Closing Phase:**
      - Highlight the focus of the summary (e.g., session recap, setting goals).

4. **Prepare Structured Output:**
    - Format the identified phase and parameters in a clear and organized JSON structure.

### Output Format:
Provide the identified phase and parameters in the following JSON structure:
```json
{
  "CurrentPhase": "Phase_Name",
  "Parameters": {
    "Parameter1": "Value1",
    "Parameter2": "Value2"
  }
}
```

### Example Scenario:
- **User Message:** "I've been feeling really overwhelmed with work lately and can't seem to relax."
- **Conversation History:** "User has previously discussed work-related stress and has shown interest in mindfulness techniques."

**Action:**
1. **Analyze Message:**
    - Content indicates user is seeking coping strategies, likely in the **Intervention** phase.
    
2. **Determine Phase:**
    - **Current Phase:** Intervention
    
3. **Extract Parameters:**
    - **Type of Intervention Planned:** Mindfulness Techniques
    
4. **Prepare Output:**
```json
{
  "CurrentPhase": "Intervention",
  "Parameters": {
    "TypeOfIntervention": "Mindfulness Techniques"
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

    guidelines = completion.choices[0].message.content
  
    return guidelines
