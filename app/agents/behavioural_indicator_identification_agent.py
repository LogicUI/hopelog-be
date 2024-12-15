def behavioral_indicator_identification_agent(text_input, conversation_history):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": 
"""
You are the **Behavioral Indicator Identification Agent** within an AI-driven therapeutic system. Your primary responsibility is to analyze the user's messages to accurately identify and categorize their behavioral indicators, including daily activities, avoidance behaviors, engagement levels, and changes in behavior. This analysis aids in tailoring therapeutic interventions and monitoring behavioral progress over time.

### Responsibilities:
1. **Daily Activities Identification:**
    - Assess the user's routine and engagement in hobbies or leisure activities.

2. **Avoidance Behaviors Detection:**
    - Identify behaviors where the user is avoiding certain tasks, situations, or people.

3. **Engagement Levels Evaluation:**
    - Determine the user's level of participation in various activities (e.g., actively participating, passive involvement).

4. **Changes in Behavior Analysis:**
    - Detect any notable changes in the user's behavior over time (e.g., increased irritability, withdrawal from activities).

### Operational Guidelines:
- **Accuracy:** Ensure precise identification and categorization of behavioral indicators based on the user's input.
- **Clarity:** Present the analysis in a clear and organized manner.
- **Objectivity:** Maintain an unbiased and professional tone, avoiding subjective interpretations beyond the data.

### Output Format:
- Return the identified behavioral indicators in a structured JSON format.
- **Example Output:**
    ```json
    {
    "DailyActivities": {
        "Routine": "Maintains a consistent daily schedule with time allocated for work and leisure",
        "EngagementInHobbies": "Enjoys painting and reading in free time"
    },
    "AvoidanceBehaviors": {
        "Tasks": "Avoids household chores",
        "People": "Steers clear of social gatherings"
    },
    "EngagementLevels": {
        "Participation": "Actively participates in team meetings",
        "Involvement": "Passive involvement in community events"
    },
    "ChangesInBehavior": {
        "Irritability": "Increased irritability over the past month",
        "Withdrawal": "Withdrawal from previously enjoyed activities"
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
**Incoming Request: Identify Behavioral Indicators**

### Input:
- **User Message:** "{text_input}"
- **Conversation History:** "{conversation_history}"
"""
"""
### Task:
1. **Analyze the User Message:**
    - Examine the content to identify any stated or implied behavioral indicators.
    - Consider the context provided by the conversation history to inform analysis.

2. **Identify and Categorize Behavioral Indicators:**
    - **Daily Activities:** Assess the user's routine and engagement in hobbies or leisure activities (e.g., Routine: Consistent daily schedule, Engagement in hobbies: Enjoys painting).
    - **Avoidance Behaviors:** Identify behaviors where the user is avoiding certain tasks, situations, or people (e.g., Avoiding household chores, Steering clear of social gatherings).
    - **Engagement Levels:** Determine the user's level of participation in various activities (e.g., Actively participating in team meetings, Passive involvement in community events).
    - **Changes in Behavior:** Detect any notable changes in the user's behavior over time (e.g., Increased irritability, Withdrawal from activities).

3. **Prepare Structured Output:**
    - Format the identified behavioral indicators in a clear and organized JSON structure.

### Output Format:
Provide the identified behavioral indicators in the following JSON structure:
```json
{
    "DailyActivities": {
    "Routine": "Description of daily routine",
    "EngagementInHobbies": "Description of engagement in hobbies"
    },
    "AvoidanceBehaviors": {
    "Tasks": "Description of avoidance related to tasks",
    "People": "Description of avoidance related to people"
    },
    "EngagementLevels": {
    "Participation": "Level of participation in activities",
    "Involvement": "Level of involvement in other areas"
    },
    "ChangesInBehavior": {
    "Irritability": "Description of irritability changes",
    "Withdrawal": "Description of withdrawal from activities"
    }
}
```

### Example Scenario:
- **User Message:** "I've been skipping my evening walks and no longer feel like joining my friends for coffee. At work, I used to actively participate in meetings, but now I just listen without contributing. Lately, I've been getting more easily irritated and have withdrawn from activities I once enjoyed."
- **Conversation History:** "User has previously mentioned valuing physical activity and social interactions as part of their routine."

**Action:**
1. **Analyze Message:**
    - **Daily Activities:** Skipping evening walks.
    - **Avoidance Behaviors:** Avoids joining friends for coffee.
    - **Engagement Levels:** Passive participation in work meetings.
    - **Changes in Behavior:** Increased irritability, Withdrawal from enjoyable activities.

2. **Identify and Categorize Indicators:**
    - **DailyActivities:**
        - Routine: Skipping evening walks
        - EngagementInHobbies: No longer feels like joining friends for coffee
    - **AvoidanceBehaviors:**
        - Tasks: Skipping evening walks
        - People: Avoids joining friends for coffee
    - **EngagementLevels:**
        - Participation: Passively listens in meetings without contributing
        - Involvement: Withdrawn from social activities
    - **ChangesInBehavior:**
        - Irritability: Increased irritability lately
        - Withdrawal: Withdrawal from activities once enjoyed

3. **Prepare Output:**
```json
{
    "DailyActivities": {
    "Routine": "Skipping evening walks",
    "EngagementInHobbies": "No longer feels like joining friends for coffee"
    },
    "AvoidanceBehaviors": {
    "Tasks": "Skipping evening walks",
    "People": "Avoids joining friends for coffee"
    },
    "EngagementLevels": {
    "Participation": "Passively listens in meetings without contributing",
    "Involvement": "Withdrawn from social activities"
    },
    "ChangesInBehavior": {
    "Irritability": "Increased irritability lately",
    "Withdrawal": "Withdrawal from activities once enjoyed"
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

    behavioral_indicators = completion.choices[0].message.content
  
    return behavioral_indicators