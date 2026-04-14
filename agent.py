from groq import Groq
import os

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------------------
# CALL FUNCTION
# ---------------------------
def call(prompt):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


# ---------------------------
# MAIN AGENT
# ---------------------------
def run_agent(problem, history=""):

    steps = []

    # STEP 1: Strategy Selection
    strategy = call(f"""
    Choose the best strategy to solve this problem:

    {problem}

    Options:
    - Logical reasoning
    - Step-by-step breakdown
    - Quick heuristic

    Answer only the strategy name.
    """)
    steps.append(("🧠 Strategy", strategy))

    # STEP 2: Initial Solution
    solution = call(f"""
    Solve this problem clearly step-by-step:

    {problem}

    Ensure the answer is complete.
    """)
    steps.append(("⚙️ Initial Solution", solution))

    # STEP 3: Iterative Improvement Loop
    for i in range(2):

        evaluation = call(f"""
        Check this solution:

        {solution}

        Is it correct and complete?

        Answer ONLY:
        GOOD or IMPROVE
        """)
        steps.append((f"🔍 Evaluation {i+1}", evaluation))

        if "good" in evaluation.lower():
            break

        solution = call(f"""
        Improve this solution and fix any missing parts:

        {solution}
        """)
        steps.append((f"✨ Improvement {i+1}", solution))

    # FINAL
    steps.append(("✅ Final Answer", solution))

    return steps, solution