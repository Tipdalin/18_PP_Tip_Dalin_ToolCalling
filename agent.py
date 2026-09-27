import json
from ollama import chat
from harness import Harness

#Model name 
MODEL = "llama3.2:3b"

# Tools that the LLM can use
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_phone",
            "description": "Search phones by name or brand.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Phone name or brand",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_stock",
            "description": "Check the stock of a phone.",
            "parameters": {
                "type": "object",
                "properties": {
                    "phone_id": {
                        "type": "integer",
                        "description": "Phone ID",
                    }
                },
                "required": ["phone_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_phone",
            "description": "Delete a phone. Admin only.",
            "parameters": {
                "type": "object",
                "properties": {
                    "phone_id": {
                        "type": "integer",
                        "description": "Phone ID",
                    }
                },
                "required": ["phone_id"],
            },
        },
    },
]

def run_agent(user_request, role="customer"):

    harness = Harness(role)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a phone shopping assistant. "
                "Use tools when necessary. "
                "Do not invent information."
            ),
        },
        {
            "role": "user",
            "content": user_request,
        },
    ]

    # Agent loop
    for _ in range(5):

        response = chat(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
        )

        message = response["message"]
        messages.append(message)

        if not message.get("tool_calls"):
            return message["content"]

        for call in message["tool_calls"]:

            tool_name = call["function"]["name"]
            arguments = call["function"]["arguments"]

            print(f"\n[Tool] {tool_name}")
            print(f"[Arguments] {arguments}")

            result = harness.execute_tool(
                tool_name,
                arguments,
            )

            print(f"[Result] {result}")

            messages.append(
                {
                    "role": "tool",
                    "content": json.dumps(result),
                }
            )

    return "Agent stopped: maximum tool calls reached."

