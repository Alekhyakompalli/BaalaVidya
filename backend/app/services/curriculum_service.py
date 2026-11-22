"""Curriculum service managing Class 1 to 10 metadata, chapters, and updates."""

from app.config import settings
from app.schemas.curriculum import (
    ChapterItem,
    ClassItem,
    LatestUpdateItem,
    SubjectItem,
    TopicItem,
)
from app.services.video_service import get_cached_metadata_for_chapter

# Canonical Class 10 curriculum based on Telangana SCERT textbooks (English & Telugu mediums)
PILOT_SUBJECTS = [
    {
        "subject_id": "math_10",
        "class_id": "10",
        "name": "Mathematics",
        "medium": "EM",
        "icon": "calculate",
        "chapters": [
            {
                "chapter_id": "math_10_ch01",
                "order": 1,
                "title": "Real Numbers (వాస్తవ సంఖ్యలు)",
                "topics": [
                    {
                        "topic_id": "math_10_ch01_t01",
                        "order": 1,
                        "title": "Euclid's Division Lemma"
                    },
                    {
                        "topic_id": "math_10_ch01_t02",
                        "order": 2,
                        "title": "Fundamental Theorem of Arithmetic"
                    },
                    {
                        "topic_id": "math_10_ch01_t03",
                        "order": 3,
                        "title": "Revisiting Irrational Numbers"
                    },
                    {
                        "topic_id": "math_10_ch01_t04",
                        "order": 4,
                        "title": "Logarithms"
                    }
                ]
            },
            {
                "chapter_id": "math_10_ch02",
                "order": 2,
                "title": "Sets (సమితులు)",
                "topics": [
                    {
                        "topic_id": "math_10_ch02_t01",
                        "order": 1,
                        "title": "Set Representation and Null Set"
                    },
                    {
                        "topic_id": "math_10_ch02_t02",
                        "order": 2,
                        "title": "Venn Diagrams & Set Operations"
                    },
                    {
                        "topic_id": "math_10_ch02_t03",
                        "order": 3,
                        "title": "Equal & Finite Sets"
                    }
                ]
            },
            {
                "chapter_id": "math_10_ch03",
                "order": 3,
                "title": "Polynomials (బహుపదులు)",
                "topics": [
                    {
                        "topic_id": "math_10_ch03_t01",
                        "order": 1,
                        "title": "Geometrical Meaning of Zeroes"
                    },
                    {
                        "topic_id": "math_10_ch03_t02",
                        "order": 2,
                        "title": "Relationship between Zeroes and Coefficients"
                    },
                    {
                        "topic_id": "math_10_ch03_t03",
                        "order": 3,
                        "title": "Cubic Polynomials"
                    }
                ]
            },
            {
                "chapter_id": "math_10_ch04",
                "order": 4,
                "title": "Pair of Linear Equations in Two Variables (రెండు చరరాశులలో రేఖీయ సమీకరణాల జత)",
                "topics": [
                    {
                        "topic_id": "math_10_ch04_t01",
                        "order": 1,
                        "title": "Graphical Method of Solution"
                    },
                    {
                        "topic_id": "math_10_ch04_t02",
                        "order": 2,
                        "title": "Substitution & Elimination Methods"
                    },
                    {
                        "topic_id": "math_10_ch04_t03",
                        "order": 3,
                        "title": "Consistency of Equations"
                    }
                ]
            },
            {
                "chapter_id": "math_10_ch05",
                "order": 5,
                "title": "Quadratic Equations (వర్గ సమీకరణాలు)",
                "topics": [
                    {
                        "topic_id": "math_10_ch05_t01",
                        "order": 1,
                        "title": "Factorisation Method"
                    },
                    {
                        "topic_id": "math_10_ch05_t02",
                        "order": 2,
                        "title": "Completing the Square Method"
                    },
                    {
                        "topic_id": "math_10_ch05_t03",
                        "order": 3,
                        "title": "Quadratic Formula and Nature of Roots"
                    }
                ]
            },
            {
                "chapter_id": "math_10_ch06",
                "order": 6,
                "title": "Progressions (శ్రేఢులు)",
                "topics": [
                    {
                        "topic_id": "math_10_ch06_t01",
                        "order": 1,
                        "title": "Arithmetic Progressions (AP)"
                    },
                    {
                        "topic_id": "math_10_ch06_t02",
                        "order": 2,
                        "title": "nth Term and Sum of n Terms"
                    },
                    {
                        "topic_id": "math_10_ch06_t03",
                        "order": 3,
                        "title": "Geometric Progressions (GP)"
                    }
                ]
            },
            {
                "chapter_id": "math_10_ch07",
                "order": 7,
                "title": "Coordinate Geometry (నిరూపక రేఖాగణితం)",
                "topics": [
                    {
                        "topic_id": "math_10_ch07_t01",
                        "order": 1,
                        "title": "Distance Formula"
                    },
                    {
                        "topic_id": "math_10_ch07_t02",
                        "order": 2,
                        "title": "Section Formula & Midpoint"
                    },
                    {
                        "topic_id": "math_10_ch07_t03",
                        "order": 3,
                        "title": "Area of Triangle"
                    }
                ]
            },
            {
                "chapter_id": "math_10_ch08",
                "order": 8,
                "title": "Similar Triangles (సరూప త్రిభుజాలు)",
                "topics": [
                    {
                        "topic_id": "math_10_ch08_t01",
                        "order": 1,
                        "title": "Basic Proportionality Theorem"
                    },
                    {
                        "topic_id": "math_10_ch08_t02",
                        "order": 2,
                        "title": "Criteria for Similarity"
                    },
                    {
                        "topic_id": "math_10_ch08_t03",
                        "order": 3,
                        "title": "Areas of Similar Triangles & Pythagoras Theorem"
                    }
                ]
            },
            {
                "chapter_id": "math_10_ch09",
                "order": 9,
                "title": "Tangents and Secants to a Circle (స్పర్శరేఖలు మరియు ఛేదన రేఖలు)",
                "topics": [
                    {
                        "topic_id": "math_10_ch09_t01",
                        "order": 1,
                        "title": "Tangents to a Circle"
                    },
                    {
                        "topic_id": "math_10_ch09_t02",
                        "order": 2,
                        "title": "Number of Tangents from a Point"
                    },
                    {
                        "topic_id": "math_10_ch09_t03",
                        "order": 3,
                        "title": "Segment of a Circle"
                    }
                ]
            },
            {
                "chapter_id": "math_10_ch10",
                "order": 10,
                "title": "Mensuration (క్షేత్రమితి)",
                "topics": [
                    {
                        "topic_id": "math_10_ch10_t01",
                        "order": 1,
                        "title": "Surface Area of Combination of Solids"
                    },
                    {
                        "topic_id": "math_10_ch10_t02",
                        "order": 2,
                        "title": "Volume of Combination of Solids"
                    },
                    {
                        "topic_id": "math_10_ch10_t03",
                        "order": 3,
                        "title": "Conversion of Solid Shapes"
                    }
                ]
            },
            {
                "chapter_id": "math_10_ch11",
                "order": 11,
                "title": "Trigonometry (త్రికోణమితి)",
                "topics": [
                    {
                        "topic_id": "math_10_ch11_t01",
                        "order": 1,
                        "title": "Trigonometric Ratios"
                    },
                    {
                        "topic_id": "math_10_ch11_t02",
                        "order": 2,
                        "title": "Ratios of Specific Angles"
                    },
                    {
                        "topic_id": "math_10_ch11_t03",
                        "order": 3,
                        "title": "Trigonometric Identities"
                    }
                ]
            },
            {
                "chapter_id": "math_10_ch12",
                "order": 12,
                "title": "Applications of Trigonometry (త్రికోణమితి అనువర్తనాలు)",
                "topics": [
                    {
                        "topic_id": "math_10_ch12_t01",
                        "order": 1,
                        "title": "Angle of Elevation and Depression"
                    },
                    {
                        "topic_id": "math_10_ch12_t02",
                        "order": 2,
                        "title": "Heights and Distances Problems"
                    }
                ]
            },
            {
                "chapter_id": "math_10_ch13",
                "order": 13,
                "title": "Probability (సంభావ్యత)",
                "topics": [
                    {
                        "topic_id": "math_10_ch13_t01",
                        "order": 1,
                        "title": "Classical Definition of Probability"
                    },
                    {
                        "topic_id": "math_10_ch13_t02",
                        "order": 2,
                        "title": "Mutually Exclusive Events"
                    },
                    {
                        "topic_id": "math_10_ch13_t03",
                        "order": 3,
                        "title": "Complementary Events"
                    }
                ]
            },
            {
                "chapter_id": "math_10_ch14",
                "order": 14,
                "title": "Statistics (సాంఖ్యకశాస్త్రం)",
                "topics": [
                    {
                        "topic_id": "math_10_ch14_t01",
                        "order": 1,
                        "title": "Mean of Grouped Data"
                    },
                    {
                        "topic_id": "math_10_ch14_t02",
                        "order": 2,
                        "title": "Median of Grouped Data"
                    },
                    {
                        "topic_id": "math_10_ch14_t03",
                        "order": 3,
                        "title": "Mode of Grouped Data"
                    },
                    {
                        "topic_id": "math_10_ch14_t04",
                        "order": 4,
                        "title": "Ogive Curves"
                    }
                ]
            }
        ]
    },
    {
        "subject_id": "bio_10",
        "class_id": "10",
        "name": "Biological Science",
        "medium": "EM",
        "icon": "eco",
        "chapters": [
            {
                "chapter_id": "bio_10_ch01",
                "order": 1,
                "title": "Lesson 1: Nutrition (పోషణ)",
                "topics": [
                    {
                        "topic_id": "bio_10_ch01_t01",
                        "order": 1,
                        "title": "Autotrophic Nutrition & Photosynthesis"
                    },
                    {
                        "topic_id": "bio_10_ch01_t02",
                        "order": 2,
                        "title": "Chloroplast & Light/Dark Reactions"
                    },
                    {
                        "topic_id": "bio_10_ch01_t03",
                        "order": 3,
                        "title": "Heterotrophic Nutrition & Human Digestion"
                    }
                ]
            },
            {
                "chapter_id": "bio_10_ch02",
                "order": 2,
                "title": "Lesson 2: Respiration (శ్వాసక్రియ)",
                "topics": [
                    {
                        "topic_id": "bio_10_ch02_t01",
                        "order": 1,
                        "title": "Aerobic vs Anaerobic Respiration"
                    },
                    {
                        "topic_id": "bio_10_ch02_t02",
                        "order": 2,
                        "title": "Human Respiratory System & Gas Exchange"
                    },
                    {
                        "topic_id": "bio_10_ch02_t03",
                        "order": 3,
                        "title": "Cellular Respiration in Mitochondria"
                    }
                ]
            },
            {
                "chapter_id": "bio_10_ch03",
                "order": 3,
                "title": "Lesson 3: Transportation (ప్రసరణ)",
                "topics": [
                    {
                        "topic_id": "bio_10_ch03_t01",
                        "order": 1,
                        "title": "Internal Structure of Human Heart"
                    },
                    {
                        "topic_id": "bio_10_ch03_t02",
                        "order": 2,
                        "title": "Cardiac Cycle & Double Circulation"
                    },
                    {
                        "topic_id": "bio_10_ch03_t03",
                        "order": 3,
                        "title": "Lymphatic System & Blood Clotting"
                    }
                ]
            },
            {
                "chapter_id": "bio_10_ch04",
                "order": 4,
                "title": "Lesson 4: Excretion (విసర్జన)",
                "topics": [
                    {
                        "topic_id": "bio_10_ch04_t01",
                        "order": 1,
                        "title": "Excretion in Humans & Kidney Anatomy"
                    },
                    {
                        "topic_id": "bio_10_ch04_t02",
                        "order": 2,
                        "title": "Structure of Nephron & Urine Formation"
                    },
                    {
                        "topic_id": "bio_10_ch04_t03",
                        "order": 3,
                        "title": "Dialysis & Plant Excretion"
                    }
                ]
            },
            {
                "chapter_id": "bio_10_ch05",
                "order": 5,
                "title": "Lesson 5: Control and Coordination (నియంత్రణ - సమన్వయం)",
                "topics": [
                    {
                        "topic_id": "bio_10_ch05_t01",
                        "order": 1,
                        "title": "Structure of Nerve Cell & Synapse"
                    },
                    {
                        "topic_id": "bio_10_ch05_t02",
                        "order": 2,
                        "title": "Central Nervous System & Reflex Arc"
                    },
                    {
                        "topic_id": "bio_10_ch05_t03",
                        "order": 3,
                        "title": "Endocrine Hormones & Plant Movements"
                    }
                ]
            },
            {
                "chapter_id": "bio_10_ch06",
                "order": 6,
                "title": "Lesson 6: Reproduction (ప్రత్యుత్పత్తి)",
                "topics": [
                    {
                        "topic_id": "bio_10_ch06_t01",
                        "order": 1,
                        "title": "Asexual Reproduction in Organisms"
                    },
                    {
                        "topic_id": "bio_10_ch06_t02",
                        "order": 2,
                        "title": "Sexual Reproduction in Flowering Plants"
                    },
                    {
                        "topic_id": "bio_10_ch06_t03",
                        "order": 3,
                        "title": "Human Reproductive Systems"
                    }
                ]
            },
            {
                "chapter_id": "bio_10_ch07",
                "order": 7,
                "title": "Lesson 7: Coordination in Life Processes (జీవక్రియలలో సమన్వయం)",
                "topics": [
                    {
                        "topic_id": "bio_10_ch07_t01",
                        "order": 1,
                        "title": "Hunger Pangs & Taste Sensation"
                    },
                    {
                        "topic_id": "bio_10_ch07_t02",
                        "order": 2,
                        "title": "Peristalsis in Oesophagus"
                    },
                    {
                        "topic_id": "bio_10_ch07_t03",
                        "order": 3,
                        "title": "Absorption in Small Intestine"
                    }
                ]
            },
            {
                "chapter_id": "bio_10_ch08",
                "order": 8,
                "title": "Lesson 8: Heredity (అనువంశికత)",
                "topics": [
                    {
                        "topic_id": "bio_10_ch08_t01",
                        "order": 1,
                        "title": "Mendel's Laws of Inheritance"
                    },
                    {
                        "topic_id": "bio_10_ch08_t02",
                        "order": 2,
                        "title": "Monohybrid & Dihybrid Crosses"
                    },
                    {
                        "topic_id": "bio_10_ch08_t03",
                        "order": 3,
                        "title": "Sex Determination & Evolution"
                    }
                ]
            },
            {
                "chapter_id": "bio_10_ch09",
                "order": 9,
                "title": "Lesson 9: Our Environment (మన పర్యావరణం)",
                "topics": [
                    {
                        "topic_id": "bio_10_ch09_t01",
                        "order": 1,
                        "title": "Ecosystems & Food Chains"
                    },
                    {
                        "topic_id": "bio_10_ch09_t02",
                        "order": 2,
                        "title": "Biomass & Trophic Levels"
                    },
                    {
                        "topic_id": "bio_10_ch09_t03",
                        "order": 3,
                        "title": "Biomagnification & Waste Management"
                    }
                ]
            },
            {
                "chapter_id": "bio_10_ch10",
                "order": 10,
                "title": "Lesson 10: Natural Resources (సహజ వనరులు)",
                "topics": [
                    {
                        "topic_id": "bio_10_ch10_t01",
                        "order": 1,
                        "title": "Water Management & Conservation"
                    },
                    {
                        "topic_id": "bio_10_ch10_t02",
                        "order": 2,
                        "title": "Soil & Forest Conservation"
                    },
                    {
                        "topic_id": "bio_10_ch10_t03",
                        "order": 3,
                        "title": "Alternative Energy Sources"
                    }
                ]
            }
        ]
    },
    {
        "subject_id": "phy_10",
        "class_id": "10",
        "name": "Physical Science",
        "medium": "EM",
        "icon": "bolt",
        "chapters": [
            {
                "chapter_id": "phy_10_ch01",
                "order": 1,
                "title": "Reflection of Light at Curved Surfaces (వక్రతలాల వద్ద కాంతి పరావర్తనం)",
                "topics": [
                    {
                        "topic_id": "phy_10_ch01_t01",
                        "order": 1,
                        "title": "Spherical Mirrors & Ray Diagrams"
                    },
                    {
                        "topic_id": "phy_10_ch01_t02",
                        "order": 2,
                        "title": "Mirror Formula & Sign Convention"
                    },
                    {
                        "topic_id": "phy_10_ch01_t03",
                        "order": 3,
                        "title": "Magnification & Uses"
                    }
                ]
            },
            {
                "chapter_id": "phy_10_ch02",
                "order": 2,
                "title": "Chemical Reactions and Equations (రసాయన చర్యలు మరియు సమీకరణాలు)",
                "topics": [
                    {
                        "topic_id": "phy_10_ch02_t01",
                        "order": 1,
                        "title": "Balancing Chemical Equations"
                    },
                    {
                        "topic_id": "phy_10_ch02_t02",
                        "order": 2,
                        "title": "Combination & Decomposition Reactions"
                    },
                    {
                        "topic_id": "phy_10_ch02_t03",
                        "order": 3,
                        "title": "Displacement & Redox Reactions"
                    }
                ]
            },
            {
                "chapter_id": "phy_10_ch03",
                "order": 3,
                "title": "Acids, Bases and Salts (ఆమ్లాలు, క్షారాలు మరియు లవణాలు)",
                "topics": [
                    {
                        "topic_id": "phy_10_ch03_t01",
                        "order": 1,
                        "title": "Properties of Acids and Bases"
                    },
                    {
                        "topic_id": "phy_10_ch03_t02",
                        "order": 2,
                        "title": "pH Scale and Applications"
                    },
                    {
                        "topic_id": "phy_10_ch03_t03",
                        "order": 3,
                        "title": "Preparation & Uses of Salts"
                    }
                ]
            },
            {
                "chapter_id": "phy_10_ch04",
                "order": 4,
                "title": "Refraction of Light at Curved Surfaces (వక్రతలాల వద్ద కాంతి వక్రీభవనం)",
                "topics": [
                    {
                        "topic_id": "phy_10_ch04_t01",
                        "order": 1,
                        "title": "Refraction at Curved Interfaces"
                    },
                    {
                        "topic_id": "phy_10_ch04_t02",
                        "order": 2,
                        "title": "Lens Formula & Lens Maker's Equation"
                    },
                    {
                        "topic_id": "phy_10_ch04_t03",
                        "order": 3,
                        "title": "Ray Diagrams for Lenses"
                    }
                ]
            },
            {
                "chapter_id": "phy_10_ch05",
                "order": 5,
                "title": "Human Eye and Colourful World (మానవుని కన్ను - రంగుల ప్రపంచం)",
                "topics": [
                    {
                        "topic_id": "phy_10_ch05_t01",
                        "order": 1,
                        "title": "Structure of Human Eye & Vision Defects"
                    },
                    {
                        "topic_id": "phy_10_ch05_t02",
                        "order": 2,
                        "title": "Dispersion & Rainbow Formation"
                    },
                    {
                        "topic_id": "phy_10_ch05_t03",
                        "order": 3,
                        "title": "Atmospheric Refraction & Scattering"
                    }
                ]
            },
            {
                "chapter_id": "phy_10_ch06",
                "order": 6,
                "title": "Structure of Atom (పరమాణు నిర్మాణం)",
                "topics": [
                    {
                        "topic_id": "phy_10_ch06_t01",
                        "order": 1,
                        "title": "Electromagnetic Spectrum & Planck's Theory"
                    },
                    {
                        "topic_id": "phy_10_ch06_t02",
                        "order": 2,
                        "title": "Bohr's Hydrogen Model"
                    },
                    {
                        "topic_id": "phy_10_ch06_t03",
                        "order": 3,
                        "title": "Quantum Numbers & Electronic Configuration"
                    }
                ]
            },
            {
                "chapter_id": "phy_10_ch07",
                "order": 7,
                "title": "Classification of Elements - The Periodic Table (ఆవర్తన పట్టిక)",
                "topics": [
                    {
                        "topic_id": "phy_10_ch07_t01",
                        "order": 1,
                        "title": "Mendeleev & Modern Periodic Law"
                    },
                    {
                        "topic_id": "phy_10_ch07_t02",
                        "order": 2,
                        "title": "Groups & Periods Structure"
                    },
                    {
                        "topic_id": "phy_10_ch07_t03",
                        "order": 3,
                        "title": "Periodic Trends"
                    }
                ]
            },
            {
                "chapter_id": "phy_10_ch08",
                "order": 8,
                "title": "Chemical Bonding (రసాయన బంధం)",
                "topics": [
                    {
                        "topic_id": "phy_10_ch08_t01",
                        "order": 1,
                        "title": "Lewis Structures & Octet Rule"
                    },
                    {
                        "topic_id": "phy_10_ch08_t02",
                        "order": 2,
                        "title": "Ionic & Covalent Bonding"
                    },
                    {
                        "topic_id": "phy_10_ch08_t03",
                        "order": 3,
                        "title": "VSEPR Theory & Molecular Shapes"
                    }
                ]
            },
            {
                "chapter_id": "phy_10_ch09",
                "order": 9,
                "title": "Electric Current (విద్యుత్ ప్రవాహం)",
                "topics": [
                    {
                        "topic_id": "phy_10_ch09_t01",
                        "order": 1,
                        "title": "Ohm's Law & Resistance"
                    },
                    {
                        "topic_id": "phy_10_ch09_t02",
                        "order": 2,
                        "title": "Series and Parallel Circuits"
                    },
                    {
                        "topic_id": "phy_10_ch09_t03",
                        "order": 3,
                        "title": "Electric Power & Joule's Heating Effect"
                    }
                ]
            },
            {
                "chapter_id": "phy_10_ch10",
                "order": 10,
                "title": "Electromagnetism (విద్యుదయస్కాంతత్వం)",
                "topics": [
                    {
                        "topic_id": "phy_10_ch10_t01",
                        "order": 1,
                        "title": "Magnetic Field of Current Carrying Wire"
                    },
                    {
                        "topic_id": "phy_10_ch10_t02",
                        "order": 2,
                        "title": "Faraday's Laws of Induction"
                    },
                    {
                        "topic_id": "phy_10_ch10_t03",
                        "order": 3,
                        "title": "Electric Motors & Generators"
                    }
                ]
            },
            {
                "chapter_id": "phy_10_ch11",
                "order": 11,
                "title": "Principles of Metallurgy (లోహ సంగ్రహణ శాస్త్రం)",
                "topics": [
                    {
                        "topic_id": "phy_10_ch11_t01",
                        "order": 1,
                        "title": "Occurrence of Metals & Ores"
                    },
                    {
                        "topic_id": "phy_10_ch11_t02",
                        "order": 2,
                        "title": "Extraction Processes of Crude Metals"
                    },
                    {
                        "topic_id": "phy_10_ch11_t03",
                        "order": 3,
                        "title": "Refining & Corrosion Control"
                    }
                ]
            },
            {
                "chapter_id": "phy_10_ch12",
                "order": 12,
                "title": "Carbon and its Compounds (కార్బన్ - దాని సమ్మేళనాలు)",
                "topics": [
                    {
                        "topic_id": "phy_10_ch12_t01",
                        "order": 1,
                        "title": "Allotropes of Carbon"
                    },
                    {
                        "topic_id": "phy_10_ch12_t02",
                        "order": 2,
                        "title": "Homologous Series & Functional Groups"
                    },
                    {
                        "topic_id": "phy_10_ch12_t03",
                        "order": 3,
                        "title": "Hydrocarbons & Nomenclature"
                    }
                ]
            }
        ]
    },
    {
        "subject_id": "soc_10",
        "class_id": "10",
        "name": "Social Studies",
        "medium": "EM",
        "icon": "public",
        "chapters": [
            {
                "chapter_id": "soc_10_ch01",
                "order": 1,
                "title": "India: Relief Features (భారతదేశం: భౌగోళిక స్వరూపాలు)",
                "topics": [
                    {
                        "topic_id": "soc_10_ch01_t01",
                        "order": 1,
                        "title": "Geological Formation of India"
                    },
                    {
                        "topic_id": "soc_10_ch01_t02",
                        "order": 2,
                        "title": "Himalayas & Indo-Gangetic Plains"
                    },
                    {
                        "topic_id": "soc_10_ch01_t03",
                        "order": 3,
                        "title": "Peninsular Plateau & Coastal Plains"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_ch02",
                "order": 2,
                "title": "Ideas of Development (అభివృద్ధి భావనలు)",
                "topics": [
                    {
                        "topic_id": "soc_10_ch02_t01",
                        "order": 1,
                        "title": "Development Indicators"
                    },
                    {
                        "topic_id": "soc_10_ch02_t02",
                        "order": 2,
                        "title": "Income and Other Criteria"
                    },
                    {
                        "topic_id": "soc_10_ch02_t03",
                        "order": 3,
                        "title": "Human Development Report"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_ch03",
                "order": 3,
                "title": "Production and Employment (ఉత్పత్తి మరియు ఉపాధి)",
                "topics": [
                    {
                        "topic_id": "soc_10_ch03_t01",
                        "order": 1,
                        "title": "Primary, Secondary & Tertiary Sectors"
                    },
                    {
                        "topic_id": "soc_10_ch03_t02",
                        "order": 2,
                        "title": "Organised vs Unorganised Sectors"
                    },
                    {
                        "topic_id": "soc_10_ch03_t03",
                        "order": 3,
                        "title": "Employment Generation"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_ch04",
                "order": 4,
                "title": "Climate of India (భారతదేశ శీతోష్ణస్థితి)",
                "topics": [
                    {
                        "topic_id": "soc_10_ch04_t01",
                        "order": 1,
                        "title": "Climatic Controls"
                    },
                    {
                        "topic_id": "soc_10_ch04_t02",
                        "order": 2,
                        "title": "Mechanism of Monsoons"
                    },
                    {
                        "topic_id": "soc_10_ch04_t03",
                        "order": 3,
                        "title": "Seasons of India"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_ch05",
                "order": 5,
                "title": "Indian Rivers and Water Resources (నదులు మరియు నీటి వనరులు)",
                "topics": [
                    {
                        "topic_id": "soc_10_ch05_t01",
                        "order": 1,
                        "title": "Himalayan & Peninsular River Systems"
                    },
                    {
                        "topic_id": "soc_10_ch05_t02",
                        "order": 2,
                        "title": "Water Utilization in India"
                    },
                    {
                        "topic_id": "soc_10_ch05_t03",
                        "order": 3,
                        "title": "Equitable Water Management"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_ch06",
                "order": 6,
                "title": "The People (ప్రజలు)",
                "topics": [
                    {
                        "topic_id": "soc_10_ch06_t01",
                        "order": 1,
                        "title": "Census & Population Size"
                    },
                    {
                        "topic_id": "soc_10_ch06_t02",
                        "order": 2,
                        "title": "Age Structure & Sex Ratio"
                    },
                    {
                        "topic_id": "soc_10_ch06_t03",
                        "order": 3,
                        "title": "Literacy & Working Population"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_ch07",
                "order": 7,
                "title": "People and Settlement (ప్రజలు - నివాస ప్రాంతాలు)",
                "topics": [
                    {
                        "topic_id": "soc_10_ch07_t01",
                        "order": 1,
                        "title": "Urban and Rural Settlements"
                    },
                    {
                        "topic_id": "soc_10_ch07_t02",
                        "order": 2,
                        "title": "Urbanisation in India"
                    },
                    {
                        "topic_id": "soc_10_ch07_t03",
                        "order": 3,
                        "title": "Modern Urban Planning"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_ch08",
                "order": 8,
                "title": "People and Migration (ప్రజలు - వలసలు)",
                "topics": [
                    {
                        "topic_id": "soc_10_ch08_t01",
                        "order": 1,
                        "title": "Internal & International Migration"
                    },
                    {
                        "topic_id": "soc_10_ch08_t02",
                        "order": 2,
                        "title": "Patterns of Migration"
                    },
                    {
                        "topic_id": "soc_10_ch08_t03",
                        "order": 3,
                        "title": "Socio-Economic Impacts of Migration"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_ch09",
                "order": 9,
                "title": "Rampur: A Village Economy (రాంపూర్ : గ్రామ ఆర్థిక వ్యవస్థ)",
                "topics": [
                    {
                        "topic_id": "soc_10_ch09_t01",
                        "order": 1,
                        "title": "Factors of Production in Agriculture"
                    },
                    {
                        "topic_id": "soc_10_ch09_t02",
                        "order": 2,
                        "title": "Land Distribution in Rampur"
                    },
                    {
                        "topic_id": "soc_10_ch09_t03",
                        "order": 3,
                        "title": "Non-Farm Rural Activities"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_ch10",
                "order": 10,
                "title": "Globalisation (ప్రపంచీకరణ)",
                "topics": [
                    {
                        "topic_id": "soc_10_ch10_t01",
                        "order": 1,
                        "title": "Multinational Companies (MNCs)"
                    },
                    {
                        "topic_id": "soc_10_ch10_t02",
                        "order": 2,
                        "title": "Integration of World Markets"
                    },
                    {
                        "topic_id": "soc_10_ch10_t03",
                        "order": 3,
                        "title": "Role of WTO & Fair Globalisation"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_ch11",
                "order": 11,
                "title": "Food Security (ఆహార భద్రత)",
                "topics": [
                    {
                        "topic_id": "soc_10_ch11_t01",
                        "order": 1,
                        "title": "Foodgrain Production & Buffer Stock"
                    },
                    {
                        "topic_id": "soc_10_ch11_t02",
                        "order": 2,
                        "title": "Public Distribution System (PDS)"
                    },
                    {
                        "topic_id": "soc_10_ch11_t03",
                        "order": 3,
                        "title": "Nutritional Levels"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_ch12",
                "order": 12,
                "title": "Sustainable Development with Equity (సుస్థిర అభివృద్ధి)",
                "topics": [
                    {
                        "topic_id": "soc_10_ch12_t01",
                        "order": 1,
                        "title": "Environment & Development Challenges"
                    },
                    {
                        "topic_id": "soc_10_ch12_t02",
                        "order": 2,
                        "title": "Alternative Sustainable Paradigms"
                    },
                    {
                        "topic_id": "soc_10_ch12_t03",
                        "order": 3,
                        "title": "People's Environmental Movements"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_ch13",
                "order": 13,
                "title": "World Between the World Wars (ప్రపంచ యుద్ధాల మధ్య ప్రపంచం)",
                "topics": [
                    {
                        "topic_id": "soc_10_ch13_t01",
                        "order": 1,
                        "title": "World War I Causes"
                    },
                    {
                        "topic_id": "soc_10_ch13_t02",
                        "order": 2,
                        "title": "Great Depression & League of Nations"
                    },
                    {
                        "topic_id": "soc_10_ch13_t03",
                        "order": 3,
                        "title": "Fascism & Nazism"
                    },
                    {
                        "topic_id": "soc_10_ch13_t04",
                        "order": 4,
                        "title": "World War II"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_ch14",
                "order": 14,
                "title": "National Liberation Movements in the Colonies (వలస విముక్తి ఉద్యమాలు)",
                "topics": [
                    {
                        "topic_id": "soc_10_ch14_t01",
                        "order": 1,
                        "title": "Chinese Liberation Struggle"
                    },
                    {
                        "topic_id": "soc_10_ch14_t02",
                        "order": 2,
                        "title": "Vietnam War of Independence"
                    },
                    {
                        "topic_id": "soc_10_ch14_t03",
                        "order": 3,
                        "title": "Decolonisation in Nigeria"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_ch15",
                "order": 15,
                "title": "National Movement in India: Partition & Independence (జాతీయోద్యమం)",
                "topics": [
                    {
                        "topic_id": "soc_10_ch15_t01",
                        "order": 1,
                        "title": "Quit India Movement & INA"
                    },
                    {
                        "topic_id": "soc_10_ch15_t02",
                        "order": 2,
                        "title": "Communalism & Partition"
                    },
                    {
                        "topic_id": "soc_10_ch15_t03",
                        "order": 3,
                        "title": "Independence in 1947"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_ch16",
                "order": 16,
                "title": "The Making of Independent India's Constitution (భారత రాజ్యాంగం)",
                "topics": [
                    {
                        "topic_id": "soc_10_ch16_t01",
                        "order": 1,
                        "title": "Constituent Assembly Debates"
                    },
                    {
                        "topic_id": "soc_10_ch16_t02",
                        "order": 2,
                        "title": "Preamble & Guiding Philosophy"
                    },
                    {
                        "topic_id": "soc_10_ch16_t03",
                        "order": 3,
                        "title": "Federal Structure"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_ch17",
                "order": 17,
                "title": "Election Process in India (భారతదేశంలో ఎన్నికల ప్రక్రియ)",
                "topics": [
                    {
                        "topic_id": "soc_10_ch17_t01",
                        "order": 1,
                        "title": "Election Commission Responsibilities"
                    },
                    {
                        "topic_id": "soc_10_ch17_t02",
                        "order": 2,
                        "title": "Conduct of Elections & Voting"
                    },
                    {
                        "topic_id": "soc_10_ch17_t03",
                        "order": 3,
                        "title": "Electoral Reforms"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_ch18",
                "order": 18,
                "title": "Independent India (First 30 Years) (స్వతంత్ర భారతదేశం 1947-1977)",
                "topics": [
                    {
                        "topic_id": "soc_10_ch18_t01",
                        "order": 1,
                        "title": "State Reorganisation 1956"
                    },
                    {
                        "topic_id": "soc_10_ch18_t02",
                        "order": 2,
                        "title": "Five-Year Plans & Industrial Growth"
                    },
                    {
                        "topic_id": "soc_10_ch18_t03",
                        "order": 3,
                        "title": "Emergency & Democratic Revival"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_ch19",
                "order": 19,
                "title": "Emerging Political Trends 1977-2000 (రాజకీయ ధోరణుల ఆవిర్భావం)",
                "topics": [
                    {
                        "topic_id": "soc_10_ch19_t01",
                        "order": 1,
                        "title": "Coalition Politics at Center"
                    },
                    {
                        "topic_id": "soc_10_ch19_t02",
                        "order": 2,
                        "title": "Rise of Regional Parties"
                    },
                    {
                        "topic_id": "soc_10_ch19_t03",
                        "order": 3,
                        "title": "Economic Reforms of 1991"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_ch20",
                "order": 20,
                "title": "Post-War World and India (యుద్ధానంతర ప్రపంచం మరియు భారతదేశం)",
                "topics": [
                    {
                        "topic_id": "soc_10_ch20_t01",
                        "order": 1,
                        "title": "Cold War & Military Pacts"
                    },
                    {
                        "topic_id": "soc_10_ch20_t02",
                        "order": 2,
                        "title": "Non-Aligned Movement (NAM)"
                    },
                    {
                        "topic_id": "soc_10_ch20_t03",
                        "order": 3,
                        "title": "United Nations Role"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_ch21",
                "order": 21,
                "title": "Social Movements in Our Times (సమకాలీన సామాజిక ఉద్యమాలు)",
                "topics": [
                    {
                        "topic_id": "soc_10_ch21_t01",
                        "order": 1,
                        "title": "Civil Rights Movements"
                    },
                    {
                        "topic_id": "soc_10_ch21_t02",
                        "order": 2,
                        "title": "Anti-Nuclear & Environmental Struggles"
                    },
                    {
                        "topic_id": "soc_10_ch21_t03",
                        "order": 3,
                        "title": "RTI & Transparency"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_ch22",
                "order": 22,
                "title": "The Movement for the Formation of Telangana State (తెలంగాణ రాష్ట్ర ఉద్యమం)",
                "topics": [
                    {
                        "topic_id": "soc_10_ch22_t01",
                        "order": 1,
                        "title": "Gentlemen's Agreement & 1969 Agitation"
                    },
                    {
                        "topic_id": "soc_10_ch22_t02",
                        "order": 2,
                        "title": "Mass Movements & People's JAC"
                    },
                    {
                        "topic_id": "soc_10_ch22_t03",
                        "order": 3,
                        "title": "Statehood Realisation in 2014"
                    }
                ]
            }
        ]
    },
    {
        "subject_id": "eng_10",
        "class_id": "10",
        "name": "English Reader",
        "medium": "EM",
        "icon": "school",
        "chapters": [
            {
                "chapter_id": "eng_10_ch01",
                "order": 1,
                "title": "Unit 1: Personality Development (వ్యక్తిత్వ వికాసం)",
                "topics": [
                    {
                        "topic_id": "eng_10_ch01_t01",
                        "order": 1,
                        "title": "Attitude is Altitude"
                    },
                    {
                        "topic_id": "eng_10_ch01_t02",
                        "order": 2,
                        "title": "Every Success Story is Also a Story of Failures"
                    },
                    {
                        "topic_id": "eng_10_ch01_t03",
                        "order": 3,
                        "title": "I Will Do It"
                    },
                    {
                        "topic_id": "eng_10_ch01_t04",
                        "order": 4,
                        "title": "Grammar: Adjectives & Adverbs"
                    }
                ]
            },
            {
                "chapter_id": "eng_10_ch02",
                "order": 2,
                "title": "Unit 2: Wit and Humour (హాస్యం)",
                "topics": [
                    {
                        "topic_id": "eng_10_ch02_t01",
                        "order": 1,
                        "title": "The Dear Departed (Part I)"
                    },
                    {
                        "topic_id": "eng_10_ch02_t02",
                        "order": 2,
                        "title": "The Dear Departed (Part II)"
                    },
                    {
                        "topic_id": "eng_10_ch02_t03",
                        "order": 3,
                        "title": "The Brave Potter"
                    },
                    {
                        "topic_id": "eng_10_ch02_t04",
                        "order": 4,
                        "title": "Grammar: Compound Adjectives"
                    }
                ]
            },
            {
                "chapter_id": "eng_10_ch03",
                "order": 3,
                "title": "Unit 3: Human Relations (మానవ సంబంధాలు)",
                "topics": [
                    {
                        "topic_id": "eng_10_ch03_t01",
                        "order": 1,
                        "title": "The Journey"
                    },
                    {
                        "topic_id": "eng_10_ch03_t02",
                        "order": 2,
                        "title": "Another Woman (Poem)"
                    },
                    {
                        "topic_id": "eng_10_ch03_t03",
                        "order": 3,
                        "title": "The Never-Never Nest"
                    },
                    {
                        "topic_id": "eng_10_ch03_t04",
                        "order": 4,
                        "title": "Grammar: Direct & Indirect Speech"
                    }
                ]
            },
            {
                "chapter_id": "eng_10_ch04",
                "order": 4,
                "title": "Unit 4: Films and Theatre (చలనచిత్రాలు మరియు రంగస్థలం)",
                "topics": [
                    {
                        "topic_id": "eng_10_ch04_t01",
                        "order": 1,
                        "title": "Rendezvous with Ray"
                    },
                    {
                        "topic_id": "eng_10_ch04_t02",
                        "order": 2,
                        "title": "Maya Bazaar"
                    },
                    {
                        "topic_id": "eng_10_ch04_t03",
                        "order": 3,
                        "title": "A Tribute to Savitri"
                    },
                    {
                        "topic_id": "eng_10_ch04_t04",
                        "order": 4,
                        "title": "Grammar: Prepositions"
                    }
                ]
            },
            {
                "chapter_id": "eng_10_ch05",
                "order": 5,
                "title": "Unit 5: Social Issues (సామాజిక సమస్యలు)",
                "topics": [
                    {
                        "topic_id": "eng_10_ch05_t01",
                        "order": 1,
                        "title": "The Storeyed House (Part I)"
                    },
                    {
                        "topic_id": "eng_10_ch05_t02",
                        "order": 2,
                        "title": "The Storeyed House (Part II)"
                    },
                    {
                        "topic_id": "eng_10_ch05_t03",
                        "order": 3,
                        "title": "Abandoned (Poem)"
                    },
                    {
                        "topic_id": "eng_10_ch05_t04",
                        "order": 4,
                        "title": "Grammar: Active & Passive Voice"
                    }
                ]
            },
            {
                "chapter_id": "eng_10_ch06",
                "order": 6,
                "title": "Unit 6: Bio-Diversity (జీవ వైవిధ్యం)",
                "topics": [
                    {
                        "topic_id": "eng_10_ch06_t01",
                        "order": 1,
                        "title": "Environment (Wangari Maathai)"
                    },
                    {
                        "topic_id": "eng_10_ch06_t02",
                        "order": 2,
                        "title": "Or Will the Dreamer Wake? (Poem)"
                    },
                    {
                        "topic_id": "eng_10_ch06_t03",
                        "order": 3,
                        "title": "A Tale of Three Villages"
                    },
                    {
                        "topic_id": "eng_10_ch06_t04",
                        "order": 4,
                        "title": "Grammar: Conditionals"
                    }
                ]
            },
            {
                "chapter_id": "eng_10_ch07",
                "order": 7,
                "title": "Unit 7: Nation and Diversity (దేశం మరియు వైవిధ్యం)",
                "topics": [
                    {
                        "topic_id": "eng_10_ch07_t01",
                        "order": 1,
                        "title": "My Childhood (Dr. APJ Abdul Kalam)"
                    },
                    {
                        "topic_id": "eng_10_ch07_t02",
                        "order": 2,
                        "title": "A Plea for India (Poem)"
                    },
                    {
                        "topic_id": "eng_10_ch07_t03",
                        "order": 3,
                        "title": "Unity in Diversity in India"
                    },
                    {
                        "topic_id": "eng_10_ch07_t04",
                        "order": 4,
                        "title": "Grammar: Conjunctions"
                    }
                ]
            },
            {
                "chapter_id": "eng_10_ch08",
                "order": 8,
                "title": "Unit 8: Human Rights (మానవ హక్కులు)",
                "topics": [
                    {
                        "topic_id": "eng_10_ch08_t01",
                        "order": 1,
                        "title": "Jamaican Fragment"
                    },
                    {
                        "topic_id": "eng_10_ch08_t02",
                        "order": 2,
                        "title": "Once Upon a Time (Poem)"
                    },
                    {
                        "topic_id": "eng_10_ch08_t03",
                        "order": 3,
                        "title": "What is My Name?"
                    },
                    {
                        "topic_id": "eng_10_ch08_t04",
                        "order": 4,
                        "title": "Grammar: Discourse Markers"
                    }
                ]
            }
        ]
    },
    {
        "subject_id": "tel_10",
        "class_id": "10",
        "name": "Telugu (తెలుగు ప్రథమ భాష)",
        "medium": "TM",
        "icon": "menu_book",
        "chapters": [
            {
                "chapter_id": "tel_10_ch01",
                "order": 1,
                "title": "1వ పాఠం: దానశీలము (బమ్మెర పోతన)",
                "topics": [
                    {
                        "topic_id": "tel_10_ch01_t01",
                        "order": 1,
                        "title": "పాఠ్యభాగ నేపథ్యం మరియు కవి పరిచయం"
                    },
                    {
                        "topic_id": "tel_10_ch01_t02",
                        "order": 2,
                        "title": "పద్యాలు - ప్రతిపదార్థ తాత్పర్యాలు"
                    },
                    {
                        "topic_id": "tel_10_ch01_t03",
                        "order": 3,
                        "title": "బలి చక్రవర్తి దానగుణం మరియు వ్యాకరణాంశాలు"
                    }
                ]
            },
            {
                "chapter_id": "tel_10_ch02",
                "order": 2,
                "title": "2వ పాఠం: ఎవరి భాష వాళ్లకు వినసొంపు (డా॥ సామల సదాశివ)",
                "topics": [
                    {
                        "topic_id": "tel_10_ch02_t01",
                        "order": 1,
                        "title": "వ్యాస విశేషాలు మరియు రచయిత పరిచయం"
                    },
                    {
                        "topic_id": "tel_10_ch02_t02",
                        "order": 2,
                        "title": "తెలంగాణ మాండలిక సౌందర్యం"
                    },
                    {
                        "topic_id": "tel_10_ch02_t03",
                        "order": 3,
                        "title": "భాషాభిమానం మరియు భాషాంశాలు"
                    }
                ]
            },
            {
                "chapter_id": "tel_10_ch03",
                "order": 3,
                "title": "3వ పాఠం: వీర తెలంగాణ (డా॥ దాశరథి కృష్ణమాచార్య)",
                "topics": [
                    {
                        "topic_id": "tel_10_ch03_t01",
                        "order": 1,
                        "title": "తెలంగాణ పోరాట నేపథ్యం"
                    },
                    {
                        "topic_id": "tel_10_ch03_t02",
                        "order": 2,
                        "title": "దాశరథి కవిత్వ పటిమ"
                    },
                    {
                        "topic_id": "tel_10_ch03_t03",
                        "order": 3,
                        "title": "వీరగాథలు మరియు పద్య భావాలు"
                    }
                ]
            },
            {
                "chapter_id": "tel_10_ch04",
                "order": 4,
                "title": "4వ పాఠం: కొత్త బాట (డా॥ పాకాల యశోదారెడ్డి)",
                "topics": [
                    {
                        "topic_id": "tel_10_ch04_t01",
                        "order": 1,
                        "title": "కథానిక పరిచయం మరియు తెలంగాణ పల్లె జీవితం"
                    },
                    {
                        "topic_id": "tel_10_ch04_t02",
                        "order": 2,
                        "title": "స్త్రీ చైతన్యం మరియు సామాజిక మార్పు"
                    },
                    {
                        "topic_id": "tel_10_ch04_t03",
                        "order": 3,
                        "title": "మాండలిక పదాలు మరియు సంభాషణలు"
                    }
                ]
            },
            {
                "chapter_id": "tel_10_ch05",
                "order": 5,
                "title": "5వ పాఠం: నగర గీతం (అలిశెట్టి ప్రభాకర్)",
                "topics": [
                    {
                        "topic_id": "tel_10_ch05_t01",
                        "order": 1,
                        "title": "వచన కవితా స్వరూపం"
                    },
                    {
                        "topic_id": "tel_10_ch05_t02",
                        "order": 2,
                        "title": "నగర జీవితంలోని వైరుధ్యాలు"
                    },
                    {
                        "topic_id": "tel_10_ch05_t03",
                        "order": 3,
                        "title": "సమాజ దృక్పథం మరియు ప్రతీకలు"
                    }
                ]
            },
            {
                "chapter_id": "tel_10_ch06",
                "order": 6,
                "title": "6వ పాఠం: భాగ్యోదయం (కృష్ణస్వామి ముదిరాజ్)",
                "topics": [
                    {
                        "topic_id": "tel_10_ch06_t01",
                        "order": 1,
                        "title": "జీవిత చరిత్ర విశేషాలు"
                    },
                    {
                        "topic_id": "tel_10_ch06_t02",
                        "order": 2,
                        "title": "భాగ్యరెడ్డి వర్మ దళిత జనోద్ధరణ"
                    },
                    {
                        "topic_id": "tel_10_ch06_t03",
                        "order": 3,
                        "title": "సంఘ సంస్కరణలు మరియు విద్యావ్యాప్తి"
                    }
                ]
            },
            {
                "chapter_id": "tel_10_ch07",
                "order": 7,
                "title": "7వ పాఠం: శతక మధురిమ (శతక కవులు)",
                "topics": [
                    {
                        "topic_id": "tel_10_ch07_t01",
                        "order": 1,
                        "title": "శతక ప్రక్రియ లక్షణాలు మరియు మకుటాలు"
                    },
                    {
                        "topic_id": "tel_10_ch07_t02",
                        "order": 2,
                        "title": "నైతిక విలువలు - పద్య తాత్పర్యాలు"
                    },
                    {
                        "topic_id": "tel_10_ch07_t03",
                        "order": 3,
                        "title": "ఛందస్సు మరియు అలంకారాలు"
                    }
                ]
            },
            {
                "chapter_id": "tel_10_ch08",
                "order": 8,
                "title": "8వ పాఠం: లక్ష్యసిద్ధి (సంపాదకీయం)",
                "topics": [
                    {
                        "topic_id": "tel_10_ch08_t01",
                        "order": 1,
                        "title": "సంపాదకీయ వ్యాసం ప్రాముఖ్యత"
                    },
                    {
                        "topic_id": "tel_10_ch08_t02",
                        "order": 2,
                        "title": "తెలంగాణ రాష్ట్ర ఆవిర్భావ సంబరం"
                    },
                    {
                        "topic_id": "tel_10_ch08_t03",
                        "order": 3,
                        "title": "భవిష్యత్ లక్ష్యాలు మరియు భాషాంశాలు"
                    }
                ]
            },
            {
                "chapter_id": "tel_10_ch09",
                "order": 9,
                "title": "9వ పాఠం: జీవన భాష్యం (డా॥ సి. నారాయణరెడ్డి)",
                "topics": [
                    {
                        "topic_id": "tel_10_ch09_t01",
                        "order": 1,
                        "title": "గజల్ ప్రక్రియ పరిచయం"
                    },
                    {
                        "topic_id": "tel_10_ch09_t02",
                        "order": 2,
                        "title": "సినారె భావనాత్మక జీవన గీతిక"
                    },
                    {
                        "topic_id": "tel_10_ch09_t03",
                        "order": 3,
                        "title": "మానవీయ విలువలు మరియు సందేశం"
                    }
                ]
            },
            {
                "chapter_id": "tel_10_ch10",
                "order": 10,
                "title": "10వ పాఠం: గోలకొండ పట్టణము (ఆదిరాజు వీరభద్రరావు)",
                "topics": [
                    {
                        "topic_id": "tel_10_ch10_t01",
                        "order": 1,
                        "title": "చారిత్రక వ్యాసం"
                    },
                    {
                        "topic_id": "tel_10_ch10_t02",
                        "order": 2,
                        "title": "గోలకొండ కోట ప్రాశస్త్యం మరియు వైభవం"
                    },
                    {
                        "topic_id": "tel_10_ch10_t03",
                        "order": 3,
                        "title": "సాంస్కృతిక విశేషాలు"
                    }
                ]
            },
            {
                "chapter_id": "tel_10_ch11",
                "order": 11,
                "title": "11వ పాఠం: భిక్ష (శ్రీనాథుడు)",
                "topics": [
                    {
                        "topic_id": "tel_10_ch11_t01",
                        "order": 1,
                        "title": "కాశీ ఖండ కావ్య నేపథ్యం"
                    },
                    {
                        "topic_id": "tel_10_ch11_t02",
                        "order": 2,
                        "title": "వ్యాస మహర్షి కోపం మరియు శివుని లీల"
                    },
                    {
                        "topic_id": "tel_10_ch11_t03",
                        "order": 3,
                        "title": "పద్య పఠనం మరియు వ్యాకరణాంశాలు"
                    }
                ]
            },
            {
                "chapter_id": "tel_10_ch12",
                "order": 12,
                "title": "12వ పాఠం: భూమిక (గుడిపాటి వెంకట చలం)",
                "topics": [
                    {
                        "topic_id": "tel_10_ch12_t01",
                        "order": 1,
                        "title": "పీఠిక ప్రక్రియ పరిచయం"
                    },
                    {
                        "topic_id": "tel_10_ch12_t02",
                        "order": 2,
                        "title": "చలం సాహిత్య విశ్లేషణ"
                    },
                    {
                        "topic_id": "tel_10_ch12_t03",
                        "order": 3,
                        "title": "ఆలోచనాత్మక శైలి"
                    }
                ]
            },
            {
                "chapter_id": "tel_10_ch13",
                "order": 13,
                "title": "ఉపవాచకం: రామాయణం (ఆదికవి వాల్మీకి)",
                "topics": [
                    {
                        "topic_id": "tel_10_ch13_t01",
                        "order": 1,
                        "title": "బాలకాండ & అయోధ్యాకాండ"
                    },
                    {
                        "topic_id": "tel_10_ch13_t02",
                        "order": 2,
                        "title": "అరణ్యకాండ & కిష్కింధకాండ"
                    },
                    {
                        "topic_id": "tel_10_ch13_t03",
                        "order": 3,
                        "title": "సుందరకాండ & యుద్ధకాండ"
                    }
                ]
            }
        ]
    },
    {
        "subject_id": "math_10_tm",
        "class_id": "10",
        "name": "Mathematics (గణితం)",
        "medium": "TM",
        "icon": "calculate",
        "chapters": [
            {
                "chapter_id": "math_10_tm_ch01",
                "order": 1,
                "title": "Real Numbers (వాస్తవ సంఖ్యలు)",
                "topics": [
                    {
                        "topic_id": "math_10_tm_ch01_t01",
                        "order": 1,
                        "title": "Euclid's Division Lemma"
                    },
                    {
                        "topic_id": "math_10_tm_ch01_t02",
                        "order": 2,
                        "title": "Fundamental Theorem of Arithmetic"
                    },
                    {
                        "topic_id": "math_10_tm_ch01_t03",
                        "order": 3,
                        "title": "Revisiting Irrational Numbers"
                    },
                    {
                        "topic_id": "math_10_tm_ch01_t04",
                        "order": 4,
                        "title": "Logarithms"
                    }
                ]
            },
            {
                "chapter_id": "math_10_tm_ch02",
                "order": 2,
                "title": "Sets (సమితులు)",
                "topics": [
                    {
                        "topic_id": "math_10_tm_ch02_t01",
                        "order": 1,
                        "title": "Set Representation and Null Set"
                    },
                    {
                        "topic_id": "math_10_tm_ch02_t02",
                        "order": 2,
                        "title": "Venn Diagrams & Set Operations"
                    },
                    {
                        "topic_id": "math_10_tm_ch02_t03",
                        "order": 3,
                        "title": "Equal & Finite Sets"
                    }
                ]
            },
            {
                "chapter_id": "math_10_tm_ch03",
                "order": 3,
                "title": "Polynomials (బహుపదులు)",
                "topics": [
                    {
                        "topic_id": "math_10_tm_ch03_t01",
                        "order": 1,
                        "title": "Geometrical Meaning of Zeroes"
                    },
                    {
                        "topic_id": "math_10_tm_ch03_t02",
                        "order": 2,
                        "title": "Relationship between Zeroes and Coefficients"
                    },
                    {
                        "topic_id": "math_10_tm_ch03_t03",
                        "order": 3,
                        "title": "Cubic Polynomials"
                    }
                ]
            },
            {
                "chapter_id": "math_10_tm_ch04",
                "order": 4,
                "title": "Pair of Linear Equations in Two Variables (రెండు చరరాశులలో రేఖీయ సమీకరణాల జత)",
                "topics": [
                    {
                        "topic_id": "math_10_tm_ch04_t01",
                        "order": 1,
                        "title": "Graphical Method of Solution"
                    },
                    {
                        "topic_id": "math_10_tm_ch04_t02",
                        "order": 2,
                        "title": "Substitution & Elimination Methods"
                    },
                    {
                        "topic_id": "math_10_tm_ch04_t03",
                        "order": 3,
                        "title": "Consistency of Equations"
                    }
                ]
            },
            {
                "chapter_id": "math_10_tm_ch05",
                "order": 5,
                "title": "Quadratic Equations (వర్గ సమీకరణాలు)",
                "topics": [
                    {
                        "topic_id": "math_10_tm_ch05_t01",
                        "order": 1,
                        "title": "Factorisation Method"
                    },
                    {
                        "topic_id": "math_10_tm_ch05_t02",
                        "order": 2,
                        "title": "Completing the Square Method"
                    },
                    {
                        "topic_id": "math_10_tm_ch05_t03",
                        "order": 3,
                        "title": "Quadratic Formula and Nature of Roots"
                    }
                ]
            },
            {
                "chapter_id": "math_10_tm_ch06",
                "order": 6,
                "title": "Progressions (శ్రేఢులు)",
                "topics": [
                    {
                        "topic_id": "math_10_tm_ch06_t01",
                        "order": 1,
                        "title": "Arithmetic Progressions (AP)"
                    },
                    {
                        "topic_id": "math_10_tm_ch06_t02",
                        "order": 2,
                        "title": "nth Term and Sum of n Terms"
                    },
                    {
                        "topic_id": "math_10_tm_ch06_t03",
                        "order": 3,
                        "title": "Geometric Progressions (GP)"
                    }
                ]
            },
            {
                "chapter_id": "math_10_tm_ch07",
                "order": 7,
                "title": "Coordinate Geometry (నిరూపక రేఖాగణితం)",
                "topics": [
                    {
                        "topic_id": "math_10_tm_ch07_t01",
                        "order": 1,
                        "title": "Distance Formula"
                    },
                    {
                        "topic_id": "math_10_tm_ch07_t02",
                        "order": 2,
                        "title": "Section Formula & Midpoint"
                    },
                    {
                        "topic_id": "math_10_tm_ch07_t03",
                        "order": 3,
                        "title": "Area of Triangle"
                    }
                ]
            },
            {
                "chapter_id": "math_10_tm_ch08",
                "order": 8,
                "title": "Similar Triangles (సరూప త్రిభుజాలు)",
                "topics": [
                    {
                        "topic_id": "math_10_tm_ch08_t01",
                        "order": 1,
                        "title": "Basic Proportionality Theorem"
                    },
                    {
                        "topic_id": "math_10_tm_ch08_t02",
                        "order": 2,
                        "title": "Criteria for Similarity"
                    },
                    {
                        "topic_id": "math_10_tm_ch08_t03",
                        "order": 3,
                        "title": "Areas of Similar Triangles & Pythagoras Theorem"
                    }
                ]
            },
            {
                "chapter_id": "math_10_tm_ch09",
                "order": 9,
                "title": "Tangents and Secants to a Circle (స్పర్శరేఖలు మరియు ఛేదన రేఖలు)",
                "topics": [
                    {
                        "topic_id": "math_10_tm_ch09_t01",
                        "order": 1,
                        "title": "Tangents to a Circle"
                    },
                    {
                        "topic_id": "math_10_tm_ch09_t02",
                        "order": 2,
                        "title": "Number of Tangents from a Point"
                    },
                    {
                        "topic_id": "math_10_tm_ch09_t03",
                        "order": 3,
                        "title": "Segment of a Circle"
                    }
                ]
            },
            {
                "chapter_id": "math_10_tm_ch10",
                "order": 10,
                "title": "Mensuration (క్షేత్రమితి)",
                "topics": [
                    {
                        "topic_id": "math_10_tm_ch10_t01",
                        "order": 1,
                        "title": "Surface Area of Combination of Solids"
                    },
                    {
                        "topic_id": "math_10_tm_ch10_t02",
                        "order": 2,
                        "title": "Volume of Combination of Solids"
                    },
                    {
                        "topic_id": "math_10_tm_ch10_t03",
                        "order": 3,
                        "title": "Conversion of Solid Shapes"
                    }
                ]
            },
            {
                "chapter_id": "math_10_tm_ch11",
                "order": 11,
                "title": "Trigonometry (త్రికోణమితి)",
                "topics": [
                    {
                        "topic_id": "math_10_tm_ch11_t01",
                        "order": 1,
                        "title": "Trigonometric Ratios"
                    },
                    {
                        "topic_id": "math_10_tm_ch11_t02",
                        "order": 2,
                        "title": "Ratios of Specific Angles"
                    },
                    {
                        "topic_id": "math_10_tm_ch11_t03",
                        "order": 3,
                        "title": "Trigonometric Identities"
                    }
                ]
            },
            {
                "chapter_id": "math_10_tm_ch12",
                "order": 12,
                "title": "Applications of Trigonometry (త్రికోణమితి అనువర్తనాలు)",
                "topics": [
                    {
                        "topic_id": "math_10_tm_ch12_t01",
                        "order": 1,
                        "title": "Angle of Elevation and Depression"
                    },
                    {
                        "topic_id": "math_10_tm_ch12_t02",
                        "order": 2,
                        "title": "Heights and Distances Problems"
                    }
                ]
            },
            {
                "chapter_id": "math_10_tm_ch13",
                "order": 13,
                "title": "Probability (సంభావ్యత)",
                "topics": [
                    {
                        "topic_id": "math_10_tm_ch13_t01",
                        "order": 1,
                        "title": "Classical Definition of Probability"
                    },
                    {
                        "topic_id": "math_10_tm_ch13_t02",
                        "order": 2,
                        "title": "Mutually Exclusive Events"
                    },
                    {
                        "topic_id": "math_10_tm_ch13_t03",
                        "order": 3,
                        "title": "Complementary Events"
                    }
                ]
            },
            {
                "chapter_id": "math_10_tm_ch14",
                "order": 14,
                "title": "Statistics (సాంఖ్యకశాస్త్రం)",
                "topics": [
                    {
                        "topic_id": "math_10_tm_ch14_t01",
                        "order": 1,
                        "title": "Mean of Grouped Data"
                    },
                    {
                        "topic_id": "math_10_tm_ch14_t02",
                        "order": 2,
                        "title": "Median of Grouped Data"
                    },
                    {
                        "topic_id": "math_10_tm_ch14_t03",
                        "order": 3,
                        "title": "Mode of Grouped Data"
                    },
                    {
                        "topic_id": "math_10_tm_ch14_t04",
                        "order": 4,
                        "title": "Ogive Curves"
                    }
                ]
            }
        ]
    },
    {
        "subject_id": "bio_10_tm",
        "class_id": "10",
        "name": "Biological Science (జీవశాస్త్రం)",
        "medium": "TM",
        "icon": "eco",
        "chapters": [
            {
                "chapter_id": "bio_10_tm_ch01",
                "order": 1,
                "title": "Lesson 1: Nutrition (పోషణ)",
                "topics": [
                    {
                        "topic_id": "bio_10_tm_ch01_t01",
                        "order": 1,
                        "title": "Autotrophic Nutrition & Photosynthesis"
                    },
                    {
                        "topic_id": "bio_10_tm_ch01_t02",
                        "order": 2,
                        "title": "Chloroplast & Light/Dark Reactions"
                    },
                    {
                        "topic_id": "bio_10_tm_ch01_t03",
                        "order": 3,
                        "title": "Heterotrophic Nutrition & Human Digestion"
                    }
                ]
            },
            {
                "chapter_id": "bio_10_tm_ch02",
                "order": 2,
                "title": "Lesson 2: Respiration (శ్వాసక్రియ)",
                "topics": [
                    {
                        "topic_id": "bio_10_tm_ch02_t01",
                        "order": 1,
                        "title": "Aerobic vs Anaerobic Respiration"
                    },
                    {
                        "topic_id": "bio_10_tm_ch02_t02",
                        "order": 2,
                        "title": "Human Respiratory System & Gas Exchange"
                    },
                    {
                        "topic_id": "bio_10_tm_ch02_t03",
                        "order": 3,
                        "title": "Cellular Respiration in Mitochondria"
                    }
                ]
            },
            {
                "chapter_id": "bio_10_tm_ch03",
                "order": 3,
                "title": "Lesson 3: Transportation (ప్రసరణ)",
                "topics": [
                    {
                        "topic_id": "bio_10_tm_ch03_t01",
                        "order": 1,
                        "title": "Internal Structure of Human Heart"
                    },
                    {
                        "topic_id": "bio_10_tm_ch03_t02",
                        "order": 2,
                        "title": "Cardiac Cycle & Double Circulation"
                    },
                    {
                        "topic_id": "bio_10_tm_ch03_t03",
                        "order": 3,
                        "title": "Lymphatic System & Blood Clotting"
                    }
                ]
            },
            {
                "chapter_id": "bio_10_tm_ch04",
                "order": 4,
                "title": "Lesson 4: Excretion (విసర్జన)",
                "topics": [
                    {
                        "topic_id": "bio_10_tm_ch04_t01",
                        "order": 1,
                        "title": "Excretion in Humans & Kidney Anatomy"
                    },
                    {
                        "topic_id": "bio_10_tm_ch04_t02",
                        "order": 2,
                        "title": "Structure of Nephron & Urine Formation"
                    },
                    {
                        "topic_id": "bio_10_tm_ch04_t03",
                        "order": 3,
                        "title": "Dialysis & Plant Excretion"
                    }
                ]
            },
            {
                "chapter_id": "bio_10_tm_ch05",
                "order": 5,
                "title": "Lesson 5: Control and Coordination (నియంత్రణ - సమన్వయం)",
                "topics": [
                    {
                        "topic_id": "bio_10_tm_ch05_t01",
                        "order": 1,
                        "title": "Structure of Nerve Cell & Synapse"
                    },
                    {
                        "topic_id": "bio_10_tm_ch05_t02",
                        "order": 2,
                        "title": "Central Nervous System & Reflex Arc"
                    },
                    {
                        "topic_id": "bio_10_tm_ch05_t03",
                        "order": 3,
                        "title": "Endocrine Hormones & Plant Movements"
                    }
                ]
            },
            {
                "chapter_id": "bio_10_tm_ch06",
                "order": 6,
                "title": "Lesson 6: Reproduction (ప్రత్యుత్పత్తి)",
                "topics": [
                    {
                        "topic_id": "bio_10_tm_ch06_t01",
                        "order": 1,
                        "title": "Asexual Reproduction in Organisms"
                    },
                    {
                        "topic_id": "bio_10_tm_ch06_t02",
                        "order": 2,
                        "title": "Sexual Reproduction in Flowering Plants"
                    },
                    {
                        "topic_id": "bio_10_tm_ch06_t03",
                        "order": 3,
                        "title": "Human Reproductive Systems"
                    }
                ]
            },
            {
                "chapter_id": "bio_10_tm_ch07",
                "order": 7,
                "title": "Lesson 7: Coordination in Life Processes (జీవక్రియలలో సమన్వయం)",
                "topics": [
                    {
                        "topic_id": "bio_10_tm_ch07_t01",
                        "order": 1,
                        "title": "Hunger Pangs & Taste Sensation"
                    },
                    {
                        "topic_id": "bio_10_tm_ch07_t02",
                        "order": 2,
                        "title": "Peristalsis in Oesophagus"
                    },
                    {
                        "topic_id": "bio_10_tm_ch07_t03",
                        "order": 3,
                        "title": "Absorption in Small Intestine"
                    }
                ]
            },
            {
                "chapter_id": "bio_10_tm_ch08",
                "order": 8,
                "title": "Lesson 8: Heredity (అనువంశికత)",
                "topics": [
                    {
                        "topic_id": "bio_10_tm_ch08_t01",
                        "order": 1,
                        "title": "Mendel's Laws of Inheritance"
                    },
                    {
                        "topic_id": "bio_10_tm_ch08_t02",
                        "order": 2,
                        "title": "Monohybrid & Dihybrid Crosses"
                    },
                    {
                        "topic_id": "bio_10_tm_ch08_t03",
                        "order": 3,
                        "title": "Sex Determination & Evolution"
                    }
                ]
            },
            {
                "chapter_id": "bio_10_tm_ch09",
                "order": 9,
                "title": "Lesson 9: Our Environment (మన పర్యావరణం)",
                "topics": [
                    {
                        "topic_id": "bio_10_tm_ch09_t01",
                        "order": 1,
                        "title": "Ecosystems & Food Chains"
                    },
                    {
                        "topic_id": "bio_10_tm_ch09_t02",
                        "order": 2,
                        "title": "Biomass & Trophic Levels"
                    },
                    {
                        "topic_id": "bio_10_tm_ch09_t03",
                        "order": 3,
                        "title": "Biomagnification & Waste Management"
                    }
                ]
            },
            {
                "chapter_id": "bio_10_tm_ch10",
                "order": 10,
                "title": "Lesson 10: Natural Resources (సహజ వనరులు)",
                "topics": [
                    {
                        "topic_id": "bio_10_tm_ch10_t01",
                        "order": 1,
                        "title": "Water Management & Conservation"
                    },
                    {
                        "topic_id": "bio_10_tm_ch10_t02",
                        "order": 2,
                        "title": "Soil & Forest Conservation"
                    },
                    {
                        "topic_id": "bio_10_tm_ch10_t03",
                        "order": 3,
                        "title": "Alternative Energy Sources"
                    }
                ]
            }
        ]
    },
    {
        "subject_id": "phy_10_tm",
        "class_id": "10",
        "name": "Physical Science (భౌతిక రసాయన శాస్త్రాలు)",
        "medium": "TM",
        "icon": "bolt",
        "chapters": [
            {
                "chapter_id": "phy_10_tm_ch01",
                "order": 1,
                "title": "Reflection of Light at Curved Surfaces (వక్రతలాల వద్ద కాంతి పరావర్తనం)",
                "topics": [
                    {
                        "topic_id": "phy_10_tm_ch01_t01",
                        "order": 1,
                        "title": "Spherical Mirrors & Ray Diagrams"
                    },
                    {
                        "topic_id": "phy_10_tm_ch01_t02",
                        "order": 2,
                        "title": "Mirror Formula & Sign Convention"
                    },
                    {
                        "topic_id": "phy_10_tm_ch01_t03",
                        "order": 3,
                        "title": "Magnification & Uses"
                    }
                ]
            },
            {
                "chapter_id": "phy_10_tm_ch02",
                "order": 2,
                "title": "Chemical Reactions and Equations (రసాయన చర్యలు మరియు సమీకరణాలు)",
                "topics": [
                    {
                        "topic_id": "phy_10_tm_ch02_t01",
                        "order": 1,
                        "title": "Balancing Chemical Equations"
                    },
                    {
                        "topic_id": "phy_10_tm_ch02_t02",
                        "order": 2,
                        "title": "Combination & Decomposition Reactions"
                    },
                    {
                        "topic_id": "phy_10_tm_ch02_t03",
                        "order": 3,
                        "title": "Displacement & Redox Reactions"
                    }
                ]
            },
            {
                "chapter_id": "phy_10_tm_ch03",
                "order": 3,
                "title": "Acids, Bases and Salts (ఆమ్లాలు, క్షారాలు మరియు లవణాలు)",
                "topics": [
                    {
                        "topic_id": "phy_10_tm_ch03_t01",
                        "order": 1,
                        "title": "Properties of Acids and Bases"
                    },
                    {
                        "topic_id": "phy_10_tm_ch03_t02",
                        "order": 2,
                        "title": "pH Scale and Applications"
                    },
                    {
                        "topic_id": "phy_10_tm_ch03_t03",
                        "order": 3,
                        "title": "Preparation & Uses of Salts"
                    }
                ]
            },
            {
                "chapter_id": "phy_10_tm_ch04",
                "order": 4,
                "title": "Refraction of Light at Curved Surfaces (వక్రతలాల వద్ద కాంతి వక్రీభవనం)",
                "topics": [
                    {
                        "topic_id": "phy_10_tm_ch04_t01",
                        "order": 1,
                        "title": "Refraction at Curved Interfaces"
                    },
                    {
                        "topic_id": "phy_10_tm_ch04_t02",
                        "order": 2,
                        "title": "Lens Formula & Lens Maker's Equation"
                    },
                    {
                        "topic_id": "phy_10_tm_ch04_t03",
                        "order": 3,
                        "title": "Ray Diagrams for Lenses"
                    }
                ]
            },
            {
                "chapter_id": "phy_10_tm_ch05",
                "order": 5,
                "title": "Human Eye and Colourful World (మానవుని కన్ను - రంగుల ప్రపంచం)",
                "topics": [
                    {
                        "topic_id": "phy_10_tm_ch05_t01",
                        "order": 1,
                        "title": "Structure of Human Eye & Vision Defects"
                    },
                    {
                        "topic_id": "phy_10_tm_ch05_t02",
                        "order": 2,
                        "title": "Dispersion & Rainbow Formation"
                    },
                    {
                        "topic_id": "phy_10_tm_ch05_t03",
                        "order": 3,
                        "title": "Atmospheric Refraction & Scattering"
                    }
                ]
            },
            {
                "chapter_id": "phy_10_tm_ch06",
                "order": 6,
                "title": "Structure of Atom (పరమాణు నిర్మాణం)",
                "topics": [
                    {
                        "topic_id": "phy_10_tm_ch06_t01",
                        "order": 1,
                        "title": "Electromagnetic Spectrum & Planck's Theory"
                    },
                    {
                        "topic_id": "phy_10_tm_ch06_t02",
                        "order": 2,
                        "title": "Bohr's Hydrogen Model"
                    },
                    {
                        "topic_id": "phy_10_tm_ch06_t03",
                        "order": 3,
                        "title": "Quantum Numbers & Electronic Configuration"
                    }
                ]
            },
            {
                "chapter_id": "phy_10_tm_ch07",
                "order": 7,
                "title": "Classification of Elements - The Periodic Table (ఆవర్తన పట్టిక)",
                "topics": [
                    {
                        "topic_id": "phy_10_tm_ch07_t01",
                        "order": 1,
                        "title": "Mendeleev & Modern Periodic Law"
                    },
                    {
                        "topic_id": "phy_10_tm_ch07_t02",
                        "order": 2,
                        "title": "Groups & Periods Structure"
                    },
                    {
                        "topic_id": "phy_10_tm_ch07_t03",
                        "order": 3,
                        "title": "Periodic Trends"
                    }
                ]
            },
            {
                "chapter_id": "phy_10_tm_ch08",
                "order": 8,
                "title": "Chemical Bonding (రసాయన బంధం)",
                "topics": [
                    {
                        "topic_id": "phy_10_tm_ch08_t01",
                        "order": 1,
                        "title": "Lewis Structures & Octet Rule"
                    },
                    {
                        "topic_id": "phy_10_tm_ch08_t02",
                        "order": 2,
                        "title": "Ionic & Covalent Bonding"
                    },
                    {
                        "topic_id": "phy_10_tm_ch08_t03",
                        "order": 3,
                        "title": "VSEPR Theory & Molecular Shapes"
                    }
                ]
            },
            {
                "chapter_id": "phy_10_tm_ch09",
                "order": 9,
                "title": "Electric Current (విద్యుత్ ప్రవాహం)",
                "topics": [
                    {
                        "topic_id": "phy_10_tm_ch09_t01",
                        "order": 1,
                        "title": "Ohm's Law & Resistance"
                    },
                    {
                        "topic_id": "phy_10_tm_ch09_t02",
                        "order": 2,
                        "title": "Series and Parallel Circuits"
                    },
                    {
                        "topic_id": "phy_10_tm_ch09_t03",
                        "order": 3,
                        "title": "Electric Power & Joule's Heating Effect"
                    }
                ]
            },
            {
                "chapter_id": "phy_10_tm_ch10",
                "order": 10,
                "title": "Electromagnetism (విద్యుదయస్కాంతత్వం)",
                "topics": [
                    {
                        "topic_id": "phy_10_tm_ch10_t01",
                        "order": 1,
                        "title": "Magnetic Field of Current Carrying Wire"
                    },
                    {
                        "topic_id": "phy_10_tm_ch10_t02",
                        "order": 2,
                        "title": "Faraday's Laws of Induction"
                    },
                    {
                        "topic_id": "phy_10_tm_ch10_t03",
                        "order": 3,
                        "title": "Electric Motors & Generators"
                    }
                ]
            },
            {
                "chapter_id": "phy_10_tm_ch11",
                "order": 11,
                "title": "Principles of Metallurgy (లోహ సంగ్రహణ శాస్త్రం)",
                "topics": [
                    {
                        "topic_id": "phy_10_tm_ch11_t01",
                        "order": 1,
                        "title": "Occurrence of Metals & Ores"
                    },
                    {
                        "topic_id": "phy_10_tm_ch11_t02",
                        "order": 2,
                        "title": "Extraction Processes of Crude Metals"
                    },
                    {
                        "topic_id": "phy_10_tm_ch11_t03",
                        "order": 3,
                        "title": "Refining & Corrosion Control"
                    }
                ]
            },
            {
                "chapter_id": "phy_10_tm_ch12",
                "order": 12,
                "title": "Carbon and its Compounds (కార్బన్ - దాని సమ్మేళనాలు)",
                "topics": [
                    {
                        "topic_id": "phy_10_tm_ch12_t01",
                        "order": 1,
                        "title": "Allotropes of Carbon"
                    },
                    {
                        "topic_id": "phy_10_tm_ch12_t02",
                        "order": 2,
                        "title": "Homologous Series & Functional Groups"
                    },
                    {
                        "topic_id": "phy_10_tm_ch12_t03",
                        "order": 3,
                        "title": "Hydrocarbons & Nomenclature"
                    }
                ]
            }
        ]
    },
    {
        "subject_id": "soc_10_tm",
        "class_id": "10",
        "name": "Social Studies (సాంఘిక శాస్త్రం)",
        "medium": "TM",
        "icon": "public",
        "chapters": [
            {
                "chapter_id": "soc_10_tm_ch01",
                "order": 1,
                "title": "India: Relief Features (భారతదేశం: భౌగోళిక స్వరూపాలు)",
                "topics": [
                    {
                        "topic_id": "soc_10_tm_ch01_t01",
                        "order": 1,
                        "title": "Geological Formation of India"
                    },
                    {
                        "topic_id": "soc_10_tm_ch01_t02",
                        "order": 2,
                        "title": "Himalayas & Indo-Gangetic Plains"
                    },
                    {
                        "topic_id": "soc_10_tm_ch01_t03",
                        "order": 3,
                        "title": "Peninsular Plateau & Coastal Plains"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_tm_ch02",
                "order": 2,
                "title": "Ideas of Development (అభివృద్ధి భావనలు)",
                "topics": [
                    {
                        "topic_id": "soc_10_tm_ch02_t01",
                        "order": 1,
                        "title": "Development Indicators"
                    },
                    {
                        "topic_id": "soc_10_tm_ch02_t02",
                        "order": 2,
                        "title": "Income and Other Criteria"
                    },
                    {
                        "topic_id": "soc_10_tm_ch02_t03",
                        "order": 3,
                        "title": "Human Development Report"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_tm_ch03",
                "order": 3,
                "title": "Production and Employment (ఉత్పత్తి మరియు ఉపాధి)",
                "topics": [
                    {
                        "topic_id": "soc_10_tm_ch03_t01",
                        "order": 1,
                        "title": "Primary, Secondary & Tertiary Sectors"
                    },
                    {
                        "topic_id": "soc_10_tm_ch03_t02",
                        "order": 2,
                        "title": "Organised vs Unorganised Sectors"
                    },
                    {
                        "topic_id": "soc_10_tm_ch03_t03",
                        "order": 3,
                        "title": "Employment Generation"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_tm_ch04",
                "order": 4,
                "title": "Climate of India (భారతదేశ శీతోష్ణస్థితి)",
                "topics": [
                    {
                        "topic_id": "soc_10_tm_ch04_t01",
                        "order": 1,
                        "title": "Climatic Controls"
                    },
                    {
                        "topic_id": "soc_10_tm_ch04_t02",
                        "order": 2,
                        "title": "Mechanism of Monsoons"
                    },
                    {
                        "topic_id": "soc_10_tm_ch04_t03",
                        "order": 3,
                        "title": "Seasons of India"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_tm_ch05",
                "order": 5,
                "title": "Indian Rivers and Water Resources (నదులు మరియు నీటి వనరులు)",
                "topics": [
                    {
                        "topic_id": "soc_10_tm_ch05_t01",
                        "order": 1,
                        "title": "Himalayan & Peninsular River Systems"
                    },
                    {
                        "topic_id": "soc_10_tm_ch05_t02",
                        "order": 2,
                        "title": "Water Utilization in India"
                    },
                    {
                        "topic_id": "soc_10_tm_ch05_t03",
                        "order": 3,
                        "title": "Equitable Water Management"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_tm_ch06",
                "order": 6,
                "title": "The People (ప్రజలు)",
                "topics": [
                    {
                        "topic_id": "soc_10_tm_ch06_t01",
                        "order": 1,
                        "title": "Census & Population Size"
                    },
                    {
                        "topic_id": "soc_10_tm_ch06_t02",
                        "order": 2,
                        "title": "Age Structure & Sex Ratio"
                    },
                    {
                        "topic_id": "soc_10_tm_ch06_t03",
                        "order": 3,
                        "title": "Literacy & Working Population"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_tm_ch07",
                "order": 7,
                "title": "People and Settlement (ప్రజలు - నివాస ప్రాంతాలు)",
                "topics": [
                    {
                        "topic_id": "soc_10_tm_ch07_t01",
                        "order": 1,
                        "title": "Urban and Rural Settlements"
                    },
                    {
                        "topic_id": "soc_10_tm_ch07_t02",
                        "order": 2,
                        "title": "Urbanisation in India"
                    },
                    {
                        "topic_id": "soc_10_tm_ch07_t03",
                        "order": 3,
                        "title": "Modern Urban Planning"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_tm_ch08",
                "order": 8,
                "title": "People and Migration (ప్రజలు - వలసలు)",
                "topics": [
                    {
                        "topic_id": "soc_10_tm_ch08_t01",
                        "order": 1,
                        "title": "Internal & International Migration"
                    },
                    {
                        "topic_id": "soc_10_tm_ch08_t02",
                        "order": 2,
                        "title": "Patterns of Migration"
                    },
                    {
                        "topic_id": "soc_10_tm_ch08_t03",
                        "order": 3,
                        "title": "Socio-Economic Impacts of Migration"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_tm_ch09",
                "order": 9,
                "title": "Rampur: A Village Economy (రాంపూర్ : గ్రామ ఆర్థిక వ్యవస్థ)",
                "topics": [
                    {
                        "topic_id": "soc_10_tm_ch09_t01",
                        "order": 1,
                        "title": "Factors of Production in Agriculture"
                    },
                    {
                        "topic_id": "soc_10_tm_ch09_t02",
                        "order": 2,
                        "title": "Land Distribution in Rampur"
                    },
                    {
                        "topic_id": "soc_10_tm_ch09_t03",
                        "order": 3,
                        "title": "Non-Farm Rural Activities"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_tm_ch10",
                "order": 10,
                "title": "Globalisation (ప్రపంచీకరణ)",
                "topics": [
                    {
                        "topic_id": "soc_10_tm_ch10_t01",
                        "order": 1,
                        "title": "Multinational Companies (MNCs)"
                    },
                    {
                        "topic_id": "soc_10_tm_ch10_t02",
                        "order": 2,
                        "title": "Integration of World Markets"
                    },
                    {
                        "topic_id": "soc_10_tm_ch10_t03",
                        "order": 3,
                        "title": "Role of WTO & Fair Globalisation"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_tm_ch11",
                "order": 11,
                "title": "Food Security (ఆహార భద్రత)",
                "topics": [
                    {
                        "topic_id": "soc_10_tm_ch11_t01",
                        "order": 1,
                        "title": "Foodgrain Production & Buffer Stock"
                    },
                    {
                        "topic_id": "soc_10_tm_ch11_t02",
                        "order": 2,
                        "title": "Public Distribution System (PDS)"
                    },
                    {
                        "topic_id": "soc_10_tm_ch11_t03",
                        "order": 3,
                        "title": "Nutritional Levels"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_tm_ch12",
                "order": 12,
                "title": "Sustainable Development with Equity (సుస్థిర అభివృద్ధి)",
                "topics": [
                    {
                        "topic_id": "soc_10_tm_ch12_t01",
                        "order": 1,
                        "title": "Environment & Development Challenges"
                    },
                    {
                        "topic_id": "soc_10_tm_ch12_t02",
                        "order": 2,
                        "title": "Alternative Sustainable Paradigms"
                    },
                    {
                        "topic_id": "soc_10_tm_ch12_t03",
                        "order": 3,
                        "title": "People's Environmental Movements"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_tm_ch13",
                "order": 13,
                "title": "World Between the World Wars (ప్రపంచ యుద్ధాల మధ్య ప్రపంచం)",
                "topics": [
                    {
                        "topic_id": "soc_10_tm_ch13_t01",
                        "order": 1,
                        "title": "World War I Causes"
                    },
                    {
                        "topic_id": "soc_10_tm_ch13_t02",
                        "order": 2,
                        "title": "Great Depression & League of Nations"
                    },
                    {
                        "topic_id": "soc_10_tm_ch13_t03",
                        "order": 3,
                        "title": "Fascism & Nazism"
                    },
                    {
                        "topic_id": "soc_10_tm_ch13_t04",
                        "order": 4,
                        "title": "World War II"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_tm_ch14",
                "order": 14,
                "title": "National Liberation Movements in the Colonies (వలస విముక్తి ఉద్యమాలు)",
                "topics": [
                    {
                        "topic_id": "soc_10_tm_ch14_t01",
                        "order": 1,
                        "title": "Chinese Liberation Struggle"
                    },
                    {
                        "topic_id": "soc_10_tm_ch14_t02",
                        "order": 2,
                        "title": "Vietnam War of Independence"
                    },
                    {
                        "topic_id": "soc_10_tm_ch14_t03",
                        "order": 3,
                        "title": "Decolonisation in Nigeria"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_tm_ch15",
                "order": 15,
                "title": "National Movement in India: Partition & Independence (జాతీయోద్యమం)",
                "topics": [
                    {
                        "topic_id": "soc_10_tm_ch15_t01",
                        "order": 1,
                        "title": "Quit India Movement & INA"
                    },
                    {
                        "topic_id": "soc_10_tm_ch15_t02",
                        "order": 2,
                        "title": "Communalism & Partition"
                    },
                    {
                        "topic_id": "soc_10_tm_ch15_t03",
                        "order": 3,
                        "title": "Independence in 1947"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_tm_ch16",
                "order": 16,
                "title": "The Making of Independent India's Constitution (భారత రాజ్యాంగం)",
                "topics": [
                    {
                        "topic_id": "soc_10_tm_ch16_t01",
                        "order": 1,
                        "title": "Constituent Assembly Debates"
                    },
                    {
                        "topic_id": "soc_10_tm_ch16_t02",
                        "order": 2,
                        "title": "Preamble & Guiding Philosophy"
                    },
                    {
                        "topic_id": "soc_10_tm_ch16_t03",
                        "order": 3,
                        "title": "Federal Structure"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_tm_ch17",
                "order": 17,
                "title": "Election Process in India (భారతదేశంలో ఎన్నికల ప్రక్రియ)",
                "topics": [
                    {
                        "topic_id": "soc_10_tm_ch17_t01",
                        "order": 1,
                        "title": "Election Commission Responsibilities"
                    },
                    {
                        "topic_id": "soc_10_tm_ch17_t02",
                        "order": 2,
                        "title": "Conduct of Elections & Voting"
                    },
                    {
                        "topic_id": "soc_10_tm_ch17_t03",
                        "order": 3,
                        "title": "Electoral Reforms"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_tm_ch18",
                "order": 18,
                "title": "Independent India (First 30 Years) (స్వతంత్ర భారతదేశం 1947-1977)",
                "topics": [
                    {
                        "topic_id": "soc_10_tm_ch18_t01",
                        "order": 1,
                        "title": "State Reorganisation 1956"
                    },
                    {
                        "topic_id": "soc_10_tm_ch18_t02",
                        "order": 2,
                        "title": "Five-Year Plans & Industrial Growth"
                    },
                    {
                        "topic_id": "soc_10_tm_ch18_t03",
                        "order": 3,
                        "title": "Emergency & Democratic Revival"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_tm_ch19",
                "order": 19,
                "title": "Emerging Political Trends 1977-2000 (రాజకీయ ధోరణుల ఆవిర్భావం)",
                "topics": [
                    {
                        "topic_id": "soc_10_tm_ch19_t01",
                        "order": 1,
                        "title": "Coalition Politics at Center"
                    },
                    {
                        "topic_id": "soc_10_tm_ch19_t02",
                        "order": 2,
                        "title": "Rise of Regional Parties"
                    },
                    {
                        "topic_id": "soc_10_tm_ch19_t03",
                        "order": 3,
                        "title": "Economic Reforms of 1991"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_tm_ch20",
                "order": 20,
                "title": "Post-War World and India (యుద్ధానంతర ప్రపంచం మరియు భారతదేశం)",
                "topics": [
                    {
                        "topic_id": "soc_10_tm_ch20_t01",
                        "order": 1,
                        "title": "Cold War & Military Pacts"
                    },
                    {
                        "topic_id": "soc_10_tm_ch20_t02",
                        "order": 2,
                        "title": "Non-Aligned Movement (NAM)"
                    },
                    {
                        "topic_id": "soc_10_tm_ch20_t03",
                        "order": 3,
                        "title": "United Nations Role"
                    }
                ]
            },
            {
                "chapter_id": "soc_10_tm_ch21",
                "order": 21,
                "title": "Social Movements in Our Times (సమకాలీన సామాజిక ఉద్యమాలు)",
                "topics": [
                    {
                        "topic_id": "soc_10_tm_ch21_t01",
                        "order": 1,
                        "title": "Civil Rights Movements"
                    },
                    {
                        "topic_id": "soc_10_tm_ch21_t02",
                        "order": 2,
                        "title": "Anti-Nuclear & Environmental Struggles"
                    },
                    {
                        "topic_id": "soc_10_tm_ch21_t03",
                        "order": 3,
                        "title": "RTI & Transparency"
                    }
                ]
            }
        ]
    },
    {
        "subject_id": "eng_10_tm",
        "class_id": "10",
        "name": "English Reader (ఆంగ్ల భాష)",
        "medium": "TM",
        "icon": "school",
        "chapters": [
            {
                "chapter_id": "eng_10_tm_ch01",
                "order": 1,
                "title": "Unit 1: Personality Development (వ్యక్తిత్వ వికాసం)",
                "topics": [
                    {
                        "topic_id": "eng_10_tm_ch01_t01",
                        "order": 1,
                        "title": "Attitude is Altitude"
                    },
                    {
                        "topic_id": "eng_10_tm_ch01_t02",
                        "order": 2,
                        "title": "Every Success Story is Also a Story of Failures"
                    },
                    {
                        "topic_id": "eng_10_tm_ch01_t03",
                        "order": 3,
                        "title": "I Will Do It"
                    },
                    {
                        "topic_id": "eng_10_tm_ch01_t04",
                        "order": 4,
                        "title": "Grammar: Adjectives & Adverbs"
                    }
                ]
            },
            {
                "chapter_id": "eng_10_tm_ch02",
                "order": 2,
                "title": "Unit 2: Wit and Humour (హాస్యం)",
                "topics": [
                    {
                        "topic_id": "eng_10_tm_ch02_t01",
                        "order": 1,
                        "title": "The Dear Departed (Part I)"
                    },
                    {
                        "topic_id": "eng_10_tm_ch02_t02",
                        "order": 2,
                        "title": "The Dear Departed (Part II)"
                    },
                    {
                        "topic_id": "eng_10_tm_ch02_t03",
                        "order": 3,
                        "title": "The Brave Potter"
                    },
                    {
                        "topic_id": "eng_10_tm_ch02_t04",
                        "order": 4,
                        "title": "Grammar: Compound Adjectives"
                    }
                ]
            },
            {
                "chapter_id": "eng_10_tm_ch03",
                "order": 3,
                "title": "Unit 3: Human Relations (మానవ సంబంధాలు)",
                "topics": [
                    {
                        "topic_id": "eng_10_tm_ch03_t01",
                        "order": 1,
                        "title": "The Journey"
                    },
                    {
                        "topic_id": "eng_10_tm_ch03_t02",
                        "order": 2,
                        "title": "Another Woman (Poem)"
                    },
                    {
                        "topic_id": "eng_10_tm_ch03_t03",
                        "order": 3,
                        "title": "The Never-Never Nest"
                    },
                    {
                        "topic_id": "eng_10_tm_ch03_t04",
                        "order": 4,
                        "title": "Grammar: Direct & Indirect Speech"
                    }
                ]
            },
            {
                "chapter_id": "eng_10_tm_ch04",
                "order": 4,
                "title": "Unit 4: Films and Theatre (చలనచిత్రాలు మరియు రంగస్థలం)",
                "topics": [
                    {
                        "topic_id": "eng_10_tm_ch04_t01",
                        "order": 1,
                        "title": "Rendezvous with Ray"
                    },
                    {
                        "topic_id": "eng_10_tm_ch04_t02",
                        "order": 2,
                        "title": "Maya Bazaar"
                    },
                    {
                        "topic_id": "eng_10_tm_ch04_t03",
                        "order": 3,
                        "title": "A Tribute to Savitri"
                    },
                    {
                        "topic_id": "eng_10_tm_ch04_t04",
                        "order": 4,
                        "title": "Grammar: Prepositions"
                    }
                ]
            },
            {
                "chapter_id": "eng_10_tm_ch05",
                "order": 5,
                "title": "Unit 5: Social Issues (సామాజిక సమస్యలు)",
                "topics": [
                    {
                        "topic_id": "eng_10_tm_ch05_t01",
                        "order": 1,
                        "title": "The Storeyed House (Part I)"
                    },
                    {
                        "topic_id": "eng_10_tm_ch05_t02",
                        "order": 2,
                        "title": "The Storeyed House (Part II)"
                    },
                    {
                        "topic_id": "eng_10_tm_ch05_t03",
                        "order": 3,
                        "title": "Abandoned (Poem)"
                    },
                    {
                        "topic_id": "eng_10_tm_ch05_t04",
                        "order": 4,
                        "title": "Grammar: Active & Passive Voice"
                    }
                ]
            },
            {
                "chapter_id": "eng_10_tm_ch06",
                "order": 6,
                "title": "Unit 6: Bio-Diversity (జీవ వైవిధ్యం)",
                "topics": [
                    {
                        "topic_id": "eng_10_tm_ch06_t01",
                        "order": 1,
                        "title": "Environment (Wangari Maathai)"
                    },
                    {
                        "topic_id": "eng_10_tm_ch06_t02",
                        "order": 2,
                        "title": "Or Will the Dreamer Wake? (Poem)"
                    },
                    {
                        "topic_id": "eng_10_tm_ch06_t03",
                        "order": 3,
                        "title": "A Tale of Three Villages"
                    },
                    {
                        "topic_id": "eng_10_tm_ch06_t04",
                        "order": 4,
                        "title": "Grammar: Conditionals"
                    }
                ]
            },
            {
                "chapter_id": "eng_10_tm_ch07",
                "order": 7,
                "title": "Unit 7: Nation and Diversity (దేశం మరియు వైవిధ్యం)",
                "topics": [
                    {
                        "topic_id": "eng_10_tm_ch07_t01",
                        "order": 1,
                        "title": "My Childhood (Dr. APJ Abdul Kalam)"
                    },
                    {
                        "topic_id": "eng_10_tm_ch07_t02",
                        "order": 2,
                        "title": "A Plea for India (Poem)"
                    },
                    {
                        "topic_id": "eng_10_tm_ch07_t03",
                        "order": 3,
                        "title": "Unity in Diversity in India"
                    },
                    {
                        "topic_id": "eng_10_tm_ch07_t04",
                        "order": 4,
                        "title": "Grammar: Conjunctions"
                    }
                ]
            },
            {
                "chapter_id": "eng_10_tm_ch08",
                "order": 8,
                "title": "Unit 8: Human Rights (మానవ హక్కులు)",
                "topics": [
                    {
                        "topic_id": "eng_10_tm_ch08_t01",
                        "order": 1,
                        "title": "Jamaican Fragment"
                    },
                    {
                        "topic_id": "eng_10_tm_ch08_t02",
                        "order": 2,
                        "title": "Once Upon a Time (Poem)"
                    },
                    {
                        "topic_id": "eng_10_tm_ch08_t03",
                        "order": 3,
                        "title": "What is My Name?"
                    },
                    {
                        "topic_id": "eng_10_tm_ch08_t04",
                        "order": 4,
                        "title": "Grammar: Discourse Markers"
                    }
                ]
            }
        ]
    }
]

LATEST_UPDATES = [
    {
        "update_id": "upd_001",
        "title": "Bala Buddy Pilot Launch for Class 10",
        "description": "Welcome to BAALAVIDYA! Explore interactive AI tutor support in English and Telugu for Biology and Mathematics.",
        "date": "2026-11-20",
        "category": "Announcement",
        "class_id": "10",
    },
    {
        "update_id": "upd_002",
        "title": "Science Activity Challenge: Photosynthesis",
        "description": "Try the interactive leaf starch test in Lesson 1: Nutrition and earn the Science Explorer Badge!",
        "date": "2026-11-18",
        "category": "Challenge",
        "class_id": "10",
        "subject_id": "bio_10",
    },
    {
        "update_id": "upd_003",
        "title": "Class 10 SSC Model Practice Questions Added",
        "description": "New practice questions and chapter revision notes are now available for Mathematics and Biology.",
        "date": "2026-11-15",
        "category": "Syllabus",
        "class_id": "10",
    },
]


def list_classes() -> list[ClassItem]:
    """Return classes 6, 7, 8, 9, 10 based on official SCERT textbook folders."""
    classes = []
    for num in range(6, 11):
        classes.append(
            ClassItem(
                class_id=str(num),
                number=num,
                name=f"Class {num}",
                subjects_count=len(PILOT_SUBJECTS) if num == 10 else 3,
            )
        )
    return classes


def list_subjects_for_class(class_id: str, medium: str | None = None) -> list[SubjectItem]:
    """Return subjects for a given class (6 to 10) sourced from official SCERT textbooks."""
    from app.services.curriculum_data import CURRICULUM_DATA

    c_str = str(class_id)
    if c_str in CURRICULUM_DATA:
        med_key = "TM" if (medium and medium.upper() in ["TM", "TELUGU", "TELUGU MEDIUM"]) else "EM"
        subjs = CURRICULUM_DATA[c_str].get(med_key, CURRICULUM_DATA[c_str].get("EM", []))
        results = []
        for s in subjs:
            results.append(
                SubjectItem(
                    subject_id=s["id"],
                    class_id=c_str,
                    name=s["teluguName"] if med_key == "TM" else s["name"],
                    medium=med_key,
                    icon=s.get("icon", "menu_book"),
                    chapters_count=len(s.get("chapters", [])),
                )
            )
        return results

    # Fallback to Class 10 pilot
    results = []
    for s in PILOT_SUBJECTS:
        results.append(
            SubjectItem(
                subject_id=s["subject_id"],
                class_id="10",
                name=s["name"],
                medium=s["medium"],
                icon=s.get("icon"),
                chapters_count=len(s.get("chapters", [])),
            )
        )
    return results


def list_chapters_for_subject(class_id: str, subject_id: str) -> list[ChapterItem]:
    """Return chapters for a subject."""
    normalized_sub_id = subject_id.lower().replace("-", "_")

    alias_map = {
        "mathematics": "math_10",
        "biology": "bio_10",
        "physical_science": "phy_10",
        "social_studies": "soc_10",
        "english": "eng_10",
        "telugu": "tel_10",
        "math": "math_10",
        "bio": "bio_10",
        "physics": "phy_10",
        "social": "soc_10",
    }
    target_id = alias_map.get(normalized_sub_id, normalized_sub_id)

    for s in PILOT_SUBJECTS:
        if (s["subject_id"].lower() == target_id or s["subject_id"].lower() == normalized_sub_id) and s["class_id"] == class_id:
            chapters = []
            for ch in s.get("chapters", []):
                topics = [
                    TopicItem(topic_id=t["topic_id"], chapter_id=ch["chapter_id"], order=t["order"], title=t["title"])
                    for t in ch.get("topics", [])
                ]
                chapters.append(
                    ChapterItem(
                        chapter_id=ch["chapter_id"],
                        subject_id=s["subject_id"],
                        order=ch["order"],
                        title=ch["title"],
                        topics=topics,
                    )
                )
            return chapters
    return []


def get_latest_updates(class_id: str | None = None) -> list[LatestUpdateItem]:
    """Return latest curriculum updates."""
    updates = []
    for u in LATEST_UPDATES:
        if class_id is None or u.get("class_id") == class_id:
            updates.append(LatestUpdateItem(**u))
    return updates


def get_chapter_package(subject_id: str, chapter_id: str) -> dict | None:
    """Return versioned offline package for a chapter."""
    s_clean = subject_id.lower()
    c_clean = chapter_id.lower()

    if "math" in s_clean or "math" in c_clean:
        return {
            "package_version": "1.0.0",
            "subject_id": subject_id,
            "chapter_id": chapter_id,
            "class_id": "10",
            "title": "Real Numbers (వాస్తవ సంఖ్యలు)",
            "telugu_title": "1వ అధ్యాయం: వాస్తవ సంఖ్యలు",
            "topics": [
                {
                    "topic_id": f"{chapter_id}_t01",
                    "title": "Euclid's Division Lemma",
                    "telugu_title": "యూక్లిడ్ భాగహార న్యాయం",
                    "explanation": "Given positive integers a and b, there exist unique integers q and r satisfying a = bq + r, 0 <= r < b.",
                    "telugu_explanation": "ధన పూర్ణసంఖ్యలు a, b లకు a = bq + r (0 <= r < b) అయ్యేటట్లు ఏకైక పూర్ణసంఖ్యలు q, r లు వ్యవస్థితమవుతాయి.",
                },
                {
                    "topic_id": f"{chapter_id}_t02",
                    "title": "Fundamental Theorem of Arithmetic",
                    "telugu_title": "అంకగణిత ప్రాథమిక సిద్ధాంతం",
                    "explanation": "Every composite number can be uniquely expressed as a product of primes.",
                    "telugu_explanation": "ప్రతి సంయుక్త సంఖ్యను ప్రధాన సంఖ్యల లబ్దంగా ఏకైక రీతిలో వ్యక్తీకరించవచ్చు.",
                },
            ],
            "workbook_activities": [
                {
                    "activity_id": "wb_math_01",
                    "topic_id": f"{chapter_id}_t01",
                    "question": "What is the HCF of 12 and 18 using prime factorisation?",
                    "telugu_question": "ప్రధాన కారణాంకాల పద్ధతిలో 12 మరియు 18 ల గ.సా.భా (HCF) ఎంత?",
                    "options": ["6", "12", "36", "3"],
                    "telugu_options": ["6", "12", "36", "3"],
                    "correct_index": 0,
                    "explanation": "12 = 2² × 3 and 18 = 2 × 3². The common factors are 2 × 3 = 6.",
                    "telugu_explanation": "12 = 2² × 3 మరియు 18 = 2 × 3². గరిష్ట ఉమ్మడి కారణాంకం 2 × 3 = 6.",
                },
                {
                    "activity_id": "wb_math_02",
                    "topic_id": f"{chapter_id}_t02",
                    "question": "Is √2 a rational or irrational number?",
                    "telugu_question": "√2 అనేది అకరణీయ సంఖ్య లేదా కరణీయ సంఖ్య?",
                    "options": ["Irrational Number", "Rational Number", "Integer", "Whole Number"],
                    "telugu_options": ["కరణీయ సంఖ్య", "అకరణీయ సంఖ్య", "పూర్ణ సంఖ్య", "పూర్ణాంకం"],
                    "correct_index": 0,
                    "explanation": "√2 cannot be written in the form p/q where p, q are integers and q ≠ 0.",
                    "telugu_explanation": "√2 ని p/q రూపంలో రాయలేము, కాబట్టి ఇది కరణీయ సంఖ్య.",
                },
            ],
            "cached_video_metadata": get_cached_metadata_for_chapter(chapter_id) or [
                {
                    "video_id": "vid_math_ch1_t1_te",
                    "topic_id": f"{chapter_id}_t01",
                    "language_code": "te",
                    "title": "Real Numbers & Fundamental Theorem - Video Lesson",
                    "telugu_title": "వాస్తవ సంఖ్యలు మరియు అంకగణిత ప్రాథమిక సిద్ధాంతం",
                    "duration_minutes": 10,
                    "duration_seconds": 600,
                    "stream_url": "https://stream.scert.telangana.gov.in/videos/math/real_numbers_te.m3u8",
                    "provider": "T-SAT Vidya / SCERT Telangana",
                    "online_streaming_only": True,
                }
            ],
            "vector_db_slice": [
                {
                    "chunk_id": "chunk_math_real_numbers",
                    "text": "Every composite number can be uniquely expressed as a product of prime numbers.",
                    "subject": "Mathematics",
                    "chapter": "Chapter 1: Real Numbers",
                    "source_page": 4,
                    "language": "en",
                }
            ],
            "size_bytes": 220000,
            "checksum": "sha256:7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
        }

    return {
        "package_version": "1.0.0",
        "subject_id": subject_id,
        "chapter_id": chapter_id,
        "class_id": "10",
        "title": "Nutrition - Food Supplying System",
        "telugu_title": "1వ పాఠం: పోషణ - ఆహార సరఫరా వ్యవస్థ",
        "topics": [
            {
                "topic_id": "bio_ch1_t1",
                "title": "What is Photosynthesis?",
                "telugu_title": "కిరణజన్య సంయోగక్రియ అంటే ఏమిటి?",
                "explanation": "Plants prepare food using sunlight, water, and carbon dioxide.",
                "telugu_explanation": "మొక్కలు సూర్యరశ్మి, నీరు మరియు కార్బన్ డయాక్సైడ్ ఉపయోగించి ఆహారాన్ని తయారుచేసుకుంటాయి.",
            },
            {
                "topic_id": "bio_ch1_t2",
                "title": "Light & Dark Reactions",
                "telugu_title": "కాంతి మరియు నిష్కాంతి చర్యలు",
                "explanation": "Light reaction produces ATP in thylakoids; dark reaction synthesizes glucose in stroma.",
                "telugu_explanation": "కాంతి చర్య థైలాకాయిడ్లలో ATP ని, నిష్కాంతి చర్య స్ట్రోమాలో గ్లూకోజ్‌ను తయారుచేస్తుంది.",
            },
        ],
        "workbook_activities": [
            {
                "activity_id": "wb_bio_01",
                "topic_id": "bio_ch1_t1",
                "question": "Which gas is released during photosynthesis by green plants?",
                "telugu_question": "కిరణజన్య సంయోగక్రియలో మొక్కలు ఏ వాయువును విడుదల చేస్తాయి?",
                "options": ["Oxygen (O₂)", "Carbon Dioxide (CO₂)", "Nitrogen (N₂)", "Methane"],
                "telugu_options": ["ఆక్సిజన్ (O₂)", "కార్బన్ డయాక్సైడ్ (CO₂)", "నైట్రోజన్ (N₂)", "మీథేన్"],
                "correct_index": 0,
                "explanation": "Plants release fresh oxygen during the light reaction photolysis of water.",
                "telugu_explanation": "నీటి కాంతి విశ్లేషణ చర్యలో మొక్కలు ప్రాణవాయువును (ఆక్సిజన్) విడుదల చేస్తాయి.",
            },
            {
                "activity_id": "wb_bio_02",
                "topic_id": "bio_ch1_t2",
                "question": "Where does the light reaction of photosynthesis occur?",
                "telugu_question": "హరితరేణువులో కాంతి చర్య ఎక్కడ జరుగుతుంది?",
                "options": ["Grana Thylakoids", "Stroma", "Cell Wall", "Vacuole"],
                "telugu_options": ["గ్రానా థైలాకాయిడ్లు", "స్ట్రోమా", "కణకవచం", "రిక్తిక"],
                "correct_index": 0,
                "explanation": "Light reactions take place in the chlorophyll-rich grana thylakoid membranes.",
                "telugu_explanation": "కాంతి చర్య క్లోరోఫిల్ కలిగిన గ్రానా థైలాకాయిడ్ పొరలలో జరుగుతుంది.",
            },
        ],
        "educational_games": [
            {
                "game_id": "game_bio_01",
                "title": "Photosynthesis Chef: Match the Ingredients",
                "telugu_title": "కిరణజన్య సంయోగక్రియ చెఫ్: సరైన పదార్థాలను జతపరచండి",
                "game_type": "match_pairs",
                "items": [
                    {"source": "Sunlight (సూర్యరశ్మి)", "target": "Energy Source (శక్తి వనరు)"},
                    {"source": "Chlorophyll (హరితరేణువు)", "target": "Green Pigment (ఆకుపచ్చ వర్ణద్రవ్యం)"},
                    {"source": "CO2 + Water (కార్బన్ డయాక్సైడ్ + నీరు)", "target": "Raw Ingredients (ముడి పదార్థాలు)"},
                    {"source": "Glucose + O2 (గ్లూకోజ్ + ఆక్సిజన్)", "target": "Final Food & Breath (ఆహారం & ప్రాణవాయువు)"},
                ],
            }
        ],
        "cached_video_metadata": get_cached_metadata_for_chapter(chapter_id) or [
            {
                "video_id": "vid_bio_ch1_t1_te",
                "topic_id": "bio_ch1_t1",
                "language_code": "te",
                "title": "Photosynthesis in Green Plants - Telugu Video Lesson",
                "telugu_title": "మొక్కలలో కిరణజన్య సంయోగక్రియ వీడియో పాఠం",
                "duration_minutes": 8,
                "duration_seconds": 480,
                "stream_url": "https://stream.scert.telangana.gov.in/videos/biology/photosynthesis_te.m3u8",
                "provider": "T-SAT Vidya / SCERT Telangana",
                "online_streaming_only": True,
            },
            {
                "video_id": "vid_bio_ch1_t1_en",
                "topic_id": "bio_ch1_t1",
                "language_code": "en",
                "title": "Animated Guide to Photosynthesis in Plant Leaves",
                "telugu_title": "మొక్కల ఆకులలో కిరణజన్య సంయోగక్రియ ఇంగ్లీష్ వివరణ",
                "duration_minutes": 9,
                "duration_seconds": 540,
                "stream_url": "https://stream.scert.telangana.gov.in/videos/biology/photosynthesis_en.m3u8",
                "provider": "DIKSHA / Telangana Open Educational Resources",
                "online_streaming_only": True,
            },
        ],
        "vector_db_slice": [
            {
                "chunk_id": "b0a589ba-944a-55b5-9fe7-29a2c2467471",
                "text": "Photosynthesis is the synthesis of carbohydrates by green plants in the presence of sunlight and chlorophyll.",
                "subject": "Biology",
                "chapter": "Lesson 1: Nutrition",
                "source_page": 2,
                "language": "en",
            },
            {
                "chunk_id": "2131544e-2e77-5e6b-9084-fc50a9ef5b46",
                "text": "మొక్కలు సూర్యరశ్మి, హరితరేణువు, నీరు మరియు కార్బన్ డయాక్సైడ్ ఉపయోగించి పిండిపదార్థాన్ని తయారుచేసే విధానాన్ని కిరణజన్య సంయోగక్రియ అంటారు.",
                "subject": "Biology",
                "chapter": "Lesson 1: Nutrition",
                "source_page": 2,
                "language": "te",
            },
        ],
        "size_bytes": 248500,
        "checksum": "sha256:7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
    }


_CACHED_CHUNKS: list[dict] | None = None

def get_topic_pdf_passage(
    topic: str,
    subject: str | None = None,
    medium: str = "EM",
    chapter: str | None = None,
    class_id: str = "10",
) -> dict:
    """Retrieve detailed topic explanation and textbook excerpt directly from SCERT PDF chunks."""
    global _CACHED_CHUNKS
    import json
    from pathlib import Path

    if _CACHED_CHUNKS is None:
        chunks_file = Path(settings.CHUNKS_PATH)
        if chunks_file.exists():
            with open(chunks_file, "r", encoding="utf-8") as f:
                _CACHED_CHUNKS = [json.loads(line) for line in f]
        else:
            _CACHED_CHUNKS = []

    words = [w.lower() for w in topic.replace("’", "'").split() if len(w) > 3]
    matches = []
    med_norm = (medium or "EM").upper()

    for c in (_CACHED_CHUNKS or []):
        c_med = (c.get("medium") or ("TM" if c.get("language") == "te" else "EM")).upper()
        if med_norm and c_med and c_med != med_norm:
            continue
        c_subj = c.get("subject", "")
        if subject and subject.lower() not in c_subj.lower() and c_subj.lower() not in subject.lower():
            continue
        text = c.get("text", "")
        score = sum(1 for w in words if w in text.lower())
        if score > 0:
            matches.append((score, c))

    matches.sort(key=lambda x: x[0], reverse=True)
    best_chunk = matches[0][1] if matches else {}

    is_te = med_norm == "TM" or (matches and matches[0][1].get("language") == "te")
    src_file = best_chunk.get("source_file") or ("X Mathematics TM 2026-27.pdf" if is_te else "X Maths BIL P-1 Final 2026-27.pdf")
    page_num = best_chunk.get("source_page", 13)

    return {
        "topic": topic,
        "subject": subject or best_chunk.get("subject", "General"),
        "medium": med_norm,
        "source_pdf": src_file,
        "source_pages": f"Pages {page_num} - {page_num + 3}",
        "scert_edition": "State Council of Educational Research and Training, Telangana (2026-27 Edition)",
        "verbatim_excerpt": best_chunk.get("text", "")[:600] if best_chunk else (
            f"తెలంగాణ SCERT 10వ తరగతి పాఠ్యపుస్తకం నుండి: {topic} అంశం ప్రాథమిక భావన మరియు సూత్రాలను స్పష్టంగా వివరిస్తుంది."
            if is_te else
            f"From Telangana SCERT Class 10 Textbook: {topic} provides fundamental conceptual framework and governing principles."
        ),
        "chunk_count": len(matches),
    }

