import asyncio
import logging
import os
from typing import Dict, List, Optional

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

# ===== КОНФИГУРАЦИЯ =====
# Токен берётся из переменной окружения BOT_TOKEN (на Render)
API_TOKEN = os.getenv("BOT_TOKEN")
if not API_TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# ===== СОСТОЯНИЯ =====
class UserState(StatesGroup):
    viewing_unit = State()
    answering_question = State()

# ===== КОНТЕНТ =====
class Content:
    BLOCKS = {
        "block1": {
            "name": "🏛️ BLOCK 1: FOUNDATIONS — WHAT IS SOCIOLOGY?",
            "description": "Introduction to sociology, sociological imagination, and why sociology matters",
            "units": {
                "unit1_1": {
                    "name": "1.1 Definition and Subject Matter",
                    "content": """📖 **WHAT IS SOCIOLOGY?**

Sociology is the scientific study of social relationships — how people are connected to each other, and how these connections shape our actions, thoughts, and feelings.

🔑 **Key Definition:**
Sociology reveals that our personal problems and successes are linked to larger social processes.

❓ **The central question of sociology:**
*How do we live in society? How does society affect what we do, think, and feel?*

To answer this, sociologists use the sociological imagination.

💡 **Why it matters:**
Sociology helps us understand that our individual experiences are not just personal — they are shaped by society.""",
                    "questions": [
                        {
                            "question": "What is the main focus of sociology?",
                            "options": ["Study of individual psychology", "Scientific study of social relationships", "Study of economics only", "Study of history"],
                            "correct": 1,
                            "explanation": "Sociology is the scientific study of social relationships — how people are connected and how these connections shape our lives."
                        }
                    ]
                },
                "unit1_2": {
                    "name": "1.2 The Sociological Imagination (C. Wright Mills, 1959)",
                    "content": """🧠 **THE SOCIOLOGICAL IMAGINATION**

**Definition:**
The sociological imagination is the ability to connect personal troubles, experiences, and biography with broader social processes, history, and social structure.

📝 **C. Wright Mills (1959):**
> "The sociological imagination enables us to grasp the relation between history and biography within society. It is the capacity to shift from one perspective to another — from the political to the psychological, from the examination of a single family to the comparative assessment of national budgets."

💡 **In simple terms:**
It is the skill to see how your "small" life is intertwined with large historical and social forces.

📌 **Key idea:**
Sociology begins where we stop believing in the obvious.""",
                    "examples": """🔍 **EXAMPLES: Personal Trouble vs. Sociological Reframing**

| Personal Problem | Sociological Reformulation |
|------------------|---------------------------|
| "I can't find a job after graduation" | "Why is youth unemployment so high? How is the labour market structured?" |
| "I have depression and constant anxiety" | "Why is anxiety so prevalent in modern society? How do social media, the cult of success, and instability affect mental health?" |
| "I didn't get a scholarship because I'm not smart enough" | "How do the Unified State Exam, Olympiads, and grading systems actually work? Are they fair?" |

**Real-life application:**
Students start looking for internships from 2nd-3rd year and often face failures. Instead of blaming personal qualities, a sociological approach analyzes how the labour market is structured right now.""",
                    "questions": [
                        {
                            "question": "What does the sociological imagination help us do?",
                            "options": ["Ignore personal problems", "Connect personal experiences to social processes", "Focus only on history", "Study only economics"],
                            "correct": 1,
                            "explanation": "Sociological imagination helps us connect personal troubles to broader social processes and structures."
                        },
                        {
                            "question": "Why do we need to study sociology?",
                            "options": ["To question common sense", "To reinforce common sense", "To learn one right way of seeing society", "To memorize theories"],
                            "correct": 0,
                            "explanation": "We study sociology to question common sense and see the 'invisible threads' connecting us to the bigger picture."
                        }
                    ]
                },
                "unit1_3": {
                    "name": "1.3 Sociology vs. Common Sense",
                    "content": """⚖️ **SOCIOLOGY vs. COMMON SENSE**

**Key difference:**
Sociology systematically tests assumptions, while common sense relies on personal experience and cultural beliefs.

**Why sociology matters:**
- To question common sense
- To understand that our behaviour is connected to the structure of society
- To learn to see the "invisible threads" that link us to the bigger picture

💡 **Remember:**
Sociology begins where we stop believing in the obvious.

**Example:**
Common sense might say: "Poor people are lazy."
Sociology asks: "How does the economic system create and reproduce poverty?""",
                    "questions": [
                        {
                            "question": "What is the main difference between sociology and common sense?",
                            "options": ["Sociology is harder to understand", "Sociology systematically tests assumptions", "Common sense is always wrong", "Sociology ignores individual experience"],
                            "correct": 1,
                            "explanation": "Sociology systematically tests assumptions, while common sense relies on personal experience and cultural beliefs."
                        }
                    ]
                }
            }
        },
        "block2": {
            "name": "🔬 BLOCK 2: WHAT AND HOW DO WE STUDY? — METHODOLOGY",
            "description": "Ontology, epistemology, paradigms, research methods, and what makes sociology scientific",
            "units": {
                "unit2_1": {
                    "name": "2.1 Ontology and Epistemology",
                    "content": """📚 **METHODOLOGY = THEORY + METHODS**

Every science relies on methodology and is based on two foundations:

**1️⃣ Ontology (WHAT):**
What is the object of study? (e.g., what is society?)

**2️⃣ Epistemology (HOW):**
How do we study and know that object? (through observation, surveys, statistics, interviews, etc.)

❓ **Three Fundamental Questions About Society:**

| Question | In Simple Terms | Example |
|----------|-----------------|---------|
| How is social order possible? | Why do people obey rules, not kill, not steal, wait in line? | You enter a reading room — it is quiet. Why? Because of social norms. |
| How are social changes possible? | Why do societies change? What drives revolutions, new technologies, new norms? | Why was it prestigious to be a lawyer 20 years ago, but now an IT specialist? |
| How does society shape the individual? | Are we free? Or are we shaped by family, school, social media, advertising? | Did you choose your major freely, or was it influenced by parents, status, market demands? |""",
                    "questions": [
                        {
                            "question": "What does ontology study?",
                            "options": ["How we know things", "What exists / what is the object of study", "Research methods", "Statistical analysis"],
                            "correct": 1,
                            "explanation": "Ontology asks 'What is the object of study?' — what exists and what is the nature of reality."
                        }
                    ]
                },
                "unit2_2": {
                    "name": "2.2 Ontological Dilemmas",
                    "content": """⚖️ **ONTOLOGICAL DILEMMAS**

**Dilemma 1: Consensus vs. Conflict**

| Perspective | Explanation | Key Thinker |
|-------------|-------------|-------------|
| Consensus | Order is based on shared norms and values | Durkheim |
| Conflict | Order is based on struggle over values, power, and resources | Coser, Marx |

**Dilemma 2: Idealism vs. Materialism**

| Perspective | Explanation | Example |
|-------------|-------------|---------|
| Idealism | Ideas, religion, culture drive society | Values and beliefs shape economic systems |
| Materialism | Economy and technology drive society | Economic base determines social relations |

**Dilemma 3: Structure vs. Agency**

| | Puppet (Structure) | Actor (Agency) |
|--|-------------------|----------------|
| Who controls? | Invisible social forces | Partly self, partly director (society) |
| Is there freedom? | No, our actions are predetermined | Yes, we are autonomous within roles |
| Can we change the script? | No | Yes, but with difficulty |

📝 **Berger & Luckmann (1966):**
> "Society is the dialectic of externalization, objectivation, and internalization." """,
                    "questions": [
                        {
                            "question": "According to the structure vs. agency debate, agency means:",
                            "options": ["People are completely controlled by society", "People have some freedom to act and shape their lives", "Society doesn't exist", "Only economic forces matter"],
                            "correct": 1,
                            "explanation": "Agency means that people have some freedom to act and shape their lives, though within social constraints."
                        },
                        {
                            "question": "Which dilemma asks: 'What drives society — ideas or economy?'",
                            "options": ["Consensus vs. Conflict", "Idealism vs. Materialism", "Structure vs. Agency", "Science vs. Religion"],
                            "correct": 1,
                            "explanation": "Idealism vs. Materialism asks whether ideas, religion, and culture (idealism) or economy and technology (materialism) drive society."
                        }
                    ]
                },
                "unit2_3": {
                    "name": "2.3 Three Approaches: Positivism, Interpretivism, Realism",
                    "content": """🔎 **THREE APPROACHES IN SOCIOLOGY**

| Criterion | Positivism | Interpretivism | Realism |
|-----------|------------|----------------|---------|
| **What is reality?** | Objective, exists "out there" like nature | Socially constructed by people | Objective but multi-layered. Behind the visible are hidden mechanisms |
| **How do we know?** | Through observation, measurement, experiment | Through understanding meanings people attach to actions (Verstehen) | Through theory we uncover hidden mechanisms (class, power, structures) |
| **Main question** | "What are the measurable patterns?" | "What does this mean for the people living it?" | "What invisible forces produce what I see?" |
| **Methods** | Surveys, statistics, experiments, quasi-experiments | In-depth interviews, focus groups, participant observation | Combination of methods + theoretical analysis |
| **Key figures** | Comte, Durkheim | Weber, Schütz, Goffman | Marx, Bhaskar, Wright |

**Society as Theater — Interpretivism:**
The world is a stage — people play roles and attach meaning to their actions.""",
                    "questions": [
                        {
                            "question": "Which approach focuses on understanding the meanings people attach to their actions?",
                            "options": ["Positivism", "Interpretivism", "Realism", "Structuralism"],
                            "correct": 1,
                            "explanation": "Interpretivism focuses on understanding the meanings people attach to their actions through Verstehen."
                        }
                    ]
                },
                "unit2_4": {
                    "name": "2.4 Three Main Sociological Paradigms",
                    "content": """🎯 **THREE MAIN SOCIOLOGICAL PARADIGMS**

| Paradigm | Core Idea | Key Figures | Example |
|----------|-----------|-------------|---------|
| **Structural Functionalism** | Society is an organism; each part has a function. Order through consensus. | Durkheim, Parsons | Education socialises and reproduces labour. Everyone agrees education is good. |
| **Conflict Paradigm** | Society is an arena of struggle over resources. Order through coercion and ideology. | Marx, Wright | Paid education filters out those who cannot pay, maintaining inequality. |
| **Symbolic Interactionism** | Society is created in each interaction through symbols and roles. | Mead, Goffman, Weber | By third year, you've mastered the "student" role. |

📊 **Summary: Paradigms and Dilemmas**

| Theory | Consensus/Conflict | Structure/Agency | Idealism/Materialism |
|--------|-------------------|------------------|---------------------|
| Functionalism | Consensus | Structure | Idealism |
| Conflict | Conflict | Structure | Materialism |
| Interactionism | Mixed | Agency | Idealism |""",
                    "questions": [
                        {
                            "question": "Which paradigm sees society as an arena of struggle over resources?",
                            "options": ["Structural Functionalism", "Conflict Paradigm", "Symbolic Interactionism", "Realism"],
                            "correct": 1,
                            "explanation": "The Conflict Paradigm sees society as an arena of struggle over resources, order through coercion and ideology."
                        },
                        {
                            "question": "Which paradigm believes that society is created through everyday interactions?",
                            "options": ["Structural Functionalism", "Conflict Paradigm", "Symbolic Interactionism", "Positivism"],
                            "correct": 2,
                            "explanation": "Symbolic Interactionism believes that society is created through everyday interactions and shared symbols."
                        }
                    ]
                },
                "unit2_5": {
                    "name": "2.5 Science vs. Non-Science: Criteria",
                    "content": """🧪 **SCIENCE vs. NON-SCIENCE — CRITERIA**

**Is sociology a science?**
Yes — but a special kind of science: multi-paradigm and reflexive.

| Criterion | What it means | Does sociology meet it? |
|-----------|---------------|-------------------------|
| **Falsifiability** (Popper) | A theory can be disproven | Partially — some theories (e.g., Marxism) are hard to falsify |
| **Paradigm** (Kuhn) | Is there a single agreement? | No — multi-paradigm → contested status |
| **Empiricism** | Relies on data, not belief | Yes — sociologists collect data |

💡 **Conclusion:**
Sociology does not meet the strict ideal of natural sciences, but it uses systematic methods, empirical data, and strives for objectivity.""",
                    "questions": [
                        {
                            "question": "Why is sociology sometimes considered a contested science?",
                            "options": ["Because it doesn't use numbers", "Because it is multi-paradigm with no single agreement", "Because it doesn't study real things", "Because it's just common sense"],
                            "correct": 1,
                            "explanation": "Sociology is multi-paradigm with no single agreement, which makes it a contested science."
                        }
                    ]
                },
                "unit2_6": {
                    "name": "2.6 Quantitative vs. Qualitative Research",
                    "content": """📊 **QUANTITATIVE vs. QUALITATIVE RESEARCH**

| Criterion | Quantitative | Qualitative |
|-----------|--------------|-------------|
| **What it provides** | Numbers, percentages, correlations | Meanings, stories, experiences |
| **Methods** | Surveys, questionnaires, statistics, experiments | In-depth interviews, focus groups, observation |
| **Sample size** | Large (hundreds/thousands) | Small (10-30 people) |
| **Strength** | Generalisation, reliability | Deep understanding, ecological validity |
| **Weakness** | Misses meanings and interpretations | Hard to generalise |

📌 **Key Quality Criteria:**

| Criterion | Meaning |
|-----------|---------|
| **Objectivity** | Results do not depend on the researcher's preferences |
| **Reliability** | Repeatability — another researcher using the same method gets the same results |
| **Validity** | Data actually measure what they claim to measure |
| **Ecological validity** | Results correspond to real life, not just lab conditions |
| **Transparency** | Methods are openly described so others can verify |

💡 **Important:**
Neither type is "better" — each serves different purposes. Both are valuable in sociology.""",
                    "questions": [
                        {
                            "question": "Which research method would be best for understanding WHY students are late to class?",
                            "options": ["Large survey with statistics", "In-depth interviews with late students", "Experiment in a lab", "Literature review"],
                            "correct": 1,
                            "explanation": "In-depth interviews with late students would be best for understanding WHY they're late — qualitative research explores meanings and reasons."
                        },
                        {
                            "question": "What is reliability in research?",
                            "options": ["The research measures what it claims to measure", "Another researcher using the same method gets the same results", "The research is objective", "The research is published"],
                            "correct": 1,
                            "explanation": "Reliability means repeatability — another researcher using the same method gets the same results."
                        }
                    ]
                }
            }
        },
        "block3": {
            "name": "👨‍🏫 BLOCK 3: FOUNDING FATHERS OF SOCIOLOGY",
            "description": "Karl Marx, Émile Durkheim, and Max Weber — their key ideas and contributions",
            "units": {
                "unit3_1": {
                    "name": "3.1 Karl Marx (1818-1883)",
                    "content": """⚡ **KARL MARX (1818-1883)**

**Ontology:** structure, conflict, materialism
**Epistemology:** critical realism

**Key Concepts:**

| Concept | Explanation |
|---------|-------------|
| **Means of production** | Factories, land, machinery, buildings owned by the rich (capitalists) |
| **Class** | Groups differing by economic position; Marx saw two main classes |
| **Bourgeoisie** | The class that owns the means of production and capital |
| **Proletariat** | The class that sells its labour and does not own the means of production |
| **Exploitation** | Workers produce more than they get in wages; surplus is appropriated by capitalists |
| **Ideology** | Ideas that justify the dominance of the bourgeoisie |
| **Alienation** | Workers are separated from the product, from their human nature, from other workers, and from the process |
| **False consciousness** | Workers do not recognise their true interests |

🔍 **Example: Student as Sales Manager**
A student works as a sales manager, brings in 400,000 rubles monthly, but gets paid 100,000. The difference (300,000) is surplus value appropriated by owners.

The student thinks 100,000 is fair — that is **false consciousness**. 
The university economics lecture that explains labour as "free exchange" is **ideology**.

The student is **alienated** from:
- The product (doesn't see who uses it)
- The process (controlled by CRM, KPIs)
- Other workers (competition)
- Their human nature (just earning, not creating)

📌 **Critique:**
- Marx didn't foresee the middle class (managers, IT specialists, lawyers)
- Workers in developed countries have decent living standards
- Capitalism adapted and survived""",
                    "questions": [
                        {
                            "question": "What is the main difference between the bourgeoisie and the proletariat according to Marx?",
                            "options": ["Amount of money", "Relation to the means of production", "Level of education", "Social status"],
                            "correct": 1,
                            "explanation": "The main difference is their relation to the means of production — the bourgeoisie owns them, the proletariat does not."
                        },
                        {
                            "question": "What does Marx mean by 'false consciousness'?",
                            "options": ["Workers understand their true interests", "Workers do not recognise their true interests", "Workers are happy", "Workers own the means of production"],
                            "correct": 1,
                            "explanation": "False consciousness means workers do not recognise their true class interests and accept the existing system as natural."
                        }
                    ]
                },
                "unit3_2": {
                    "name": "3.2 Émile Durkheim (1858-1917)",
                    "content": """📊 **ÉMILE DURKHEIM (1858-1917)**

**Ontology:** structure, consensus, idealism
**Epistemology:** positivism and social realism

**Key Concepts:**

| Concept | Explanation |
|---------|-------------|
| **Social fact** | Phenomena external to the individual that constrain them (laws, norms, language, fashion) |
| **Collective consciousness** | Shared beliefs and sentiments of society |
| **Division of labour** | Specialisation of tasks in society |
| **Mechanical solidarity** | Order in traditional societies — everyone is similar, common values are strong |
| **Organic solidarity** | Order in modern societies — people are different but interdependent (like organs in a body) |
| **Anomie** | A state of normlessness when old rules break down and new ones have not yet formed |

🔍 **Examples:**

| Concept | Example |
|---------|---------|
| **Social fact** | You are silent during a lecture — that is a social fact (norm) |
| **Anomie** | After finals, you feel empty and anxious — old rules broke down, new ones haven't formed |
| **Mechanical solidarity** | In school, everyone studied the same subjects |
| **Organic solidarity** | At university, everyone has different majors, yet you depend on others |

📌 **Critique:**
- Durkheim ignored conflict and struggle for resources
- Anomie is vague and hard to measure""",
                    "questions": [
                        {
                            "question": "What is anomie according to Durkheim?",
                            "options": ["A state of social harmony", "A state of normlessness when old rules break down", "A type of solidarity", "A political system"],
                            "correct": 1,
                            "explanation": "Anomie is a state of normlessness when old rules have broken down and new ones have not yet formed."
                        },
                        {
                            "question": "What is the difference between mechanical and organic solidarity?",
                            "options": ["Mechanical is modern, organic is traditional", "Mechanical is traditional (everyone similar), organic is modern (interdependent but different)", "Mechanical is conflict-based, organic is consensus-based", "They are the same thing"],
                            "correct": 1,
                            "explanation": "Mechanical solidarity is traditional (everyone is similar, shared values); organic solidarity is modern (people are different but interdependent like organs in a body)."
                        }
                    ]
                },
                "unit3_3": {
                    "name": "3.3 Max Weber (1864-1920)",
                    "content": """📝 **MAX WEBER (1864-1920)**

**Ontology:** individualism, conflict, idealism
**Epistemology:** interpretivism (Verstehen)

**Key Concepts:**

| Concept | Explanation |
|---------|-------------|
| **Social action** | Action oriented toward others and having meaning for the actor |
| **Verstehen** | Interpretive understanding of subjective meanings |
| **Ideal type** | Analytical construct that highlights essential features (not found in reality in pure form) |
| **Types of social action** | Traditional, affective, value-rational, instrumentally rational |
| **Rationalisation** | More spheres of life governed by calculation, efficiency, planning |
| **Iron cage** | Modern humans trapped in bureaucracy and formal rationality that stifles freedom |
| **Bureaucracy** | Ideal type: hierarchy, written rules, appointment by qualification |
| **Types of legitimate authority** | Traditional, charismatic, legal-rational |

🔍 **Examples:**

| Concept | Example |
|---------|---------|
| **Social action** | You fall silent when the lecturer enters — you give meaning to their entry |
| **Ideal type** | "Career-oriented student" vs. "Enthusiast student" — compare motivations |
| **Iron cage** | HSE — grades, KPIs, rankings — you feel trapped |
| **Bureaucracy** | Getting a certificate from the dean's office — waiting, forms, rules |

📌 **Critique:**
- Deep understanding requires time and small samples — hard to generalise
- Focus on individual action does not easily explain structural inequality

❓ **What is important according to Weber?**
Understanding the meanings that people attach to their actions!""",
                    "questions": [
                        {
                            "question": "What is important according to Weber?",
                            "options": ["Seeing the overall picture of the situation", "Understanding the meanings people attach to their actions", "Measuring social facts statistically", "Analysing class conflict"],
                            "correct": 1,
                            "explanation": "Weber believed it is important to understand the meanings people attach to their actions through Verstehen."
                        },
                        {
                            "question": "What is an 'ideal type' in Weber's sociology?",
                            "options": ["A perfect person", "An analytical construct highlighting essential features", "A statistical average", "A real-life example"],
                            "correct": 1,
                            "explanation": "An ideal type is an analytical construct that highlights essential features of a phenomenon — it's not found in reality in pure form."
                        }
                    ]
                },
                "unit3_4": {
                    "name": "3.4 Comparative Table: The Three Classics",
                    "content": """📊 **COMPARATIVE TABLE: MARX, DURKHEIM, WEBER**

| Aspect | Marx | Durkheim | Weber |
|--------|------|----------|-------|
| **Core question** | Why is there inequality and exploitation? | How is social order possible? | What meaning do people give to their actions? |
| **Ontology** | Materialism, conflict, structure | Idealism, consensus, structure | Idealism, conflict, agency |
| **Epistemology** | Critical realism | Positivism | Interpretivism (Verstehen) |
| **View of society** | Arena of class struggle | Organism with parts functioning together | Web of meaningful social actions |
| **Key concept** | Class struggle, alienation | Social fact, anomie | Ideal type, rationalisation |
| **Method** | Historical materialism | Statistical analysis, comparison | Interpretive understanding, historical analysis |
| **Legacy** | Inspired conflict theory and critical sociology | Laid foundation for functionalism and empirical sociology | Founded interpretive sociology and theory of rationalisation |

💡 **Remember:**
- **Marx** → Conflict, class, economy
- **Durkheim** → Order, norms, solidarity
- **Weber** → Meaning, action, rationality""",
                    "questions": [
                        {
                            "question": "Which sociologist focused on 'social facts' as the key unit of analysis?",
                            "options": ["Karl Marx", "Émile Durkheim", "Max Weber", "C. Wright Mills"],
                            "correct": 1,
                            "explanation": "Durkheim focused on social facts — phenomena external to the individual that constrain them."
                        },
                        {
                            "question": "Which sociologist is associated with Verstehen (interpretive understanding)?",
                            "options": ["Karl Marx", "Émile Durkheim", "Max Weber", "Auguste Comte"],
                            "correct": 2,
                            "explanation": "Weber is associated with Verstehen — interpretive understanding of subjective meanings."
                        },
                        {
                            "question": "Which sociologist saw society as an arena of class struggle?",
                            "options": ["Karl Marx", "Émile Durkheim", "Max Weber", "Talcott Parsons"],
                            "correct": 0,
                            "explanation": "Marx saw society as an arena of class struggle between the bourgeoisie and proletariat."
                        }
                    ]
                }
            }
        }
    }

    @classmethod
    def get_block_names(cls) -> List[str]:
        return list(cls.BLOCKS.keys())

    @classmethod
    def get_block_name(cls, block_id: str) -> str:
        return cls.BLOCKS[block_id]["name"]

    @classmethod
    def get_unit_names(cls, block_id: str) -> Dict[str, str]:
        return {unit_id: cls.BLOCKS[block_id]["units"][unit_id]["name"]
                for unit_id in cls.BLOCKS[block_id]["units"]}

    @classmethod
    def get_unit_content(cls, block_id: str, unit_id: str) -> str:
        return cls.BLOCKS[block_id]["units"][unit_id]["content"]

    @classmethod
    def get_unit_examples(cls, block_id: str, unit_id: str) -> Optional[str]:
        return cls.BLOCKS[block_id]["units"][unit_id].get("examples")

    @classmethod
    def get_unit_questions(cls, block_id: str, unit_id: str) -> List[Dict]:
        return cls.BLOCKS[block_id]["units"][unit_id].get("questions", [])

# ===== КЛАВИАТУРЫ =====
def get_main_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for block_id, block_data in Content.BLOCKS.items():
        builder.button(text=block_data["name"], callback_data=f"block_{block_id}")
    builder.button(text="📋 About This Bot", callback_data="about")
    builder.button(text="ℹ️ Help", callback_data="help")
    builder.adjust(1)
    return builder.as_markup()

def get_block_menu(block_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    units = Content.get_unit_names(block_id)
    for unit_id, unit_name in units.items():
        builder.button(text=unit_name, callback_data=f"unit_{block_id}_{unit_id}")
    builder.button(text="⬅️ Back to Menu", callback_data="menu")
    builder.adjust(1)
    return builder.as_markup()

def get_unit_navigation(block_id: str, unit_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    units = list(Content.get_unit_names(block_id).keys())
    current_index = units.index(unit_id) if unit_id in units else -1
    builder.button(text="❓ Questions", callback_data=f"questions_{block_id}_{unit_id}")
    if current_index < len(units) - 1:
        next_unit = units[current_index + 1]
        builder.button(text="➡️ Next Unit", callback_data=f"unit_{block_id}_{next_unit}")
    builder.button(text="📋 Block Menu", callback_data=f"block_{block_id}")
    builder.button(text="🏠 Main Menu", callback_data="menu")
    builder.adjust(2)
    return builder.as_markup()

def get_question_keyboard(block_id: str, unit_id: str, question_index: int, total_questions: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for i in range(4):
        builder.button(text=f"{chr(65 + i)}", callback_data=f"answer_{block_id}_{unit_id}_{question_index}_{i}")
    if question_index < total_questions - 1:
        builder.button(text="⏭️ Next Question", callback_data=f"next_q_{block_id}_{unit_id}_{question_index + 1}")
    else:
        builder.button(text="✅ Done — Back to Unit", callback_data=f"unit_{block_id}_{unit_id}")
    builder.button(text="⬅️ Back to Unit", callback_data=f"unit_{block_id}_{unit_id}")
    builder.adjust(4, 1)
    return builder.as_markup()

# ===== ОБРАБОТЧИКИ =====
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    welcome_text = """👋 Welcome to the **Sociology ICEF Guide**!

This bot will help you learn the foundations of sociology through:
• 📖 Clear definitions
• 💡 Real-life examples
• 📊 Comparative tables
• ❓ Interactive questions

Choose a block below to begin:

**🏛️ BLOCK 1:** Foundations — What is Sociology?
**🔬 BLOCK 2:** What and How Do We Study? — Methodology
**👨‍🏫 BLOCK 3:** Founding Fathers of Sociology

Use the buttons to navigate. Good luck with your studies! 📚"""
    await message.answer(welcome_text, reply_markup=get_main_menu())

@dp.message(Command("menu"))
async def cmd_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("📋 **Main Menu** — Choose a block:", reply_markup=get_main_menu())

@dp.callback_query(F.data == "menu")
async def callback_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("📋 **Main Menu** — Choose a block:", reply_markup=get_main_menu())
    await callback.answer()

@dp.callback_query(F.data == "about")
async def callback_about(callback: CallbackQuery):
    about_text = """📚 **About This Bot**

This educational bot was created as a project for the ICEF sociology course at HSE University.

**Author:** Anna Pavlova
**Supervisor:** Elena Danilova

**Content includes:**
• 3 main blocks
• 13 units
• Definitions, examples, tables
• Interactive questions with feedback

**Sources:**
• Mills, C. W. (1959). The Sociological Imagination.
• Durkheim, E. (1893). The Division of Labor in Society.
• Marx, K. — various works.
• Weber, M. — various works.
• Berger, P. L. & Luckmann, T. (1966). The Social Construction of Reality.

🔗 **Telegram Channel:** @sociologyICEF"""
    await callback.message.edit_text(about_text, reply_markup=get_main_menu())
    await callback.answer()

@dp.callback_query(F.data == "help")
async def callback_help(callback: CallbackQuery):
    help_text = """ℹ️ **Help & Navigation**

**How to use this bot:**

• Click on a **block** to see its units
• Click on a **unit** to view the content
• Use **Questions** to test your knowledge
• Use navigation buttons to move around

**Commands:**
• /start — Start the bot
• /menu — Go to main menu

**Buttons:**
• 📋 Block Menu — Go back to unit list
• 🏠 Main Menu — Go to home screen
• ❓ Questions — Start interactive questions
• ⬅️ Back to Unit — Return to content

**Tips:**
• Read the content first, then try the questions
• Each question has an explanation for the correct answer
• You can go back and review any unit at any time"""
    await callback.message.edit_text(help_text, reply_markup=get_main_menu())
    await callback.answer()

@dp.callback_query(F.data.startswith("block_"))
async def callback_block(callback: CallbackQuery, state: FSMContext):
    block_id = callback.data.replace("block_", "")
    if block_id not in Content.BLOCKS:
        await callback.answer("Block not found")
        return
    await state.clear()
    block_name = Content.get_block_name(block_id)
    text = f"**{block_name}**\n\n{Content.BLOCKS[block_id]['description']}\n\n📖 **Choose a unit:**"
    await callback.message.edit_text(text, reply_markup=get_block_menu(block_id))
    await callback.answer()

@dp.callback_query(F.data.startswith("unit_"))
async def callback_unit(callback: CallbackQuery, state: FSMContext):
    parts = callback.data.split("_")
    if len(parts) < 3:
        await callback.answer("Invalid unit")
        return
    block_id = parts[1]
    unit_id = "_".join(parts[2:])
    if block_id not in Content.BLOCKS or unit_id not in Content.BLOCKS[block_id]["units"]:
        await callback.answer("Unit not found")
        return
    await state.update_data(current_block=block_id, current_unit=unit_id)
    await state.set_state(UserState.viewing_unit)

    unit_name = Content.get_unit_names(block_id)[unit_id]
    content = Content.get_unit_content(block_id, unit_id)
    examples = Content.get_unit_examples(block_id, unit_id)

    text = f"**{unit_name}**\n\n" + content
    if examples:
        text += "\n\n" + examples
    text += "\n\n---\n*Use the buttons below to continue.*"
    await callback.message.edit_text(text, reply_markup=get_unit_navigation(block_id, unit_id))
    await callback.answer()

@dp.callback_query(F.data.startswith("questions_"))
async def callback_questions(callback: CallbackQuery, state: FSMContext):
    parts = callback.data.split("_")
    block_id = parts[1]
    unit_id = "_".join(parts[2:])
    questions = Content.get_unit_questions(block_id, unit_id)
    if not questions:
        await callback.answer("No questions available")
        return
    await state.update_data(
        current_block=block_id,
        current_unit=unit_id,
        question_index=0,
        total_questions=len(questions),
        questions=questions
    )
    await state.set_state(UserState.answering_question)
    await display_question(callback.message, callback, block_id, unit_id, 0, questions)

async def display_question(message, callback, block_id, unit_id, index, questions):
    if index >= len(questions):
        text = "✅ **You've completed all the questions for this unit!**\n\nGreat job! You can review the content or move to the next unit."
        if callback:
            await callback.message.edit_text(text, reply_markup=get_unit_navigation(block_id, unit_id))
            await callback.answer()
        else:
            await message.answer(text, reply_markup=get_unit_navigation(block_id, unit_id))
        return
    q = questions[index]
    text = f"❓ **Question {index + 1} of {len(questions)}**\n\n{q['question']}\n\n**Choose an answer:**"
    for i, opt in enumerate(q["options"]):
        text += f"\n{chr(65 + i)}) {opt}"
    keyboard = get_question_keyboard(block_id, unit_id, index, len(questions))
    if callback:
        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer()
    else:
        await message.answer(text, reply_markup=keyboard)

@dp.callback_query(F.data.startswith("answer_"))
async def callback_answer(callback: CallbackQuery, state: FSMContext):
    parts = callback.data.split("_")
    block_id = parts[1]
    unit_id = "_".join(parts[2:-2])
    q_index = int(parts[-2])
    selected = int(parts[-1])
    data = await state.get_data()
    questions = data.get("questions", [])
    if q_index >= len(questions):
        await callback.answer("Invalid question")
        return
    q = questions[q_index]
    is_correct = (selected == q["correct"])
    feedback_text = "✅ **Correct!** " if is_correct else "❌ **Incorrect.** "
    feedback_text += q["explanation"] + "\n\n*Select another option or continue.*"
    lines = callback.message.text.split("\n")
    new_lines = [line for line in lines if not line.startswith(("Choose", "A)", "B)", "C)", "D)"))]
    new_text = "\n".join(new_lines) + "\n\n" + feedback_text
    builder = InlineKeyboardBuilder()
    if q_index < len(questions) - 1:
        builder.button(text="⏭️ Next Question", callback_data=f"next_q_{block_id}_{unit_id}_{q_index + 1}")
    else:
        builder.button(text="✅ Done — Back to Unit", callback_data=f"unit_{block_id}_{unit_id}")
    builder.button(text="⬅️ Back to Unit", callback_data=f"unit_{block_id}_{unit_id}")
    builder.adjust(1)
    await callback.message.edit_text(new_text, reply_markup=builder.as_markup())
    await callback.answer()

@dp.callback_query(F.data.startswith("next_q_"))
async def callback_next_question(callback: CallbackQuery, state: FSMContext):
    parts = callback.data.split("_")
    block_id = parts[2]
    unit_id = "_".join(parts[3:-1])
    q_index = int(parts[-1])
    data = await state.get_data()
    questions = data.get("questions", [])
    await state.update_data(question_index=q_index)
    await display_question(callback.message, callback, block_id, unit_id, q_index, questions)

@dp.callback_query(F.data == "back_to_unit")
async def callback_back_to_unit(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    block_id = data.get("current_block")
    unit_id = data.get("current_unit")
    if block_id and unit_id:
        await state.set_state(UserState.viewing_unit)
        await callback_unit_from_data(callback, block_id, unit_id)
    else:
        await callback.message.edit_text("Returning to menu...", reply_markup=get_main_menu())
        await callback.answer()

@dp.callback_query(F.data == "continue_questions")
async def callback_continue_questions(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    block_id = data.get("current_block")
    unit_id = data.get("current_unit")
    q_index = data.get("question_index", 0)
    questions = data.get("questions", [])
    if block_id and unit_id and questions:
        await display_question(callback.message, callback, block_id, unit_id, q_index, questions)
    else:
        await callback.answer("No questions available")

async def callback_unit_from_data(callback: CallbackQuery, block_id: str, unit_id: str):
    unit_name = Content.get_unit_names(block_id)[unit_id]
    content = Content.get_unit_content(block_id, unit_id)
    examples = Content.get_unit_examples(block_id, unit_id)
    text = f"**{unit_name}**\n\n" + content
    if examples:
        text += "\n\n" + examples
    text += "\n\n---\n*Use the buttons below to continue.*"
    await callback.message.edit_text(text, reply_markup=get_unit_navigation(block_id, unit_id))
    await callback.answer()

# ===== ЗАПУСК =====
async def main():
    logger.info("Starting bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())