from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------------------
# CALL FUNCTION
# ---------------------------
def call(prompt):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt.strip()}
            ],
            temperature=0.6,
            max_tokens=5000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


# ---------------------------
# MAIN AGENT
# ---------------------------
def run_agent(problem):

    steps = []

    # Strategy
    strategy = call(f"""
    Give a short strategy (1 line):
    {problem}
    """)
    steps.append(("🧠 Strategy", strategy))

    # Solution
    solution = call(f"""
    Solve this clearly with:
    - Step-by-step points
    - Short explanations
    - Proper formatting

    Problem: {problem}
    """)
    steps.append(("⚙️ Solution", solution))

    # Evaluation
    evaluation = call(f"""
    Check if this solution is complete:

    {solution}

    Answer: COMPLETE or IMPROVE
    """)
    steps.append(("🔍 Evaluation", evaluation))

    # Improve
    if "improve" in evaluation.lower():
        solution = call(f"""
        Improve and complete this answer:

        {solution}
        """)
        steps.append(("✨ Improved Solution", solution))

    steps.append(("✅ Final Answer", solution))

    return steps, solution