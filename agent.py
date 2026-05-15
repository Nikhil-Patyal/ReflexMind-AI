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
            max_tokens=700
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
    Briefly explain the best approach for answering this query.

    Query:
    {problem}
    """, model_name)

    steps.append(("🧠 Strategy", strategy))

    # Initial Answer
    answer = call(f"""
    Answer this query naturally and intelligently.

    IMPORTANT:
    - Do NOT always use step-by-step format
    - If the question is simple, answer normally
    - If the question is complex, use structure where needed
    - Keep the response clean and readable
    - Explain clearly like ChatGPT

    Query:
    {problem}
    """, model_name)

    steps.append(("⚙️ Initial Response", answer))

    # Evaluation
    evaluation = call(f"""
    Evaluate this response briefly.

    Response:
    {answer}

    Mention:
    - What is good
    - What can improve
    """, model_name)

    steps.append(("🔍 Evaluation", evaluation))

    # Improved Answer
    improved = call(f"""
    Improve this response.

    Original Response:
    {answer}

    Feedback:
    {evaluation}

    IMPORTANT:
    - Keep the response natural
    - Avoid unnecessary steps
    - Improve clarity and quality
    - Format only where needed

    Query:
    {problem}
    """, model_name)

    steps.append(("✨ Improved Response", improved))

    return steps, improved