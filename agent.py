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

    # ---------------------------
    # STRATEGY
    # ---------------------------
    strategy = call(f"""
    Briefly explain the best approach for answering this query.

    IMPORTANT:
    - Respond in plain English only
    - Never use HTML
    - Never use code
    - Keep answer short

    Query:
    {problem}
    """, model_name)

    steps.append(("🧠 Strategy", strategy))

    # ---------------------------
    # INITIAL RESPONSE
    # ---------------------------
    answer = call(f"""
    Answer this query naturally and intelligently.

    IMPORTANT:
    - NEVER use HTML
    - NEVER use CSS
    - NEVER use code blocks
    - NEVER generate tags like <div>
    - NEVER write programming syntax
    - Respond naturally like ChatGPT
    - Keep formatting clean and readable
    - Use bullets only if needed
    - If question is simple, answer normally
    - If question is complex, structure properly

    Query:
    {problem}
    """, model_name)

    steps.append(("⚙️ Initial Response", answer))

    # ---------------------------
    # EVALUATION
    # ---------------------------
    evaluation = call(f"""
    Evaluate this response briefly.

    IMPORTANT:
    - Plain English only
    - No HTML
    - No code

    Response:
    {answer}

    Mention:
    - What is good
    - What can improve
    """, model_name)

    steps.append(("🔍 Evaluation", evaluation))

    # ---------------------------
    # IMPROVED RESPONSE
    # ---------------------------
    improved = call(f"""
    Improve this response in normal English.

    IMPORTANT:
    - NEVER use HTML
    - NEVER use code
    - NEVER generate tags
    - Keep response human readable
    - Write naturally like ChatGPT
    - Avoid unnecessary step-by-step formatting
    - Keep answer clean and professional

    Original Response:
    {answer}

    Feedback:
    {evaluation}

    Query:
    {problem}
    """, model_name)

    steps.append(("✨ Improved Response", improved))

    return steps, improved