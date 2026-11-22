"""Progress, gamification and topic mastery service tracking learner achievements.

Adheres to:
- [PS: 9. Learning Progress]
- [PS: 11. Play & Learn Module; Topic Mastery System; Mission Challenges; Learning Rewards]
- [Arch: Gamification engine; R8 Mastery and XP formulas]
- [ADR 0010: Gamification, Mastery Formulas & Play and Learn Specification]
"""

import uuid
from datetime import UTC, datetime

from app.schemas.progress import (
    ActivityLogRequest,
    CertificateGenerationRequest,
    CertificateResponse,
    MasteryBreakdown,
    MissionChallengeRequest,
    MissionChallengeResponse,
    PersonalizedExercise,
    PersonalizedPracticeRequest,
    PersonalizedPracticeResponse,
    ProgressResponse,
)

# In-memory progress database for development / pilot
_LEARNER_DB: dict[str, dict] = {}


def get_learner_level(xp: int) -> tuple[int, str]:
    """Calculate learner level and child-friendly level name from XP.
    
    Formula from ADR 0010:
    level = floor(xp / 100) + 1
    """
    level = (xp // 100) + 1
    if level == 1:
        return 1, "Curious Scout 🌱"
    elif level == 2:
        return 2, "Eager Explorer 🚀"
    elif level == 3:
        return 3, "Knowledge Seeker 📚"
    elif level == 4:
        return 4, "Rising Scholar 💡"
    else:
        return level, "Master Learner 🏆"


def calculate_topic_mastery(
    reading: float = 0.0,
    workbook: float = 0.0,
    quiz: float = 0.0,
    game: float = 0.0,
    ai_doubts: float = 0.0,
) -> tuple[float, str]:
    """Calculate deterministic topic mastery score and level.

    Weights (ADR 0010 / R8):
    - Reading (R): 20% (0.20)
    - Workbook (W): 30% (0.30)
    - Quiz (Q): 20% (0.20)
    - Game (G): 20% (0.20)
    - AI Doubts / Interaction (A): 10% (0.10)

    Total S = (0.20*R + 0.30*W + 0.20*Q + 0.20*G + 0.10*A) * 100
    Thresholds:
    - S < 30: Beginner 🌱
    - 30 <= S < 60: Learning 📖
    - 60 <= S < 85: Practicing 💪
    - S >= 85: Mastered 🏆
    """
    r_clamp = max(0.0, min(1.0, reading))
    w_clamp = max(0.0, min(1.0, workbook))
    q_clamp = max(0.0, min(1.0, quiz))
    g_clamp = max(0.0, min(1.0, game))
    a_clamp = max(0.0, min(1.0, ai_doubts))

    score = (0.20 * r_clamp + 0.30 * w_clamp + 0.20 * q_clamp + 0.20 * g_clamp + 0.10 * a_clamp) * 100.0
    score = round(score, 1)

    if score < 30.0:
        level = "Beginner"
    elif score < 60.0:
        level = "Learning"
    elif score < 85.0:
        level = "Practicing"
    else:
        level = "Mastered"

    return score, level


def get_learner_progress(learner_id: str) -> ProgressResponse:
    """Return progress record for learner, initializing if new."""
    if learner_id not in _LEARNER_DB:
        # Default starting state for pilot learner
        initial_xp = 50
        lvl, lvl_name = get_learner_level(initial_xp)
        _LEARNER_DB[learner_id] = {
            "learner_id": learner_id,
            "completed_topics": [],
            "completed_chapters": [],
            "questions_asked": 0,
            "learning_streak_days": 1,
            "xp": initial_xp,
            "coins": 10,  # 1 Coin = 1 Learning Point
            "stars": 3,
            "level": lvl,
            "level_name": lvl_name,
            "badges": ["explorer"],
            "unlocked_items": ["game_bio_01", "theme_default"],
            "certificates": [],
            "mastery_levels": {
                "bio_ch1_t1": "Learning",
                "math_10_ch01": "Beginner",
            },
            "mastery_breakdowns": {
                "bio_ch1_t1": {
                    "reading_score": 1.0,
                    "workbook_score": 0.5,
                    "quiz_score": 0.5,
                    "game_score": 0.0,
                    "ai_score": 0.0,
                    "total_score": 45.0,
                    "level": "Learning",
                },
                "math_10_ch01": {
                    "reading_score": 0.5,
                    "workbook_score": 0.0,
                    "quiz_score": 0.0,
                    "game_score": 0.0,
                    "ai_score": 0.0,
                    "total_score": 10.0,
                    "level": "Beginner",
                },
            },
        }

    data = _LEARNER_DB[learner_id]
    lvl, lvl_name = get_learner_level(data["xp"])
    data["level"] = lvl
    data["level_name"] = lvl_name

    # Transform dicts to Pydantic models
    breakdowns = {
        tid: MasteryBreakdown(**b) if isinstance(b, dict) else b
        for tid, b in data.get("mastery_breakdowns", {}).items()
    }
    certs = [
        CertificateResponse(**c) if isinstance(c, dict) else c
        for c in data.get("certificates", [])
    ]

    return ProgressResponse(
        learner_id=data["learner_id"],
        completed_topics=data["completed_topics"],
        completed_chapters=data["completed_chapters"],
        questions_asked=data["questions_asked"],
        learning_streak_days=data["learning_streak_days"],
        xp=data["xp"],
        coins=data["coins"],
        stars=data["stars"],
        level=lvl,
        level_name=lvl_name,
        badges=data["badges"],
        unlocked_items=data["unlocked_items"],
        certificates=certs,
        mastery_levels=data["mastery_levels"],
        mastery_breakdowns=breakdowns,
    )


def increment_questions_asked(learner_id: str) -> int:
    """Increment questions_asked counter when student queries Bala Buddy."""
    get_learner_progress(learner_id)
    rec = _LEARNER_DB[learner_id]
    rec["questions_asked"] += 1
    rec["xp"] += 5  # 5 XP per question asked
    rec["coins"] += 1

    lvl, lvl_name = get_learner_level(rec["xp"])
    rec["level"] = lvl
    rec["level_name"] = lvl_name

    return rec["questions_asked"]


def log_activity(learner_id: str, request: ActivityLogRequest) -> ProgressResponse:
    """Log an educational activity and update mastery, XP, coins, stars, badges and unlockables."""
    get_learner_progress(learner_id)
    rec = _LEARNER_DB[learner_id]
    rec["activities_logged_count"] = rec.get("activities_logged_count", 0) + 1
    topic_id = request.topic_id
    atype = request.activity_type

    # Ensure mastery breakdown exists for this topic
    if "mastery_breakdowns" not in rec:
        rec["mastery_breakdowns"] = {}
    if topic_id not in rec["mastery_breakdowns"]:
        rec["mastery_breakdowns"][topic_id] = {
            "reading_score": 0.0,
            "workbook_score": 0.0,
            "quiz_score": 0.0,
            "game_score": 0.0,
            "ai_score": 0.0,
            "total_score": 0.0,
            "level": "Beginner",
        }

    mb = rec["mastery_breakdowns"][topic_id]

    if atype in ("read_topic", "topic_read"):
        if topic_id not in rec["completed_topics"]:
            rec["completed_topics"].append(topic_id)
        rec["xp"] += 20
        rec["coins"] += 5
        mb["reading_score"] = 1.0
        if "reading_hero" not in rec["badges"] and len(rec["completed_topics"]) >= 2:
            rec["badges"].append("reading_hero")

    elif atype in ("workbook", "workbook_completed"):
        score_val = (request.score if request.score is not None else 80) / 100.0
        mb["workbook_score"] = max(mb["workbook_score"], min(1.0, score_val))
        rec["xp"] += 30
        rec["coins"] += 10
        if score_val >= 0.9:
            rec["stars"] += 3
        elif score_val >= 0.7:
            rec["stars"] += 2
        else:
            rec["stars"] += 1

        if "science_genius" not in rec["badges"] and "bio" in topic_id:
            rec["badges"].append("science_genius")
        if "math_champion" not in rec["badges"] and "math" in topic_id:
            rec["badges"].append("math_champion")
        if "game_mission_challenge" not in rec["unlocked_items"]:
            rec["unlocked_items"].append("game_mission_challenge")

    elif atype in ("quiz", "quiz_question"):
        score_val = (request.score if request.score is not None else 80) / 100.0
        mb["quiz_score"] = max(mb["quiz_score"], min(1.0, score_val))
        rec["xp"] += 20
        rec["coins"] += 5
        rec["stars"] += 1

    elif atype in ("game", "game_played"):
        score_val = (request.score if request.score is not None else 100) / 100.0
        mb["game_score"] = max(mb["game_score"], min(1.0, score_val))
        rec["xp"] += 30
        rec["coins"] += 10
        if "theme_galaxy" not in rec["unlocked_items"]:
            rec["unlocked_items"].append("theme_galaxy")

    elif atype in ("watch_video", "video_watched"):
        rec["xp"] += 15
        rec["coins"] += 5
        if topic_id not in rec["completed_topics"]:
            rec["completed_topics"].append(topic_id)

    elif atype in ("ask_question", "question_asked"):
        rec["questions_asked"] += 1
        rec["xp"] += 5
        rec["coins"] += 1
        mb["ai_score"] = 1.0

    elif atype in ("mission_challenge", "mission_completed"):
        rec["xp"] += 50
        rec["coins"] += 25
        rec["stars"] += 3
        if "mission_master" not in rec["badges"]:
            rec["badges"].append("mission_master")
        if "bio_ch1" not in rec["completed_chapters"]:
            rec["completed_chapters"].append("bio_ch1")

    # Recalculate deterministic topic mastery
    tot_score, m_level = calculate_topic_mastery(
        reading=mb["reading_score"],
        workbook=mb["workbook_score"],
        quiz=mb["quiz_score"],
        game=mb["game_score"],
        ai_doubts=mb["ai_score"],
    )
    mb["total_score"] = tot_score
    mb["level"] = m_level
    rec["mastery_levels"][topic_id] = m_level

    # Check for explorer badge
    if "explorer" not in rec["badges"] and rec["completed_topics"]:
        rec["badges"].append("explorer")

    return get_learner_progress(learner_id)


def generate_certificate(learner_id: str, request: CertificateGenerationRequest) -> CertificateResponse:
    """Generate and store an official Achievement Certificate for a chapter."""
    get_learner_progress(learner_id)
    rec = _LEARNER_DB[learner_id]

    cert_id = f"CERT-{request.chapter_id.upper()}-{uuid.uuid4().hex[:6].upper()}"
    today_str = datetime.now(UTC).strftime("%d %B %Y")

    chapter_titles = {
        "bio_ch1": ("Nutrition - Food Supplying System", "పోషణ - ఆహార సరఫరా వ్యవస్థ"),
        "bio_ch2": ("Respiration - Energy Releasing System", "శ్వాసక్రియ - శక్తి ఉత్పాదక వ్యవస్థ"),
        "math_ch1": ("Real Numbers", "వాస్తవ సంఖ్యలు"),
    }
    title_en, title_te = chapter_titles.get(
        request.chapter_id, ("Syllabus Chapter Mastery", "పాఠ్యాంశ నైపుణ్య ధ్రువీకరణ")
    )

    cert = CertificateResponse(
        certificate_id=cert_id,
        learner_id=learner_id,
        learner_name=request.learner_name,
        subject_id="biology" if "bio" in request.chapter_id else "mathematics",
        chapter_id=request.chapter_id,
        chapter_title=title_en,
        telugu_chapter_title=title_te,
        score_percentage=request.score_percentage,
        issue_date=today_str,
        badge_name="Mission Champion 🏅",
        verified_by="Bala Buddy Official AI Tutor",
    )

    rec["certificates"].append(cert.model_dump())
    if "mission_master" not in rec["badges"]:
        rec["badges"].append("mission_master")

    return cert


def generate_personalized_practice(request: PersonalizedPracticeRequest) -> PersonalizedPracticeResponse:
    """Generate child-friendly personalized practice exercises and simplified analogies
    when student struggles with a topic [PS: 11. AI Generated Personalized Practice].
    """
    is_struggling = request.current_score_percentage < 60
    topic = request.topic_id.lower()

    if "math" in topic or "fraction" in topic:
        simplified_en = (
            "Think of fractions like sharing a yummy round dosa or pizza with your friends! "
            "If you cut 1 dosa into 4 equal slices and give 1 slice to your friend, that's 1/4!"
        )
        simplified_te = (
            "భిన్నాలను మీ స్నేహితులతో రుచికరమైన దోసె లేదా పిజ్జాను సమానంగా పంచుకోవడంలా ఊహించుకోండి! "
            "ఒక దోసెను 4 సమాన ముక్కలుగా చేసి, 1 ముక్కను మీ స్నేహితుడికి ఇస్తే, అది 1/4 భిన్నం అవుతుంది!"
        )
        exercises = [
            PersonalizedExercise(
                exercise_id="pp_math_01",
                question="If Bala Rabbit cuts 1 carrot into 2 equal halves, what fraction is one half?",
                telugu_question="బాల కుందేలు 1 క్యారెట్‌ను 2 సమాన భాగాలుగా చేస్తే, ఒక భాగం ఎంత భిన్నం?",
                options=["1/2", "1/4", "2/1", "1/3"],
                telugu_options=["1/2", "1/4", "2/1", "1/3"],
                correct_index=0,
                simplified_hint="1 carrot divided by 2 parts = 1/2",
                telugu_simplified_hint="1 క్యారెట్ రెండు భాగాలుగా పంచితే = 1/2",
            ),
            PersonalizedExercise(
                exercise_id="pp_math_02",
                question="Which fraction is bigger: 1/2 of a cake or 1/4 of a cake?",
                telugu_question="ఏది పెద్దది: 1/2 కేక్ ముక్క లేదా 1/4 కేక్ ముక్క?",
                options=["1/2", "1/4", "Both are equal", "Cannot say"],
                telugu_options=["1/2", "1/4", "రెండూ సమానం", "చెప్పలేము"],
                correct_index=0,
                simplified_hint="Sharing among 2 people gives bigger slices than sharing among 4!",
                telugu_simplified_hint="ఇద్దరికి పంచితే ఎక్కువ భాగం వస్తుంది!",
            ),
        ]
    else:
        # Default to Biology / Photosynthesis
        simplified_en = (
            "Plants are like little kitchen chefs in your garden! 🌿 They take sunlight from the sky, "
            "water from the soil, and air from around them to cook sweet glucose food, and happily release fresh oxygen for you!"
        )
        simplified_te = (
            "మొక్కలు తోటలోని చిన్న చెఫ్‌ల వంటివి! 🌿 అవి ఆకాశం నుండి సూర్యరశ్మిని, నేల నుండి నీటిని, "
            "గాలి నుండి కార్బన్ డయాక్సైడ్ తీసుకొని గ్లూకోజ్ ఆహారాన్ని తయారుచేస్తాయి, మనకోసం ఆక్సిజన్ ఇస్తాయి!"
        )
        exercises = [
            PersonalizedExercise(
                exercise_id="pp_bio_01",
                question="What is the green kitchen inside plant cells where food is cooked?",
                telugu_question="మొక్కల కణాలలో ఆహారాన్ని తయారుచేసే ఆకుపచ్చని భాగం ఏది?",
                options=["Chloroplast (హరితరేణువు)", "Root Hair", "Bark", "Flower"],
                telugu_options=["హరితరేణువు", "వేరు వెంట్రుకలు", "బెరడు", "పువ్వు"],
                correct_index=0,
                simplified_hint="It has the green pigment chlorophyll that absorbs sunlight!",
                telugu_simplified_hint="ఇందులోని క్లోరోఫిల్ సూర్యకాంతిని గ్రహిస్తుంది!",
            ),
            PersonalizedExercise(
                exercise_id="pp_bio_02",
                question="Which clean, life-giving gas do plants release during the day?",
                telugu_question="మొక్కలు కిరణజన్య సంయోగక్రియలో ఏ ప్రాణవాయువును విడుదల చేస్తాయి?",
                options=["Oxygen (ఆక్సిజన్)", "Carbon Dioxide", "Nitrogen", "Smoke"],
                telugu_options=["ఆక్సిజన్", "కార్బన్ డయాక్సైడ్", "నైట్రోజన్", "పొగ"],
                correct_index=0,
                simplified_hint="The same gas that we breathe in every second!",
                telugu_simplified_hint="మనం ప్రతి క్షణం పీల్చుకునే ప్రాణవాయువు!",
            ),
        ]

    encouragement = (
        "Don't worry at all! 🌟 Making mistakes is how our brain gets super strong. "
        "Let's review these easy-peasy questions with Bala Buddy!"
        if is_struggling
        else "Superstar learner! 🌟 You're doing great. Try these bonus booster questions!"
    )

    return PersonalizedPracticeResponse(
        topic_id=request.topic_id,
        struggling_detected=is_struggling,
        encouragement_message=encouragement,
        simplified_explanation=simplified_en,
        telugu_simplified_explanation=simplified_te,
        extra_exercises=exercises,
    )


def evaluate_mission_challenge(learner_id: str, request: MissionChallengeRequest) -> MissionChallengeResponse:
    """Evaluate end-of-chapter Mission Challenge [PS: 11. End-of-Chapter Challenge]."""
    get_learner_progress(learner_id)
    rec = _LEARNER_DB[learner_id]

    passed = (
        request.quiz_score >= 50
        and request.puzzle_solved
        and request.scenario_answered
        and request.mini_game_score >= 50
    )

    earned_xp = 50 if passed else 15
    earned_coins = 25 if passed else 5
    badge = "mission_master" if passed else "none"

    rec["xp"] += earned_xp
    rec["coins"] += earned_coins
    if passed:
        rec["stars"] += 3
        if badge not in rec["badges"]:
            rec["badges"].append(badge)
        if request.chapter_id not in rec["completed_chapters"]:
            rec["completed_chapters"].append(request.chapter_id)

    cert_id = None
    if passed:
        cert_req = CertificateGenerationRequest(
            chapter_id=request.chapter_id,
            learner_name="Bala Learner",
            score_percentage=max(request.quiz_score, request.mini_game_score),
        )
        cert = generate_certificate(learner_id, cert_req)
        cert_id = cert.certificate_id

    feedback_en = (
        "🌟 MISSION ACCOMPLISHED! You solved the chapter challenge, mastered the puzzle, and earned your Chapter Badge!"
        if passed
        else "Great try! You gave your best on the mission. Practice a bit more and challenge Bala Buddy again!"
    )
    feedback_te = (
        "🌟 అధ్యాయం మిషన్ పూర్తయింది! మీరు పజిల్స్ మరియు క్విజ్‌ను అద్భుతంగా పూర్తి చేసి అధ్యాయం బ్యాడ్జ్ గెలుచుకున్నారు!"
        if passed
        else "మంచి ప్రయత్నం! ఇంకొంచెం సాధన చేసి మళ్ళీ మిషన్ పూర్తి చేయండి!"
    )

    return MissionChallengeResponse(
        chapter_id=request.chapter_id,
        completed=passed,
        earned_xp=earned_xp,
        earned_coins=earned_coins,
        earned_badge=badge,
        certificate_id=cert_id,
        feedback=feedback_en,
        telugu_feedback=feedback_te,
    )


def delete_learner_progress(learner_id: str) -> bool:
    """Permanently delete student progress records [Right to be Forgotten - ADR 0012]."""
    if learner_id in _LEARNER_DB:
        del _LEARNER_DB[learner_id]
        return True
    return False

