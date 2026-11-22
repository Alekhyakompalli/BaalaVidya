# -*- coding: utf-8 -*-
"""Comprehensive Multi-Class SCERT Curriculum Data (Classes 6 to 10).

Sourced directly from the official Telangana SCERT textbook PDFs in:
ingestion/data/raw/class 6, 7, 8, 9, 10 (English and Telugu mediums, 2026-27 Edition).

Subjects per class:
- English Medium: Sanskrit, Maths, Physics, Biology, Science, English
- Telugu Medium: Telugu, English, Maths, Physics, Biology, Social (Telugu names only)
"""

import re
from typing import Any

# Multi-class curriculum dictionary: Class -> Medium ('EM', 'TM') -> List of Subjects
CURRICULUM_DATA: dict[str, dict[str, list[dict[str, Any]]]] = {
    "6": {
        "EM": [
            {
                "id": "sanskrit_6",
                "name": "Sanskrit",
                "teluguName": "సంస్కృతం",
                "icon": "📜",
                "iconBg": "#FFF8E1",
                "iconColor": "#FF8F00",
                "progress": 20,
                "pdf": "6th sanskrit cc.pdf",
                "chapters": [
                    {"num": 1, "title": "Parichaya (Introduction)", "topics": ["Varnamala (Alphabet)", "Svara & Vyanjana", "Simple Sanskrit Greetings"], "summary": "Foundational introduction to Sanskrit script, sounds, and daily greetings."},
                    {"num": 2, "title": "Vidyalaya (Our School)", "topics": ["Classroom Vocabulary", "Teacher and Student Dialogues", "Singular and Plural Nouns"], "summary": "Conversational sentences about school, books, and playground activities."},
                    {"num": 3, "title": "Vrikshah (Trees)", "topics": ["Poem on Nature", "Parts of Tree in Sanskrit", "Importance of Forest Protection"], "summary": "Appreciating nature through lyrical Sanskrit verse and tree vocabulary."},
                    {"num": 4, "title": "Krida (Sports and Games)", "topics": ["Traditional Indian Games", "Action Verbs (Dhavati, Patati, Kridati)"], "summary": "Action verbs and playful sentences describing children playing sports."},
                    {"num": 5, "title": "Vrikshanam Mahima (Glory of Trees)", "topics": ["Environmental Care", "Subhashitas on Giving and Charity"], "summary": "Moral lessons drawn from how trees offer shade and fruits selflessly."},
                    {"num": 6, "title": "Samudra-tata (Seashore)", "topics": ["Beaches of India", "Dative Case Usages", "Tourism Vocabulary"], "summary": "Grammatical case endings and descriptive tour of Indian coastlines."},
                    {"num": 7, "title": "Bakasya Pratikarah (The Heron's Revenge)", "topics": ["Panchatantra Story", "Friendship and Justice", "Dialogue Reading"], "summary": "Classic fable teaching mutual respect, fairness, and empathy."},
                    {"num": 8, "title": "Sukti-stabaka (Bouquet of Good Sayings)", "topics": ["Subhashita Verses", "Virtues of Truth and Hard Work"], "summary": "Timeless Sanskrit moral maxims for character building."}
                ]
            },
            {
                "id": "math_6",
                "name": "Mathematics",
                "teluguName": "గణితం",
                "icon": "📐",
                "iconBg": "#FFF1C8",
                "iconColor": "#996100",
                "progress": 25,
                "pdf": "VI Maths EM Final 2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "Knowing Our Numbers", "topics": ["Comparing Numbers", "Large Numbers in Practice", "Estimation & Rounding", "Roman Numerals"], "summary": "Indian and International place value systems, large numbers comparison, and Roman numerals."},
                    {"num": 2, "title": "Whole Numbers", "topics": ["Natural Numbers & Whole Numbers", "Number Line Operations", "Properties of Whole Numbers"], "summary": "Closure, commutative, associative, and distributive properties of whole numbers."},
                    {"num": 3, "title": "Playing with Numbers", "topics": ["Factors and Multiples", "Prime & Composite Numbers", "Divisibility Rules (2 to 11)", "HCF and LCM"], "summary": "Prime factorisation, co-primes, twin primes, and finding HCF and LCM with real-life applications."},
                    {"num": 4, "title": "Basic Geometrical Ideas", "topics": ["Points, Lines, Segments & Rays", "Curves & Polygons", "Angles, Triangles & Quadrilaterals", "Circles"], "summary": "Foundational geometric elements, interior/exterior regions, and circle parts."},
                    {"num": 5, "title": "Measures of Lines and Angles", "topics": ["Measuring Line Segments", "Right, Straight, Acute, Obtuse Angles", "Reflex & Complete Angles"], "summary": "Comparison of line segments using divider, angle measurement using protractor."},
                    {"num": 6, "title": "Integers", "topics": ["Positive & Negative Integers", "Number Line Representation", "Addition and Subtraction of Integers"], "summary": "Real-world negative numbers (temperatures, debts, depths) and rules of integer addition and subtraction."},
                    {"num": 7, "title": "Fractions and Decimals", "topics": ["Proper, Improper & Mixed Fractions", "Equivalent Fractions", "Decimal Numbers on Number Line", "Addition & Subtraction of Decimals"], "summary": "Fraction operations, comparing like/unlike fractions, and decimal place values."},
                    {"num": 8, "title": "Data Handling", "topics": ["Recording Data", "Tally Marks & Frequency", "Pictographs & Bar Graphs"], "summary": "Organising observational data and interpreting vertical and horizontal bar graphs."},
                    {"num": 9, "title": "Introduction to Algebra", "topics": ["Matchstick Patterns & Variables", "Writing Algebraic Expressions", "Simple Equations & Trial and Error"], "summary": "Understanding variables, expressions with variables, and forming simple balance equations."},
                    {"num": 10, "title": "Perimeter and Area", "topics": ["Perimeter of Regular Shapes", "Perimeter of Rectangle and Square", "Area by Counting Squares"], "summary": "Boundary calculations and surface measurement using unit square grids."},
                    {"num": 11, "title": "Ratio and Proportion", "topics": ["Concept of Ratio", "Comparing Quantities", "Proportion and Unitary Method"], "summary": "Simplest ratio form, equality of ratios, and solving daily life unit cost problems."},
                    {"num": 12, "title": "Symmetry", "topics": ["Line of Symmetry", "Figures with Multiple Lines of Symmetry", "Reflection Symmetry"], "summary": "Mirror line symmetry in nature, letters, and regular geometrical figures."},
                    {"num": 13, "title": "Practical Geometry", "topics": ["Constructing Circles with Compass", "Perpendicular to a Line", "Perpendicular Bisector", "Angle Bisector with Compass and Ruler"], "summary": "Using compass, ruler, and protractor for accurate geometric constructions, circles, perpendiculars, and bisectors."},
                    {"num": 14, "title": "Understanding 3D and 2D Shapes", "topics": ["Faces, Edges and Vertices", "Prisms and Pyramids", "Cylinders, Cones and Spheres"], "summary": "Three-dimensional solids, spatial visualization, and nets of polyhedrons."}
                ]
            },
            {
                "id": "phy_6",
                "name": "Physical Science",
                "teluguName": "భౌతిక శాస్త్రం",
                "icon": "⚡",
                "iconBg": "#EDE7F6",
                "iconColor": "#512DA8",
                "progress": 30,
                "pdf": "VI Gen. Science 2026-27 EM.pdf",
                "chapters": [
                    {"num": 1, "title": "Playing with Magnets", "topics": ["Discovery of Magnets", "Magnetic vs Non-Magnetic Materials", "Poles of Magnet & Attraction/Repulsion", "Magnetic Compass"], "summary": "Properties of bar and horseshoe magnets, Earth's magnetic field, and navigation."},
                    {"num": 2, "title": "Materials and Objects", "topics": ["Transparent, Opaque & Translucent", "Solubility in Water", "Sink or Float", "Conductors of Heat"], "summary": "Classifying materials based on appearance, hardness, density, and thermal conductivity."},
                    {"num": 3, "title": "Separation of Substances", "topics": ["Handpicking, Winnowing, Sieving", "Sedimentation & Decantation", "Filtration & Evaporation"], "summary": "Techniques for separating mixtures based on particle size and solubility."},
                    {"num": 4, "title": "Simple Electric Circuits", "topics": ["Electric Cell & Bulb Components", "Electric Switch & Closed Circuit", "Conductors and Insulators"], "summary": "Current flow, schematic circuit diagrams, and electrical safety measures."},
                    {"num": 5, "title": "Learning How to Measure", "topics": ["Traditional Units vs SI System", "Measuring Length with Ruler", "Area of Irregular Surfaces"], "summary": "Standard units of measurement (metres, kilograms, seconds) and measuring techniques."},
                    {"num": 6, "title": "Light, Shadows and Images", "topics": ["Luminous vs Non-Luminous Objects", "Shadow Formation & Pinhole Camera", "Plane Mirror Reflection"], "summary": "Rectilinear propagation of light, opaque obstacles, and mirror reflections."}
                ]
            },
            {
                "id": "bio_6",
                "name": "Biological Science",
                "teluguName": "జీవశాస్త్రం",
                "icon": "🌿",
                "iconBg": "#E8F5E9",
                "iconColor": "#2E7D32",
                "progress": 35,
                "pdf": "VI Gen. Science 2026-27 EM.pdf",
                "chapters": [
                    {"num": 1, "title": "Our Food", "topics": ["Food Ingredients & Sources", "Cooking Methods & Preservation", "Food Habits across Telangana"], "summary": "Plant and animal sources of nutrients, cooking methods, and food hygiene."},
                    {"num": 2, "title": "Rain: Where Does It Come From?", "topics": ["Evaporation & Condensation", "Water Cycle in Nature", "Cloud Formation & Precipitation"], "summary": "Physical state transitions of water, humidity, and the hydrological cycle."},
                    {"num": 3, "title": "What Do Animals Eat?", "topics": ["Herbivores, Carnivores & Omnivores", "Food Chains & Feeding Habits", "Animal Adaptations (Beaks, Teeth)"], "summary": "Food dependency, ecological balance, and specialized animal adaptations."},
                    {"num": 4, "title": "Habitat", "topics": ["Terrestrial & Aquatic Habitats", "Pond Ecosystem & Desert Life", "Adaptations in Plants and Animals"], "summary": "Biotic and abiotic factors shaping survival in diverse ecosystems."},
                    {"num": 5, "title": "Fibre to Fabric", "topics": ["Natural vs Synthetic Fibres", "Cotton Ginning & Spinning", "Weaving and Knitting Jute/Cotton"], "summary": "Conversion of plant fibres into yarn and woven textiles."},
                    {"num": 6, "title": "Plants: Parts and Functions", "topics": ["Taproot & Fibrous Root Systems", "Stem & Leaf Venation", "Flower Parts & Photosynthesis"], "summary": "Root absorption, transpiration via stomata, and floral reproductive anatomy."},
                    {"num": 7, "title": "Changes Around Us", "topics": ["Reversible and Irreversible Changes", "Slow and Fast Changes", "Physical vs Chemical Transformations"], "summary": "Distinguishing everyday reversible state changes from irreversible chemical changes."},
                    {"num": 8, "title": "Water in Our Life", "topics": ["Daily Uses of Water", "Water Scarcity & Droughts", "Floods & Rainwater Harvesting"], "summary": "Conservation of freshwater resources and watershed management."},
                    {"num": 9, "title": "Movements in Animals", "topics": ["Human Skeleton & Joints (Ball & Socket, Hinge)", "Muscles & Tendons", "Locomotion in Birds, Fish, Earthworm"], "summary": "Bones, cartilage, and muscular contractions enabling animal locomotion."},
                    {"num": 10, "title": "Living and Non-Living", "topics": ["Characteristics of Living Beings", "Growth, Respiration, Response to Stimuli", "Reproduction & Excretion"], "summary": "Fundamental biological criteria distinguishing living organisms from non-living things."}
                ]
            },
            {
                "id": "sci_6",
                "name": "General Science",
                "teluguName": "సామాన్య శాస్త్రం",
                "icon": "🔬",
                "iconBg": "#E0F2F1",
                "iconColor": "#00796B",
                "progress": 30,
                "pdf": "VI Gen. Science 2026-27 EM.pdf",
                "chapters": [
                    {"num": 1, "title": "Our Food", "topics": ["Ingredients", "Preservation", "Nutrition"], "summary": "Food sources, preservation techniques, and regional food habits."},
                    {"num": 2, "title": "Playing with Magnets", "topics": ["Magnets", "Poles", "Compass"], "summary": "Magnetic properties, attractions, and compass navigation."},
                    {"num": 3, "title": "Rain: Where Does It Come From?", "topics": ["Water Cycle", "Evaporation", "Clouds"], "summary": "The continuous hydrological cycle and weather patterns."},
                    {"num": 4, "title": "What Do Animals Eat?", "topics": ["Food Chains", "Herbivores", "Carnivores"], "summary": "Ecological food relationships and animal feeding habits."},
                    {"num": 5, "title": "Materials and Objects", "topics": ["Solubility", "Transparency", "Density"], "summary": "Properties of matter and classification of common objects."},
                    {"num": 6, "title": "Habitat", "topics": ["Pond Ecosystem", "Desert Habitat", "Adaptations"], "summary": "Organisms thriving in diverse ecological niches."},
                    {"num": 7, "title": "Separation of Substances", "topics": ["Filtration", "Decantation", "Evaporation"], "summary": "Separating mixtures with physical techniques."},
                    {"num": 8, "title": "Fibre to Fabric", "topics": ["Ginning", "Spinning", "Weaving"], "summary": "From cotton fields to wearable cloth."},
                    {"num": 9, "title": "Plants: Parts and Functions", "topics": ["Roots", "Leaves", "Photosynthesis"], "summary": "Plant vegetative and reproductive organ functions."},
                    {"num": 10, "title": "Changes Around Us", "topics": ["Reversible", "Irreversible", "Physical Changes"], "summary": "Recognizing physical and chemical changes."},
                    {"num": 11, "title": "Water in Our Life", "topics": ["Water Conservation", "Droughts", "Rainwater Harvesting"], "summary": "Safe water usage and environmental protection."},
                    {"num": 12, "title": "Simple Electric Circuits", "topics": ["Cells", "Switches", "Conductors"], "summary": "Electric circuits, switches, and electrical flow."},
                    {"num": 13, "title": "Learning How to Measure", "topics": ["Length", "Area", "SI Units"], "summary": "Standard measurement units and instruments."},
                    {"num": 14, "title": "Movements in Animals", "topics": ["Skeletal System", "Joints", "Muscles"], "summary": "Locomotion across human and animal bodies."},
                    {"num": 15, "title": "Light, Shadows and Images", "topics": ["Pinhole Camera", "Shadows", "Reflections"], "summary": "Light propagation and image formation."},
                    {"num": 16, "title": "Living and Non-Living", "topics": ["Cellular Organization", "Response to Stimuli", "Life Cycles"], "summary": "Defining characteristics of living organisms."}
                ]
            },
            {
                "id": "eng_6",
                "name": "English Reader",
                "teluguName": "ఆంగ్లం",
                "icon": "📖",
                "iconBg": "#FBE9E7",
                "iconColor": "#D84315",
                "progress": 40,
                "pdf": "6 english reader-2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "Peace and Harmony", "topics": ["Animal Unity Story", "Poem: I Want Peace", "Reading Comprehension & Vocabulary"], "summary": "Fable about unity and peaceful coexistence in the forest."},
                    {"num": 2, "title": "Telangana, The Pride of the People", "topics": ["Telangana Heritage & Festivals (Bathukamma, Bonalu)", "Historical Forts & Monuments", "Poem: In the Bazaars of Hyderabad"], "summary": "Rich culture, arts, crafts, and festive spirit of Telangana."},
                    {"num": 3, "title": "What Can a Dollar and Eleven Cents Do?", "topics": ["Compassion & Sibling Love", "Medical Miracle Narrative", "Grammar: Degrees of Comparison"], "summary": "Touching story of a girl using her pocket savings to help her sick brother."},
                    {"num": 4, "title": "An Adventure", "topics": ["Mystery Exploration", "Courage and Teamwork", "Grammar: Prepositions of Place"], "summary": "Exciting adventure story of curious children exploring ancient ruins."},
                    {"num": 5, "title": "Plant a Tree", "topics": ["Environmental Protection", "Value of Trees", "Vocabulary Building"], "summary": "Persuasive discourse on protecting greenery and planting trees."},
                    {"num": 6, "title": "Rip Van Winkle", "topics": ["Classic Adaptation", "Humour & Fantasy", "Grammar: Adverbs of Time"], "summary": "Famous folk tale of the lazy man who slept through twenty years in the mountains."},
                    {"num": 7, "title": "P.T. Usha, The Golden Girl", "topics": ["Sports Biography", "Dedication & Olympic Training", "Inspirational Life Lessons"], "summary": "Inspiring sports journey of India's sprinting champion P.T. Usha."},
                    {"num": 8, "title": "Half a Rupee Worth", "topics": ["Greed vs Humanity", "R.K. Narayan Style Short Story", "Grammar: Reported Speech"], "summary": "Moral tale examining honesty, greed, and ethical living."}
                ]
            }
        ],
        "TM": [
            {
                "id": "tel_6_tm",
                "name": "తెలుగు",
                "teluguName": "తెలుగు",
                "icon": "📚",
                "iconBg": "#FFE0B2",
                "iconColor": "#E65100",
                "progress": 30,
                "pdf": "6th Class Telugu FL 2026-27 Inner Pages.pdf",
                "chapters": [
                    {"num": 1, "title": "అభినందన", "topics": ["రైతులు మరియు సైనికుల త్యాగం", "దేశభక్తి గేయం", "భాషాంశాలు"], "summary": "దేశానికి వెన్నెముకైన రైతులు, దేశ సరిహద్దులను కాపాడే వీర జవానులకు వందనం."},
                    {"num": 2, "title": "స్నేహబంధం", "topics": ["కథాంశం (కాకి, తాబేలు, జింక, ఎలుక)", "స్నేహం గొప్పతనం", "వ్యాకరణం (నామవాచకం)"], "summary": "ఆపదలో ఆదుకునే స్నేహితుల ఐకమత్యం మరియు ప్రాముఖ్యతను వివరించే కథ."},
                    {"num": 3, "title": "వర్షం", "topics": ["వర్షాకాల వర్ణన", "కవిత్వం (పల్లా దుర్గయ్య)", "సహజ సౌందర్యం"], "summary": "రైతుల ఆనందం మరియు ప్రకృతి పరవశాన్ని వర్ణించే మనోహరమైన పద్యాలు."},
                    {"num": 4, "title": "లేఖ", "topics": ["తెలంగాణ దర్శనీయ స్థలాలు", "లేఖా రచన శైలి", "సంస్కృతి మరియు చరిత్ర"], "summary": "నాగార్జున సాగర్, వరంగల్ కోట తదితర చారిత్రక ప్రదేశాల పరిచయ లేఖ."},
                    {"num": 5, "title": "శతక సుధ", "topics": ["నైతిక విలువలు", "సుమతీ, వేమన శతక పద్యాలు", "భావామృతం"], "summary": "సమాజంలో ఉత్తమ గుణాలు, సత్ప్రవర్తన పెంపొందించే శతక నీతి పద్యాలు."},
                    {"num": 6, "title": "పోతన బాల్యం", "topics": ["బమ్మెర పోతన జీవితం", "భాగవత రచయిత", "బాల్య విశేషాలు"], "summary": "మహాకవి బమ్మెర పోతన బాల్యం, విద్యాభ్యాసం మరియు భక్తి ప్రపత్తులు."}
                ]
            },
            {
                "id": "eng_6_tm",
                "name": "ఆంగ్లం",
                "teluguName": "ఆంగ్లం",
                "icon": "📖",
                "iconBg": "#FBE9E7",
                "iconColor": "#D84315",
                "progress": 25,
                "pdf": "6 english reader-2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "Peace and Harmony (శాంతి మరియు సామరస్యం)", "topics": ["శాంతి గేయం", "జంతువుల ఐక్యత కథ", "ఆంగ్ల పదజాలం"], "summary": "అడవిలో జంతువుల ఐక్యత మరియు శాంతియుత సహజీవనం గురించిన కథ."},
                    {"num": 2, "title": "Telangana, The Pride of the People (తెలంగాణ ప్రజల గర్వకారణం)", "topics": ["బతుకమ్మ, బోనాలు", "హైదరాబాద్ బజార్లు", "తెలంగాణ సంస్కృతి"], "summary": "తెలంగాణ రాష్ట్ర పండుగలు, సంస్కృతి మరియు కళల పరిచయం."},
                    {"num": 3, "title": "What Can a Dollar and Eleven Cents Do? (ఒక డాలర్ పదకొండు సెంట్లు)", "topics": ["సోదరి ప్రేమ", "వైద్య సహాయం కథ", "వ్యాకరణం"], "summary": "అనారోగ్యంతో ఉన్న తమ్ముడి కోసం చిన్నారి చూపిన అపారమైన ప్రేమ కథ."},
                    {"num": 4, "title": "An Adventure (ఒక సాహస యాత్ర)", "topics": ["సాహసం", "పరిశోధన", "ఆంగ్ల సంభాషణలు"], "summary": "ప్రాచీన కట్టడాలను అన్వేషించిన పిల్లల ఉత్సాహభరిత సాహస కథ."}
                ]
            },
            {
                "id": "math_6_tm",
                "name": "గణితం",
                "teluguName": "గణితం",
                "icon": "📐",
                "iconBg": "#FFF1C8",
                "iconColor": "#996100",
                "progress": 25,
                "pdf": "VI Maths TM Final 2026-27).pdf",
                "chapters": [
                    {"num": 1, "title": "సంఖ్యలని తెలుసుకుందాం", "topics": ["సంఖ్యల పోలిక", "హిందూ-అరబిక్ స్థాన విలువలు", "రోమన్ సంఖ్యలు"], "summary": "పెద్ద సంఖ్యల పఠనం, స్థాన విలువల పోలిక మరియు రోమన్ సంఖ్యలు."},
                    {"num": 2, "title": "పూర్ణాంకాలు", "topics": ["సహజ సంఖ్యలు మరియు పూర్ణాంకాలు", "సంఖ్యా రేఖ", "పూర్ణాంకాల ధర్మాలు"], "summary": "సంవృత, స్థిత్యంతర, సహచర మరియు విభాగ న్యాయాలు."},
                    {"num": 3, "title": "సంఖ్యలతో ఆడుకుందాం", "topics": ["కారణాంకాలు మరియు గుణిజాలు", "ప్రధాన, సంయుక్త సంఖ్యలు", "భాజనీయతా సూత్రాలు", "గ.సా.భా మరియు క.సా.గు"], "summary": "భాజనీయతా సూత్రాలు, ప్రధాన కారణాంకాల విభజన మరియు క.సా.గు/గ.సా.భా అనువర్తనాలు."},
                    {"num": 4, "title": "ప్రాథమిక జ్యామితీయ భావనలు", "topics": ["బిందువు, రేఖ, రేఖాఖండం, కిరణం", "కోణాలు, త్రిభుజాలు, చతుర్భుజాలు", "వృత్తం భాగాలు"], "summary": "జ్యామితీయ ప్రాథమిక అంశాలు మరియు వృత్త లక్షణాలు."},
                    {"num": 5, "title": "రేఖలు మరియు కోణాల కొలతలు", "topics": ["కోణాల రకాలు (లఘు, లంబ, గురు కోణాలు)", "కోణమానినితో కొలవడం"], "summary": "కోణాల కొలత మరియు పోలికలు."},
                    {"num": 6, "title": "పూర్ణ సంఖ్యలు", "topics": ["ధన, రుణ సంఖ్యలు", "సంఖ్యా రేఖపై సంకలనం, వ్యవకలనం"], "summary": "నిత్యజీవితంలో రుణ సంఖ్యలు మరియు వాటి పరిక్రియలు."},
                    {"num": 7, "title": "భిన్నాలు మరియు దశాంశాలు", "topics": ["క్రమ, అపక్రమ, మిశ్రమ భిన్నాలు", "దశాంశ సంఖ్యల కూడిక, తీసివేత"], "summary": "భిన్నాలు మరియు దశాంశాల పోలిక మరియు గణనలు."},
                    {"num": 8, "title": "దత్తాంశ నిర్వహణ", "topics": ["గణన చిహ్నాలు", "చిత్ర లేఖాచిత్రాలు", "కమ్మీ రేఖాచిత్రాలు"], "summary": "సమాచారాన్ని సేకరించి గ్రాఫ్‌లలో ప్రదర్శించడం."},
                    {"num": 9, "title": "బీజగణిత పరిచయం", "topics": ["చరరాశులు", "బీజీయ సమాసాలు", "సరళ సమీకరణాలు"], "summary": "అజ్ఞాత రాశులు మరియు బీజగణిత సమీకరణాల రూపకల్పన."},
                    {"num": 10, "title": "చుట్టుకొలత మరియు వైశాల్యం", "topics": ["దీర్ఘచతురస్రం, చతురస్రం చుట్టుకొలత", "గ్రిడ్ పద్ధతిలో వైశాల్యం"], "summary": "సమతల పటాల సరిహద్దు మరియు అంతర్భాగ విస్తీర్ణం లెక్కించడం."},
                    {"num": 11, "title": "నిష్పత్తి మరియు అనుపాతం", "topics": ["నిష్పత్తి భావన", "సమాన నిష్పత్తులు", "ఏక వస్తు పద్ధతి"], "summary": "రాశుల పోలిక మరియు ఏక వస్తు పద్ధతి లెక్కలు."},
                    {"num": 12, "title": "సౌష్టవం", "topics": ["సౌష్టవ అక్షం", "ప్రతిబింబ సౌష్టవం"], "summary": "ప్రకృతి మరియు ఆకారాలలో సౌష్టవ రేఖల గుర్తింపు."},
                    {"num": 13, "title": "ప్రాయోగిక జ్యామితి / ప్రాక్టికల్ జామెట్రీ", "topics": ["వృత్తాల నిర్మాణం", "లంబద్విఖండన రేఖ", "కోణ ద్విఖండన రేఖ"], "summary": "స్కేలు, కంపాస్ ఉపయోగించి ఖచ్చితమైన వృత్తాలు, లంబ రేఖలు మరియు కోణ ద్విఖండన రేఖల నిర్మాణం."},
                    {"num": 14, "title": "3D మరియు 2D ఆకారాల అవగాహన", "topics": ["ముఖాలు, అంచులు, శీర్షాలు", "పట్టకాలు, పిరమిడ్లు", "గోళం, స్తూపం"], "summary": "త్రిమితీయ ఘనాకారాల లక్షణాలు మరియు వాటి వల పటాలు."}
                ]
            },
            {
                "id": "phy_6_tm",
                "name": "భౌతిక శాస్త్రం",
                "teluguName": "భౌతిక శాస్త్రం",
                "icon": "⚡",
                "iconBg": "#EDE7F6",
                "iconColor": "#512DA8",
                "progress": 30,
                "pdf": "VI Science 2026-27 TM.pdf",
                "chapters": [
                    {"num": 1, "title": "అయస్కాంతాలతో ఆటలు", "topics": ["అయస్కాంతాల రకాలు", "ధ్రువాలు (ఉత్తర, దక్షిణ)", "దిక్సూచి ఉపయోగం"], "summary": "ఆకర్షణ, వికర్షణ ధర్మాలు మరియు దిశలను గుర్తించే దిక్సూచి."},
                    {"num": 2, "title": "పదార్థాలు మరియు వస్తువులు", "topics": ["పారదర్శక, అపారదర్శక, పాక్షిక పారదర్శక", "నీటిలో కరిగేవి - కరగనివి", "తేలేవి - మునిగేవి"], "summary": "పదార్థాల ధర్మాలు మరియు వర్గీకరణ."},
                    {"num": 3, "title": "పదార్థాలను వేరుచేయడం", "topics": ["చేత్తో ఏరివేయడం, తూర్పారబట్టడం", "తేర్చడం, వడపోత", "బాష్పీభవనం"], "summary": "మిశ్రమాల నుండి అనుఘటకాలను వేరుచేసే శాస్త్రీయ పద్ధతులు."},
                    {"num": 4, "title": "సాధారణ విద్యుత్ వలయాలు", "topics": ["విద్యుత్ ఘటం మరియు బల్బు", "స్విచ్ పనితీరు", "విద్యుత్ వాహకాలు, బంధకాలు"], "summary": "కరెంట్ ప్రవాహం, వలయాలు మరియు విద్యుత్ భద్రతా నియమాలు."},
                    {"num": 5, "title": "కొలతలు ఎలా కొలవాలి?", "topics": ["ప్రామాణిక కొలతలు (మీటర్, కిలోగ్రామ్)", "స్కేలుతో పొడవు కొలవడం"], "summary": "నిత్యజీవితంలో ప్రామాణిక ప్రమాణాలతో కొలతలు కొలవడం."},
                    {"num": 6, "title": "వెలుగు, నీడలు మరియు ప్రతిబింబాలు", "topics": ["కాంతి రుజుమార్గ ప్రయాణం", "నీడలు ఎలా ఏర్పడతాయి?", "సమతల దర్పణ ప్రతిబింబం"], "summary": "కాంతి సరళరేఖా మార్గం, నీడలు మరియు దర్పణ పరావర్తనం."}
                ]
            },
            {
                "id": "bio_6_tm",
                "name": "జీవశాస్త్రం",
                "teluguName": "జీవశాస్త్రం",
                "icon": "🌿",
                "iconBg": "#E8F5E9",
                "iconColor": "#2E7D32",
                "progress": 35,
                "pdf": "VI Science 2026-27 TM.pdf",
                "chapters": [
                    {"num": 1, "title": "మన ఆహారం", "topics": ["ఆహార దినుసులు మరియు లభ్యత", "వండే పద్ధతులు మరియు నిల్వ", "తెలంగాణ ఆహార సంస్కృతి"], "summary": "పోషకాహారం, ఆహార పదార్థాల తయారీ మరియు ఆరోగ్య సూత్రాలు."},
                    {"num": 2, "title": "వర్షం: ఎక్కడి నుంచి వస్తుంది?", "topics": ["బాష్పీభవనం మరియు సాంద్రీకరణం", "జల చక్రం", "మేఘాలు ఏర్పడటం"], "summary": "నీటి రూపాల మార్పు మరియు వర్షపాతం జరిగే విధానం."},
                    {"num": 3, "title": "జంతువులు ఏమి తింటాయి?", "topics": ["శాకాహారులు, మాంసాహారులు, సర్వాహారులు", "ఆహారపు గొలుసు", "జంతువుల అనుకూలనాలు"], "summary": "ఆహార సంబంధాలు మరియు జీవావరణ సమతుల్యత."},
                    {"num": 4, "title": "ఆవాసం", "topics": ["చెరువు ఆవరణ వ్యవస్థ", "ఎడారి జీవులు", "మొక్కలు, జంతువుల అనుకూలనాలు"], "summary": "వివిధ ఆవాసాలలో జీవుల మనుగడ మరియు జీవనం."},
                    {"num": 5, "title": "దారాల నుండి దుస్తుల దాకా", "topics": ["సహజ, కృత్రిమ దారాలు", "పత్తి నుండి నూలు తయారీ"], "summary": "వస్త్రాల చరిత్ర మరియు దారాల తయారీ విధానం."},
                    {"num": 6, "title": "మొక్కలు: భాగాలు మరియు విధులు", "topics": ["తల్లివేరు, పీచువేరు వ్యవస్థ", "పత్రాలు మరియు కిరణజన్య సంయోగక్రియ", "పువ్వు భాగాలు"], "summary": "మొక్క వేర్లు, కాండం, పత్రాలు మరియు పుష్పం విధులు."}
                ]
            },
            {
                "id": "soc_6_tm",
                "name": "సాంఘిక శాస్త్రం",
                "teluguName": "సాంఘిక శాస్త్రం",
                "icon": "🌍",
                "iconBg": "#FFF9C4",
                "iconColor": "#F57F17",
                "progress": 20,
                "pdf": "6th Socal TM-2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "పటాల పఠనం మరియు తయారీ", "topics": ["దిక్కులు మరియు చిహ్నాలు", "స్కేలు ఉపయోగం", "భౌతిక మరియు రాజకీయ పటాలు"], "summary": "పటాల గుర్తులు, కొలతలు మరియు మ్యాప్ పఠన నైపుణ్యాలు."},
                    {"num": 2, "title": "గ్లోబ్ - భూమి నమూనా", "topics": ["అక్షాంశాలు మరియు రేఖాంశాలు", "భూభ్రమణం, భూపరిభ్రమణం", "ఋతువులు"], "summary": "భూమి ఆకారం, అక్షాంశ రేఖాంశాలు మరియు పగలు-రాత్రి చక్రం."},
                    {"num": 3, "title": "తెలంగాణ భూస్వరూపాలు", "topics": ["పీఠభూములు, మైదానాలు మరియు కొండలు", "గోదావరి, కృష్ణా పరివాహక ప్రాంతాలు", "జీవన విధానం"], "summary": "తెలంగాణ దక్కన్ పీఠభూమి నేలలు, చెరువులు మరియు వ్యవసాయం."}
                ]
            }
        ]
    },
    "7": {
        "EM": [
            {
                "id": "sanskrit_7",
                "name": "Sanskrit",
                "teluguName": "సంస్కృతం",
                "icon": "📜",
                "iconBg": "#FFF8E1",
                "iconColor": "#FF8F00",
                "progress": 20,
                "pdf": "7_SAN_CC.pdf",
                "chapters": [
                    {"num": 1, "title": "Subhashitani", "topics": ["Gems of Wisdom", "Truth and Charity", "Noble Character"], "summary": "Reflective moral verses guiding right conduct and truthfulness."},
                    {"num": 2, "title": "Dur-buddhir Vinashyati", "topics": ["The Foolish Turtle Fable", "Power of Speech Control", "Panchatantra Story"], "summary": "Classic Panchatantra tale cautioning against talking out of turn."},
                    {"num": 3, "title": "Swavalambanam", "topics": ["Self-Reliance", "Dignity of Labour", "Daily Chores"], "summary": "Lesson celebrating the happiness and freedom that comes from self-reliance."},
                    {"num": 4, "title": "Pandita Ramabai", "topics": ["Biography of Social Reformer", "Women's Education in India"], "summary": "Inspirational life of pioneering scholar and social reformer Pandita Ramabai."}
                ]
            },
            {
                "id": "math_7",
                "name": "Mathematics",
                "teluguName": "గణితం",
                "icon": "📐",
                "iconBg": "#FFF1C8",
                "iconColor": "#996100",
                "progress": 30,
                "pdf": "7 Maths EM.pdf",
                "chapters": [
                    {"num": 1, "title": "Integers", "topics": ["Properties of Addition & Subtraction", "Multiplication & Division of Integers", "Word Problems"], "summary": "Rules of signs, commutative, associative properties of integers."},
                    {"num": 2, "title": "Fractions, Decimals and Rational Numbers", "topics": ["Multiplication & Division of Fractions", "Operations on Decimals", "Rational Numbers Concept"], "summary": "Arithmetic operations on rational numbers and decimal conversions."},
                    {"num": 3, "title": "Simple Equations", "topics": ["Forming Equations", "Transposition Method", "Real-Life Applications"], "summary": "Solving linear equations in one variable."},
                    {"num": 4, "title": "Lines and Angles", "topics": ["Complementary & Supplementary Angles", "Adjacent Angles", "Parallel Lines & Transversal"], "summary": "Angle relationships formed when parallel lines are cut by a transversal."},
                    {"num": 5, "title": "Triangle and Its Properties", "topics": ["Medians & Altitudes", "Angle Sum Property", "Pythagoras Property"], "summary": "Fundamental properties of triangles and right-angled triangle theorem."},
                    {"num": 6, "title": "Ratio - Applications", "topics": ["Percentages", "Profit and Loss", "Simple Interest Formula (PTR/100)"], "summary": "Commercial arithmetic calculations for interest and trade margins."},
                    {"num": 7, "title": "Data Handling", "topics": ["Arithmetic Mean", "Median and Mode", "Double Bar Graphs"], "summary": "Measures of central tendency and comparative data visualization."},
                    {"num": 8, "title": "Congruency of Triangles", "topics": ["Congruence Criteria (SSS, SAS, ASA, RHS)"], "summary": "Establishing geometric equality and triangle congruence."},
                    {"num": 9, "title": "Construction of Triangles (Practical Geometry)", "topics": ["Constructing Triangles with SSS, SAS, ASA, RHS", "Using Compass and Ruler"], "summary": "Step-by-step practical geometric construction of triangles with given parameters."},
                    {"num": 10, "title": "Algebraic Expressions", "topics": ["Terms, Factors, Coefficients", "Like and Unlike Terms", "Addition and Subtraction"], "summary": "Forming algebraic expressions and combining like terms."}
                ]
            },
            {
                "id": "phy_7",
                "name": "Physical Science",
                "teluguName": "భౌతిక శాస్త్రం",
                "icon": "⚡",
                "iconBg": "#EDE7F6",
                "iconColor": "#512DA8",
                "progress": 30,
                "pdf": "7th science em pdf 2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "Motion and Time", "topics": ["Uniform vs Non-Uniform Motion", "Speed Formula (Distance/Time)", "Simple Pendulum"], "summary": "Measuring speed, distance-time graphs, and oscillatory timekeeping."},
                    {"num": 2, "title": "Temperature and Its Measurement", "topics": ["Clinical vs Laboratory Thermometers", "Heat Transfer (Conduction, Convection, Radiation)"], "summary": "Thermal scales and mechanisms of heat propagation through matter."},
                    {"num": 3, "title": "Electricity - Current and Its Effects", "topics": ["Electric Symbols", "Heating Effect (Fuse)", "Magnetic Effect & Electromagnets"], "summary": "Joule heating, safety fuses, and constructing temporary electromagnets."},
                    {"num": 4, "title": "Air, Winds and Cyclones", "topics": ["Atmospheric Pressure", "High-Speed Winds", "Thunderstorms and Cyclones"], "summary": "Air convection currents, storms, and disaster mitigation."},
                    {"num": 5, "title": "Light: Reflection and Dispersion", "topics": ["Plane & Spherical Mirrors", "Lenses", "Dispersion & Newton's Disc"], "summary": "Reflection, convergence/divergence in lenses, and rainbow dispersion."}
                ]
            },
            {
                "id": "bio_7",
                "name": "Biological Science",
                "teluguName": "జీవశాస్త్రం",
                "icon": "🌿",
                "iconBg": "#E8F5E9",
                "iconColor": "#2E7D32",
                "progress": 35,
                "pdf": "7th science em pdf 2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "Food Components", "topics": ["Carbohydrates, Proteins, Fats", "Vitamins & Minerals", "Deficiency Diseases"], "summary": "Nutrient identification tests and balanced dietary health."},
                    {"num": 2, "title": "Acids and Bases", "topics": ["Natural Indicators (Litmus, Turmeric)", "Neutralisation Reaction", "Salts"], "summary": "pH indicators and everyday neutralisation remedies."},
                    {"num": 3, "title": "Animal Fibre", "topics": ["Silk Production (Sericulture)", "Wool Extraction from Sheep"], "summary": "Silkworm lifecycle and wool processing stages."},
                    {"num": 4, "title": "Weather and Climate", "topics": ["Weather Elements", "Animal Adaptations in Polar & Tropical Regions"], "summary": "Meteorology and wildlife morphological adaptations."},
                    {"num": 5, "title": "Respiration in Organisms", "topics": ["Aerobic vs Anaerobic", "Breathing Mechanism in Humans, Fish, Insects"], "summary": "Cellular respiration and diverse respiratory organs."},
                    {"num": 6, "title": "Reproduction in Plants", "topics": ["Asexual Modes (Budding, Spores)", "Pollination & Fertilisation"], "summary": "Floral reproductive biology and seed dispersal."}
                ]
            },
            {
                "id": "sci_7",
                "name": "General Science",
                "teluguName": "సామాన్య శాస్త్రం",
                "icon": "🔬",
                "iconBg": "#E0F2F1",
                "iconColor": "#00796B",
                "progress": 30,
                "pdf": "7th science em pdf 2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "Food Components", "topics": ["Nutrition", "Vitamins", "Deficiency"], "summary": "Components of balanced diet and nutritional health."},
                    {"num": 2, "title": "Acids and Bases", "topics": ["Indicators", "Salts", "Neutralisation"], "summary": "Chemical properties of common acids, bases, and salts."},
                    {"num": 3, "title": "Animal Fibre", "topics": ["Silk", "Wool", "Sericulture"], "summary": "Animal fibres and industrial textile processing."},
                    {"num": 4, "title": "Motion and Time", "topics": ["Speed", "Pendulum", "Time Units"], "summary": "Kinematics and measurement of time intervals."},
                    {"num": 5, "title": "Temperature and Its Measurement", "topics": ["Thermometers", "Conduction", "Radiation"], "summary": "Thermal physics and temperature measurements."}
                ]
            },
            {
                "id": "eng_7",
                "name": "English Reader",
                "teluguName": "ఆంగ్లం",
                "icon": "📖",
                "iconBg": "#FBE9E7",
                "iconColor": "#D84315",
                "progress": 35,
                "pdf": "7 English Reader-2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "The Town Mouse and The Country Mouse", "topics": ["Fable Adaptation", "Simplicity vs Luxury", "Grammar: Clauses"], "summary": "Entertaining fable contrasting simple village life with noisy town life."},
                    {"num": 2, "title": "C.V. Raman, The Pride of India", "topics": ["Nobel Laureate Biography", "Raman Effect Discovery", "Scientific Spirit"], "summary": "Story of Sir C.V. Raman's groundbreaking optics research."},
                    {"num": 3, "title": "Puru, The Brave", "topics": ["Historical Drama", "King Puru and Alexander", "Courage and Self-Respect"], "summary": "Inspiring dialogue between King Porus and Alexander the Great."},
                    {"num": 4, "title": "Tenali Paints a Horse", "topics": ["Wit and Humour", "Tenali Ramalinga's Cleverness", "Grammar: Modals"], "summary": "Humorous courtroom story of Tenali Raman's witty painting challenge."}
                ]
            }
        ],
        "TM": [
            {
                "id": "tel_7_tm",
                "name": "తెలుగు",
                "teluguName": "తెలుగు",
                "icon": "📚",
                "iconBg": "#FFE0B2",
                "iconColor": "#E65100",
                "progress": 30,
                "pdf": "7th Telugu FL 2026-27 Inner.pdf",
                "chapters": [
                    {"num": 1, "title": "చదువు", "topics": ["కొఱవి గోపరాజు", "చదువు ఆవశ్యకత", "విక్రమార్కుని కథలు"], "summary": "విద్య యొక్క ప్రాముఖ్యత మరియు జ్ఞాన సంపాదన గొప్పతనం."},
                    {"num": 2, "title": "నాయనమ్మ", "topics": ["కుటుంబ అనుబంధాలు", "వృద్ధుల పట్ల ప్రేమ, గౌరవం"], "summary": "కుటుంబంలో పెద్దల పట్ల పిల్లలు చూపించవలసిన గౌరవ భావం."},
                    {"num": 3, "title": "శతక సుధ", "topics": ["నీతి పద్యాలు", "భావామృతం", "ఛందస్సు"], "summary": "సమాజంలో మంచి ప్రవర్తనను పెంపొందించే శతక పద్యాలు."},
                    {"num": 4, "title": "అమ్మ జ్ఞాపకాలు", "topics": ["మాతృమూర్తి త్యాగం", "కవితా సౌందర్యం"], "summary": "తల్లి ప్రేమ, త్యాగం మరియు అనురాగాన్ని గుర్తుచేసుకునే భావకవిత."},
                    {"num": 5, "title": "ప్రేరణ", "topics": ["డాక్టర్ ఏ.పి.జె. అబ్దుల్ కలాం", "శాస్త్రవేత్త ప్రయాణం", "స్ఫూర్తిదాయక జీవితం"], "summary": "మాజీ రాష్ట్రపతి కలాం గారి బాల్యం మరియు శాస్త్రవేత్తగా ఎదిగిన స్ఫూర్తిదాయక కథ."}
                ]
            },
            {
                "id": "eng_7_tm",
                "name": "ఆంగ్లం",
                "teluguName": "ఆంగ్లం",
                "icon": "📖",
                "iconBg": "#FBE9E7",
                "iconColor": "#D84315",
                "progress": 25,
                "pdf": "7 English Reader-2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "The Town Mouse and The Country Mouse (పట్టణపు ఎలుక, పల్లెటూరి ఎలుక)", "topics": ["నీతికథ", "పదజాలం", "సరళ ఆంగ్ల వాక్యాలు"], "summary": "పట్టణ, గ్రామీణ జీవన విధానాల మధ్య తేడాలను వివరించే ఆసక్తికరమైన కథ."},
                    {"num": 2, "title": "C.V. Raman, The Pride of India (సి.వి. రామన్)", "topics": ["భారతీయ శాస్త్రవేత్త", "రామన్ ఎఫెక్ట్", "నోబెల్ పురస్కారం"], "summary": "సర్ సి.వి. రామన్ గారి జీవితం మరియు భౌతిక శాస్త్ర పరిశోధనల పరిచయం."}
                ]
            },
            {
                "id": "math_7_tm",
                "name": "గణితం",
                "teluguName": "గణితం",
                "icon": "📐",
                "iconBg": "#FFF1C8",
                "iconColor": "#996100",
                "progress": 30,
                "pdf": "7 Maths TM.pdf",
                "chapters": [
                    {"num": 1, "title": "పూర్ణ సంఖ్యలు", "topics": ["సంకలనం, వ్యవకలనం ధర్మాలు", "గుణకారం మరియు భాగహారం"], "summary": "పూర్ణ సంఖ్యల లక్షణాలు మరియు పరిక్రియలు."},
                    {"num": 2, "title": "భిన్నాలు, దశాంశాలు మరియు అకరణీయ సంఖ్యలు", "topics": ["భిన్నాల గుణకారం", "దశాంశాల భాగహారం"], "summary": "భిన్నాలు మరియు దశాంశాల సాధనలు."},
                    {"num": 3, "title": "సరళ సమీకరణాలు", "topics": ["సమీకరణాన్ని రూపొందించడం", "పక్షాంతరం ద్వారా సాధన"], "summary": "ఏక చరరాశిలో రేఖీయ సమీకరణాల సాధన."},
                    {"num": 4, "title": "రేఖలు మరియు కోణాలు", "topics": ["పూరక, సంపూరక కోణాలు", "సమాంతర రేఖలు - తిర్యగ్రేఖ"], "summary": "కోణాల జతలు మరియు రేఖీయ లక్షణాలు."},
                    {"num": 5, "title": "త్రిభుజం మరియు దాని ధర్మాలు", "topics": ["మధ్యగత రేఖలు, ఉన్నతులు", "పైథాగరస్ సిద్ధాంతం"], "summary": "త్రిభుజ కోణాల మొత్తం ధర్మం మరియు పైథాగరస్ అనువర్తనం."},
                    {"num": 6, "title": "త్రిభుజాల నిర్మాణాలు (ప్రాయోగిక జ్యామితి)", "topics": ["SSS, SAS, ASA కొలతలతో త్రిభుజాల నిర్మాణం", "స్కేలు, కంపాస్ ఉపయోగం"], "summary": "ఇచ్చిన కొలతలతో స్కేలు, కంపాస్ సహాయంతో త్రిభుజాలను నిర్మించే విధానం."}
                ]
            },
            {
                "id": "phy_7_tm",
                "name": "భౌతిక శాస్త్రం",
                "teluguName": "భౌతిక శాస్త్రం",
                "icon": "⚡",
                "iconBg": "#EDE7F6",
                "iconColor": "#512DA8",
                "progress": 30,
                "pdf": "7th genral science tm 2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "చలనం మరియు కాలం", "topics": ["క్రమ, అక్రమ చలనాలు", "వడి సూత్రం (దూరం/కాలం)", "లోలకం"], "summary": "వడి గణన మరియు కాల గణన విధానాలు."},
                    {"num": 2, "title": "ఉష్ణోగ్రత మరియు దాని కొలత", "topics": ["థర్మామీటర్ రకాలు", "ఉష్ణ సంక్రమణ పద్ధతులు (ఉష్ణవహనం, ఉష్ణసంవహనం, వికిరణం)"], "summary": "ఉష్ణ ప్రసార పద్ధతులు మరియు ఉష్ణోగ్రత కొలతలు."},
                    {"num": 3, "title": "విద్యుత్ ప్రవాహం మరియు దాని ఫలితాలు", "topics": ["విద్యుత్ చిహ్నాలు", "ఉష్ణ ఫలితం (ఫ్యూజ్)", "విద్యుదయస్కాంతాలు"], "summary": "కరెంట్ ఉష్ణ మరియు అయస్కాంత ప్రభావాలు."}
                ]
            },
            {
                "id": "bio_7_tm",
                "name": "జీవశాస్త్రం",
                "teluguName": "జీవశాస్త్రం",
                "icon": "🌿",
                "iconBg": "#E8F5E9",
                "iconColor": "#2E7D32",
                "progress": 35,
                "pdf": "7th genral science tm 2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "ఆహారంలోని అంశాలు", "topics": ["పిండిపదార్థాలు, మాంసకృత్తులు, కొవ్వులు", "విటమిన్లు", "సమతులాహారం"], "summary": "ఆహార పరీక్షలు మరియు లోప వ్యాధుల నివారణ."},
                    {"num": 2, "title": "ఆమ్లాలు - క్షారాలు", "topics": ["సహజ సూచికలు", "తటస్థీకరణ చర్య", "లవణాలు"], "summary": "ఆమ్ల క్షార లక్షణాలు మరియు నిత్యజీవిత అనువర్తనాలు."},
                    {"num": 3, "title": "పట్టు - ఉన్ని", "topics": ["పట్టు పురుగు జీవిత చక్రం", "గొర్రెల నుండి ఉన్ని తీయడం"], "summary": "జంతువుల నుండి సహజ దారాలు లభించే విధానం."}
                ]
            },
            {
                "id": "soc_7_tm",
                "name": "సాంఘిక శాస్త్రం",
                "teluguName": "సాంఘిక శాస్త్రం",
                "icon": "🌍",
                "iconBg": "#FFF9C4",
                "iconColor": "#F57F17",
                "progress": 20,
                "pdf": "7th Social TM-2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "పటాల అధ్యయనం మరియు విశ్లేషణ", "topics": ["ఎత్తులు చూపించే పటాలు", "కాంటూర్ రేఖలు"], "summary": "భూస్వరూపాల ఎత్తులను పటాలలో చూపించే విధానం."},
                    {"num": 2, "title": "చెరువులు మరియు భూగర్భ జలాలు", "topics": ["గొలుసుకట్టు చెరువులు", "రీఛార్జ్ బావులు"], "summary": "తెలంగాణ గొలుసుకట్టు చెరువుల వ్యవస్థ మరియు నీటి సంరక్షణ."},
                    {"num": 3, "title": "కాకతీయులు - తెలంగాణ వైభవం", "topics": ["రుద్రమదేవి", "ప్రతాపరుద్రుడు", "వరంగల్ కోట నిర్మాణం"], "summary": "కాకతీయ రాజుల పరిపాలన, చెరువుల నిర్మాణం మరియు కళా వైభవం."}
                ]
            }
        ]
    },
    "8": {
        "EM": [
            {
                "id": "sanskrit_8",
                "name": "Sanskrit",
                "teluguName": "సంస్కృతం",
                "icon": "📜",
                "iconBg": "#FFF8E1",
                "iconColor": "#FF8F00",
                "progress": 20,
                "pdf": "8_san_cc.pdf",
                "chapters": [
                    {"num": 1, "title": "Subhashitani", "topics": ["Ethical Maxims", "Value of Knowledge and Friendship"], "summary": "Subhashitas teaching universal virtues and intellectual pursuit."},
                    {"num": 2, "title": "Bilasya Vani Na Kadapi Me Shruta", "topics": ["Panchatantra Lion and Jackal", "Presence of Mind"], "summary": "Clever story demonstrating how alertness averts danger."},
                    {"num": 3, "title": "Digi-Bharatam", "topics": ["Digital India Initiative", "Modern Sanskrit Vocabulary"], "summary": "Sanskrit narrative describing technological advancement in India."},
                    {"num": 4, "title": "Sadaiva Purato Nidhehi Charanam", "topics": ["Patriotic Marching Song", "Overcoming Obstacles with Courage"], "summary": "Motivational song urging youth to keep marching forward."}
                ]
            },
            {
                "id": "math_8",
                "name": "Mathematics",
                "teluguName": "గణితం",
                "icon": "📐",
                "iconBg": "#FFF1C8",
                "iconColor": "#996100",
                "progress": 30,
                "pdf": "8 Maths EM.pdf",
                "chapters": [
                    {"num": 1, "title": "Rational Numbers", "topics": ["Properties of Rational Numbers", "Distributive Law", "Numbers between Rationals"], "summary": "p/q form numbers, density property, and arithmetic operations."},
                    {"num": 2, "title": "Linear Equations in One Variable", "topics": ["Equations with Variables on Both Sides", "Age and Number Word Problems"], "summary": "Algebraic modeling and linear equation algorithms."},
                    {"num": 3, "title": "Construction of Quadrilaterals (Practical Geometry)", "topics": ["Constructing Quadrilaterals with 4 Sides and 1 Diagonal", "Special Quadrilaterals (Parallelogram, Rhombus, Rectangle)"], "summary": "Precision compass-and-ruler constructions of various quadrilaterals."},
                    {"num": 4, "title": "Exponents and Powers", "topics": ["Negative Exponents", "Laws of Exponents", "Scientific Notation"], "summary": "Standard exponential form for microscopic and astronomical numbers."},
                    {"num": 5, "title": "Comparing Quantities using Proportion", "topics": ["Compound Ratio & Percentages", "Discount, Profit and Loss", "Compound Interest Formula"], "summary": "Commercial arithmetic and compound growth formulas."}
                ]
            },
            {
                "id": "phy_8",
                "name": "Physical Science",
                "teluguName": "భౌతిక శాస్త్రం",
                "icon": "⚡",
                "iconBg": "#EDE7F6",
                "iconColor": "#512DA8",
                "progress": 30,
                "pdf": "viii class physical science_em_2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "Force", "topics": ["Contact vs Non-Contact Forces", "Gravitational & Electrostatic Forces", "Pressure (Force/Area)"], "summary": "Net force vectors, atmospheric pressure, and liquid pressure dynamics."},
                    {"num": 2, "title": "Friction", "topics": ["Factors Affecting Friction", "Static, Sliding and Rolling Friction", "Lubricants"], "summary": "Microscopic interlocking, ball bearings, and reducing energy dissipation."},
                    {"num": 3, "title": "Synthetic Fibres and Plastics", "topics": ["Rayon, Nylon, Polyester", "Thermoplastics vs Thermosetting", "4R Principle"], "summary": "Polymer chemistry and environmental waste management."},
                    {"num": 4, "title": "Metals and Non-Metals", "topics": ["Malleability & Ductility", "Reactions with Oxygen and Acids", "Reactivity Series"], "summary": "Physical and chemical properties of elemental metals and alloys."},
                    {"num": 5, "title": "Sound", "topics": ["Vibration as Source", "Human Larynx", "Amplitude, Pitch & Frequency", "Noise Pollution"], "summary": "Sound wave propagation, human audibility range, and hearing conservation."}
                ]
            },
            {
                "id": "bio_8",
                "name": "Biological Science",
                "teluguName": "జీవశాస్త్రం",
                "icon": "🌿",
                "iconBg": "#E8F5E9",
                "iconColor": "#2E7D32",
                "progress": 35,
                "pdf": "viii biology em inner 2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "What is Science?", "topics": ["Scientific Inquiry", "Hypotheses and Experiments", "Laboratory Safety"], "summary": "Empirical scientific methods and research ethics."},
                    {"num": 2, "title": "Cell - The Basic Unit of Life", "topics": ["Discovery of Cell (Robert Hooke)", "Plant vs Animal Cells (Onion Peel, Cheek Cells)", "Cell Organelles"], "summary": "Cell wall, membrane, nucleus, cytoplasm, and microscopic observation."},
                    {"num": 3, "title": "The World of Microorganisms Part 1 & 2", "topics": ["Bacteria, Fungi, Protozoa & Algae", "Viruses & Useful Microbes (Curd, Penicillin)", "Food Poisoning"], "summary": "Microbial diversity, fermentation, antibiotics, and disease control."},
                    {"num": 4, "title": "Reproduction in Animals", "topics": ["Asexual Modes (Binary Fission, Budding)", "Internal vs External Fertilization", "Frog Metamorphosis"], "summary": "Sexual and asexual reproduction, zygotes, and embryo development."},
                    {"num": 5, "title": "The Age of Adolescence", "topics": ["Puberty & Secondary Sexual Characteristics", "Endocrine Hormones", "Nutritional Needs"], "summary": "Endocrine regulation, growth spurts, and adolescent health."}
                ]
            },
            {
                "id": "sci_8",
                "name": "General Science",
                "teluguName": "సామాన్య శాస్త్రం",
                "icon": "🔬",
                "iconBg": "#E0F2F1",
                "iconColor": "#00796B",
                "progress": 30,
                "pdf": "viii class physical science_em_2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "Force and Pressure", "topics": ["Types of Forces", "Atmospheric Pressure"], "summary": "Newtonian forces and pressure principles."},
                    {"num": 2, "title": "Cell Biology", "topics": ["Cell Structure", "Microscope Work"], "summary": "Cell organelles and foundational cytological concepts."},
                    {"num": 3, "title": "Friction and Energy", "topics": ["Tribology", "Energy Loss"], "summary": "Frictional resistance and mechanical efficiency."}
                ]
            },
            {
                "id": "eng_8",
                "name": "English Reader",
                "teluguName": "ఆంగ్లం",
                "icon": "📖",
                "iconBg": "#FBE9E7",
                "iconColor": "#D84315",
                "progress": 40,
                "pdf": "8 English Reader-2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "The Best Christmas Present in the World", "topics": ["WWI Christmas Truce", "Letter from the Trenches", "Humanity in Wartime"], "summary": "Heart-warming historical fiction on peace amidst World War I."},
                    {"num": 2, "title": "The Tsunami", "topics": ["2004 Tsunami Stories", "Animal Instincts & Survival Courage"], "summary": "Real-life narratives of bravery and resilience during natural catastrophe."},
                    {"num": 3, "title": "Glimpses of the Past", "topics": ["Freedom Struggle Pictorial", "1857 First War of Independence"], "summary": "Graphic history of India's struggle against British colonial rule."},
                    {"num": 4, "title": "Bepin Choudhury's Lapse of Memory", "topics": ["Psychological Comedy", "Friendship Trick", "Grammar: Conditionals"], "summary": "Satyajit Ray's witty tale of an elaborate prank played on a busy man."}
                ]
            }
        ],
        "TM": [
            {
                "id": "tel_8_tm",
                "name": "తెలుగు",
                "teluguName": "తెలుగు",
                "icon": "📚",
                "iconBg": "#FFE0B2",
                "iconColor": "#E65100",
                "progress": 30,
                "pdf": "8th telugu fl inner 2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "త్యాగనిరతి", "topics": ["నన్నయ భారతం", "శిబి చక్రవర్తి త్యాగం", "శరణాగత రక్షణ"], "summary": "శరణు కోరిన పావురాన్ని రక్షించడానికి తన దేహాన్ని అర్పించిన శిబి చక్రవర్తి త్యాగ గుణం."},
                    {"num": 2, "title": "సముద్ర లంఘనం", "topics": ["వాల్మీకి రామాయణం", "హనుమంతుని శౌర్యం", "సముద్రం దాటడం"], "summary": "సీతాన్వేషణకై మహేంద్ర పర్వతం నుండి లంకకు ఎగిరిన హనుమంతుని అద్భుత పరాక్రమం."},
                    {"num": 3, "title": "బండారి బసవన్న", "topics": ["పాల్కురికి సోమనాథుడు", "నిజాయితీ మరియు భక్తి"], "summary": "రాజకోశాగారాధికారి బండారి బసవన్న అచంచల భక్తి మరియు నిష్కళంక నిజాయితీ."},
                    {"num": 4, "title": "అసామాన్యులు", "topics": ["చేతివృత్తుల శ్రమ సౌందర్యం", "కార్మికుల గౌరవం"], "summary": "సమాజానికి సేవలందిస్తూ జీవించే కమ్మరి, కుమ్మరి, నేత కార్మికుల శ్రమను గౌరవించడం."}
                ]
            },
            {
                "id": "eng_8_tm",
                "name": "ఆంగ్లం",
                "teluguName": "ఆంగ్లం",
                "icon": "📖",
                "iconBg": "#FBE9E7",
                "iconColor": "#D84315",
                "progress": 25,
                "pdf": "8 English Reader-2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "The Best Christmas Present in the World (ప్రపంచంలోనే ఉత్తమ క్రిస్మస్ బహుమతి)", "topics": ["యుద్ధంలో శాంతి", "లేఖ", "ఆంగ్ల పదజాలం"], "summary": "మొదటి ప్రపంచ యుద్ధ సమయంలో సైనికులు చాటిన మానవతా విలువలు."},
                    {"num": 2, "title": "The Tsunami (సునామీ విషాదం మరియు సాహసం)", "topics": ["ప్రకృతి విపత్తు", "ధైర్యసాహసాలు"], "summary": "సునామీ విపత్తులో ప్రాణాలు కాపాడిన ధైర్యవంతుల యదార్థ కథలు."}
                ]
            },
            {
                "id": "math_8_tm",
                "name": "గణితం",
                "teluguName": "గణితం",
                "icon": "📐",
                "iconBg": "#FFF1C8",
                "iconColor": "#996100",
                "progress": 30,
                "pdf": "8 Maths TM 2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "అకరణీయ సంఖ్యలు", "topics": ["సంవృత, స్థిత్యంతర, సహచర ధర్మాలు", "విభాగ న్యాయం"], "summary": "p/q రూప సంఖ్యలు మరియు వాటి పరిక్రియలు."},
                    {"num": 2, "title": "ఏక చరరాశిలో రేఖీయ సమీకరణాలు", "topics": ["ఇరువైపులా చరరాశులు గల సమీకరణాలు", "సమస్యల సాధన"], "summary": "బీజీయ సమీకరణాల రూపకల్పన మరియు సాధన."},
                    {"num": 3, "title": "చతుర్భుజాల నిర్మాణాలు (ప్రాయోగిక జ్యామితి)", "topics": ["4 భుజాలు, 1 కర్ణం ఇచ్చినప్పుడు చతుర్భుజ నిర్మాణం", "సమాంతర చతుర్భుజం, రాంబస్ నిర్మాణాలు"], "summary": "స్కేలు, కంపాస్ ఉపయోగించి చతుర్భుజాలను ఖచ్చితంగా నిర్మించే ప్రాయోగిక జ్యామితి పద్ధతులు."},
                    {"num": 4, "title": "ఘాతాంకాలు మరియు ఘాతాలు", "topics": ["రుణ ఘాతాంకాలు", "ఘాతాంక న్యాయాలు"], "summary": "అతిపెద్ద మరియు అతిచిన్న సంఖ్యలను ప్రామాణిక రూపంలో రాయడం."}
                ]
            },
            {
                "id": "phy_8_tm",
                "name": "భౌతిక శాస్త్రం",
                "teluguName": "భౌతిక శాస్త్రం",
                "icon": "⚡",
                "iconBg": "#EDE7F6",
                "iconColor": "#512DA8",
                "progress": 30,
                "pdf": "VIII Physical Science (TM)  2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "బలం", "topics": ["స్పర్శా బలాలు మరియు క్షేత్ర బలాలు", "గురుత్వాకర్షణ, ఘర్షణ బలం", "పీడనం (బలం/వైశాల్యం)"], "summary": "తోసే లేదా లాగే శక్తులు, వాతావరణ పీడనం మరియు ద్రవాల పీడనం."},
                    {"num": 2, "title": "ఘర్షణ", "topics": ["ఘర్షణను ప్రభావితం చేసే అంశాలు", "స్థితిక, జారుడు, దొర్లుడు ఘర్షణ", "కందెనలు"], "summary": "ఘర్షణ లాభనష్టాలు మరియు బాల్ బేరింగ్‌ల ఉపయోగం."},
                    {"num": 3, "title": "కృత్రిమ దారాలు మరియు ప్లాస్టిక్‌లు", "topics": ["రేయాన్, నైలాన్, పాలియెస్టర్", "థర్మోప్లాస్టిక్ మరియు థర్మోసెట్టింగ్", "4R సూత్రం"], "summary": "పాలిమర్ రకాలు మరియు ప్లాస్టిక్ కాలుష్య నివారణ."},
                    {"num": 4, "title": "లోహాలు మరియు అలోహాలు", "topics": ["ద్యుతిగుణం, స్తరనీయత, తాంతవత", "ఆమ్లాలు, ఆక్సిజన్‌తో చర్యలు"], "summary": "లోహాల భౌతిక మరియు రసాయన ధర్మాలు."},
                    {"num": 5, "title": "ధ్వని", "topics": ["కంపించే వస్తువుల ధ్వని ఉత్పత్తి", "మానవ స్వరపేటిక", "తీవ్రత, పిచ్, పౌనఃపున్యం"], "summary": "ధ్వని తరంగ ప్రసారం మరియు శబ్ద కాలుష్య నియంత్రణ."}
                ]
            },
            {
                "id": "bio_8_tm",
                "name": "జీవశాస్త్రం",
                "teluguName": "జీవశాస్త్రం",
                "icon": "🌿",
                "iconBg": "#E8F5E9",
                "iconColor": "#2E7D32",
                "progress": 35,
                "pdf": "viii biology tm inner 2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "సైన్స్ అంటే ఏమిటి?", "topics": ["శాస్త్రీయ పద్ధతి", "పరిశీలనలు మరియు ప్రయోగాలు"], "summary": "శాస్త్రీయ దృక్పథం మరియు ప్రయోగశాల భద్రత."},
                    {"num": 2, "title": "కణం - జీవుల ప్రాథమిక ప్రమాణం", "topics": ["కణ ఆవిష్కరణ", "వృక్ష మరియు జంతు కణాలు", "కణాంగాలు"], "summary": "కణ నిర్మాణం, కేంద్రకం మరియు సూక్ష్మదర్శిని పరిశీలన."},
                    {"num": 3, "title": "సూక్ష్మజీవుల ప్రపంచం భాగం 1 & 2", "topics": ["బ్యాక్టీరియా, శిలీంధ్రాలు, శైవలాలు", "వైరస్‌లు, ఉపయోగకర సూక్ష్మజీవులు (యాంటీబయాటిక్స్)"], "summary": "సూక్ష్మజీవుల ప్రయోజనాలు మరియు అంటువ్యాధుల నివారణ."},
                    {"num": 4, "title": "జంతువులలో ప్రత్యుత్పత్తి", "topics": ["అలైంగిక ప్రత్యుత్పత్తి (ద్విధావిచ్ఛితి, కోరకీభవనం)", "ఫలదీకరణం", "కప్ప రూపాంతరం"], "summary": "సంతానోత్పత్తి రకాలు మరియు పిండం అభివృద్ధి దశలు."}
                ]
            },
            {
                "id": "soc_8_tm",
                "name": "సాంఘిక శాస్త్రం",
                "teluguName": "సాంఘిక శాస్త్రం",
                "icon": "🌍",
                "iconBg": "#FFF9C4",
                "iconColor": "#F57F17",
                "progress": 20,
                "pdf": "8th Social TM_2026-2027_Errata_FINAL (1).pdf",
                "chapters": [
                    {"num": 1, "title": "భూగోళంపై మానవుల ప్రభావం", "topics": ["పర్యావరణం మరియు వనరుల వినియోగం"], "summary": "మానవ కార్యకలాపాలు మరియు పర్యావరణ పరిరక్షణ."},
                    {"num": 2, "title": "చేతివృత్తులు మరియు పారిశ్రామికీకరణ", "topics": ["చేనేత పరిశ్రమ", "యంత్రాల రాకతో మార్పులు"], "summary": "పారిశ్రామిక విప్లవం మరియు సంప్రదాయ వృత్తుల స్థితిగతులు."},
                    {"num": 3, "title": "జమీందారీ వ్యవస్థ రద్దు మరియు తెలంగాణ సాయుధ పోరాటం", "topics": ["దొరల పెత్తనం", "తెలంగాణ రైతాంగ సాయుధ పోరాటం"], "summary": "భూస్వామ్య పీడనపై తెలంగాణ ప్రజల చారిత్రక సాయుధ తిరుగుబాటు."}
                ]
            }
        ]
    },
    "9": {
        "EM": [
            {
                "id": "sanskrit_9",
                "name": "Sanskrit",
                "teluguName": "సంస్కృతం",
                "icon": "📜",
                "iconBg": "#FFF8E1",
                "iconColor": "#FF8F00",
                "progress": 20,
                "pdf": "9_SAN_CC.pdf",
                "chapters": [
                    {"num": 1, "title": "Bharati-Vasant-Gitih", "topics": ["Saraswati Vandana", "Spring Nature Lyric", "Classical Metres"], "summary": "Melodious invocation to Goddess Saraswati celebrating spring renewal."},
                    {"num": 2, "title": "Swarna-Kakah", "topics": ["Golden Crow Fable", "Greed vs Contentment", "Karma Lessons"], "summary": "Burmese-origin folk story contrasting humble virtue with greedy pride."},
                    {"num": 3, "title": "Kalpa-Taruh", "topics": ["Wish-Fulfilling Tree", "Jimutavahana's Compassion", "Selfless Benevolence"], "summary": "Inspiring Buddhist legend of a prince asking the wish-granting tree to end world poverty."},
                    {"num": 4, "title": "Sukti-Mauktikam", "topics": ["Pearls of Wisdom", "Subhashitas on Friendship and Virtue"], "summary": "Poetic verses comparing friendship with shadows and pure gold."}
                ]
            },
            {
                "id": "math_9",
                "name": "Mathematics",
                "teluguName": "గణితం",
                "icon": "📐",
                "iconBg": "#FFF1C8",
                "iconColor": "#996100",
                "progress": 35,
                "pdf": "9th Maths EM.pdf",
                "chapters": [
                    {"num": 1, "title": "Real Numbers", "topics": ["Rational & Irrational Numbers", "Representing Irrationals on Number Line", "Laws of Radicals", "Rationalising Denominators"], "summary": "Real number system, surd properties, and rationalisation techniques."},
                    {"num": 2, "title": "Polynomials and Factorisation", "topics": ["Degree of Polynomial", "Remainder & Factor Theorems", "Algebraic Identities"], "summary": "Factorising quadratics and cubics via identity expansions."},
                    {"num": 3, "title": "The Elements of Geometry", "topics": ["Euclid's Definitions, Axioms & Postulates", "Fifth Postulate Equivalents"], "summary": "Axiomatic foundations of planar Euclidean geometry."},
                    {"num": 4, "title": "Lines and Angles", "topics": ["Linear Pair Axiom", "Parallel Lines & Transversals", "Angle Sum Theorem"], "summary": "Geometric proofs of parallel and intersecting line theorems."},
                    {"num": 5, "title": "Co-Ordinate Geometry", "topics": ["Cartesian Plane", "Quadrants", "Plotting Points (x, y)"], "summary": "Locating positions on grid planes and understanding abscissa/ordinate."},
                    {"num": 6, "title": "Linear Equations in Two Variables", "topics": ["Standard Form ax + by + c = 0", "Graph of Linear Equations"], "summary": "Visualising infinite pairs of solutions on straight lines."},
                    {"num": 7, "title": "Triangles", "topics": ["Congruence Criteria (SAS, ASA, SSS, RHS)", "Inequalities in a Triangle"], "summary": "Rigorous proofs of triangle properties and congruent triangles."},
                    {"num": 8, "title": "Quadrilaterals", "topics": ["Angle Sum of Quadrilateral", "Properties of Parallelograms", "Mid-point Theorem"], "summary": "Proof of midpoint theorem and diagonal properties of parallelograms."},
                    {"num": 9, "title": "Geometrical Constructions (Practical Geometry)", "topics": ["Bisecting Angles", "Perpendicular Bisectors", "Constructing Triangles with Perimeter and Base Angles"], "summary": "Advanced compass and straightedge constructions for precision geometric figures."}
                ]
            },
            {
                "id": "phy_9",
                "name": "Physical Science",
                "teluguName": "భౌతిక శాస్త్రం",
                "icon": "⚡",
                "iconBg": "#EDE7F6",
                "iconColor": "#512DA8",
                "progress": 30,
                "pdf": "ix physics em 2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "Matter Around Us", "topics": ["States of Matter (Solid, Liquid, Gas)", "Latent Heat of Fusion", "Evaporation Factors"], "summary": "Kinetic particle theory of matter and phase change thermodynamics."},
                    {"num": 2, "title": "Motion", "topics": ["Distance vs Displacement", "Uniform & Non-uniform Velocity", "Equations of Motion (v=u+at, s=ut+½at², v²-u²=2as)"], "summary": "Kinematic vector equations and graphical motion curves."},
                    {"num": 3, "title": "Laws of Motion", "topics": ["Newton's First Law & Inertia", "Newton's Second Law (F = ma)", "Newton's Third Law (Action-Reaction)", "Linear Momentum Conservation"], "summary": "Forces, momentum conservation, and rocket propulsion mechanics."},
                    {"num": 4, "title": "Refraction of Light at Plane Surfaces", "topics": ["Refractive Index", "Snell's Law", "Total Internal Reflection & Critical Angle", "Mirages & Optical Fibres"], "summary": "Light refraction at dielectric boundaries and total internal reflection."},
                    {"num": 5, "title": "Gravitation", "topics": ["Universal Gravitation Law (F = G m1m2/r²)", "Acceleration due to Gravity (g)", "Mass vs Weight", "Free Fall"], "summary": "Planetary gravity, orbital acceleration, and weightlessness."}
                ]
            },
            {
                "id": "bio_9",
                "name": "Biological Science",
                "teluguName": "జీవశాస్త్రం",
                "icon": "🌿",
                "iconBg": "#E8F5E9",
                "iconColor": "#2E7D32",
                "progress": 40,
                "pdf": "ix biology em inner 2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "Cell - Structure and Functions", "topics": ["Prokaryotic vs Eukaryotic Cells", "Plasma Membrane & Fluid Mosaic Model", "Organelles (Nucleus, Mitochondria, Chloroplasts)"], "summary": "Ultrastructure and physiological roles of eukaryotic cell organelles."},
                    {"num": 2, "title": "Plant Tissues", "topics": ["Meristematic Tissue", "Dermal & Ground Tissues", "Vascular Tissue (Xylem and Phloem)"], "summary": "Plant histology, mechanical support, and sap transport."},
                    {"num": 3, "title": "Animal Tissues", "topics": ["Epithelial Tissues", "Connective Tissues (Bone, Cartilage, Blood)", "Muscular & Nervous Tissues"], "summary": "Animal histology, neuron anatomy, and blood components."},
                    {"num": 4, "title": "Transportation of materials through Plasma Membrane", "topics": ["Diffusion", "Osmosis (Hypotonic, Hypertonic, Isotonic)", "Plasmolysis"], "summary": "Cellular membrane transport gradients and osmotic equilibrium."},
                    {"num": 5, "title": "Diversity in Living Organisms - Classification", "topics": ["Five Kingdom Classification", "Binomial Nomenclature", "Plant and Animal Phyla"], "summary": "Taxonomic hierarchy and biodiversity classification systems."}
                ]
            },
            {
                "id": "sci_9",
                "name": "General Science",
                "teluguName": "సామాన్య శాస్త్రం",
                "icon": "🔬",
                "iconBg": "#E0F2F1",
                "iconColor": "#00796B",
                "progress": 30,
                "pdf": "ix physics em 2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "Matter in Our Surroundings", "topics": ["States of Matter", "Evaporation"], "summary": "Physical characteristics and changes of state."},
                    {"num": 2, "title": "Forces and Motion", "topics": ["Newton's Laws", "Momentum"], "summary": "Classical mechanics and momentum principles."},
                    {"num": 3, "title": "Cellular Organization", "topics": ["Plant and Animal Cells", "Tissues"], "summary": "Microscopic structural basis of plant and animal biology."}
                ]
            },
            {
                "id": "eng_9",
                "name": "English Reader",
                "teluguName": "ఆంగ్లం",
                "icon": "📖",
                "iconBg": "#FBE9E7",
                "iconColor": "#D84315",
                "progress": 35,
                "pdf": "9 English Reader-2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "Humour: The Snake and the Mirror", "topics": ["Vaikom Muhammad Basheer Story", "Vanity and Fear", "Irony & Humour"], "summary": "Masterful comedy of a vain homeopathic doctor trapped with a cobra."},
                    {"num": 2, "title": "Games and Sports: True Height", "topics": ["Michael Stone Pole Vaulting", "Overcoming Blindness", "Sports Perseverance"], "summary": "Inspiring story of a blind athlete achieving championship victory."},
                    {"num": 3, "title": "School Life: Swami is Expelled from School", "topics": ["R.K. Narayan Malgudi Days", "Child Psychology", "Humour in School Discipline"], "summary": "Delightful excerpt of young Swaminathan's misadventures at school."},
                    {"num": 4, "title": "Environment: What is Man without the Beasts?", "topics": ["Chief Seattle Speech", "Ecological Wisdom", "Sacred Earth"], "summary": "Powerful ecological manifesto advocating deep reverence for nature."}
                ]
            }
        ],
        "TM": [
            {
                "id": "tel_9_tm",
                "name": "తెలుగు",
                "teluguName": "తెలుగు",
                "icon": "📚",
                "iconBg": "#FFE0B2",
                "iconColor": "#E65100",
                "progress": 30,
                "pdf": "9th telugu fl inner 2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "ధర్మబోధ", "topics": ["తిక్కన భారతం", "ధర్మం ప్రాధాన్యత", "సత్యవాక్పరిపాలన"], "summary": "మహాభారతంలోని శాంతి పర్వ ధర్మ సూక్ష్మాలు మరియు సత్యవాక్పాలన."},
                    {"num": 2, "title": "నేనెరిగిన బూర్గుల", "topics": ["బూర్గుల రామకృష్ణారావు", "హైదరాబాద్ తొలి ముఖ్యమంత్రి", "మహనీయుల సేవలు"], "summary": "విజ్ఞాన ఖని, నిరాడంబర నాయకుడు బూర్గుల రామకృష్ణారావు గారి వ్యక్తిత్వ విశేషాలు."},
                    {"num": 3, "title": "వలస కూలీ", "topics": ["డా. ముకురాల రామారెడ్డి", "పాలమూరు వలసలు", "శ్రామికుల వేదన"], "summary": "జీవనోపాధి కోసం పొట్టచేతపట్టుకుని వలసవెళ్లిన తెలంగాణ కూలీల హృదయవిదారక గాధ."},
                    {"num": 4, "title": "రంగాచార్యతో ముఖాముఖి", "topics": ["దాశరథి రంగాచార్య", "తెలంగాణ జనజీవనం", "నవలా సాహిత్యం"], "summary": "తెలంగాణ విముక్తి పోరాటాన్ని చిత్రించిన ప్రముఖ రచయిత దాశరథి రంగాచార్య ఇంటర్వ్యూ."}
                ]
            },
            {
                "id": "eng_9_tm",
                "name": "ఆంగ్లం",
                "teluguName": "ఆంగ్లం",
                "icon": "📖",
                "iconBg": "#FBE9E7",
                "iconColor": "#D84315",
                "progress": 25,
                "pdf": "9 English Reader-2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "Humour: The Snake and the Mirror (పాము మరియు అద్దం)", "topics": ["హాస్య కథ", "ఆంగ్ల వ్యాకరణం", "పదజాలం"], "summary": "అద్దంలో తన అందాన్ని చూసుకునే డాక్టర్ గదిలోకి పాము వచ్చినప్పటి హాస్యభరిత కథ."},
                    {"num": 2, "title": "Games and Sports: True Height (నిజమైన ఎత్తు)", "topics": ["క్రీడా స్ఫూర్తి", "పోల్ వాల్ట్ ఛాంపియన్"], "summary": "కంటిచూపు లేకున్నా పోల్ వాల్ట్ క్రీడలో రికార్డు సృష్టించిన మైఖేల్ స్టోన్ కథ."}
                ]
            },
            {
                "id": "math_9_tm",
                "name": "గణితం",
                "teluguName": "గణితం",
                "icon": "📐",
                "iconBg": "#FFF1C8",
                "iconColor": "#996100",
                "progress": 35,
                "pdf": "9 Maths TM 2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "వాస్తవ సంఖ్యలు", "topics": ["అకరణీయ, కరణీయ సంఖ్యలు", "సంఖ్యా రేఖపై కరణీయ సంఖ్యలు", "కరణుల ధర్మాలు"], "summary": "కరణీయ సంఖ్యల నిరూపణ మరియు హారాల కరణీకరణం."},
                    {"num": 2, "title": "బహుపదులు మరియు కారణాంకాల విభజన", "topics": ["బహుపది పరిమాణం, శూన్యాలు", "శేష సిద్ధాంతం, కారణాంక సిద్ధాంతం"], "summary": "బీజీయ సర్వసమీకరణాలు మరియు బహుపదుల విభజన."},
                    {"num": 3, "title": "జ్యామితి మూల సూత్రాలు - యూక్లిడ్ జ్యామితి", "topics": ["యూక్లిడ్ స్వీకృతాలు", "నిర్వచనాలు"], "summary": "యూక్లిడ్ జ్యామితీయ ప్రాథమిక సూత్రాలు."},
                    {"num": 4, "title": "రేఖలు మరియు కోణాలు", "topics": ["రేఖీయ జత స్వీకృతం", "తిర్యగ్రేఖ కోణాలు"], "summary": "సమాంతర రేఖలు మరియు కోణాల ధర్మాలు."},
                    {"num": 5, "title": "నిరూపక జ్యామితి", "topics": ["కార్టీషియన్ తలం", "పాదాలు, బిందువుల గుర్తింపు"], "summary": "బిందువులను నిరూపక తలంలో గుర్తించడం."},
                    {"num": 6, "title": "జ్యామితీయ నిర్మాణాలు (ప్రాయోగిక జ్యామితి)", "topics": ["కోణ ద్విఖండన రేఖ", "లంబద్విఖండన రేఖ", "చుట్టుకొలత, భూకోణాలు ఇచ్చినపుడు త్రిభుజ నిర్మాణం"], "summary": "కంపాస్, స్కేలు ఉపయోగించి త్రిభుజాల ఖచ్చితమైన నిర్మాణాలు."}
                ]
            },
            {
                "id": "phy_9_tm",
                "name": "భౌతిక శాస్త్రం",
                "teluguName": "భౌతిక శాస్త్రం",
                "icon": "⚡",
                "iconBg": "#EDE7F6",
                "iconColor": "#512DA8",
                "progress": 30,
                "pdf": "ix physics tm 2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "మన చుట్టూ ఉన్న పదార్థం", "topics": ["పదార్థ స్థితులు (ఘన, ద్రవ, వాయు)", "బాష్పీభవనం"], "summary": "కణ సిద్ధాంతం మరియు స్థితి మార్పులు."},
                    {"num": 2, "title": "చలనం", "topics": ["దూరం, స్థానభ్రంశం", "వడి, వేగం, త్వరణం", "చలన సమీకరణాలు"], "summary": "గమన సమీకరణాలు (v = u + at, s = ut + ½at²)."},
                    {"num": 3, "title": "గమన నియమాలు", "topics": ["న్యూటన్ మొదటి, రెండవ, మూడవ నియమాలు", "ద్రవ్యవేగ పరిరక్షణ న్యాయం"], "summary": "బలాల ప్రభావం, జడత్వం మరియు రాకెట్ గమనం."},
                    {"num": 4, "title": "సమతల ఉపరితలాల వద్ద కాంతి వక్రీభవనం", "topics": ["వక్రీభవన గుణకం", "స్నెల్ నియమం", "సంపూర్ణ అంతర్గత పరావర్తనం"], "summary": "కాంతి వక్రీభవనం, ఎండమావులు మరియు ఆప్టికల్ ఫైబర్ టెక్నాలజీ."},
                    {"num": 5, "title": "గురుత్వాకర్షణ", "topics": ["సార్వత్రిక గురుత్వాకర్షణ నియమం", "గురుత్వ త్వరణం (g)", "భారరాహిత్య స్థితి"], "summary": "భూమి గురుత్వాకర్షణ బలం మరియు ఉపగ్రహాల గమనం."}
                ]
            },
            {
                "id": "bio_9_tm",
                "name": "జీవశాస్త్రం",
                "teluguName": "జీవశాస్త్రం",
                "icon": "🌿",
                "iconBg": "#E8F5E9",
                "iconColor": "#2E7D32",
                "progress": 40,
                "pdf": "IX Biology TM Inner 2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "కణం - నిర్మాణం మరియు విధులు", "topics": ["కేంద్రక పూర్వ మరియు నిజ కేంద్రక కణాలు", "ప్లాస్మా పొర", "కణాంగాలు (మైటోకాండ్రియా, గాల్జీ)"], "summary": "కణ నిర్మాణం మరియు జీవక్రియలలో కణాంగాల విధులు."},
                    {"num": 2, "title": "వృక్ష కణజాలాలు", "topics": ["విభాజ్య కణజాలం", "త్వచ కణజాలం", "దారువు, పోషక కణజాలం"], "summary": "మొక్కల కణజాల రకాలు మరియు పదార్థ రవాణా."},
                    {"num": 3, "title": "జంతు కణజాలాలు", "topics": ["ఉపకళా కణజాలం", "సంయోజక కణజాలం (రక్తం, ఎముక)", "కండర, నాడీ కణజాలాలు"], "summary": "జంతు శరీర కణజాలాల నిర్మాణం మరియు సమన్వయం."},
                    {"num": 4, "title": "ప్లాస్మా పొర గుండా పదార్థాల రవాణా", "topics": ["వ్యాపనం", "ద్రవాభిసరణం (ఆస్మాసిస్)", "జీవద్రవ్య సంకోచం"], "summary": "కణంలోకి నీరు, వాయువులు రవాణా అయ్యే ప్రక్రియలు."},
                    {"num": 5, "title": "జీవులలో వైవిధ్యం - వర్గీకరణ", "topics": ["ఐదు రాజ్యాల వర్గీకరణ", "ద్వినామీకరణ విధానం"], "summary": "జీవ వైవిధ్యం మరియు వర్గీకరణ సూత్రాలు."}
                ]
            },
            {
                "id": "soc_9_tm",
                "name": "సాంఘిక శాస్త్రం",
                "teluguName": "సాంఘిక శాస్త్రం",
                "icon": "🌍",
                "iconBg": "#FFF9C4",
                "iconColor": "#F57F17",
                "progress": 20,
                "pdf": "9 Social Studies TM 2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "మన భూమి", "topics": ["భూమి అంతర్నిర్మాణం", "భూఫలకాలు", "ఖండాల కదలిక"], "summary": "భూమి నిర్మాణం, భూకంపాలు మరియు అగ్నిపర్వతాలు."},
                    {"num": 2, "title": "జలావరణం", "topics": ["మహాసముద్రాలు", "సముద్ర ప్రవాహాలు", "నీటి వనరులు"], "summary": "సముద్రాల ఉపరితల స్వరూపం మరియు నీటి వనరుల సంరక్షణ."},
                    {"num": 3, "title": "వాతావరణం", "topics": ["వాతావరణ పొరలు", "సౌర వికిరణం", "పీడన మేఖలలు"], "summary": "భూ వాతావరణం, ఉష్ణోగ్రత మరియు గాలులు."}
                ]
            }
        ]
    },
    "10": {
        "EM": [
            {
                "id": "sanskrit_10",
                "name": "Sanskrit",
                "teluguName": "సంస్కృతం",
                "icon": "📜",
                "iconBg": "#FFF8E1",
                "iconColor": "#FF8F00",
                "progress": 25,
                "pdf": "10_SAN_CC.pdf",
                "chapters": [
                    {"num": 1, "title": "Shuchi-Paryavaranam", "topics": ["Clean Environment", "Urban Pollution Evils", "Nature Refuge Lyric"], "summary": "Poetic plea for ecological preservation against urban noise and toxic pollution."},
                    {"num": 2, "title": "Buddhir Balavati Sada", "topics": ["Shukra-Saptati Story", "Wit Overcoming Danger", "Tiger in the Forest"], "summary": "Folk tale illustrating how clever intelligence triumphs over physical might."},
                    {"num": 3, "title": "Vyayamah Sarvada Pathyah", "topics": ["Sushruta Samhita Verses", "Health and Longevity", "Daily Exercise"], "summary": "Ancient ayurvedic wisdom on the preventive healthcare benefits of regular physical exercise."},
                    {"num": 4, "title": "Shishu-Lalanam", "topics": ["Kundamala Drama", "Rama and His Sons Lava-Kusha", "Paternal Affection"], "summary": "Touching dramatic dialogue exploring deep filial affection and regal court etiquette."}
                ]
            },
            {
                "id": "mathematics",
                "name": "Mathematics",
                "teluguName": "గణితం",
                "icon": "📐",
                "iconBg": "#FFF1C8",
                "iconColor": "#996100",
                "progress": 35,
                "pdf": "X Mathematics EM  2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "Real Numbers", "topics": ["Euclid’s Division Lemma", "Fundamental Theorem of Arithmetic", "Revisiting Irrational Numbers", "Logarithms"], "summary": "Every composite number factors uniquely into primes. Real numbers comprise rationals and irrationals."},
                    {"num": 2, "title": "Sets", "topics": ["Set Representation & Null Set", "Venn Diagrams & Set Operations", "Equal & Finite Sets"], "summary": "Well-defined collections of objects, union, intersection, and disjoint sets."},
                    {"num": 3, "title": "Polynomials", "topics": ["Geometrical Meaning of Zeroes", "Zeroes and Coefficients Relationship", "Cubic Polynomials"], "summary": "Graphing zeroes of linear, quadratic, and cubic polynomials."},
                    {"num": 4, "title": "Pair of Linear Equations in Two Variables", "topics": ["Graphical Solution", "Substitution & Elimination", "Consistency Criteria"], "summary": "Intersecting, parallel, and coincident lines in coordinate systems."},
                    {"num": 5, "title": "Quadratic Equations", "topics": ["Factorisation Method", "Completing the Square", "Quadratic Formula & Discriminant"], "summary": "Standard form ax² + bx + c = 0 and real root properties."},
                    {"num": 6, "title": "Progressions", "topics": ["Arithmetic Progressions (AP)", "nth Term & Sum of Terms", "Geometric Progressions (GP)"], "summary": "Constant common differences and compounding ratio series."},
                    {"num": 7, "title": "Coordinate Geometry", "topics": ["Distance Formula", "Section Formula & Midpoint", "Area of Triangle"], "summary": "Computing lengths, division points, and collinearity in Cartesian coordinates."},
                    {"num": 8, "title": "Similar Triangles", "topics": ["Basic Proportionality Theorem (Thales)", "Similarity Criteria (AAA, SSS, SAS)", "Pythagoras Theorem"], "summary": "Ratio of corresponding sides and right-triangle geometric proofs."},
                    {"num": 9, "title": "Tangents and Secants to a Circle", "topics": ["Tangents from an External Point", "Segment Areas", "Practical Tangent Constructions"], "summary": "Lines touching circles at single points and circular segment geometry."},
                    {"num": 10, "title": "Mensuration", "topics": ["Surface Area of Solids", "Volume of Combinations", "Solid Shape Conversions"], "summary": "Cylinders, cones, spheres, hemispheres, and frustums."},
                    {"num": 11, "title": "Trigonometry", "topics": ["Trigonometric Ratios (sin, cos, tan)", "Ratios of Specific Angles (30, 45, 60)", "Trigonometric Identities (sin²θ+cos²θ=1)"], "summary": "Right-triangle angle ratios and fundamental trigonometric identities."},
                    {"num": 12, "title": "Applications of Trigonometry", "topics": ["Angles of Elevation & Depression", "Heights and Distances"], "summary": "Solving inaccessible heights of towers, trees, and buildings."},
                    {"num": 13, "title": "Probability", "topics": ["Classical Probability Definition", "Mutually Exclusive Events", "Dice & Cards"], "summary": "Number of favourable outcomes divided by total sample space."},
                    {"num": 14, "title": "Statistics", "topics": ["Mean of Grouped Data", "Median and Mode", "Ogive Curves"], "summary": "Measures of central tendency and cumulative frequency distributions."}
                ]
            },
            {
                "id": "physical_science",
                "name": "Physical Science",
                "teluguName": "భౌతిక రసాయన శాస్త్రాలు",
                "icon": "⚡",
                "iconBg": "#EDE7F6",
                "iconColor": "#512DA8",
                "progress": 30,
                "pdf": "x physics em 2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "Reflection of Light at Curved Surfaces", "topics": ["Concave and Convex Mirrors", "Ray Diagrams", "Mirror Formula & Magnification"], "summary": "Real and virtual image formations by spherical curved mirrors."},
                    {"num": 2, "title": "Chemical Reactions and Equations", "topics": ["Balancing Equations", "Combination, Decomposition, Displacement, Redox", "Corrosion & Rancidity"], "summary": "Conservation of mass and classifying chemical transformations."},
                    {"num": 3, "title": "Acids, Bases and Salts", "topics": ["pH Scale", "Neutralisation", "Bleaching Powder, Baking Soda, Plaster of Paris"], "summary": "Hydronium and hydroxide ions, indicators, and useful chemical salts."},
                    {"num": 4, "title": "Refraction of Light at Curved Surfaces", "topics": ["Lens Formula", "Lens Maker's Equation", "Convex and Concave Lenses"], "summary": "Refraction at curved interfaces and focal power calculations."},
                    {"num": 5, "title": "Human Eye and Colourful World", "topics": ["Eye Defects (Myopia, Hypermetropia)", "Prism Dispersion", "Atmospheric Scattering (Blue Sky)"], "summary": "Vision correction with lenses, rainbow dispersion, and Rayleigh scattering."},
                    {"num": 6, "title": "Structure of Atom", "topics": ["Bohr Model", "Quantum Numbers", "Aufbau Principle & Hund's Rule"], "summary": "Electronic configurations and orbital quantum numbers."},
                    {"num": 7, "title": "Classification of Elements - The Periodic Table", "topics": ["Modern Periodic Law", "Groups and Periods", "Periodic Trends"], "summary": "Periodic trends in atomic radius, ionisation enthalpy, and electronegativity."},
                    {"num": 8, "title": "Chemical Bonding", "topics": ["Ionic and Covalent Bonds", "Lewis Dot Structures", "VSEPR Shapes"], "summary": "Octet rule, electron transfer, and molecular geometry."},
                    {"num": 9, "title": "Electric Current", "topics": ["Ohm's Law (V = IR)", "Resistivity Factors", "Series & Parallel Resistors", "Joule Heating"], "summary": "Electric circuits, potential difference, and power calculations."},
                    {"num": 10, "title": "Electromagnetism", "topics": ["Oersted Experiment", "Faraday Induction Laws", "Electric Motor & Generator"], "summary": "Magnetic effects of current and electromagnetic induction."},
                    {"num": 11, "title": "Principles of Metallurgy", "topics": ["Ore Concentration", "Roasting, Calcination & Smelting", "Refining"], "summary": "Extraction of crude metals from geological mineral ores."},
                    {"num": 12, "title": "Carbon and its Compounds", "topics": ["Catenation", "Allotropes of Carbon", "Hydrocarbons & Functional Groups"], "summary": "Organic chemistry, covalent catenation, and soaps/detergents."}
                ]
            },
            {
                "id": "biology",
                "name": "Biological Science",
                "teluguName": "జీవశాస్త్రం",
                "icon": "🔬",
                "iconBg": "#E8F5E9",
                "iconColor": "#2E7D32",
                "progress": 50,
                "pdf": "x biology em inner 2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "Lesson 1: Nutrition - Food Supplying System", "topics": ["Autotrophic Nutrition & Photosynthesis", "Chloroplast Structure", "Human Digestive System"], "summary": "Plants produce glucose using solar energy, releasing oxygen; human digestion enzyme processes."},
                    {"num": 2, "title": "Lesson 2: Respiration - The Energy Releasing System", "topics": ["Aerobic vs Anaerobic Respiration", "Human Lungs & Gas Exchange", "Mitochondrial 38 ATP Production"], "summary": "Biochemical oxidation of glucose generating ATP energy currency in cells."},
                    {"num": 3, "title": "Lesson 3: Transportation - The Circulatory System", "topics": ["Four-Chambered Human Heart", "Cardiac Cycle & Double Circulation", "Blood Pressure & Lymph"], "summary": "Systemic and pulmonary blood circuits pumping oxygenated nutrients to all tissues."},
                    {"num": 4, "title": "Lesson 4: Excretion - The Waste Disposing System", "topics": ["Kidney Structure", "Nephron Anatomy & Urine Formation", "Dialysis"], "summary": "Renal filtration of nitrogenous metabolic wastes and osmoregulation."},
                    {"num": 5, "title": "Lesson 5: Control and Coordination - The Linking System", "topics": ["Neuron Structure & Synapse", "Brain & Spinal Reflex Arc", "Endocrine Hormones & Plant Tropisms"], "summary": "Neural impulses and hormonal chemicals maintaining physiological homeostasis."},
                    {"num": 6, "title": "Lesson 6: Reproduction - The Generating System", "topics": ["Asexual Modes", "Flowering Plant Pollination", "Human Reproductive Anatomy"], "summary": "Continuity of genetic life, sexual gametogenesis, and floral fertilisation."},
                    {"num": 7, "title": "Lesson 7: Coordination in Life Processes", "topics": ["Hunger Pangs & Ghrelin/Leptin", "Peristalsis in Gut", "Taste and Smell Link"], "summary": "Coordinated nervous and digestive interactions during feeding and digestion."},
                    {"num": 8, "title": "Lesson 8: Heredity - From Parent to Progeny", "topics": ["Mendelian Genetics", "Monohybrid & Dihybrid Crosses", "Sex Determination & Evolution"], "summary": "Chromosomal inheritance, dominant/recessive alleles, and natural selection."},
                    {"num": 9, "title": "Lesson 9: Our Environment - Our Concern", "topics": ["Ecosystem Trophic Levels", "Ecological Pyramids", "Biomagnification"], "summary": "Unidirectional energy flow through food webs and environmental toxins accumulation."},
                    {"num": 10, "title": "Lesson 10: Natural Resources", "topics": ["Watersheds & Rainwater Harvesting", "Forest Conservation", "Fossil Fuels vs Solar"], "summary": "Sustainable development and rational conservation of natural ecological wealth."}
                ]
            },
            {
                "id": "sci_10",
                "name": "General Science",
                "teluguName": "సామాన్య శాస్త్రం",
                "icon": "🧪",
                "iconBg": "#E0F2F1",
                "iconColor": "#00796B",
                "progress": 35,
                "pdf": "x physics em 2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "Physical and Chemical Principles", "topics": ["Optics", "Chemical Reactions", "Electric Current"], "summary": "Core physical and chemical phenomena governing everyday science."},
                    {"num": 2, "title": "Living World and Life Processes", "topics": ["Nutrition", "Circulation", "Heredity"], "summary": "Vital organ systems and genetic processes sustaining life."}
                ]
            },
            {
                "id": "english",
                "name": "English Reader",
                "teluguName": "ఆంగ్లం",
                "icon": "📖",
                "iconBg": "#FBE9E7",
                "iconColor": "#D84315",
                "progress": 40,
                "pdf": "10 English Reader-2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "Personality Development: Attitude is Altitude", "topics": ["Nick Vujicic Biography", "Overcoming Physical Adversity", "Optimism"], "summary": "Inspiring life of Nick Vujicic proving that determination conquers all limitations."},
                    {"num": 2, "title": "Wit and Humour: The Dear Departed", "topics": ["Stanley Houghton One-Act Play", "Greed and Elderly Care", "Dramatic Irony"], "summary": "Satirical drama mocking selfish family members fighting over an elderly grandfather's assets."},
                    {"num": 3, "title": "Human Relations: The Journey", "topics": ["Father and Son Bond", "Dignity of Labour", "Rural Emotional Ties"], "summary": "Touching narrative exploring generational sacrifice and fatherly love."},
                    {"num": 4, "title": "Films and Theatre: Rendezvous with Ray", "topics": ["Satyajit Ray Biography", "Father Gaston Roberge", "Cinema as Art"], "summary": "Tribute to master filmmaker Satyajit Ray and artistic cinematic vision."}
                ]
            }
        ],
        "TM": [
            {
                "id": "tel_10_tm",
                "name": "తెలుగు",
                "teluguName": "తెలుగు",
                "icon": "📚",
                "iconBg": "#FFE0B2",
                "iconColor": "#E65100",
                "progress": 45,
                "pdf": "10th telugu fl inner 2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "దానశీలము", "topics": ["బమ్మెర పోతన భాగవతం", "బలి చక్రవర్తి దాన గుణం", "ఛందస్సు (మత్తేభం, ఉత్పలమాల)"], "summary": "శుక్రాచార్యుని హెచ్చరికను కాదని వామనునికి మూడడుగుల నేల దానమిచ్చిన బలి చక్రవర్తి ఉదారత."},
                    {"num": 2, "title": "ఎవరి భాష వాళ్లకు వినసొంపు", "topics": ["సామల సదాశివ యాది వ్యాసాలు", "తెలంగాణ మాండలిక సొగసులు", "ఉర్దూ-తెలుగు భాషా సమన్వయం"], "summary": "తెలంగాణ ప్రాంతీయ భాషా మాధుర్యం, యాసలోని గొప్పతనం మరియు జీవద్భాష విశిష్టత."},
                    {"num": 3, "title": "వీరతెలంగాణ", "topics": ["దాశరథి కృష్ణమాచార్య కవిత్వం", "నిజాం నిరంకుశ పాలనపై తిరుగుబాటు", "తెలంగాణ పోరాట వీరుల శౌర్యం"], "summary": "తెలంగాణ వీరుల పోరాట పటిమ, నవయుగ చైతన్యం మరియు స్వేచ్ఛాకాంక్ష ప్రతిబింబించే ఉత్తేజకర కవితలు."},
                    {"num": 4, "title": "కొత్త బాట", "topics": ["డాక్టర్ పాకాల యశోదారెడ్డి కథ", "గ్రామీణ జీవనంలో వచ్చిన మార్పులు"], "summary": "తెలంగాణ పల్లెల్లో వచ్చిన మార్పులు మరియు స్త్రీ చైతన్యం."},
                    {"num": 5, "title": "నగర గీతం", "topics": ["అలిశెట్టి ప్రభాకర్ మినీ కవితలు", "నగర జీవితంలోని అసమానతలు"], "summary": "మహానగర జీవితంలోని సంక్లిష్టతలు, యాంత్రిక జీవనం మరియు పేదల కష్టాలు."},
                    {"num": 6, "title": "భాగ్యోదయం", "topics": ["కృష్ణస్వామి ముదిరాజ్", "భాగ్యరెడ్డి వర్మ దళిత జనోద్ధరణ"], "summary": "దళిత జాతి అభ్యున్నతికి జీవితాన్ని ధారపోసిన భాగ్యరెడ్డి వర్మ జీవిత చరిత్ర."}
                ]
            },
            {
                "id": "eng_10_tm",
                "name": "ఆంగ్లం",
                "teluguName": "ఆంగ్లం",
                "icon": "📖",
                "iconBg": "#FBE9E7",
                "iconColor": "#D84315",
                "progress": 30,
                "pdf": "10 English Reader-2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "Personality Development: Attitude is Altitude (వ్యక్తిత్వ వికాసం)", "topics": ["నిక్ వుయిసిచ్ జీవిత కథ", "ఆత్మవిశ్వాసం", "ఆంగ్ల పదజాలం"], "summary": "అంగవైకల్యాన్ని జయించి ప్రపంచవ్యాప్తంగా లక్షలాదిమందికి స్ఫూర్తిగా నిలిచిన నిక్ కథ."},
                    {"num": 2, "title": "Wit and Humour: The Dear Departed (హాస్యం - ప్రియమైన మృతుడు)", "topics": ["నాటకం", "హాస్యం మరియు వ్యంగ్యం", "కుటుంబ బంధాలు"], "summary": "ఆస్తి కోసం పాకులాడే కుటుంబ సభ్యుల స్వార్థాన్ని హాస్యభరితంగా ఎండగట్టే నాటకం."}
                ]
            },
            {
                "id": "math_10_tm",
                "name": "గణితం",
                "teluguName": "గణితం",
                "icon": "📐",
                "iconBg": "#FFF1C8",
                "iconColor": "#996100",
                "progress": 35,
                "pdf": "X Mathematics TM 2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "వాస్తవ సంఖ్యలు", "topics": ["యూక్లిడ్ భాగహార న్యాయం", "అంకగణిత ప్రాథమిక సిద్ధాంతం", "కరణీయ సంఖ్యలు", "సంవర్గమానాలు"], "summary": "అకరణీయ మరియు కరణీయ సంఖ్యల స్వభావం, ప్రాథమిక అంకగణిత సిద్ధాంతం."},
                    {"num": 2, "title": "సమితులు", "topics": ["సమితి రూపాలు, శూన్య సమితి", "వెన్ చిత్రాలు, సమితుల పరిక్రియలు", "సమాన, పరిమిత సమితులు"], "summary": "సమితుల మూలకాలు, సమ్మేళనం, ఛేదనం మరియు వెన్ చిత్రాల ద్వారా సమస్యా సాధన."},
                    {"num": 3, "title": "బహుపదులు", "topics": ["బహుపదుల శూన్యాలు", "గుణకాలు మరియు శూన్యాల మధ్య సంబంధం"], "summary": "రేఖీయ, వర్గ బహుపదుల శూన్యాలు మరియు రేఖాచిత్రాలు."},
                    {"num": 4, "title": "రెండు చరరాశులలో రేఖీయ సమీకరణాల జత", "topics": ["గ్రాఫ్ పద్ధతి", "ప్రతిక్షేపణ మరియు చరరాశి తొలగింపు పద్ధతులు"], "summary": "ఖండన, సమాంతర, ఏకీభవించే సరళరేఖలు."},
                    {"num": 5, "title": "వర్గ సమీకరణాలు", "topics": ["కారణాంకాల విభజన పద్ధతి", "వర్గ సూత్రం"], "summary": "ax² + bx + c = 0 సమీకరణ సాధన మరియు మూలాల స్వభావం."},
                    {"num": 6, "title": "శ్రేఢులు", "topics": ["అంకశ్రేఢి (AP)", "సాధారణ భేదం, nవ పదం, n పదాల మొత్తం", "గుణశ్రేఢి (GP)"], "summary": "అంకశ్రేఢి మరియు గుణశ్రేఢుల అనువర్తనాలు."},
                    {"num": 7, "title": "నిరూపక జ్యామితి", "topics": ["దూరం సూత్రం", "విభజన సూత్రం", "త్రిభుజ వైశాల్యం"], "summary": "కార్టీషియన్ తలంలో బిందువుల మధ్య దూరం మరియు విభజన బిందువులు."},
                    {"num": 8, "title": "సరూప త్రిభుజాలు", "topics": ["థేల్స్ సిద్ధాంతం", "పైథాగరస్ సిద్ధాంతం"], "summary": "సరూప త్రిభుజాల సిద్ధాంతాలు మరియు నిరూపణలు."},
                    {"num": 9, "title": "స్పర్శరేఖలు మరియు ఛేదన రేఖలు", "topics": ["బాహ్య బిందువు నుండి స్పర్శరేఖల నిర్మాణం", "వృత్తఖండ వైశాల్యం"], "summary": "వృత్త స్పర్శరేఖల ధర్మాలు మరియు ప్రాయోగిక నిర్మాణాలు."},
                    {"num": 10, "title": "క్షేత్రమితి", "topics": ["సంయుక్త ఘనాకారాల ఉపరితల వైశాల్యాలు", "ఘనపరిమాణాలు"], "summary": "స్తూపం, శంకువు, గోళం మరియు అర్ధగోళాల వైశాల్యాలు, ఘనపరిమాణాలు."},
                    {"num": 11, "title": "త్రికోణమితి", "topics": ["త్రికోణమితి నిష్పత్తులు (sin, cos, tan)", "నిర్దిష్ట కోణాల నిష్పత్తులు", "త్రికోణమితి సర్వసమీకరణాలు"], "summary": "లంబకోణ త్రిభుజ భుజాల నిష్పత్తులు మరియు sin²θ + cos²θ = 1 సూత్రం."},
                    {"num": 12, "title": "త్రికోణమితి అనువర్తనాలు", "topics": ["ఊర్ధ్వ కోణం", "నిమ్న కోణం", "ఎత్తులు మరియు దూరాలు"], "summary": "భవనాలు, గోపురాల ఎత్తులు మరియు దూరాల లెక్కింపు."},
                    {"num": 13, "title": "సంభావ్యత", "topics": ["ఘటనల సంభావ్యత", "పాచికలు, పేకముక్కల సమస్యలు"], "summary": "సానుకూల పర్యవసానాలు / మొత్తం పర్యవసానాల సూత్రం."},
                    {"num": 14, "title": "సాంఖ్యకశాస్త్రం", "topics": ["వర్గీకృత దత్తాంశ సగటు", "మధ్యగతం మరియు బాహుళకం", "ఓజీవ్ వక్రాలు"], "summary": "కేంద్ర స్థానపు కొలతలు: సగటు, మధ్యగతం మరియు బాహుళకం."}
                ]
            },
            {
                "id": "phy_10_tm",
                "name": "భౌతిక శాస్త్రం",
                "teluguName": "భౌతిక శాస్త్రం",
                "icon": "⚡",
                "iconBg": "#EDE7F6",
                "iconColor": "#512DA8",
                "progress": 30,
                "pdf": "x physics tm 2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "వక్రతలాల వద్ద కాంతి పరావర్తనం", "topics": ["పుటాకార, కుంభాకార దర్పణాలు", "దర్పణ సూత్రం", "కిరణ చిత్రాలు"], "summary": "గోళాకార దర్పణాలలో నిజ, మిథ్యా ప్రతిబింబాలు ఏర్పడే విధానం."},
                    {"num": 2, "title": "రసాయన చర్యలు - సమీకరణాలు", "topics": ["రసాయన సమీకరణాలను తుల్యం చేయడం", "సంయోగం, వియోగం, స్థానభ్రంశం, ద్వంద్వ వియోగం"], "summary": "ద్రవ్య నిత్యత్వ నియమం మరియు రసాయన సమీకరణాల తుల్యత."},
                    {"num": 3, "title": "ఆమ్లాలు, క్షారాలు మరియు లవణాలు", "topics": ["pH స్కేలు", "తటస్థీకరణం", "బ్లీచింగ్ పౌడర్, బేకింగ్ సోడా, ప్లాస్టర్ ఆఫ్ పారిస్"], "summary": "H+ మరియు OH- అయాన్లు, సూచికలు మరియు నిత్యజీవితంలో లవణాలు."},
                    {"num": 4, "title": "వక్రతలాల వద్ద కాంతి వక్రీభవనం", "topics": ["కటక సూత్రం", "కటక తయారీదారుల సూత్రం"], "summary": "కుంభాకార మరియు పుటాకార కటకాల ద్వారా కాంతి వక్రీభవనం."},
                    {"num": 5, "title": "మానవుని కన్ను - రంగుల ప్రపంచం", "topics": ["దృష్టి లోపాలు (హ్రస్వదృష్టి, దూరదృష్టి)", "ప్రిజం ద్వారా కాంతి విక్షేపణం", "ఆకాశం నీలిరంగు"], "summary": "కంటి నిర్మాణం, దృష్టి దోషాల నివారణ మరియు కాంతి విక్షేపణం, వికీరణం."},
                    {"num": 6, "title": "పరమాణు నిర్మాణం", "topics": ["బోర్ పరమాణు నమూనా", "క్వాంటమ్ సంఖ్యలు", "ఆఫ్‌బౌ సూత్రం, హుండ్ నియమం"], "summary": "ఎలక్ట్రాన్ విన్యాసం మరియు ఆర్బిటాళ్ల అమరిక."},
                    {"num": 7, "title": "మూలకాల వర్గీకరణ - ఆవర్తన పట్టిక", "topics": ["ఆధునిక ఆవర్తన నియమం", "గ్రూపులు, పీరియడ్‌లు", "ఆవర్తన ధర్మాలు"], "summary": "పరమాణు సంఖ్య ఆధారంగా మూలకాల అమరిక మరియు ధర్మాల మార్పులు."},
                    {"num": 8, "title": "రసాయన బంధం", "topics": ["అయానిక బంధం", "సమయోజనీయ బంధం", "లూయిస్ బిందు నిర్మాణాలు"], "summary": "అష్టక నియమం మరియు పరమాణువుల మధ్య బంధాల రకాలు."},
                    {"num": 9, "title": "విద్యుత్ ప్రవాహం", "topics": ["ఓమ్ నియమం (V = IR)", "నిరోధాలు (శ్రేణి, సమాంతర సంధానం)", "జౌల్ ఉష్ణ ఫలితం"], "summary": "విద్యుత్ ప్రవాహం, పొటెన్షియల్ తేడా మరియు విద్యుత్ సామర్థ్యం."},
                    {"num": 10, "title": "విద్యుదయస్కాంతత్వం", "topics": ["ఆయిర్‌స్టెడ్ ప్రయోగం", "ఫారడే విద్యుదయస్కాంత ప్రేరణ నియమాలు", "మోటార్, జనరేటర్"], "summary": "కరెంట్ వల్ల ఏర్పడే అయస్కాంత క్షేత్రం మరియు విద్యుత్ ఉత్పత్తి."},
                    {"num": 11, "title": "లోహ సంగ్రహణ శాస్త్రం", "topics": ["ఖనిజాలు మరియు ధాతువులు", "భర్జనం, భస్మీకరణం, ప్రగళనం"], "summary": "ధాతువుల నుండి శుద్ధ లోహాలను వేరుచేసే పద్ధతులు."},
                    {"num": 12, "title": "కార్బన్ - దాని సమ్మేళనాలు", "topics": ["కాటనేషన్", "కార్బన్ రూపాంతరాలు (వజ్రం, గ్రాఫైట్)", "హైడ్రోకార్బన్లు"], "summary": "సేంద్రియ రసాయన శాస్త్రం మరియు సబ్బులు, డిటర్జెంట్ల పనితీరు."}
                ]
            },
            {
                "id": "bio_10_tm",
                "name": "జీవశాస్త్రం",
                "teluguName": "జీవశాస్త్రం",
                "icon": "🔬",
                "iconBg": "#E8F5E9",
                "iconColor": "#2E7D32",
                "progress": 50,
                "pdf": "X Biology TM Inner 2026-27.pdf",
                "chapters": [
                    {"num": 1, "title": "1వ పాఠం: పోషణ - ఆహార సరఫరా వ్యవస్థ", "topics": ["స్వయంపోషణ & కిరణజన్య సంయోగక్రియ", "హరితరేణువు నిర్మాణం, కాంతి మరియు నిష్కాంతి చర్యలు", "మానవ జీర్ణ వ్యవస్థ"], "summary": "మొక్కలు సూర్యరశ్మి, క్లోరోఫిల్, నీరు, CO2 తో ఆహారాన్ని తయారు చేసుకోవడం మరియు జీర్ణక్రియ."},
                    {"num": 2, "title": "2వ పాఠం: శ్వాసక్రియ - శక్తి ఉత్పాదక వ్యవస్థ", "topics": ["వాయు సహిత మరియు అవాయు శ్వాసక్రియ", "మానవ శ్వాస వ్యవస్థ మరియు వాయుగోణులు", "కణ శ్వాసక్రియ (మైటోకాండ్రియా, 38 ATP)"], "summary": "శ్వాసక్రియ ద్వారా గ్లూకోజ్ విచ్ఛిన్నమై శక్తి విడుదలయ్యే విధానం."},
                    {"num": 3, "title": "3వ పాఠం: ప్రసరణ - పదార్థాల రవాణా వ్యవస్థ", "topics": ["మానవ గుండె నిర్మాణం (4 గదులు)", "రక్త ప్రసరణ మరియు హృదయ స్పందన చక్రం", "శోషరస వ్యవస్థ మరియు రక్తం గడ్డకట్టడం"], "summary": "గుండె నాలుగు గదుల ద్వారా శరీరంలోని అన్ని భాగాలకు రక్తం సరఫరా అయ్యే విధానం."},
                    {"num": 4, "title": "4వ పాఠం: విసర్జన - వ్యర్థాల తొలగింపు వ్యవస్థ", "topics": ["మూత్రపిండాల నిర్మాణం", "నెఫ్రాన్ నిర్మాణం మరియు మూత్రం ఏర్పడే విధానం", "డయాలసిస్"], "summary": "రక్తంలోని నైట్రోజన్ వ్యర్థాలను మూత్రపిండాలు వడపోసే అద్భుత ప్రక్రియ."},
                    {"num": 5, "title": "5వ పాఠం: నియంత్రణ - సమన్వయం - అనుసంధాన వ్యవస్థ", "topics": ["నాడీ కణం నిర్మాణం", "మెదడు, వెన్నుపాము, ప్రతిచర్యా చాపం", "హార్మోన్లు మరియు మొక్కలలో అనువర్తనాలు"], "summary": "శరీరంలోని వివిధ అవయవాల మధ్య నాడీ మరియు హార్మోన్ల సమన్వయం."},
                    {"num": 6, "title": "6వ పాఠం: ప్రత్యుత్పత్తి - పునరుత్పాదక వ్యవస్థ", "topics": ["అలైంగిక ప్రత్యుత్పత్తి పద్ధతులు", "పుష్పించే మొక్కలలో పరాగసంపర్కం, ఫలదీకరణం", "మానవ ప్రత్యుత్పత్తి వ్యవస్థ"], "summary": "జీవుల కొనసాగింపుకు అవసరమైన ప్రత్యుత్పత్తి పద్ధతులు."},
                    {"num": 7, "title": "7వ పాఠం: జీవక్రియలలో సమన్వయం", "topics": ["ఆకలి కోరికలు (గ్రెలిన్, లెప్టిన్)", "జీర్ణవ్యవస్థలో పెరిస్టాల్సిస్ చలనాలు"], "summary": "ఆహారం తినడం, జీర్ణం కావడంలో నాడీ మరియు హార్మోన్ల సమన్వయం."},
                    {"num": 8, "title": "8వ పాఠం: అనువంశికత - తరతరాల వారసత్వం", "topics": ["మెండల్ జన్యుశాస్త్ర ప్రయోగాలు", "ఏకసంకర, ద్విసంకర సంకరణాలు", "లింగ నిర్ధారణ మరియు పరిణామం"], "summary": "తల్లిదండ్రుల నుండి పిల్లలకు లక్షణాలు సంక్రమించే విధానం."},
                    {"num": 9, "title": "9వ పాఠం: మన పర్యావరణం - మన బాధ్యత", "topics": ["ఆవరణ వ్యవస్థలో పోషక స్థాయిలు", "ఆహారపు జాలకం", "జీవవర్ధనం (బయోమాగ్నిఫికేషన్)"], "summary": "శక్తి ప్రవాహం, పర్యావరణ పిరమిడ్లు మరియు వ్యర్థాల నిర్వహణ."},
                    {"num": 10, "title": "10వ పాఠం: సహజ వనరులు", "topics": ["జలవనరుల నిర్వహణ", "వాటర్‌షెడ్ పథకాలు", "సహజ వనరుల సుస్థిర వినియోగం"], "summary": "భవిష్యత్ తరాల కోసం ప్రకృతి వనరులను పొదుపుగా సంరక్షించుకోవడం."}
                ]
            },
            {
                "id": "soc_10_tm",
                "name": "సాంఘిక శాస్త్రం",
                "teluguName": "సాంఘిక శాస్త్రం",
                "icon": "🌍",
                "iconBg": "#FFF9C4",
                "iconColor": "#F57F17",
                "progress": 25,
                "pdf": "X SOCIAL TM_2026-27_Errata_FINAL.pdf",
                "chapters": [
                    {"num": 1, "title": "భారతదేశం: భౌగోళిక స్వరూపాలు", "topics": ["హిమాలయాలు", "గంగా-సింధు మైదానం", "ద్వీపకల్ప పీఠభూమి", "తీర మైదానాలు"], "summary": "భారతదేశ నైసర్గిక స్వరూపాలు, పర్వతాలు మరియు మైదానాల విశిష్టత."},
                    {"num": 2, "title": "అభివృద్ధి భావనలు", "topics": ["తలసరి ఆదాయం", "మానవాభివృద్ధి సూచిక (HDI)", "ప్రజా సౌకర్యాలు"], "summary": "ఆదాయం కంటే ఆరోగ్యం, విద్య, స్వేచ్ఛలతో కూడిన సమగ్ర అభివృద్ధి భావన."},
                    {"num": 3, "title": "ఉత్పత్తి మరియు ఉపాధి", "topics": ["ప్రాథమిక, ద్వితీయ, తృతీయ రంగాలు", "వ్యవస్థీకృత మరియు అవ్యవస్థీకృత రంగాలు"], "summary": "జీడీపీలో సేవా రంగం వాటా మరియు వ్యవసాయ రంగంలో ఉపాధి ధోరణులు."}
                ]
            }
        ]
    }
}


def find_topic_across_all_classes(query: str) -> dict[str, Any] | None:
    """Search for any chapter or topic query across ALL classes (6, 7, 8, 9, 10).
    Returns matched chapter dictionary with class_id, subject_name, chapter_title, etc.
    """
    q_clean = query.lower().strip()
    words = [w for w in re.split(r"[^a-zA-Z0-9ఀ-౿]+", q_clean) if len(w) > 3]

    # 1. Exact or strong substring match on chapter titles or topics
    for class_id, mediums in CURRICULUM_DATA.items():
        for med_key in ["EM", "TM"]:
            for subj in mediums.get(med_key, []):
                for ch in subj.get("chapters", []):
                    ch_title = ch.get("title", "").lower()
                    ch_topics = [t.lower() for t in ch.get("topics", [])]

                    # Exact phrase match in chapter title
                    if q_clean in ch_title:
                        return {
                            "class_id": class_id,
                            "medium": med_key,
                            "subject_id": subj["id"],
                            "subject_name": subj["name"],
                            "subject_telugu": subj.get("teluguName", subj["name"]),
                            "chapter_num": ch.get("num", 1),
                            "chapter_title": ch.get("title", ""),
                            "topics": ch.get("topics", []),
                            "summary": ch.get("summary", ""),
                            "pdf": subj.get("pdf", ""),
                            "match_type": "exact_title",
                        }

                    # Topic exact match
                    for t in ch_topics:
                        if q_clean in t:
                            return {
                                "class_id": class_id,
                                "medium": med_key,
                                "subject_id": subj["id"],
                                "subject_name": subj["name"],
                                "subject_telugu": subj.get("teluguName", subj["name"]),
                                "chapter_num": ch.get("num", 1),
                                "chapter_title": ch.get("title", ""),
                                "matched_topic": t,
                                "topics": ch.get("topics", []),
                                "summary": ch.get("summary", ""),
                                "pdf": subj.get("pdf", ""),
                                "match_type": "exact_topic",
                            }

    # 2. Token overlap match (e.g. "practical geometry" matching "Practical Geometry")
    best_match = None
    max_score = 0
    for class_id, mediums in CURRICULUM_DATA.items():
        for med_key in ["EM", "TM"]:
            for subj in mediums.get(med_key, []):
                for ch in subj.get("chapters", []):
                    ch_title = ch.get("title", "").lower()
                    score = sum(2 for w in words if w in ch_title)
                    for t in ch.get("topics", []):
                        score += sum(1 for w in words if w in t.lower())
                    if score > max_score and score >= 2:
                        max_score = score
                        best_match = {
                            "class_id": class_id,
                            "medium": med_key,
                            "subject_id": subj["id"],
                            "subject_name": subj["name"],
                            "subject_telugu": subj.get("teluguName", subj["name"]),
                            "chapter_num": ch.get("num", 1),
                            "chapter_title": ch.get("title", ""),
                            "topics": ch.get("topics", []),
                            "summary": ch.get("summary", ""),
                            "pdf": subj.get("pdf", ""),
                            "match_type": "token_overlap",
                        }

    return best_match


def is_syllabus_query(query: str) -> bool:
    """Check if the user is asking about syllabus, chapters, course outline, or curriculum."""
    q = query.lower()
    terms = [
        "syllabus", "curriculum", "chapters", "chapter list", "chapter names",
        "lessons", "lesson list", "what lessons", "what are the chapters",
        "topics list", "course content", "textbook chapters",
        "సిలబస్", "పాఠాలు", "అధ్యాయాలు", "పాఠాల జాబితా", "ఏయే పాఠాలు"
    ]
    return any(t in q for t in terms)


def build_authoritative_syllabus_answer(
    query: str,
    language: str = "en",
    subject_hint: str | None = None,
    class_name: str | None = None,
) -> str:
    """Generate an authoritative, structured syllabus answer with real chapters and topics from SCERT textbooks."""
    q = query.lower()

    # Detect class (6, 7, 8, 9, 10)
    detected_class = class_name or "10"
    for c in ["6", "7", "8", "9", "10"]:
        if f"class {c}" in q or f"{c}th" in q or f"{c}వ" in q or f"class-{c}" in q or f"grade {c}" in q:
            detected_class = c
            break

    # Detect medium
    is_te = (
        language.startswith("te")
        or "telugu" in q
        or "tm" in q
        or bool(re.search(r"[\u0C00-\u0C7F]", query))
    )
    medium = "TM" if is_te else "EM"

    # Detect subject
    subj_code = "biology"
    if any(k in q for k in ["sanskrit", "సంస్కృతం"]):
        subj_code = "sanskrit"
    elif any(k in q for k in ["math", "mathematics", "గణితం", "లెక్కలు", "geometry", "జామెట్రీ"]):
        subj_code = "math"
    elif any(k in q for k in ["bio", "biology", "biological", "జీవశాస్త్రం"]):
        subj_code = "biology"
    elif any(k in q for k in ["phy", "physics", "physical science", "భౌతిక", "రసాయన"]):
        subj_code = "physical_science"
    elif any(k in q for k in ["sci", "science", "సామాన్య శాస్త్రం", "సైన్స్"]):
        subj_code = "science"
    elif any(k in q for k in ["social", "సాంఘిక"]):
        subj_code = "social"
    elif any(k in q for k in ["telugu", "తెలుగు"]):
        subj_code = "telugu"
    elif any(k in q for k in ["english", "ఆంగ్లం"]):
        subj_code = "english"
    elif subject_hint:
        sh = subject_hint.lower()
        if "sanskrit" in sh: subj_code = "sanskrit"
        elif "math" in sh: subj_code = "math"
        elif "bio" in sh: subj_code = "biology"
        elif "phy" in sh: subj_code = "physical_science"
        elif "sci" in sh: subj_code = "science"
        elif "soc" in sh: subj_code = "social"
        elif "tel" in sh: subj_code = "telugu"
        elif "eng" in sh: subj_code = "english"

    class_data = CURRICULUM_DATA.get(detected_class, CURRICULUM_DATA["10"])
    subjects_list = class_data.get(medium, class_data.get("EM", []))

    # Match subject
    matched_subject = None
    for s in subjects_list:
        sid = s["id"].lower()
        sname = s["name"].lower()
        if subj_code in sid or subj_code in sname:
            matched_subject = s
            break
    if not matched_subject and subjects_list:
        matched_subject = subjects_list[0]

    sub_name = matched_subject.get("teluguName" if is_te else "name", matched_subject.get("name"))
    pdf_file = matched_subject.get("pdf", f"Class {detected_class} {sub_name} SCERT.pdf")
    chapters = matched_subject.get("chapters", [])

    if is_te:
        response = (
            f"నమస్కారం! 🌟 తెలంగాణ రాష్ట్ర SCERT **{detected_class}వ తరగతి {sub_name}** ({medium} మీడియం) "
            f"అధికారిక పాఠ్య ప్రణాళిక మరియు అధ్యాయాల పూర్తి జాబితా ఇదిగో:\n\n"
        )
        for ch in chapters:
            c_title = ch.get("title", "")
            c_topics = ch.get("topics", [])
            topics_str = ", ".join(c_topics) if c_topics else "పాఠ్యాంశ భావనలు"
            response += f"📘 **{c_title}**\n"
            response += f"   • ముఖ్యాంశాలు: {topics_str}\n\n"

        response += (
            f"*(అధికారిక మూలం: తెలంగాణ రాష్ట్ర విద్యా పరిశోధన శిక్షణ మండలి (SCERT), హైదరాబాద్ (2026-27 ఎడిషన్) - `{pdf_file}`)*\n\n"
            f"మీకు ఈ పాఠాలలో ఏ అంశం గురించైనా మరింత వివరణ కావాలంటే నన్ను అడగండి, నేను వివరిస్తాను! 😊"
        )
    else:
        response = (
            f"Hello! 🌟 Here is the official Telangana SCERT **Class {detected_class} {sub_name}** ({medium} Medium) "
            f"curriculum and complete chapter list:\n\n"
        )
        for ch in chapters:
            c_title = ch.get("title", "")
            c_topics = ch.get("topics", [])
            topics_str = ", ".join(c_topics) if c_topics else "Core concepts & activities"
            response += f"📘 **{c_title}**\n"
            response += f"   • Key Topics: {topics_str}\n\n"

        response += (
            f"*(Official Source: State Council of Educational Research and Training, Telangana (2026-27 Edition) - `{pdf_file}`)*\n\n"
            f"Feel free to ask me to explain any of these chapters or concepts in detail! 😊"
        )

    return response


def find_topic_across_all_classes(query: str, language: str = "en") -> dict[str, Any] | None:
    """
    Search for a topic across ALL classes (6 to 10), subjects, chapters, and topics.
    Returns matched chapter/subject metadata or None.
    """
    q = query.lower().strip()
    # Strip common conversational prefixes
    clean_q = re.sub(
        r"^(explain\s+(about\s+)?|tell\s+me\s+(about\s+)?|what\s+is\s+|what\s+are\s+|describe\s+|how\s+to\s+|నేర్చుకుందాం\s+|గురించి\s+చెప్పండి\s+|వివరించండి\s+)",
        "",
        q,
        flags=re.IGNORECASE,
    ).strip()

    best_match = None
    best_score = 0

    # Search in all classes 6, 7, 8, 9, 10
    for cls_id in ["6", "7", "8", "9", "10"]:
        cls_data = CURRICULUM_DATA.get(cls_id, {})
        for medium in ["EM", "TM"]:
            for subject in cls_data.get(medium, []):
                for ch in subject.get("chapters", []):
                    ch_title = ch.get("title", "")
                    ch_title_lower = ch_title.lower()
                    ch_summary = ch.get("summary", "").lower()
                    ch_topics = [t.lower() for t in ch.get("topics", [])]

                    score = 0
                    # Direct phrase match in title
                    if clean_q and clean_q in ch_title_lower:
                        score = 100
                    # Direct phrase match in topics
                    elif any(clean_q and clean_q in t for t in ch_topics):
                        score = 90
                    # Substring match of individual words
                    else:
                        words = [w for w in clean_q.split() if len(w) > 3 and w not in ["about", "what", "tell", "explain", "chapter", "lesson"]]
                        if words:
                            matching_words = sum(1 for w in words if w in ch_title_lower or any(w in t for t in ch_topics) or w in ch_summary)
                            score = int((matching_words / len(words)) * 70)

                    if score > best_score:
                        best_score = score
                        best_match = {
                            "class": cls_id,
                            "medium": medium,
                            "subject_id": subject.get("id"),
                            "subject_name": subject.get("name"),
                            "subject_telugu": subject.get("teluguName", subject.get("name")),
                            "chapter_num": ch.get("num"),
                            "chapter_title": ch_title,
                            "topics": ch.get("topics", []),
                            "summary": ch.get("summary", ""),
                            "pdf": subject.get("pdf", ""),
                            "score": score,
                        }

    return best_match if best_score >= 40 else None


def generate_child_friendly_explanation(match: dict[str, Any], language: str = "en") -> str:
    """Generate a cheerful, kid-friendly Bala Buddy explanation for a topic found across classes."""
    is_te = language.startswith("te") or match.get("medium") == "TM"
    cls_num = match["class"]
    subj = match["subject_telugu"] if is_te else match["subject_name"]
    ch_num = match["chapter_num"]
    ch_title = match["chapter_title"]
    topics = match.get("topics", [])
    topics_list = ", ".join(topics) if topics else ""
    summary = match.get("summary", "")

    # Specialized friendly answers for popular topics
    title_lower = ch_title.lower()
    if "practical geometry" in title_lower or "ప్రాయోగిక జ్యామితి" in title_lower:
        if is_te:
            return (
                f"నమస్కారం! 🌟 ఈ ఆసక్తికరమైన అంశం మీ **{cls_num}వ తరగతి {subj} (అధ్యాయం {ch_num}: {ch_title})** లో ఉంది!\n\n"
                f"📐 **ప్రాయోగిక జ్యామితి (Practical Geometry) అంటే ఏమిటి?**\n"
                f"ప్రాయోగిక జ్యామితి అంటే ప్రత్యేక రేఖాగణిత పనిముట్లను ఉపయోగించి సమతల పటాలను ఖచ్చితమైన కొలతలతో నిర్మించే సరదా ప్రక్రియ! ✏️📏\n\n"
                f"ఈ అధ్యాయంలో మనం ఉపయోగించే ముఖ్యమైన పరికరాలు:\n"
                f"1. 📏 **స్కేలు (రూలర్):** సరళరేఖలను గీయడానికి మరియు పొడవును ఖచ్చితంగా కొలవడానికి.\n"
                f"2. ⭕ **కంపాస్ (వృత్తలేఖిని):** ఇచ్చిన వ్యాసార్థంతో ఖచ్చితమైన వృత్తాలు మరియు చాపాలను గీయడానికి.\n"
                f"3. 📐 **కోణమానిని (Protractor):** వివిధ కోణాలను కొలవడానికి మరియు గీయడానికి.\n\n"
                f"✨ **ఈ అధ్యాయంలో నేర్చుకునే ముఖ్య నైపుణ్యాలు:**\n"
                f"• ఇచ్చిన వ్యాసార్థంతో అందమైన వృత్తాలను నిర్మించడం.\n"
                f"• ఒక రేఖాఖండానికి ఖచ్చితమైన లంబద్విఖండన రేఖను గీయడం.\n"
                f"• కోణ ద్విఖండన రేఖ ద్వారా కోణాన్ని రెండు సమాన భాగాలుగా విభజించడం.\n"
                f"• కేవలం స్కేలు మరియు కంపాస్ ఉపయోగించి 60°, 30°, 90°, 45° కోణాలను నిర్మించడం!\n\n"
                f"*(అధికారిక SCERT {cls_num}వ తరగతి పాఠ్యపుస్తకం: `{match.get('pdf', '')}`)*\n\n"
                f"మీరు ఏ నిర్మాణాన్ని సాధన చేయాలనుకుంటున్నారో చెప్పండి, నేను సులభమైన దశలతో వివరిస్తాను! 😊"
            )
        else:
            return (
                f"Hello! 🌟 I found this exciting topic in your **Class {cls_num} {subj} (Chapter {ch_num}: {ch_title})**!\n\n"
                f"📐 **What is Practical Geometry?**\n"
                f"Practical Geometry is the wonderful hands-on art of drawing and constructing accurate shapes using drawing instruments! "
                f"Instead of just rough sketches, it teaches us how to create perfect geometric figures using real tools. ✏️📏\n\n"
                f"Here are the special geometric tools used:\n"
                f"1. 📏 **Ruler (Straightedge):** To draw clean straight lines and measure distances accurately.\n"
                f"2. ⭕ **Compass:** With a sharp pencil point to draw circles and circular arcs.\n"
                f"3. 📐 **Protractor:** A semi-circular tool marked with degrees (0° to 180°) to measure angles.\n"
                f"4. 📐 **Set Squares:** Triangular tools to draw parallel and perpendicular lines.\n\n"
                f"✨ **Key Concepts you master in this chapter:**\n"
                f"• **Circles:** Setting the compass width and turning it smoothly around the center point.\n"
                f"• **Perpendicular Bisector:** Drawing intersecting arcs from both endpoints of a line to cut it exactly in half at 90°.\n"
                f"• **Angle Bisector:** Splitting any angle into two perfectly equal halves.\n"
                f"• **Special Angles:** Constructing 60°, 90°, and 45° angles accurately using just a compass and ruler!\n\n"
                f"*(Official Telangana SCERT Class {cls_num} Textbook: `{match.get('pdf', '')}`)*\n\n"
                f"Would you like step-by-step instructions on how to construct a specific angle or circle? I'd love to help! 😊"
            )

    # General child-friendly template
    if is_te:
        return (
            f"నమస్కారం! 🌟 ఈ అంశం మీ **{cls_num}వ తరగతి {subj} (అధ్యాయం {ch_num}: {ch_title})** లో ఉంది!\n\n"
            f"💡 **ముఖ్యాంశాలు:**\n"
            f"{summary}\n\n"
            f"ఈ అధ్యాయంలో మీరు నేర్చుకునే అంశాలు: {topics_list}.\n\n"
            f"*(అధికారిక SCERT {cls_num}వ తరగతి పాఠ్యపుస్తకం: `{match.get('pdf', '')}`)*\n\n"
            f"ఈ పాఠంపై మీకు ఇంకా ఏమైనా సందేహాలు ఉంటే నన్ను అడగండి! 😊"
        )
    else:
        return (
            f"Hello! 🌟 I found this topic in your **Class {cls_num} {subj} (Chapter {ch_num}: {ch_title})**!\n\n"
            f"💡 **Key Concepts:**\n"
            f"{summary}\n\n"
            f"In this chapter, you will learn about: {topics_list}.\n\n"
            f"*(Official Telangana SCERT Class {cls_num} Textbook: `{match.get('pdf', '')}`)*\n\n"
            f"Would you like to learn more about any specific topic from this chapter? Just ask! 😊"
        )

