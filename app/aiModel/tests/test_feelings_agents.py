import pytest
from app.aiModel.ai_therapist import feelings_analysis_agent
from app.aiModel.filter_model import is_greeting


@pytest.mark.asyncio
async def test_feelings_analysis():
    # Test conversation history
    conversation_history = [
        {"user": "I'm feeling really sad and overwhelmed today"},
        {
            "therapist": "I hear that you're feeling sad and overwhelmed. Would you like to talk more about what's causing these feelings?"
        },
    ]

    # Call the feelings analysis agent
    result = await feelings_analysis_agent(conversation_history)

    # Assert results
    assert isinstance(result, dict), "Result should be a dictionary"
    assert "emotions" in result, "Result should contain emotions"
    assert len(result["emotions"]) <= 5, "Too many emotions detected"
    assert any(
        emotion["emotion"] == "Sadness" for emotion in result["emotions"]
    ), "Sadness not detected"
    assert not is_greeting(
        conversation_history[0]["user"]
    ), "Incorrectly detected as greeting"


@pytest.mark.asyncio
async def test_feelings_analysis_edge_cases():
    # Test conversation with multiple emotions
    conversation_history = [
        {"user": "I'm feeling angry and frustrated with my job"},
        {
            "therapist": "That sounds difficult. Can you tell me more about what's making you angry?"
        },
        {
            "user": "I'm scared I'll lose my position but also hopeful about new opportunities"
        },
        {"therapist": "It's natural to feel both fear and hope in such situations."},
        {
            "user": "Yes, I'm surprised by how optimistic I still feel despite everything"
        },
        {"therapist": "That shows great resilience."},
        {"user": "I trust things will work out but feel guilty about wanting to leave"},
        {"therapist": "Those are very complex emotions you're experiencing."},
    ]

    result = await feelings_analysis_agent(conversation_history)

    # Verify only top 5 emotions are returned despite more being present
    assert len(result["emotions"]) == 5, "Should only return top 5 emotions"

    # Verify structure of each emotion
    for emotion in result["emotions"]:
        assert "emotion" in emotion, "Each emotion should have an emotion type"
        assert "intensity" in emotion, "Each emotion should have an intensity"
        assert "evidence" in emotion, "Each emotion should have evidence"
        assert 0 <= emotion["intensity"] <= 1, "Intensity should be between 0 and 1"


@pytest.mark.asyncio
async def test_feelings_analysis_expected_output():
    conversation_history = [
        {"user": "I'm feeling very sad today, just completely devastated"},
        {"therapist": "I hear how deeply sad you're feeling. What happened?"},
        {"user": "I lost my job and I'm scared about the future"},
    ]

    result = await feelings_analysis_agent(conversation_history)

    # Assert structure
    assert "emotions" in result, "Result should contain emotions"
    assert len(result["emotions"]) >= 3, "Should detect at least 3 emotions"

    # Find emotions in result
    sadness = next((e for e in result["emotions"] if e["emotion"] == "Sadness"), None)
    fear = next((e for e in result["emotions"] if e["emotion"] == "Fear"), None)
    disappointment = next(
        (e for e in result["emotions"] if e["emotion"] == "Disappointment"), None
    )

    # Assert presence and intensity ranges
    assert sadness is not None, "Should detect Sadness"
    assert fear is not None, "Should detect Fear"
    assert disappointment is not None, "Should detect Disappointment"

    # Check intensity ranges with tolerance
    assert (
        0.8 <= sadness["intensity"] <= 1.0
    ), "Sadness should have high intensity (0.8-1.0)"
    assert (
        0.6 <= fear["intensity"] <= 0.8
    ), "Fear should have medium-high intensity (0.6-0.8)"
    assert (
        0.5 <= disappointment["intensity"] <= 0.7
    ), "Disappointment should have medium intensity (0.5-0.7)"

    # Verify relative ordering
    assert (
        sadness["intensity"] > fear["intensity"]
    ), "Sadness should be more intense than Fear"
    assert (
        fear["intensity"] > disappointment["intensity"]
    ), "Fear should be more intense than Disappointment"
