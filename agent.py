from groq import Groq
import os

# Initialize client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------------------
# CALL GROQ
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

    context = f"{history}\nProblem: {problem}"

    steps = []

    # Strategy
    strategy = call(f"Choose best strategy for:\n{context}")
    steps.append(("🧠 Strategy", strategy))

    # Initial solution
    solution = call(f"""
    Solve this problem clearly:

    {context}

    - Use steps
    - Give complete answer
    """)
    steps.append(("⚙️ Initial Solution", solution))

    # Iteration
    for i in range(2):

        evaluation = call(f"""
        Evaluate this solution:

        {solution}

        Answer only: GOOD or IMPROVE
        """)
        steps.append((f"🔍 Evaluation {i+1}", evaluation))

        if "good" in evaluation.lower():
            break

        solution = call(f"""
        Improve this solution:

        {solution}
        """)
        steps.append((f"✨ Improvement {i+1}", solution))

    steps.append(("✅ Final Answer", solution))

    return steps, solution