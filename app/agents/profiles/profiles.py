def create_user_profile(
    age: int,
    gender_identity: str,
    occupation: str,
    education_level: str,
    cultural_background: str,
    language_preferences: str,
    relationship_status: str
) -> dict:
    """
    Creates a user profile dictionary based on provided demographic information.

    Parameters:
    - age (int): The user's age.
    - gender_identity (str): The user's gender identity.
    - occupation (str): The user's occupation.
    - education_level (str): The user's education level.
    - cultural_background (str): The user's cultural background.
    - language_preferences (str): A list of languages the user prefers.
    - relationship_status (str): The user's relationship status.

    Returns:
    - dict: A dictionary containing the user profile information.
    """
    user_profile = {
        "Age": age,
        "GenderIdentity": gender_identity,
        "Occupation": occupation,
        "EducationLevel": education_level,
        "CulturalBackground": cultural_background,
        "LanguagePreferences": language_preferences,
        "RelationshipStatus": relationship_status
    }
    return user_profile
