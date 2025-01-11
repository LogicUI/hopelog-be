import re
import random
import logging


def is_greeting(user_message):
    greeting_phrases = [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening",
        "hello there",
        "hey there",
        "what's up",
        "greetings",
    ]

    normalized_message = user_message.strip().lower()

    return any(
        re.search(rf"\b{phrase}\b", normalized_message) for phrase in greeting_phrases
    )


def check_toxic_words(user_message):
    toxic_words = [
        "2g1c",
        "2 girls 1 cup",
        "screw",
        "acrotomophilia",
        "alabama hot pocket",
        "alaskan pipeline",
        "anal",
        "anilingus",
        "anus",
        "apeshit",
        "arsehole",
        "ass",
        "asshole",
        "assmunch",
        "auto erotic",
        "autoerotic",
        "babeland",
        "baby batter",
        "baby juice",
        "ball gag",
        "ball gravy",
        "ball kicking",
        "ball licking",
        "ball sack",
        "ball sucking",
        "bangbros",
        "bangbus",
        "bareback",
        "barely legal",
        "barenaked",
        "bastard",
        "bastardo",
        "bastinado",
        "bbw",
        "bdsm",
        "beaner",
        "beaners",
        "beaver cleaver",
        "beaver lips",
        "beastiality",
        "bestiality",
        "big black",
        "big breasts",
        "big knockers",
        "big tits",
        "bimbos",
        "birdlock",
        "bitch",
        "bitches",
        "black cock",
        "blonde action",
        "blonde on blonde action",
        "blowjob",
        "blow job",
        "blow your load",
        "blue waffle",
        "blumpkin",
        "bollocks",
        "bondage",
        "boner",
        "boob",
        "boobs",
        "booty call",
        "brown showers",
        "brunette action",
        "bukkake",
        "bulldyke",
        "bullet vibe",
        "bullshit",
        "bung hole",
        "bunghole",
        "busty",
        "butt",
        "buttcheeks",
        "butthole",
        "camel toe",
        "camgirl",
        "camslut",
        "camwhore",
        "carpet muncher",
        "carpetmuncher",
        "chocolate rosebuds",
        "cialis",
        "circlejerk",
        "cleveland steamer",
        "clit",
        "clitoris",
        "clover clamps",
        "clusterfuck",
        "cock",
        "cocks",
        "coprolagnia",
        "coprophilia",
        "cornhole",
        "coon",
        "coons",
        "creampie",
        "cum",
        "cumming",
        "cumshot",
        "cumshots",
        "cunnilingus",
        "cunt",
        "darkie",
        "date rape",
        "daterape",
        "deep throat",
        "deepthroat",
        "dendrophilia",
        "dick",
        "dildo",
        "dingleberry",
        "dingleberries",
        "dirty pillows",
        "dirty sanchez",
        "doggie style",
        "doggiestyle",
        "doggy style",
        "doggystyle",
        "dog style",
        "dolcett",
        "domination",
        "dominatrix",
        "dommes",
        "donkey punch",
        "double dong",
        "double penetration",
        "dp action",
        "dry hump",
        "dvda",
        "eat my ass",
        "ecchi",
        "ejaculation",
        "erotic",
        "erotism",
        "escort",
        "eunuch",
        "fag",
        "faggot",
        "fecal",
        "felch",
        "fellatio",
        "feltch",
        "female squirting",
        "femdom",
        "figging",
        "fingerbang",
        "fingering",
        "fisting",
        "foot fetish",
        "footjob",
        "frotting",
        "fuck",
        "fuck buttons",
        "fuckin",
        "fucking",
        "fucktards",
        "fudge packer",
        "fudgepacker",
        "futanari",
        "gangbang",
        "gang bang",
        "gay sex",
        "genitals",
        "giant cock",
        "girl on",
        "girl on top",
        "girls gone wild",
        "goatcx",
        "goatse",
        "god damn",
        "gokkun",
        "golden shower",
        "goodpoop",
        "goo girl",
        "goregasm",
        "grope",
        "group sex",
        "g-spot",
        "guro",
        "hand job",
        "handjob",
        "hard core",
        "hardcore",
        "hentai",
        "homoerotic",
        "honkey",
        "hooker",
        "horny",
        "hot carl",
        "hot chick",
        "how to kill",
        "how to murder",
        "huge fat",
        "humping",
        "incest",
        "intercourse",
        "jack off",
        "jail bait",
        "jailbait",
        "jelly donut",
        "jerk off",
        "jigaboo",
        "jiggaboo",
        "jiggerboo",
        "jizz",
        "juggs",
        "kike",
        "kinbaku",
        "kinkster",
        "kinky",
        "knobbing",
        "leather restraint",
        "leather straight jacket",
        "lemon party",
        "livesex",
        "lolita",
        "lovemaking",
        "make me come",
        "male squirting",
        "masturbate",
        "masturbating",
        "masturbation",
        "menage a trois",
        "milf",
        "missionary position",
        "mong",
        "motherfucker",
        "mound of venus",
        "mr hands",
        "muff diver",
        "muffdiving",
        "nambla",
        "nawashi",
        "negro",
        "neonazi",
        "nigga",
        "nigger",
        "nig nog",
        "nimphomania",
        "nipple",
        "nipples",
        "nsfw",
        "nsfw images",
        "nude",
        "nudity",
        "nutten",
        "nympho",
        "nymphomania",
        "octopussy",
        "omorashi",
        "one cup two girls",
        "one guy one jar",
        "orgasm",
        "orgy",
        "paedophile",
        "paki",
        "panties",
        "panty",
        "pedobear",
        "pedophile",
        "pegging",
        "penis",
        "phone sex",
        "piece of shit",
        "pikey",
        "pissing",
        "piss pig",
        "pisspig",
        "playboy",
        "pleasure chest",
        "pole smoker",
        "ponyplay",
        "poof",
        "poon",
        "poontang",
        "punany",
        "poop chute",
        "poopchute",
        "porn",
        "porno",
        "pornography",
        "prince albert piercing",
        "pthc",
        "pubes",
        "pussy",
        "queaf",
        "queef",
        "quim",
        "raghead",
        "raging boner",
        "rape",
        "raping",
        "rapist",
        "rectum",
        "reverse cowgirl",
        "rimjob",
        "rimming",
        "rosy palm",
        "rosy palm and her 5 sisters",
        "rusty trombone",
        "sadism",
        "santorum",
        "scat",
        "schlong",
        "scissoring",
        "semen",
        "sex",
        "sexcam",
        "sexo",
        "sexy",
        "sexual",
        "sexually",
        "sexuality",
        "shaved beaver",
        "shaved pussy",
        "shemale",
        "shibari",
        "shit",
        "shitblimp",
        "shitty",
        "shota",
        "shrimping",
        "skeet",
        "slanteye",
        "slut",
        "s&m",
        "smut",
        "snatch",
        "snowballing",
        "sodomize",
        "sodomy",
        "spastic",
        "spic",
        "splooge",
        "splooge moose",
        "spooge",
        "spread legs",
        "spunk",
        "strap on",
        "strapon",
        "strappado",
        "strip club",
        "style doggy",
        "suck",
        "sucks",
        "suicide girls",
        "sultry women",
        "swastika",
        "swinger",
        "tainted love",
        "taste my",
        "tea bagging",
        "threesome",
        "throating",
        "thumbzilla",
        "tied up",
        "tight white",
        "tit",
        "tits",
        "titties",
        "titty",
        "tongue in a",
        "topless",
        "tosser",
        "towelhead",
        "tranny",
        "tribadism",
        "tub girl",
        "tubgirl",
        "tushy",
        "twat",
        "twink",
        "twinkie",
        "two girls one cup",
        "undressing",
        "upskirt",
        "urethra play",
        "urophilia",
        "vagina",
        "venus mound",
        "viagra",
        "vibrator",
        "violet wand",
        "vorarephilia",
        "voyeur",
        "voyeurweb",
        "voyuer",
        "vulva",
        "wank",
        "wetback",
        "wet dream",
        "white power",
        "whore",
        "worldsex",
        "wrapping men",
        "wrinkled starfish",
        "xx",
        "xxx",
        "yaoi",
        "yellow showers",
        "yiffy",
        "zoophilia",
        "🖕",
    ]

    normalized_message = user_message.lower()

    return any(re.search(rf"\b{word}\b", normalized_message) for word in toxic_words)


def is_uncertain(user_message):
    uncertain_phrases = [
        "i'm not sure",
        "i don't know",
        "maybe",
        "probably",
        "not sure",
    ]

    normalized_message = user_message.strip().lower()

    return any(
        re.search(rf"\b{phrase}\b", normalized_message) for phrase in uncertain_phrases
    )


def is_complaint(user_message):
    complaint_phrases = [
        "i'm tired",
        "this is hard",
        "i don't like",
        "i hate",
        "tired",
        "this is annoying",
        "i'm frustrated",
        "i'm angry",
        "i can't do this",
    ]

    normalized_message = user_message.strip().lower()

    return any(
        re.search(rf"\b{phrase}\b", normalized_message) for phrase in complaint_phrases
    )


def is_negation(user_message):
    negation_phrases = [
        "no",
        "not really",
        "nah",
        "nope",
        "never",
        "i don't think so",
    ]

    normalized_message = user_message.strip().lower()

    return any(
        re.search(rf"\b{phrase}\b", normalized_message) for phrase in negation_phrases
    )


def is_affirmation(user_message):
    affirmation_phrases = [
        "yes",
        "yup",
        "yeah",
        "of course",
        "sure",
        "absolutely",
        "definitely",
        "okay",
        "ok",
    ]

    normalized_message = user_message.strip().lower()

    return any(
        re.search(rf"\b{phrase}\b", normalized_message)
        for phrase in affirmation_phrases
    )


def is_short_message(user_message):
    """
    Detects if the user message is a short response based on predefined criteria,
    while excluding complaints, negations, and affirmations.

    Args:
        user_message (str): The input message from the user.

    Returns:
        bool: True if the message is considered short, False otherwise.
    """
    short_phrases = {
        "ok",
        "yeah",
        "hi",
        "yes",
        "no",
        "hey",
        "yup",
        "yo",
        "hmm",
        "sure",
        "nah",
    }

    normalized_message = user_message.strip().lower()

    if normalized_message in short_phrases:
        return True

    word_count = len(re.findall(r"\b\w+\b", normalized_message))
    if len(normalized_message) < 10 or word_count < 3:
        return True

    return False


def is_goodbye(user_message):
    goodbye_phrases = [
        "bye",
        "goodbye",
        "see you",
        "take care",
        "farewell",
        "later",
        "catch you later",
        "peace out",
        "adios",
        "ciao",
    ]

    normalized_message = user_message.strip().lower()

    return any(
        re.search(rf"\b{phrase}\b", normalized_message) for phrase in goodbye_phrases
    )


def is_thank_you(user_message):
    thank_you_phrases = [
        "thank you",
        "thanks",
        "thx",
        "thank u",
        "i appreciate it",
        "much obliged",
        "many thanks",
        "gracias",
        "ty",
        "thankful",
    ]

    normalized_message = user_message.strip().lower()

    return any(
        re.search(rf"\b{phrase}\b", normalized_message) for phrase in thank_you_phrases
    )


def is_apology(user_message):
    apology_phrases = [
        "sorry",
        "my apologies",
        "i apologize",
        "apologies",
        "pardon me",
        "forgive me",
        "i'm sorry",
        "oops",
        "my bad",
        "excuse me",
    ]

    normalized_message = user_message.strip().lower()

    return any(
        re.search(rf"\b{phrase}\b", normalized_message) for phrase in apology_phrases
    )


def is_gibberish(user_message):
    gibberish_patterns = [
        r"(.)\1{3,}",  # Repeated characters (aaa, !!!, etc.)
        r"(\b\w+\b)(\s+\1){2,}",  # Repeated words (e.g., "hello hello hello")
        r"([a-z]{2,})(\1){2,}",  # Repeated syllables (e.g., "rwarwarwar")
    ]

    valid_short_messages = {"ok", "yeah", "hi", "yes", "no", "hey", "yo", "hmm"}

    normalized_message = user_message.strip().lower()

    if normalized_message in valid_short_messages:
        return False

    if len(normalized_message) < 5:
        return True

    words = re.findall(r"\b\w+\b", normalized_message)
    if len(set(words)) <= 1 and len(words) > 2:
        return True

    return any(re.search(pattern, normalized_message) for pattern in gibberish_patterns)


def therapist_reply(user_message, responses):
    return random.choice(responses)


def is_inappropriate_request(user_message):
    inappropriate_phrases = [
        "summarize",
        "generate",
        "write this",
        "do this",
        "can you do",
        "please do",
        "help me do",
        "make this",
        "create",
        "solve this",
        "answer this",
    ]

    normalized_message = user_message.strip().lower()

    return any(
        re.search(rf"\b{phrase}\b", normalized_message)
        for phrase in inappropriate_phrases
    )
