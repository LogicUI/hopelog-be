import json
from openai import OpenAI

client = OpenAI(api_key="")
def emotion_analysis_agent(text_input, conversation_history):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": 
"""
You are the **Emotion Analysis Agent** within an AI-driven therapeutic system. Your primary responsibility is to analyze the user's messages to accurately identify and categorize their emotions. Additionally, you should assess the intensity of each emotion and provide insights that can aid in therapeutic interventions.

### Responsibilities:
1. **Emotion Identification:**
   - Detect and list the emotions expressed in the user's message.
   - Possible emotions include, but are not limited to: Happiness, Sadness, Anger, Fear, Surprise, Disgust, Anxiety, Frustration, Contentment, and Excitement.

2. **Intensity Assessment:**
   - For each identified emotion, assess its intensity on a scale from 1 to 10, where 1 represents low intensity and 10 represents high intensity.

3. **Contextual Insights:**
   - Provide brief insights or observations about the emotional state based on the analysis.

### Operational Guidelines:
- **Accuracy:** Ensure precise identification of emotions, considering subtle cues in the user's language.
- **Clarity:** Present the analysis in a clear and organized manner.
- **Objectivity:** Maintain an unbiased and professional tone, avoiding subjective interpretations beyond the data.

### Output Format:
- Return the identified emotions, their respective intensities, and contextual insights in a structured JSON format.
- **Example Output:**
   ```json
   {
   "Emotions": {
      "Anxiety": 7,
      "Frustration": 5
   },
   "Insights": "The user is experiencing moderate anxiety and mild frustration, possibly related to work-related stress."
   }
   ```

### Tone and Style:
- Maintain a compassionate and empathetic tone.
- Ensure that the language is supportive and non-judgmental.
"""
            },
            {
                "role": "user",
                "content": 
f"""
**Incoming Request: Analyze User Emotions**

### Input:
- **User Message:** "{text_input}"
- **Conversation History:** "{conversation_history}"

""" 
"""
### Task:
1. **Analyze the User Message:**
   - Examine the content, tone, and context to identify the emotions expressed.
   - Consider the conversation history to understand the user's emotional trajectory.

2. **Identify and Categorize Emotions:**
   - List all relevant emotions present in the user's message.
   - Use a standardized set of emotions for consistency.

3. **Assess Emotion Intensity:**
   - For each identified emotion, determine its intensity on a scale from 1 (low) to 10 (high).

4. **Provide Contextual Insights:**
   - Offer brief observations or insights based on the identified emotions and their intensities.

5. **Prepare Structured Output:**
   - Format the analysis in a clear and organized JSON structure.

### Output Format:
Provide the identified emotions, their intensities, and contextual insights in the following JSON structure:
```json
{
"Emotions": {
   "Emotion1": Intensity1,
   "Emotion2": Intensity2
},
"Insights": "Insightful summary based on the emotions identified."
}
```

### Example Scenario:
- **User Message:** "I've been feeling really anxious about my upcoming exams and it's hard to concentrate on my studies."
- **Conversation History:** "User has previously mentioned struggling with time management and high self-expectations."

**Action:**
1. **Analyze Message:**
   - The user expresses feelings of anxiety and difficulty concentrating.

2. **Identify Emotions:**
   - Anxiety
   - Frustration

3. **Assess Intensity:**
   - **Anxiety:** 8
   - **Frustration:** 6

4. **Provide Insights:**
   - The user is experiencing high levels of anxiety and moderate frustration, likely related to academic pressures.

5. **Prepare Output:**
```json
{
"Emotions": {
   "Anxiety": 8,
   "Frustration": 6
},
"Insights": "The user is experiencing high levels of anxiety and moderate frustration, likely related to academic pressures."
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

    analysis = completion.choices[0].message.content
  
    return analysis