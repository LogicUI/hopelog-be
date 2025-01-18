from pydantic import BaseModel, Field
from typing import List


class EmotionScore(BaseModel):
    emotion: str = Field(
        description="Type of emotion detected",
        pattern="^(Joy|Trust|Fear|Surprise|Sadness|Disgust|Anger|Anticipation|Love|Optimism|Disappointment|Remorse|Aggressiveness|Submission|Contempt|Awe|Guilt|Envy|Pride|Anxiety|Hope)$",
    )
    intensity: float = Field(
        description="Intensity score of the emotion", ge=0.0, le=1.0
    )
    evidence: str = Field(description="Supporting quote from conversation")


class EmotionalState(BaseModel):
    emotions: List[EmotionScore] = Field(
        description="Top 5 detected emotions with scores", max_length=5
    )
