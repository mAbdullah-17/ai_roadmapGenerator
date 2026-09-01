import streamlit as st
from groq import Groq


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Learning Roadmap Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main container */
    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Header */
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #666;
        margin-bottom: 35px;
    }

    /* Section headings */
    .section-title {
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 15px;
    }

    /* Info box */
    .info-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #f5f7fa;
        margin-top: 10px;
        margin-bottom: 15px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #777;
        margin-top: 40px;
        padding: 20px;
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">AI Learning Roadmap Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        Turn your learning goal into a personalized,
        practical roadmap with AI.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# GROQ CONFIGURATION
# ============================================================

try:

    groq_api_key = st.secrets["GROQ_API_KEY"]

except Exception:

    st.error(
        """
        **Groq API key not found.**

        Please add `GROQ_API_KEY` to your Streamlit Secrets.
        """
    )

    st.stop()


client = Groq(
    api_key=groq_api_key
)

MODEL_NAME = "openai/gpt-oss-120b"


# ============================================================
# LEARNING TIME DATA
# ============================================================

DAILY_HOURS = {
    "30 minutes": 0.5,
    "1 hour": 1,
    "2 hours": 2,
    "3 hours": 3,
    "4 hours": 4
}


DURATION_DAYS = {
    "1 Month": 30,
    "2 Months": 60,
    "3 Months": 90,
    "6 Months": 180,
    "1 Year": 365
}


# ============================================================
# CALCULATE AVAILABLE LEARNING HOURS
# ============================================================

def calculate_learning_hours(duration, daily_time):

    daily_hours = DAILY_HOURS.get(
        daily_time,
        1
    )

    days = DURATION_DAYS.get(
        duration,
        30
    )

    return daily_hours * days


# ============================================================
# GENERATE ROADMAP
# ============================================================

def generate_roadmap(
    domain,
    level,
    duration,
    daily_time,
    goal
):

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not domain or not domain.strip():

        return None, "Please enter a learning domain."

    if not level:
        level = "Beginner"

    if not duration:
        duration = "3 Months"

    if not daily_time:
        daily_time = "1 hour"

    if not goal or not goal.strip():

        goal = "Become proficient in this domain."

    # Limit input size

    domain = domain.strip()[:100]

    goal = goal.strip()[:300]


    # --------------------------------------------------------
    # CALCULATE AVAILABLE HOURS
    # --------------------------------------------------------

    total_hours = calculate_learning_hours(
        duration,
        daily_time
    )


    # --------------------------------------------------------
    # AI PROMPT
    # --------------------------------------------------------

    prompt = f"""
Create a personalized learning roadmap for this learner.

LEARNER:
Domain: {domain}
Current level: {level}
Learning duration: {duration}
Daily study time: {daily_time}
Approximate total study time: {total_hours} hours
Goal: {goal}

INSTRUCTIONS:
- Tailor the roadmap specifically to the learner's level, goal, and available time.
- Make it realistic and achievable within the available study hours.
- Start at the learner's current level.
- Do not repeat basic material unnecessarily for intermediate or advanced learners.
- Prioritize the most important skills instead of trying to cover everything.
- Progress logically from easier concepts to more advanced concepts.
- Divide the roadmap into clear phases and weeks.
- For every week, include key topics and practical tasks.
- Include progressively harder projects.
- Include one final project related to the learner's goal.
- Include clear milestones.
- Include recommended types of learning resources.
- Do not invent URLs.
- Keep the roadmap concise and practical.
- Do not overload the learner.

OUTPUT FORMAT:

# Personalized Learning Roadmap

## Learner Profile

Include:
- Domain
- Current Level
- Duration
- Daily Study Time
- Estimated Total Study Hours
- Goal

## Roadmap Overview

Briefly explain the learning strategy.

## Phase 1

Explain the main skills and concepts.

### Week 1

**Topics:**
- ...

**Practice:**
- ...

**Milestone:**
- ...

Continue with appropriate weeks.

## Phase 2

Continue the learning progression.

### Week X

**Topics:**
- ...

**Practice:**
- ...

**Milestone:**
- ...

Create additional phases only when justified by the learning duration.

## Projects

List 2–4 practical projects appropriate for the learner's level.

## Final Project

Provide:
- Project idea
- Main features
- Skills required
- Expected outcome

## Recommended Resource Types

Suggest useful resource categories such as:
- Official documentation
- Courses
- Books
- Tutorials
- Practice platforms

Do not provide fabricated URLs.

## Milestones

List the major milestones.

## Skills After Completion

Explain what the learner should realistically be able to do.

## Next Steps

Recommend what the learner should learn or do after finishing this roadmap.
"""


    # --------------------------------------------------------
    # GROQ API CALL
    # --------------------------------------------------------

    try:

        response = client.chat.completions.create(

            model=MODEL_NAME,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert curriculum designer "
                        "who creates realistic, personalized "
                        "learning roadmaps."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.7,

            max_tokens=5000
        )

        roadmap = response.choices[0].message.content

        return roadmap, None


    except Exception as e:

        print("Groq Error:", e)

        return None, (
            "Something went wrong while communicating "
            "with the AI. Please try again."
        )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "## Create Your Roadmap"
    )

    st.markdown(
        """
        Enter your learning information below.

        The AI will create a personalized roadmap based on
        your current level, available time, and goal.
        """
    )

    st.divider()


    # --------------------------------------------------------
    # LEARNING DOMAIN
    # --------------------------------------------------------

    domain = st.text_input(
        "Learning Domain",
        placeholder="e.g. Python, Machine Learning"
    )


    # --------------------------------------------------------
    # SKILL LEVEL
    # --------------------------------------------------------

    level = st.selectbox(
        "Current Skill Level",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )


    # --------------------------------------------------------
    # DURATION
    # --------------------------------------------------------

    duration = st.selectbox(
        "Learning Duration",
        [
            "1 Month",
            "2 Months",
            "3 Months",
            "6 Months",
            "1 Year"
        ],
        index=2
    )


    # --------------------------------------------------------
    # DAILY TIME
    # --------------------------------------------------------

    daily_time = st.selectbox(
        "Daily Learning Time",
        [
            "30 minutes",
            "1 hour",
            "2 hours",
            "3 hours",
            "4 hours"
        ],
        index=1
    )


    # --------------------------------------------------------
    # GOAL
    # --------------------------------------------------------

    goal = st.text_area(
        "Learning Goal",
        placeholder=(
            "Example: I want to become a Python developer "
            "and build real-world projects."
        ),
        height=120
    )


    st.divider()


    # --------------------------------------------------------
    # BUTTONS
    # --------------------------------------------------------

    generate_button = st.button(
        "Generate My Roadmap",
        type="primary",
        use_container_width=True
    )


    reset_button = st.button(
        "Reset",
        use_container_width=True
    )


# ============================================================
# RESET
# ============================================================

if reset_button:

    st.rerun()


# ============================================================
# MAIN CONTENT
# ============================================================

if not generate_button:

    # --------------------------------------------------------
    # WELCOME SCREEN
    # --------------------------------------------------------

    st.markdown(
        """
        ## Start Your Learning Journey

        Enter your information in the sidebar and click
        **Generate My Roadmap**.

        Your roadmap will include:
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            """
            **Learning Phases**

            A structured progression from your current level
            toward your goal.
            """
        )

    with col2:

        st.info(
            """
            **Weekly Plan**

            Topics, practice tasks, and milestones for each
            stage.
            """
        )

    with col3:

        st.info(
            """
            **Projects**

            Practical projects that gradually increase in
            difficulty.
            """
        )


# ============================================================
# GENERATE ROADMAP
# ============================================================

if generate_button:

    with st.spinner(
        "Creating your personalized learning roadmap..."
    ):

        roadmap, error = generate_roadmap(
            domain,
            level,
            duration,
            daily_time,
            goal
        )


    if error:

        st.error(error)

    else:

        # ----------------------------------------------------
        # SUMMARY
        # ----------------------------------------------------

        st.success(
            "Your personalized roadmap has been generated!"
        )

        total_hours = calculate_learning_hours(
            duration,
            daily_time
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Level",
                level
            )

        with col2:
            st.metric(
                "Duration",
                duration
            )

        with col3:
            st.metric(
                "Daily Time",
                daily_time
            )

        with col4:
            st.metric(
                "Total Hours",
                f"{total_hours:g}"
            )


        st.divider()


        # ----------------------------------------------------
        # ROADMAP
        # ----------------------------------------------------

        st.markdown(
            "## Your Personalized Roadmap"
        )

        st.markdown(
            roadmap
        )


        # ----------------------------------------------------
        # DOWNLOAD
        # ----------------------------------------------------

        st.divider()

        st.markdown(
            "### Save Your Roadmap"
        )

        st.download_button(
            label="Download Roadmap",
            data=roadmap,
            file_name=(
                f"{domain.replace(' ', '_')}_"
                f"Learning_Roadmap.md"
            ),
            mime="text/markdown"
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        AI Learning Roadmap Generator
        • Powered by Groq
    </div>
    """,
    unsafe_allow_html=True
)
