from app.retriever import search
from app.llm import ask_llm


# ------------------------------------
# Off-topic keywords
# ------------------------------------
OFF_TOPIC = [
    "weather",
    "cricket",
    "ipl",
    "movie",
    "recipe",
    "bitcoin",
    "president",
    "prime minister",
    "football",
    "stock market",
    "politics",
]


# ------------------------------------
# Prompt Injection keywords
# ------------------------------------
INJECTION = [
    "ignore previous",
    "ignore all instructions",
    "forget instructions",
    "system prompt",
    "developer prompt",
]


# ------------------------------------
# Compare Assessments
# ------------------------------------
def compare_assessments(query):
    results = search(query, top_k=2)

    if len(results) < 2:
        return {
            "reply": "I couldn't find enough SHL assessments to compare.",
            "recommendations": [],
            "end_of_conversation": False,
        }

    first = results[0]
    second = results[1]

    prompt = f"""
You are an SHL Assessment Assistant.

Compare ONLY these two assessments.

Assessment 1

Name: {first["name"]}
Description: {first["description"]}
Categories: {", ".join(first.get("keys", []))}
Duration: {first.get("duration", "Not Available")}
Job Levels: {", ".join(first.get("job_levels", []))}

Assessment 2

Name: {second["name"]}
Description: {second["description"]}
Categories: {", ".join(second.get("keys", []))}
Duration: {second.get("duration", "Not Available")}
Job Levels: {", ".join(second.get("job_levels", []))}

Compare:

- Purpose
- Skills Measured
- Job Levels
- Duration

Do not invent information.
Keep answer under 150 words.
"""

    reply = ask_llm(prompt)

    return {
        "reply": reply,
        "recommendations": [],
        "end_of_conversation": True,
    }


# ------------------------------------
# Main Chat Logic
# ------------------------------------
def generate_response(messages):

    # ------------------------------------
    # Latest user message
    # ------------------------------------
    user_message = ""

    for msg in reversed(messages):
        if msg["role"] == "user":
            user_message = msg["content"]
            break

    text = user_message.lower().strip()

    # ------------------------------------
    # Build conversation query
    # Uses all previous user messages
    # ------------------------------------
    conversation_query = ""

    for msg in messages:
        if msg["role"] == "user":
            conversation_query += msg["content"] + " "

    conversation_query = conversation_query.strip()

    # ------------------------------------
    # Off-topic Detection
    # ------------------------------------
    for word in OFF_TOPIC:
        if word in text:
            return {
                "reply": "Sorry, I can only help with SHL assessment recommendations.",
                "recommendations": [],
                "end_of_conversation": False,
            }

    # ------------------------------------
    # Prompt Injection Detection
    # ------------------------------------
    for word in INJECTION:
        if word in text:
            return {
                "reply": "Sorry, I can only answer questions related to SHL assessments.",
                "recommendations": [],
                "end_of_conversation": False,
            }

    # ------------------------------------
    # Better Clarifying Questions
    # ------------------------------------
    vague_words = [
        "assessment",
        "test",
        "need assessment",
        "need test",
        "i need assessment",
        "i need an assessment",
        "recommend assessment",
        "recommend test",
    ]

    # Count user messages
    user_messages = [
        msg["content"] for msg in messages if msg["role"] == "user"
    ]

    # Ask clarification only for the first vague request
    if (
        len(user_messages) == 1
        and ("assessment" in text or "test" in text)
        and not any(
            word in text
            for word in [
                "year",
                "years",
                "fresher",
                "entry",
                "junior",
                "mid",
                "senior",
                "experienced",
            ]
        )
    ):
        return {
            "reply": (
                "What experience level are you hiring for? "
                "(Fresher, Entry, Mid, Senior or number of years)"
            ),
            "recommendations": [],
            "end_of_conversation": False,
        }

    # ------------------------------------
    # Compare Assessments
    # ------------------------------------
    if (
        "compare" in text
        or "vs" in text
        or "versus" in text
        or "difference" in text
    ):
        return compare_assessments(user_message)

    # ------------------------------------
    # Search Catalog
    # Uses conversation history
    # ------------------------------------
    results = search(conversation_query, top_k=5)

    recommendations = []
    catalog_text = ""

    for item in results:
        recommendations.append(
            {
                "name": item["name"],
                "url": item["link"],
                "test_type": ", ".join(item.get("keys", [])),
            }
        )

        catalog_text += f"""
    Name: {item["name"]}

    Description:
    {item["description"]}

    Categories:
    {", ".join(item.get("keys", []))}

    Job Levels:
    {", ".join(item.get("job_levels", []))}

    Duration:
    {item.get("duration", "Not Available")}

------------------------------------------------
"""

    # ------------------------------------
    # Gemini Prompt
    # ------------------------------------
    prompt = f"""
You are an SHL Assessment Recommendation Assistant.

Conversation:

{conversation_query}

Available SHL Assessments:

{catalog_text}

Instructions:

1. Recommend ONLY assessments provided above.

2. Explain why they match the user's hiring needs.

3. Never invent assessment names.

4. Never recommend assessments outside the catalog.

5. If multiple assessments are suitable,
briefly explain the differences.

6. Keep response under 150 words.
"""

    reply = ask_llm(prompt)

    return {
        "reply": reply,
        "recommendations": recommendations,
        "end_of_conversation": True,
    }