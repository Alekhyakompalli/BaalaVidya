"""Videos service providing curated educational video metadata and stream endpoints.

Adheres to:
- [PS: 7. Video Section]
- [Arch: Data model, Videos (`video_id`, `topic_id`, `language_code`, `title`, `url`, `duration`)]
- [Arch: R5 Video licensing and source]
- [Phase 7: Video section]
"""

from app.schemas.videos import VideoItem, VideoQualityLevel

# Curated pilot video catalog covering Class 10 pilot curriculum (Biology, Math, Telugu)
PILOT_VIDEOS: list[dict] = [
    # Biology Chapter 1, Topic 1: What is Photosynthesis?
    {
        "video_id": "vid_bio_ch1_t1_te",
        "topic_id": "bio_ch1_t1",
        "aliases": ["bio_10_ch01_t01"],
        "language_code": "te",
        "title": "Photosynthesis in Green Plants - Telugu Video Lesson",
        "telugu_title": "మొక్కలలో కిరణజన్య సంయోగక్రియ వీడియో పాఠం",
        "description": "Animated explainer showing how plants absorb sunlight, water, and CO2 to produce glucose and fresh oxygen.",
        "telugu_description": "సూర్యకాంతి, నీరు మరియు కార్బన్ డయాక్సైడ్ ఉపయోగించి మొక్కలు ఆహారాన్ని ఎలా తయారుచేస్తాయో తెలిపే యానిమేషన్ పాఠం.",
        "duration_seconds": 480,
        "duration_minutes": 8,
        "url": "https://stream.scert.telangana.gov.in/videos/biology/photosynthesis_te.m3u8",
        "provider": "T-SAT Vidya / SCERT Telangana",
        "quality_levels": [
            {"label": "360p (Data Saver)", "resolution": "360p", "stream_url": "https://stream.scert.telangana.gov.in/videos/biology/photosynthesis_te_360p.m3u8"},
            {"label": "480p (Standard)", "resolution": "480p", "stream_url": "https://stream.scert.telangana.gov.in/videos/biology/photosynthesis_te_480p.m3u8"},
            {"label": "720p (HD)", "resolution": "720p", "stream_url": "https://stream.scert.telangana.gov.in/videos/biology/photosynthesis_te_720p.m3u8"},
        ],
        "online_streaming_only": True,
        "thumbnail_icon": "🌿",
    },
    {
        "video_id": "vid_bio_ch1_t1_en",
        "topic_id": "bio_ch1_t1",
        "aliases": ["bio_10_ch01_t01"],
        "language_code": "en",
        "title": "Animated Guide to Photosynthesis in Plant Leaves",
        "telugu_title": "మొక్కల ఆకులలో కిరణజన్య సంయోగక్రియ ఇంగ్లీష్ వివరణ",
        "description": "Kid-friendly illustrated walkthrough of plant nutrition and chlorophyll energy capture in leaves.",
        "telugu_description": "ఆకులలో క్లోరోఫిల్ శక్తిని గ్రహించి ఆహారంగా మార్చే విధానంపై ఇంగ్లీష్ దృశ్య రూపం.",
        "duration_seconds": 540,
        "duration_minutes": 9,
        "url": "https://stream.scert.telangana.gov.in/videos/biology/photosynthesis_en.m3u8",
        "provider": "DIKSHA / Telangana Open Educational Resources",
        "quality_levels": [
            {"label": "360p (Data Saver)", "resolution": "360p", "stream_url": "https://stream.scert.telangana.gov.in/videos/biology/photosynthesis_en_360p.m3u8"},
            {"label": "480p (Standard)", "resolution": "480p", "stream_url": "https://stream.scert.telangana.gov.in/videos/biology/photosynthesis_en_480p.m3u8"},
            {"label": "720p (HD)", "resolution": "720p", "stream_url": "https://stream.scert.telangana.gov.in/videos/biology/photosynthesis_en_720p.m3u8"},
        ],
        "online_streaming_only": True,
        "thumbnail_icon": "🍃",
    },

    # Biology Chapter 1, Topic 2: Light & Dark Reactions
    {
        "video_id": "vid_bio_ch1_t2_te",
        "topic_id": "bio_ch1_t2",
        "aliases": ["bio_10_ch01_t02"],
        "language_code": "te",
        "title": "Stages of Photosynthesis: Light and Dark Reactions",
        "telugu_title": "కాంతి మరియు నిష్కాంతి చర్యల సమగ్ర వివరణ",
        "description": "Visual breakdown of grana thylakoid light absorption and stroma glucose synthesis.",
        "telugu_description": "హరితరేణువులోని గ్రానా థైలాకాయిడ్లలో కాంతి చర్య మరియు స్ట్రోమాలో నిష్కాంతి చర్యల యానిమేషన్.",
        "duration_seconds": 600,
        "duration_minutes": 10,
        "url": "https://stream.scert.telangana.gov.in/videos/biology/light_dark_reactions_te.m3u8",
        "provider": "T-SAT Vidya / SCERT Telangana",
        "quality_levels": [
            {"label": "360p (Data Saver)", "resolution": "360p", "stream_url": "https://stream.scert.telangana.gov.in/videos/biology/light_dark_te_360p.m3u8"},
            {"label": "480p (Standard)", "resolution": "480p", "stream_url": "https://stream.scert.telangana.gov.in/videos/biology/light_dark_te_480p.m3u8"},
            {"label": "720p (HD)", "resolution": "720p", "stream_url": "https://stream.scert.telangana.gov.in/videos/biology/light_dark_te_720p.m3u8"},
        ],
        "online_streaming_only": True,
        "thumbnail_icon": "☀️",
    },
    {
        "video_id": "vid_bio_ch1_t2_en",
        "topic_id": "bio_ch1_t2",
        "aliases": ["bio_10_ch01_t02"],
        "language_code": "en",
        "title": "Light & Dark Reactions of Photosynthesis Explained",
        "telugu_title": "కాంతి & నిష్కాంతి చర్యల ఇంగ్లీష్ వీడియో పాఠం",
        "description": "Step-by-step breakdown of ATP photolysis of water and carbohydrate synthesis.",
        "telugu_description": "ATP తయారీ మరియు పిండిపదార్థం ఉత్పత్తిపై ఇంగ్లీష్ వివరణ.",
        "duration_seconds": 660,
        "duration_minutes": 11,
        "url": "https://stream.scert.telangana.gov.in/videos/biology/light_dark_reactions_en.m3u8",
        "provider": "DIKSHA / Telangana Open Educational Resources",
        "quality_levels": [
            {"label": "360p (Data Saver)", "resolution": "360p", "stream_url": "https://stream.scert.telangana.gov.in/videos/biology/light_dark_en_360p.m3u8"},
            {"label": "480p (Standard)", "resolution": "480p", "stream_url": "https://stream.scert.telangana.gov.in/videos/biology/light_dark_en_480p.m3u8"},
            {"label": "720p (HD)", "resolution": "720p", "stream_url": "https://stream.scert.telangana.gov.in/videos/biology/light_dark_en_720p.m3u8"},
        ],
        "online_streaming_only": True,
        "thumbnail_icon": "⚡",
    },

    # Biology Chapter 1, Topic 3: Chloroplast & Leaf Anatomy
    {
        "video_id": "vid_bio_ch1_t3_te",
        "topic_id": "bio_ch1_t3",
        "aliases": ["bio_10_ch01_t03"],
        "language_code": "te",
        "title": "Chloroplast Structure and Leaf Anatomy Under Microscope",
        "telugu_title": "సూక్ష్మదర్శినిలో హరితరేణువు నిర్మాణం మరియు ఆకు అంతర్నిర్మాణం",
        "description": "High-magnification 3D model of leaf cross section, stomata, and chloroplast membranes.",
        "telugu_description": "ఆకు అడ్డుకోత, పత్రరంధ్రాలు మరియు హరితరేణువు పొరల 3D దృశ్యరూపం.",
        "duration_seconds": 420,
        "duration_minutes": 7,
        "url": "https://stream.scert.telangana.gov.in/videos/biology/chloroplast_leaf_te.m3u8",
        "provider": "T-SAT Vidya / SCERT Telangana",
        "quality_levels": [
            {"label": "360p (Data Saver)", "resolution": "360p", "stream_url": "https://stream.scert.telangana.gov.in/videos/biology/chloroplast_te_360p.m3u8"},
            {"label": "480p (Standard)", "resolution": "480p", "stream_url": "https://stream.scert.telangana.gov.in/videos/biology/chloroplast_te_480p.m3u8"},
        ],
        "online_streaming_only": True,
        "thumbnail_icon": "🔬",
    },
    {
        "video_id": "vid_bio_ch1_t3_en",
        "topic_id": "bio_ch1_t3",
        "aliases": ["bio_10_ch01_t03"],
        "language_code": "en",
        "title": "Microscopic View of Chloroplast Structure",
        "telugu_title": "హరితరేణువు అంతర్గత నిర్మాణం ఇంగ్లీష్ వివరణ",
        "description": "Explore the double membrane, stroma, and thylakoid stacks inside leaf cells.",
        "telugu_description": "ద్వంద్వ త్వచం, స్ట్రోమా మరియు థైలాకాయిడ్ దొంతరల నిర్మాణం.",
        "duration_seconds": 450,
        "duration_minutes": 7,
        "url": "https://stream.scert.telangana.gov.in/videos/biology/chloroplast_leaf_en.m3u8",
        "provider": "DIKSHA / Telangana Open Educational Resources",
        "quality_levels": [
            {"label": "360p (Data Saver)", "resolution": "360p", "stream_url": "https://stream.scert.telangana.gov.in/videos/biology/chloroplast_en_360p.m3u8"},
            {"label": "480p (Standard)", "resolution": "480p", "stream_url": "https://stream.scert.telangana.gov.in/videos/biology/chloroplast_en_480p.m3u8"},
        ],
        "online_streaming_only": True,
        "thumbnail_icon": "🔬",
    },

    # Biology Chapter 2, Topic 1: Respiration
    {
        "video_id": "vid_bio_ch2_t1_te",
        "topic_id": "bio_ch2_t1",
        "aliases": ["bio_10_ch02_t01"],
        "language_code": "te",
        "title": "Aerobic vs Anaerobic Respiration in Living Cells",
        "telugu_title": "వాయు సహిత మరియు అవాయు శ్వాసక్రియ తేడాలు",
        "description": "Comparing energy release in mitochondria with anaerobic fermentation in yeast and human muscles.",
        "telugu_description": "మైటోకాండ్రియాలో వాయు సహిత శ్వాసక్రియ మరియు ఈస్ట్‌లో అవాయు శ్వాసక్రియ మధ్య తేడాలు.",
        "duration_seconds": 510,
        "duration_minutes": 8,
        "url": "https://stream.scert.telangana.gov.in/videos/biology/respiration_te.m3u8",
        "provider": "T-SAT Vidya / SCERT Telangana",
        "quality_levels": [
            {"label": "360p (Data Saver)", "resolution": "360p", "stream_url": "https://stream.scert.telangana.gov.in/videos/biology/respiration_te_360p.m3u8"},
            {"label": "480p (Standard)", "resolution": "480p", "stream_url": "https://stream.scert.telangana.gov.in/videos/biology/respiration_te_480p.m3u8"},
        ],
        "online_streaming_only": True,
        "thumbnail_icon": "🫁",
    },
    {
        "video_id": "vid_bio_ch2_t1_en",
        "topic_id": "bio_ch2_t1",
        "aliases": ["bio_10_ch02_t01"],
        "language_code": "en",
        "title": "Aerobic and Anaerobic Respiration Compared",
        "telugu_title": "శ్వాసక్రియ రకాలు ఇంగ్లీష్ వీడియో పాఠం",
        "description": "How glucose breaks down to yield 38 ATP molecules with oxygen vs 2 ATP without oxygen.",
        "telugu_description": "ఆక్సిజన్‌తో 38 ATP మరియు ఆక్సిజన్ లేకుండా 2 ATP శక్తి విడుదలయ్యే విధానం.",
        "duration_seconds": 540,
        "duration_minutes": 9,
        "url": "https://stream.scert.telangana.gov.in/videos/biology/respiration_en.m3u8",
        "provider": "DIKSHA / Telangana Open Educational Resources",
        "quality_levels": [
            {"label": "360p (Data Saver)", "resolution": "360p", "stream_url": "https://stream.scert.telangana.gov.in/videos/biology/respiration_en_360p.m3u8"},
            {"label": "480p (Standard)", "resolution": "480p", "stream_url": "https://stream.scert.telangana.gov.in/videos/biology/respiration_en_480p.m3u8"},
        ],
        "online_streaming_only": True,
        "thumbnail_icon": "🫁",
    },

    # Mathematics Chapter 1, Topic 1: Real Numbers
    {
        "video_id": "vid_math_ch1_t1_te",
        "topic_id": "math_ch1_t1",
        "aliases": ["math_10_ch01_t01", "math_10_ch01_t02"],
        "language_code": "te",
        "title": "Real Numbers & Fundamental Theorem of Arithmetic",
        "telugu_title": "వాస్తవ సంఖ్యలు మరియు అంకగణిత ప్రాథమిక సిద్ధాంతం",
        "description": "Simple visual examples explaining prime factorisation, HCF, and LCM for Class 10.",
        "telugu_description": "ప్రధాన కారణాంకాల లబ్దంగా రాయడం, గ.సా.భా మరియు క.సా.గు కనుగొనే పద్ధతి.",
        "duration_seconds": 600,
        "duration_minutes": 10,
        "url": "https://stream.scert.telangana.gov.in/videos/math/real_numbers_te.m3u8",
        "provider": "T-SAT Vidya / SCERT Telangana",
        "quality_levels": [
            {"label": "360p (Data Saver)", "resolution": "360p", "stream_url": "https://stream.scert.telangana.gov.in/videos/math/real_numbers_te_360p.m3u8"},
            {"label": "480p (Standard)", "resolution": "480p", "stream_url": "https://stream.scert.telangana.gov.in/videos/math/real_numbers_te_480p.m3u8"},
        ],
        "online_streaming_only": True,
        "thumbnail_icon": "📐",
    },
    {
        "video_id": "vid_math_ch1_t1_en",
        "topic_id": "math_ch1_t1",
        "aliases": ["math_10_ch01_t01", "math_10_ch01_t02"],
        "language_code": "en",
        "title": "The Fundamental Theorem of Arithmetic - Class 10 Math",
        "telugu_title": "అంకగణిత ప్రాథమిక సిద్ధాంతం ఇంగ్లీష్ వీడియో",
        "description": "Understanding prime factorisation tree and proving unique representation of composite numbers.",
        "telugu_description": "సంయుక్త సంఖ్యల కారణాంకాల వృక్షం మరియు ప్రత్యేక లబ్దం.",
        "duration_seconds": 630,
        "duration_minutes": 10,
        "url": "https://stream.scert.telangana.gov.in/videos/math/real_numbers_en.m3u8",
        "provider": "DIKSHA / Telangana Open Educational Resources",
        "quality_levels": [
            {"label": "360p (Data Saver)", "resolution": "360p", "stream_url": "https://stream.scert.telangana.gov.in/videos/math/real_numbers_en_360p.m3u8"},
            {"label": "480p (Standard)", "resolution": "480p", "stream_url": "https://stream.scert.telangana.gov.in/videos/math/real_numbers_en_480p.m3u8"},
        ],
        "online_streaming_only": True,
        "thumbnail_icon": "📐",
    },

    # Telugu First Language Chapter 1: దానశీలము
    {
        "video_id": "vid_tel_ch1_t1_te",
        "topic_id": "tel_ch1_t1",
        "aliases": ["tel_10_ch01_t01"],
        "language_code": "te",
        "title": "దానశీలము - బలి చక్రవర్తి కథ మరియు పద్యాల భావాలు",
        "telugu_title": "దానశీలము - బలి చక్రవర్తి కథ మరియు పద్యాల భావాలు",
        "description": "బమ్మెర పోతన రచించిన శ్రీమదాంధ్ర భాగవతంలోని బలి చక్రవర్తి దాన గుణం మరియు పద్యాల ప్రతిపదార్థాలు.",
        "telugu_description": "బమ్మెర పోతన రచించిన శ్రీమదాంధ్ర భాగవతంలోని బలి చక్రవర్తి దాన గుణం మరియు పద్యాల ప్రతిపదార్థాలు.",
        "duration_seconds": 720,
        "duration_minutes": 12,
        "url": "https://stream.scert.telangana.gov.in/videos/telugu/danaseelamu_te.m3u8",
        "provider": "T-SAT Vidya / SCERT Telangana",
        "quality_levels": [
            {"label": "360p (Data Saver)", "resolution": "360p", "stream_url": "https://stream.scert.telangana.gov.in/videos/telugu/danaseelamu_te_360p.m3u8"},
            {"label": "480p (Standard)", "resolution": "480p", "stream_url": "https://stream.scert.telangana.gov.in/videos/telugu/danaseelamu_te_480p.m3u8"},
        ],
        "online_streaming_only": True,
        "thumbnail_icon": "📖",
    },
]


def _to_video_item(raw: dict) -> VideoItem:
    """Convert raw dictionary to VideoItem schema."""
    quality_levels = [
        VideoQualityLevel(label=q["label"], resolution=q["resolution"], stream_url=q["stream_url"])
        for q in raw.get("quality_levels", [])
    ]
    return VideoItem(
        video_id=raw["video_id"],
        topic_id=raw["topic_id"],
        language_code=raw["language_code"],
        title=raw["title"],
        telugu_title=raw["telugu_title"],
        description=raw["description"],
        telugu_description=raw["telugu_description"],
        duration_seconds=raw["duration_seconds"],
        duration_minutes=raw["duration_minutes"],
        url=raw["url"],
        provider=raw.get("provider", "T-SAT Vidya / SCERT Telangana"),
        quality_levels=quality_levels,
        online_streaming_only=raw.get("online_streaming_only", True),
        thumbnail_icon=raw.get("thumbnail_icon", "🎬"),
    )


def list_videos_for_topic(topic_id: str, language: str | None = None) -> list[VideoItem]:
    """
    Return educational videos for a given topic ID or alias.
    Adheres to [PS: 7. Video Section]:
    Returns Telugu and English explanation videos per topic, filtered by language if requested.
    """
    matches = []
    clean_id = topic_id.strip().lower()

    for item in PILOT_VIDEOS:
        tid = item["topic_id"].lower()
        aliases = [a.lower() for a in item.get("aliases", [])]

        if (clean_id == tid or clean_id in aliases) and (
            language is None or item["language_code"].lower() == language.lower()
        ):
            matches.append(_to_video_item(item))

    # Sort so that if language is 'te', Telugu comes first; otherwise English or stable order
    if language == "te":
        matches.sort(key=lambda v: 0 if v.language_code == "te" else 1)
    elif language == "en":
        matches.sort(key=lambda v: 0 if v.language_code == "en" else 1)

    return matches


def get_video_by_id(video_id: str) -> VideoItem | None:
    """Return a specific video by its ID."""
    clean_id = video_id.strip().lower()
    for item in PILOT_VIDEOS:
        if item["video_id"].lower() == clean_id:
            return _to_video_item(item)
    return None


def get_cached_metadata_for_chapter(chapter_id: str) -> list[dict]:
    """
    Return lightweight cached video metadata dictionary items for offline chapter package bundling.
    Guarantees: Zero video files are bundled, strictly metadata only.
    """
    prefix = chapter_id.split("_")[0]  # e.g., 'bio', 'math', 'tel'
    chapter_num = chapter_id.split("_")[-1]  # e.g., 'ch1', 'ch01'

    results = []
    for item in PILOT_VIDEOS:
        tid = item["topic_id"]
        # Match topics belonging to this chapter
        if tid.startswith((f"{prefix}_{chapter_num}", f"{prefix}_10_{chapter_num}")):
            results.append({
                "video_id": item["video_id"],
                "topic_id": item["topic_id"],
                "language_code": item["language_code"],
                "title": item["title"],
                "telugu_title": item["telugu_title"],
                "duration_seconds": item["duration_seconds"],
                "duration_minutes": item["duration_minutes"],
                "stream_url": item["url"],
                "provider": item["provider"],
                "online_streaming_only": True,
            })
    return results
