"""Guardrails and safety checks for BAALAVIDYA chatbot.

Implements two-tiered safety architecture [ADR 0012]:
1. Tier 1: Input guardrails (Prompt injection, harmful queries, off-topic requests)
2. Tier 2: Output safety filter (Second check after prompt generation, PII & profanity suppression)
3. Polite, encouraging refusal templates in English and Telugu
"""

import re

INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior)\s+instructions",
    r"disregard\s+(the\s+)?system\s+prompt",
    r"you\s+are\s+(now\s+)?in\s+developer\s+mode",
    r"system\s*prompt",
    r"jailbreak",
    r"bypass\s+guardrails",
    r"pretend\s+you\s+have\s+no\s+rules",
    r"output\s+the\s+initial\s+(developer\s+)?prompt",
    # Telugu injection keywords
    r"(మునుపటి\s*సూచనలన్నీ?\s*విస్మరించు|నియమాలను\s*ఉల్లంఘించు|సిస్టమ్\s*ప్రాంప్ట్|జైల్‌బ్రేక్|రహస్య\s*ప్రాంప్ట్|డెవలపర్\s*మోడ్)",
]

HARMFUL_PATTERNS = [
    r"\b(bomb|weapon|explosive|knife|attack|kill|suicide|poison|self[\s-]harm|hurt|assault)\b",
    r"\b(hack|steal|password|credit card|cvv|pin|bank account)\b",
    r"\b(drugs|alcohol|smoke|cocaine|cigarette|beer|wine)\b",
    r"\b(sex|nude|porn|adult|erotic)\b",
    # Telugu harmful keywords
    r"(బాంబు|తుపాకీ|కత్తి|దాడి|హత్య|చంప|ఆత్మహత్య|ప్రాణం\s*తీసుకో|విషం)",
    r"(హ్యాక్|దొంగతనం|పాస్‌వర్డ్|బ్యాంక్|ఖాతా)",
    r"(డ్రగ్స్|మద్యం|సిగరెట్|వైన్|బీరు)",
    r"(అశ్లీల|సెక్స్|నగ్న|నీలి\s*చిత్రాలు)",
]

OFF_TOPIC_PATTERNS = [
    r"\b(crypto|bitcoin|binance|stock market|ipl score|cricket match score|movie download|pirated movie)\b",
    r"\b(politics|political|election results|who will win election|political party)\b",
    # Telugu off-topic keywords
    r"(బిట్‌కాయిన్|క్రిప్టో|స్టాక్\s*మార్కెట్|సినిమా\s*డౌన్‌లోడ్|ఎన్నికలు|రాజకీయ\s*పార్టీ|క్రికెట్\s*స్కోర్)",
]

OUTPUT_UNSAFE_PATTERNS = [
    # Profanity and vulgarity
    r"\b(fuck\w*|shit\w*|bitch\w*|bastard\w*|asshole\w*|cunt\w*|dick\w*)\b",
    # Harmful instruction leakage
    r"\b(mix potassium nitrate|synthesize ricin|detonate|suicide method)\b",
    # PII Leakage (Emails, Phone numbers, Indian Aadhaar)
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    r"\b(?:\+?91[\s-]?)?[6-9]\d{9}\b",
    r"\b\d{4}[\s-]\d{4}[\s-]\d{4}\b",
    # Secret / API key leakage
    r"\b(sk-[a-zA-Z0-9]{20,}|AIza[0-9A-Za-z-_]{35}|Bearer\s+[a-zA-Z0-9_\-\.]+)\b",
    # System prompt leak
    r"You are Bala Buddy, the cheerful, kind, and encouraging AI study companion",
]

REFUSAL_MESSAGES = {
    "injection": {
        "en": "I am Bala Buddy, your school study friend! Let's stay focused on learning and explore your textbook lessons together.",
        "te": "నేను బాల బడ్డీని, మీ చదువుల స్నేహితుడిని! మనం సరదాగా మన పాఠ్యపుస్తక పాఠాలను నేర్చుకుందాం.",
    },
    "harmful": {
        "en": "I can only share safe, friendly, and educational information for children! Let's explore a fun science or math topic instead.",
        "te": "నేను పిల్లల కోసం సురక్షితమైన మరియు ఉపయోగకరమైన విద్యా విషయాలను మాత్రమే చెప్పగలను! మనం సైన్స్ లేదా మ్యాథ్స్ పాఠాన్ని నేర్చుకుందాం.",
    },
    "off_topic": {
        "en": "I can only help with your school lessons and homework! Let's pick a fun topic from your syllabus to study.",
        "te": "నేను మీ బడి పాఠాలు మరియు హోంవర్క్‌తో మాత్రమే సహాయం చేయగలను! మీ సిలబస్‌లోని ఒక మంచి పాఠాన్ని ఎంచుకుందాం.",
    },
    "output_unsafe": {
        "en": "I can only share child-safe school explanations! Let's review a fun concept from your textbook.",
        "te": "నేను పిల్లల కోసం సురక్షితమైన విద్యా విషయాలను మాత్రమే పంచుకోగలను! మనం పాఠ్యపుస్తకంలోని మంచి పాఠాన్ని చదువుకుందాం.",
    },
}


def check_input_guardrails(query: str, language: str = "en") -> tuple[bool, str | None, str | None]:
    """Check student question against Tier 1 safety and guardrail rules.

    Returns (is_safe, refusal_message_or_None, category_or_None).
    category: 'injection', 'harmful', 'off_topic', or None.
    """
    q_lower = query.lower().strip()
    lang = "te" if language.startswith("te") else "en"

    # 1. Prompt injection check
    for pat in INJECTION_PATTERNS:
        if re.search(pat, q_lower, re.IGNORECASE):
            return False, REFUSAL_MESSAGES["injection"][lang], "injection"

    # 2. Child safety & harmful content check
    for pat in HARMFUL_PATTERNS:
        if re.search(pat, q_lower, re.IGNORECASE):
            return False, REFUSAL_MESSAGES["harmful"][lang], "harmful"

    # 3. Off-topic check
    for pat in OFF_TOPIC_PATTERNS:
        if re.search(pat, q_lower, re.IGNORECASE):
            return False, REFUSAL_MESSAGES["off_topic"][lang], "off_topic"

    return True, None, None


def check_output_safety(text: str, language: str = "en") -> tuple[bool, str | None, str | None]:
    """Check generated model answer against Tier 2 safety filter [ADR 0012].

    Second check after prompt rules to catch hallucinations, profanity, PII leakage, or prompt leaks.
    Returns (is_safe, refusal_message_or_None, category_or_None).
    """
    if not text:
        return True, None, None

    lang = "te" if language.startswith("te") else "en"

    for pat in OUTPUT_UNSAFE_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            return False, REFUSAL_MESSAGES["output_unsafe"][lang], "output_unsafe"

    # Also run harmful pattern check against generated output as defense-in-depth
    for pat in HARMFUL_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            return False, REFUSAL_MESSAGES["harmful"][lang], "harmful"

    return True, None, None


GREETING_PHRASES = {
    "hi",
    "hii",
    "hiii",
    "hello",
    "helo",
    "hey",
    "hi there",
    "hey there",
    "hello bala buddy",
    "hi bala buddy",
    "hey bala buddy",
    "hello buddy",
    "hi buddy",
    "hey buddy",
    "good morning",
    "good afternoon",
    "good evening",
    "namaste",
    "namaskar",
    "namaskaram",
    "vanakkam",
    "pranam",
    # Telugu greetings
    "హలో",
    "హాయ్",
    "నమస్తే",
    "నమస్కారం",
    "నమస్కారము",
    "హలో బాల బడ్డీ",
    "హాయ్ బాల బడ్డీ",
    "నమస్తే బాల బడ్డీ",
    "నమస్కారం బాల బడ్డీ",
}

GREETING_REPLY_EN = (
    "Hello, dear friend! 😊 I'm Bala Buddy, your study companion! "
    "What would you like to learn today? Ask me anything about your textbook lessons "
    "and I will explain it with fun examples!"
)

GREETING_REPLY_TE = (
    "నమస్కారం, ప్రియమైన స్నేహితుడా! 😊 నేను బాల బడ్డీని, మీ చదువుల స్నేహితుడిని! "
    "ఈ రోజు ఏం నేర్చుకోవాలనుకుంటున్నారు? మీ పాఠ్యపుస్తక పాఠాల గురించి ఏదైనా అడగండి, "
    "నేను సరదా ఉదాహరణలతో వివరిస్తాను!"
)


def is_greeting(query: str) -> bool:
    """Return True if the whole message is a short greeting.

    Lowercases, replaces punctuation with spaces, then checks against GREETING_PHRASES
    or whether the normalized text starts with common greeting salutations.
    """
    if not query:
        return False
    # Remove punctuation, keep letters, numbers, and spaces across Unicode
    text = re.sub(r"[^\w\s]", " ", query.lower())
    text = " ".join(text.split())
    if not text:
        return False
    words = text.split()
    if len(words) > 5:
        return False
    if text in GREETING_PHRASES:
        return True
    first_word = words[0]
    return first_word in {
        "hi", "hello", "hey", "namaste", "namaskar", "namaskaram",
        "హలో", "హాయ్", "నమస్తే", "నమస్కారం", "నమస్కారము"
    }

