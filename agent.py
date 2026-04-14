from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------------------
# SAFE CALL FUNCTION
# ---------------------------
def call(prompt):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",   # ✅ FINAL WORKING MODEL
            messages=[
                {"role": "user", "content": prompt.strip()}
            ],
            temperature=0.5,
            max_tokens=120
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


# ---------------------------
# MAIN AGENT
# ---------------------------
def run_agent(problem):

    steps = []

    strategy = call("Best strategy: " + problem)
    steps.append(("🧠 Strategy", strategy))

    solution = call("Solve step by step: " + problem)
    steps.append(("⚙️ Initial Solution", solution))

    evaluation = call("Is this correct? Answer YES or NO:\n" + solution)
    steps.append(("🔍 Evaluation", evaluation))

    if "no" in evaluation.lower():
        solution = call("Improve this answer:\n" + solution)
        steps.append(("✨ Improved Solution", solution))

    steps.append(("✅ Final Answer", solution))

    return steps, solution