from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------------------
# SAFE CALL FUNCTION
# ---------------------------
def call(prompt):
    response = client.chat.completions.create(
        model="llama3-8b-8192",   # 🔥 smaller + stable model
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message.content


# ---------------------------
# FINAL AGENT (SAFE VERSION)
# ---------------------------
def run_agent(problem):

    steps = []

    # STEP 1: Strategy
    strategy = call(f"Best way to solve: {problem}. Answer in 3 words.")
    steps.append(("🧠 Strategy", strategy))

    # STEP 2: Solution
    solution = call(f"Solve step by step: {problem}")
    steps.append(("⚙️ Initial Solution", solution))

    # STEP 3: Evaluation
    evaluation = call(f"Is this correct? Answer YES or NO:\n{solution}")
    steps.append(("🔍 Evaluation", evaluation))

    # STEP 4: Improve if needed
    if "no" in evaluation.lower():
        solution = call(f"Improve this answer:\n{solution}")
        steps.append(("✨ Improved Solution", solution))

    # FINAL
    steps.append(("✅ Final Answer", solution))

    return steps, solution