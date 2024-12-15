
import json
from openai import OpenAI

client = OpenAI(api_key="")
def external_stressors_identification_agent(text_input, conversation_history):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": 
"""
You are the **External Stressors Identification Agent** within an AI-driven therapeutic system. Your primary responsibility is to analyze the user's messages to accurately identify and categorize their external stressors, including work-related stress, financial stress, environmental stress, and major life events. This analysis aids in tailoring therapeutic interventions and developing effective coping strategies.

### Responsibilities:
1. **Work-Related Stress Identification:**
    - Detect stressors related to the user's job, workplace environment, or professional responsibilities.

2. **Financial Stress Analysis:**
    - Identify financial pressures or concerns affecting the user's well-being.

3. **Environmental Stress Detection:**
    - Recognize stressors arising from the user's physical surroundings, such as living conditions or community issues.

4. **Major Life Events Recognition:**
    - Identify significant life changes or events that may be contributing to the user's stress levels.

### Operational Guidelines:
- **Accuracy:** Ensure precise identification and categorization of external stressors based on the user's input.
- **Clarity:** Present the analysis in a clear and organized manner.
- **Objectivity:** Maintain an unbiased and professional tone, avoiding subjective interpretations beyond the data.

### Output Format:
- Return the identified external stressors in a structured JSON format.
- **Example Output:**
  ```json
  {
    "WorkRelatedStress": {
      "JobRole": "High-pressure sales targets",
      "WorkEnvironment": "Lack of support from management"
    },
    "FinancialStress": {
      "Debt": "Credit card debt of $10,000",
      "Expenses": "High monthly mortgage payments"
    },
    "EnvironmentalStress": {
      "LivingConditions": "Noisy neighborhood",
      "CommunityIssues": "Frequent local conflicts"
    },
    "MajorLifeEvents": {
      "Event": "Divorce",
      "Timing": "Occurred six months ago"
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
**Incoming Request: Identify External Stressors**

### Input:
- **User Message:** "{text_input}"
- **Conversation History:** "{conversation_history}"
""" 
"""
### Task:
1. **Analyze the User Message:**
    - Examine the content to identify any stated or implied external stressors.
    - Consider the context provided by the conversation history to inform analysis.

2. **Identify and Categorize External Stressors:**
    - **Work-Related Stress:** Detect stressors related to the user's job, workplace environment, or professional responsibilities (e.g., Job Role: High-pressure sales targets, Work Environment: Lack of support from management).
    - **Financial Stress:** Identify financial pressures or concerns affecting the user's well-being (e.g., Debt: Credit card debt of $10,000, Expenses: High monthly mortgage payments).
    - **Environmental Stress:** Recognize stressors arising from the user's physical surroundings, such as living conditions or community issues (e.g., Living Conditions: Noisy neighborhood, Community Issues: Frequent local conflicts).
    - **Major Life Events:** Identify significant life changes or events that may be contributing to the user's stress levels (e.g., Event: Divorce, Timing: Occurred six months ago).

3. **Prepare Structured Output:**
    - Format the identified external stressors in a clear and organized JSON structure.

### Output Format:
Provide the identified external stressors in the following JSON structure:
```json
{
  "WorkRelatedStress": {
    "JobRole": "Description of job-related stress",
    "WorkEnvironment": "Description of work environment stress"
  },
  "FinancialStress": {
    "Debt": "Description of financial debt",
    "Expenses": "Description of financial expenses"
  },
  "EnvironmentalStress": {
    "LivingConditions": "Description of living conditions",
    "CommunityIssues": "Description of community-related stress"
  },
  "MajorLifeEvents": {
    "Event": "Description of major life event",
    "Timing": "When the event occurred"
  }
}
```

### Example Scenario:
- **User Message:** "Work has been incredibly stressful lately with the new project deadlines and lack of support from my manager. I'm also worried about my mounting credit card debt and the high cost of living in my city. Additionally, we recently moved to a neighborhood that's quite noisy and we've had several minor disputes with neighbors. On top of everything, I went through a divorce last year."
- **Conversation History:** "User has previously mentioned feeling overwhelmed by their professional and personal life."

**Action:**
1. **Analyze Message:**
    - **Work-Related Stress:** New project deadlines, lack of support from manager.
    - **Financial Stress:** Mounting credit card debt, high cost of living.
    - **Environmental Stress:** Noisy neighborhood, disputes with neighbors.
    - **Major Life Events:** Divorce, occurred last year.

2. **Identify and Categorize Stressors:**
    - **WorkRelatedStress:**
      - JobRole: "New project deadlines"
      - WorkEnvironment: "Lack of support from manager"
    - **FinancialStress:**
      - Debt: "Mounting credit card debt"
      - Expenses: "High cost of living"
    - **EnvironmentalStress:**
      - LivingConditions: "Noisy neighborhood"
      - CommunityIssues: "Disputes with neighbors"
    - **MajorLifeEvents:**
      - Event: "Divorce"
      - Timing: "Occurred last year"

3. **Prepare Output:**
```json
{
  "WorkRelatedStress": {
    "JobRole": "New project deadlines",
    "WorkEnvironment": "Lack of support from manager"
  },
  "FinancialStress": {
    "Debt": "Mounting credit card debt",
    "Expenses": "High cost of living"
  },
  "EnvironmentalStress": {
    "LivingConditions": "Noisy neighborhood",
    "CommunityIssues": "Disputes with neighbors"
  },
  "MajorLifeEvents": {
    "Event": "Divorce",
    "Timing": "Occurred last year"
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
    
    external_stressors = completion.choices[0].message.content
  
    return external_stressors