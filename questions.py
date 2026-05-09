import os, pickle, random, copy

try:
    from images_data import IMAGES
except ImportError:
    IMAGES = {}

CUSTOM_QUESTIONS_FILE = "custom_questions.pkl"

# ═══════════════════════════════════════════════════════════════════════════════
# PART 1 — Oddiy savollar pool (har birida 5+ savol, random 3 tasi tanlanadi)
# ═══════════════════════════════════════════════════════════════════════════════
PART1_QUESTIONS = [
    {"id": 1, "questions": [
        "Please tell me about your family.",
        "What do you like to do on weekends?",
        "Tell me about your hometown or city."
    ]},
    {"id": 2, "questions": [
        "How often do you go to the cinema?",
        "What was the last film you saw?",
        "Tell me what you like doing in your free time.",
    ]},
    {"id": 3, "questions": [
        "Are you a social person?",
        "What kind of social networking websites do you like to use?",
        "Is it easy to find a real friend on a social networking website?",
    ]},
    {"id": 4, "questions": [
        "What is your dream job?",
        "How important is a knowledge of English for finding a job in your country?",
        "Do you think you would enjoy an outdoor job?",
    ]},
    {"id": 5, "questions": [
        "What does religion mean to you?",
        "Why is it important to celebrate special occasions with family and friends?",
        "When do you give presents in your culture?",
    ]},
    {"id": 6, "questions": [
        "Do you want to be a teacher?",
        "What qualities should a good teacher have?",
        "Do you still keep in touch with any of your teachers?",
    ]},
    {"id": 7, "questions": [
        "What is your favorite dish? How often do you eat it?",
        "Do you like cooking? Why or why not?",
        "Are you satisfied with your lifestyle and diet?",
    ]},
    {"id": 8, "questions": [
        "Do you get up early or late?",
        "Are you interested in news?",
        "What do you do to relax?",
    ]},
    {"id": 9, "questions": [
        "Do you like to watch sports on TV?",
        "Do you play any sports?",
        "Which is the most popular sport in your country?",
    ]},
    {"id": 10, "questions": [
        "Tell me about your school.",
        "How do you stay healthy?",
        "What is your favorite part of the day?",
    ]},
]

# ═══════════════════════════════════════════════════════════════════════════════
# PART 1.1 — Rasm + savollar
# prep_times: [10, 5, 5]  →  1-savolga 10s, 2 va 3-savolga 5s
# ═══════════════════════════════════════════════════════════════════════════════
PART1_1_QUESTIONS = [
    {
        "id": 1, "img_key": "img1",
        "image_description": "Golf and Basketball",
        "questions": [
            "What kind of people play these two sports?",
            "Which of these two sports is more difficult to play?",
            "What kind of sport do you like the most?"
        ],
        "prep_times": [10, 5, 5], "speak_time": 30,
    },
    {
        "id": 2, "img_key": "img2",
        "image_description": "A child using a computer and children playing football",
        "questions": [
            "Tell me what you can see in these two pictures.",
            "How can the two activities help children develop?",
            "Which activity would you encourage your children to do?"
        ],
        "prep_times": [10, 5, 5], "speak_time": 30,
    },
    {
        "id": 3, "img_key": "img3",
        "image_description": "A modern city skyline and an English countryside village",
        "questions": [
            "What can you see in these two pictures?",
            "What kinds of city do you like?",
            "Have you ever lived in the countryside?"
        ],
        "prep_times": [10, 5, 5], "speak_time": 30,
    },
    {
        "id": 4, "img_key": "img4",
        "image_description": "A scientist in a lab and miners underground",
        "questions": [
            "Tell me what you see in the two pictures.",
            "Which job do you think is more difficult?",
            "Which job is more rewarding?"
        ],
        "prep_times": [10, 5, 5], "speak_time": 30,
    },
    {
        "id": 5, "img_key": "img5",
        "image_description": "Students studying in a group and a student studying alone",
        "questions": [
            "Describe what you see in the two pictures.",
            "Do you study alone or in groups? Why?",
            "Why do students study in groups?"
        ],
        "prep_times": [10, 5, 5], "speak_time": 30,
    },
    {
        "id": 6, "img_key": "img6",
        "image_description": "A school classroom and a university lecture hall",
        "questions": [
            "Tell me what you can see in these two pictures.",
            "What is the difference between school teachers and university teachers?",
            "Do you remember your favorite teacher from primary school?"
        ],
        "prep_times": [10, 5, 5], "speak_time": 30,
    },
    {
        "id": 7, "img_key": "img7",
        "image_description": "Children with junk food and a family having a healthy meal",
        "questions": [
            "Tell me what you can see in these two pictures.",
            "Why do people eat unhealthy food?",
            "How can unhealthy eating affect people?"
        ],
        "prep_times": [10, 5, 5], "speak_time": 30,
    },
    {
        "id": 8, "img_key": "img8",
        "image_description": "A family at an airport and grandparents with a child on a train",
        "questions": [
            "Compare traveling by plane and traveling by train.",
            "What are the disadvantages of traveling by plane?",
            "What are the benefits of traveling?"
        ],
        "prep_times": [10, 5, 5], "speak_time": 30,
    },
    {
        "id": 9, "img_key": "img9",
        "image_description": "Outdoor workout park and an indoor sports hall",
        "questions": [
            "What can you see in these two pictures?",
            "Which sport do you like the most — indoor or outdoor?",
            "What kind of sport do people like in your country?"
        ],
        "prep_times": [10, 5, 5], "speak_time": 30,
    },
    {
        "id": 10, "img_key": "img10",
        "image_description": "A person reading an e-book and scattered paper books",
        "questions": [
            "What can you see in these two pictures?",
            "Which one would you prefer — an e-book or a paper book?",
            "What are the advantages or disadvantages of reading e-books?"
        ],
        "prep_times": [10, 5, 5], "speak_time": 30,
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# PART 2
# ═══════════════════════════════════════════════════════════════════════════════
PART2_QUESTIONS = [
    {"id": 1, "image_description": "🏔️ A person sitting alone in nature — hills and forests.",
     "questions": ["Tell me a time when you were on your own.", "How did you feel about it?", "What are some ways of passing time on your own?"]},
    {"id": 2, "image_description": "⚽🏀 Various sports balls.",
     "questions": ["Do you play any sports?", "What sports do you like watching on TV?", "Which sports do you find boring or entertaining?"]},
    {"id": 3, "image_description": "🎓 Students in graduation gowns celebrating.",
     "questions": ["Tell me about an important event in your life.", "How did the event make you feel?", "How do events like this bring people together?"]},
    {"id": 4, "image_description": "📚 Historical classroom with students at wooden desks.",
     "questions": ["Describe this picture.", "How has education changed over the years?", "How is technology affecting education?"]},
    {"id": 5, "image_description": "🚚 A moving truck with boxes and furniture.",
     "questions": ["Tell me about a time when you moved house.", "How did you feel?", "What can people do to ease moving house?"]},
    {"id": 6, "image_description": "🌐 A woman interacting with holographic technology.",
     "questions": ["What is the most common technology in your country?", "Are there places that need more technology?", "Is it possible to live without technology?"]},
    {"id": 7, "image_description": "🍽️ Traditional foods from different cultures.",
     "questions": ["Why try traditional cuisine abroad?", "Describe traditional cuisine of your country.", "How does food reflect a country's culture?"]},
    {"id": 8, "image_description": "🎉 People celebrating an achievement in an office.",
     "questions": ["Describe when you celebrated an achievement.", "When and who did you celebrate with?", "How did you feel about it?"]},
    {"id": 9, "image_description": "🧑‍🎒 A teenager in a school corridor.",
     "questions": ["Describe a teenager you know.", "What do they look like?", "How did you get to know them and why do you like them?"]},
    {"id": 10, "image_description": "🎯 A person aiming a dart at a dartboard.",
     "questions": ["Describe a recent goal you set yourself.", "Why did you want it and what did you do?", "How did you feel about achieving it?"]},
]

# ═══════════════════════════════════════════════════════════════════════════════
# PART 3
# ═══════════════════════════════════════════════════════════════════════════════
PART3_QUESTIONS = [
    {"id": 1, "topic": "Public transportation should be free for everyone.",
     "for_points": ["Reduces traffic congestion and pollution", "Makes transportation accessible to low-income individuals", "Encourages use of public transport"],
     "against_points": ["Increased tax burden on citizens", "May lead to overcrowding", "Funding and maintenance challenges"],
     "questions": ["Discuss whether public transportation should be free."]},
    {"id": 2, "topic": "Advertising is a key part of modern business.",
     "for_points": ["Informs us about choices", "Prevents unemployment", "Companies need to reach customers"],
     "against_points": ["Children pressure parents to buy things", "Use glamorous people", "Brand association with status"],
     "questions": ["Is advertising necessary in modern business?"]},
    {"id": 3, "topic": "Companies should sponsor sport events for advertising.",
     "for_points": ["Players can focus on sport", "Companies link name to successful players", "People think positively of sponsors"],
     "against_points": ["Companies showcase products", "Some advertise harmful products", "Unsuccessful player affects sales"],
     "questions": ["Should companies sponsor sporting events?"]},
    {"id": 4, "topic": "Businesses should provide sports facilities for employees.",
     "for_points": ["Staff can improve health", "Healthy staff = more productivity", "Incentive for loyalty"],
     "against_points": ["Health is personal responsibility", "Too expensive for small businesses", "Better to spend on bonuses"],
     "questions": ["Should businesses provide sports facilities?"]},
    {"id": 5, "topic": "It is better to live in a rented house than to buy.",
     "for_points": ["More economical short term", "Easier to relocate for work", "Landlord handles repairs"],
     "against_points": ["Pay rent for many years", "Cannot renovate as you want", "You may be asked to move"],
     "questions": ["Is it better to rent or buy your own home?"]},
    {"id": 6, "topic": "Homework should be optional in schools.",
     "for_points": ["Encourages independent learning", "Reduces stress", "Quality over quantity"],
     "against_points": ["Reinforces learning", "Teaches responsibility", "Provides feedback to teachers"],
     "questions": ["Should homework be optional in schools?"]},
    {"id": 7, "topic": "Video games — beneficial or harmful?",
     "for_points": ["Improves cognitive skills", "Social interaction", "Stress relief"],
     "against_points": ["Addiction issues", "Physical health problems", "Exposure to violent content"],
     "questions": ["Are video games beneficial or harmful for young people?"]},
    {"id": 8, "topic": "Smartphones should be banned in schools.",
     "for_points": ["Distraction from learning", "Academic integrity concerns", "Mental health and cyberbullying"],
     "against_points": ["Educational tools", "Emergency communication", "Digital literacy development"],
     "questions": ["Should smartphones be banned in schools?"]},
    {"id": 9, "topic": "Animal testing should be banned in scientific research.",
     "for_points": ["No moral right to experiment on animals", "Animal lives should be respected", "Alternative methods exist"],
     "against_points": ["Used in important research", "Necessary for testing new drugs", "Advances medical knowledge"],
     "questions": ["Should animal testing be completely banned?"]},
    {"id": 10, "topic": "Electric cars should replace gasoline cars.",
     "for_points": ["Environmental impact", "Energy efficiency", "Long-term cost savings"],
     "against_points": ["Limited charging infrastructure", "Battery disposal issues", "High initial cost"],
     "questions": ["Should electric cars fully replace gasoline cars?"]},
]


# ═══════════════════════════════════════════════════════════════════════════════
# CUSTOM QUESTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def load_custom_questions():
    if os.path.exists(CUSTOM_QUESTIONS_FILE):
        try:
            with open(CUSTOM_QUESTIONS_FILE, "rb") as f:
                return pickle.load(f)
        except Exception:
            return {}
    return {}


def save_custom_questions(data):
    with open(CUSTOM_QUESTIONS_FILE, "wb") as f:
        pickle.dump(data, f)


# ═══════════════════════════════════════════════════════════════════════════════
# CORE: Random 3 ta savol tanlash
# ═══════════════════════════════════════════════════════════════════════════════
def _pick3(questions: list, rng: random.Random) -> list:
    pool = list(questions)
    rng.shuffle(pool)
    return pool[:3]


# ═══════════════════════════════════════════════════════════════════════════════
# get_random_mock  — to'liq test
# ═══════════════════════════════════════════════════════════════════════════════
def get_random_mock(seed=None):
    rng = random.Random(seed)
    custom = load_custom_questions()

    # Part 1
    p1_pool = copy.deepcopy(rng.choice(PART1_QUESTIONS))
    extra_q = custom.get("custom_part1", {}).get("questions", [])
    if extra_q:
        p1_pool["questions"] += extra_q
    chosen_p1 = _pick3(p1_pool["questions"], rng)

    # Part 1.1
    p11 = copy.deepcopy(rng.choice(PART1_1_QUESTIONS))
    img_b64 = IMAGES.get(p11.get("img_key", ""), "")

    # Part 2
    p2 = copy.deepcopy(rng.choice(PART2_QUESTIONS))

    # Part 3
    p3 = copy.deepcopy(rng.choice(PART3_QUESTIONS))
    c3 = custom.get("custom_part3", {})
    for field in ("topic", "for_points", "against_points", "questions"):
        if c3.get(field):
            p3[field] = c3[field]

    return {
        "part1": {
            "title": "PART 1",
            "instruction": "I'm going to ask you three short questions about yourself. You will have 30 seconds to reply to each question.",
            "questions": chosen_p1,
            "prep_time": 5,
            "speak_time": 30,
            "pool_id": p1_pool["id"],
            "is_part1_1": False,
        },
        "part1_1": {
            "title": "PART 1.1",
            "instruction": "Now look at the pictures carefully. I will ask you three questions. You will have time to prepare before each question.",
            "image_description": p11.get("image_description", ""),
            "img_b64": img_b64,
            "questions": p11["questions"],
            "prep_times": p11.get("prep_times", [10, 5, 5]),
            "speak_time": p11.get("speak_time", 30),
            "pool_id": p11["id"],
            "is_part1_1": True,
        },
        "part2": {
            "title": "PART 2",
            "instruction": "Look at the picture and answer the questions below. You will have 60 seconds to prepare.",
            "image_description": p2.get("image_description", ""),
            "img_b64": "",
            "questions": p2["questions"],
            "prep_time": 60,
            "speak_time": 120,
            "pool_id": p2["id"],
        },
        "part3": {
            "title": "PART 3",
            "instruction": "Discuss the following statement using the FOR and AGAINST points.",
            "topic": p3.get("topic", ""),
            "for_points": p3.get("for_points", []),
            "against_points": p3.get("against_points", []),
            "questions": p3["questions"],
            "prep_time": 60,
            "speak_time": 120,
            "pool_id": p3["id"],
        },
    }


def get_random_part(part_key: str, seed=None) -> dict:
    rng = random.Random(seed)
    custom = load_custom_questions()

    if part_key == "part1":
        p1_pool = copy.deepcopy(rng.choice(PART1_QUESTIONS))
        extra_q = custom.get("custom_part1", {}).get("questions", [])
        if extra_q:
            p1_pool["questions"] += extra_q
        return {
            "title": "PART 1",
            "instruction": "I'm going to ask you three short questions about yourself.",
            "questions": _pick3(p1_pool["questions"], rng),
            "prep_time": 5,
            "speak_time": 30,
            "pool_id": p1_pool["id"],
            "is_part1_1": False,
        }

    elif part_key == "part1_1":
        p11 = copy.deepcopy(rng.choice(PART1_1_QUESTIONS))
        img_b64 = IMAGES.get(p11.get("img_key", ""), "")
        return {
            "title": "PART 1.1",
            "instruction": "Look at the pictures. I will ask you three questions.",
            "image_description": p11.get("image_description", ""),
            "img_b64": img_b64,
            "questions": p11["questions"],
            "prep_times": p11.get("prep_times", [10, 5, 5]),
            "speak_time": p11.get("speak_time", 30),
            "pool_id": p11["id"],
            "is_part1_1": True,
        }

    elif part_key == "part2":
        p2 = copy.deepcopy(rng.choice(PART2_QUESTIONS))
        return {
            "title": "PART 2",
            "instruction": "Look at the picture and answer the questions. 60 seconds to prepare.",
            "image_description": p2.get("image_description", ""),
            "img_b64": "",
            "questions": p2["questions"],
            "prep_time": 60, "speak_time": 120,
            "pool_id": p2["id"],
        }

    elif part_key == "part3":
        p3 = copy.deepcopy(rng.choice(PART3_QUESTIONS))
        c3 = custom.get("custom_part3", {})
        for field in ("topic", "for_points", "against_points", "questions"):
            if c3.get(field):
                p3[field] = c3[field]
        return {
            "title": "PART 3",
            "instruction": "Discuss the statement using FOR and AGAINST points.",
            "topic": p3.get("topic", ""),
            "for_points": p3.get("for_points", []),
            "against_points": p3.get("against_points", []),
            "questions": p3["questions"],
            "prep_time": 60, "speak_time": 120,
            "pool_id": p3["id"],
        }

    return {}


def get_all_pools():
    return {
        "part1":   PART1_QUESTIONS,
        "part1_1": PART1_1_QUESTIONS,
        "part2":   PART2_QUESTIONS,
        "part3":   PART3_QUESTIONS,
    }
