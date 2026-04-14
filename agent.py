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
            temperature=0.7,
            max_tokens=500   # safe limit
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


# ---------------------------
# MAIN AGENT (FULL OUTPUT)
# ---------------------------
def run_agent(problem):

    steps = []

    # STEP 1: Strategy
    strategy = call("Give best strategy in 1 line: " + problem)
    steps.append(("🧠 Strategy", strategy))

    # STEP 2: Initial Answer
    solution = call(f"""
    Solve this problem with:
    - Step-by-step explanation
    - Clear concepts
    - Simple language

    Problem: {problem}
    """)
    steps.append(("⚙️ Initial Solution", solution))

    # STEP 3: Expand (MORE DETAILS)
    expanded = call(f"""
    Expand this answer:
    - Add detailed explanation
    - Add examples
    - Explain each step clearly

    {solution}
    """)
    steps.append(("📈 Expanded Explanation", expanded))

    # STEP 4: Deep Expand (VERY LONG)
    deep = call(f"""
    Make this answer very detailed:
    - Add headings
    - Add bullet points
    - Add real-life examples
    - Add advantages / disadvantages

    {expanded}
    """)
    steps.append(("🧩 Detailed Version", deep))

    # STEP 5: Final Formatting
    final = call(f"""
    Format this into clean notes:
    - Use headings
    - Use bullet points
    - Make it easy to read
    - Make it look like exam answer

    {deep}
    """)
    steps.append(("✅ Final Answer", final))

    return steps, final