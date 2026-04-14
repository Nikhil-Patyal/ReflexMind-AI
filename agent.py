from groq import Groq
import os

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------------------
# SAFE CALL FUNCTION
# ---------------------------
def call(prompt):
    try:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",   # ✅ stable model
            messages=[
                {"role": "user", "content": prompt.strip()}
            ],
            temperature=0.5,
            max_tokens=150   # ✅ safe limit
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


# ---------------------------
# MAIN AGENT
# ---------------------------
def run_agent(problem):

    steps = []

    # STEP 1: Strategy
    strategy = call("Best strategy to solve: " + problem)
    steps.append(("🧠 Strategy", strategy))

    # STEP 2: Initial Solution
    solution = call("Solve step by step: " + problem)
    steps.append(("⚙️ Initial Solution", solution))

    # STEP 3: Evaluation
    evaluation = call("Is this correct? Answer YES or NO:\n" + solution)
    steps.append(("🔍 Evaluation", evaluation))

    # STEP 4: Improve if needed
    if "no" in evaluation.lower():
        solution = call("Improve this answer:\n" + solution)
        steps.append(("✨ Improved Solution", solution))

    # FINAL
    steps.append(("✅ Final Answer", solution))

    return steps, solution