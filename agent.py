from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------------------
# CALL FUNCTION
# ---------------------------
def call(prompt, model_name):

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt.strip()
                }
            ],
            temperature=0.7,
            max_tokens=5000
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"


# ---------------------------
# MAIN AGENT
# ---------------------------
def run_agent(problem, model_name):

    steps = []

    # Strategy
    strategy = call(f"""
    Give the best strategy in 1 line.

    Problem:
    {problem}
    """, model_name)

    steps.append(("🧠 Strategy", strategy))

    # Initial Solution
    solution = call(f"""
    Solve this clearly:
    - Step-by-step
    - Clear explanation
    - Proper formatting

    Problem:
    {problem}
    """, model_name)

    steps.append(("⚙️ Initial Solution", solution))

    # Evaluation
    evaluation = call(f"""
    Evaluate this solution carefully.

    Solution:
    {solution}

    Tell:
    - What is correct
    - What can improve
    """, model_name)

    steps.append(("🔍 Evaluation", evaluation))

    # Improved Solution
    improved = call(f"""
    Improve this solution.

    Original:
    {solution}

    Feedback:
    {evaluation}

    Make it:
    - More detailed
    - Better formatted
    - Easier to understand
    """, model_name)

    steps.append(("✨ Improved Solution", improved))

    return steps, improved