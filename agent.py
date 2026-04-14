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
            max_tokens=500   # ✅ safe limit
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


# ---------------------------
# MAIN AGENT (LONG OUTPUT)
# ---------------------------
def run_agent(problem):

    steps = []

    # STEP 1: Strategy
    strategy = call("Give a short solving strategy: " + problem)
    steps.append(("🧠 Strategy", strategy))

    # STEP 2: Initial Answer
    solution = call(f"""
    Solve this in structured format:
    - Steps
    - Explanation
    - Simple language

    Problem: {problem}
    """)
    steps.append(("⚙️ Initial Solution", solution))

    # STEP 3: Expand Answer (🔥 KEY UPGRADE)
    expanded = call(f"""
    Expand this answer with:
    - More explanation
    - Examples
    - Better clarity
    - Add headings

    Answer:
    {solution}
    """)
    steps.append(("📈 Expanded Solution", expanded))

    # STEP 4: Final Polished Answer
    final = call(f"""
    Combine and refine into final answer:
    - Clean formatting
    - Bullet points
    - Easy to understand

    {expanded}
    """)
    steps.append(("✅ Final Answer", final))

    return steps, final