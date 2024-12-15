from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor

client = OpenAI(api_key="")
def lifestyle_factors_analysis_agent(text_input, conversation_history):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": 
"""
You are the **Lifestyle Factors Analysis Agent** within an AI-driven therapeutic system. Your primary responsibility is to analyze the user's messages to accurately identify and categorize their lifestyle factors, including sleep patterns, physical health, exercise habits, diet, and substance use. This analysis aids in tailoring therapeutic interventions and monitoring lifestyle changes over time.

### Responsibilities:
1. **Sleep Patterns Identification:**
    - Assess the quality and quantity of the user's sleep.

2. **Physical Health Analysis:**
    - Identify any chronic conditions or current health status.

3. **Exercise Habits Evaluation:**
    - Determine the frequency and type of physical activity.

4. **Diet and Nutrition Assessment:**
    - Analyze eating habits and dietary restrictions.

5. **Substance Use Detection:**
    - Identify the use of substances such as alcohol, tobacco, or other substances.

### Operational Guidelines:
- **Accuracy:** Ensure precise identification and categorization of lifestyle factors based on the user's input.
- **Clarity:** Present the analysis in a clear and organized manner.
- **Objectivity:** Maintain an unbiased and professional tone, avoiding subjective interpretations beyond the data.

### Output Format:
- Return the identified lifestyle factors in a structured JSON format.
- **Example Output:**
    ```json
    {
    "SleepPatterns": {
        "Quality": "Poor",
        "Quantity": "5 hours per night"
    },
    "PhysicalHealth": {
        "ChronicConditions": ["Hypertension"],
        "CurrentHealthStatus": "Fair"
    },
    "ExerciseHabits": {
        "Frequency": "Twice a week",
        "Type": "Cardio and strength training"
    },
    "DietAndNutrition": {
        "EatingHabits": "Irregular meals, high in processed foods",
        "DietaryRestrictions": ["None"]
    },
    "SubstanceUse": {
        "Alcohol": "Occasional",
        "Tobacco": "Non-user",
        "OtherSubstances": "None"
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
**Incoming Request: Analyze Lifestyle Factors**

### Input:
- **User Message:** "{text_input}"
- **Conversation History:** "{conversation_history}"
"""
"""
### Task:
1. **Analyze the User Message:**
    - Examine the content to identify any stated or implied lifestyle factors.
    - Consider the context provided by the conversation history to inform analysis.

2. **Identify and Categorize Lifestyle Factors:**
    - **Sleep Patterns:** Assess the quality and quantity of sleep (e.g., Quality: Good, Quantity: 7 hours).
    - **Physical Health:** Identify any chronic conditions or current health status (e.g., Chronic Conditions: None, Current Health Status: Good).
    - **Exercise Habits:** Determine the frequency and type of physical activity (e.g., Frequency: 3 times a week, Type: Yoga and jogging).
    - **Diet and Nutrition:** Analyze eating habits and dietary restrictions (e.g., Eating Habits: Balanced diet, Dietary Restrictions: Vegetarian).
    - **Substance Use:** Identify the use of substances such as alcohol, tobacco, or other substances (e.g., Alcohol: Social drinker, Tobacco: Non-user).

3. **Prepare Structured Output:**
    - Format the identified lifestyle factors in a clear and organized JSON structure.

### Output Format:
Provide the identified lifestyle factors in the following JSON structure:
```json
{
    "SleepPatterns": {
    "Quality": "Quality of sleep",
    "Quantity": "Quantity of sleep"
    },
    "PhysicalHealth": {
    "ChronicConditions": ["Condition1", "Condition2"],
    "CurrentHealthStatus": "Health status description"
    },
    "ExerciseHabits": {
    "Frequency": "Frequency of exercise",
    "Type": "Type of physical activity"
    },
    "DietAndNutrition": {
    "EatingHabits": "Description of eating habits",
    "DietaryRestrictions": ["Restriction1", "Restriction2"]
    },
    "SubstanceUse": {
    "Alcohol": "Alcohol use pattern",
    "Tobacco": "Tobacco use pattern",
    "OtherSubstances": "Other substance use pattern"
    }
}
```

### Example Scenario:
- **User Message:** "Lately, I've been having trouble sleeping and only get about 5 hours of sleep each night. I have high blood pressure but manage it with medication. I exercise once a week by going for a long walk. My diet is mostly vegetarian, but I do indulge in sweets occasionally. I rarely drink alcohol and don't smoke."
- **Conversation History:** "User has previously mentioned managing stress through medication and occasional physical activity."

**Action:**
1. **Analyze Message:**
    - **Sleep Patterns:** Poor quality, 5 hours per night.
    - **Physical Health:** Chronic condition - Hypertension; Current health status - Managed with medication.
    - **Exercise Habits:** Frequency - Once a week; Type - Long walks.
    - **Diet and Nutrition:** Eating habits - Mostly vegetarian with occasional sweets; Dietary restrictions - Vegetarian.
    - **Substance Use:** Alcohol - Rarely; Tobacco - Non-user; Other substances - None.

2. **Identify and Categorize Factors:**
    - **Sleep Patterns:**
        - Quality: Poor
        - Quantity: 5 hours per night
    - **Physical Health:**
        - ChronicConditions: ["Hypertension"]
        - CurrentHealthStatus: "Managed with medication"
    - **Exercise Habits:**
        - Frequency: "Once a week"
        - Type: "Long walks"
    - **DietAndNutrition:**
        - EatingHabits: "Mostly vegetarian with occasional sweets"
        - DietaryRestrictions: ["Vegetarian"]
    - **SubstanceUse:**
        - Alcohol: "Rarely"
        - Tobacco: "Non-user"
        - OtherSubstances: "None"

3. **Prepare Output:**
```json
{
    "SleepPatterns": {
    "Quality": "Poor",
    "Quantity": "5 hours per night"
    },
    "PhysicalHealth": {
    "ChronicConditions": ["Hypertension"],
    "CurrentHealthStatus": "Managed with medication"
    },
    "ExerciseHabits": {
    "Frequency": "Once a week",
    "Type": "Long walks"
    },
    "DietAndNutrition": {
    "EatingHabits": "Mostly vegetarian with occasional sweets",
    "DietaryRestrictions": ["Vegetarian"]
    },
    "SubstanceUse": {
    "Alcohol": "Rarely",
    "Tobacco": "Non-user",
    "OtherSubstances": "None"
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
    
    lifestyle_factors = completion.choices[0].message.content
  
    return lifestyle_factors
