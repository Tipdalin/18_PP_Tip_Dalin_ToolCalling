# Phone Shopping Agent

## 1. Project Overview

Phone Shopping Agent is a small agentic application that helps users search for phones and check phone stock.

The agent uses an LLM to:

1. Receive a user's request.
2. Decide whether a tool is needed.
3. Select a tool.
4. Call the tool.
5. Observe the tool result.
6. Decide whether another tool is needed.
7. Return a final answer.

The application also has a basic permission system:

* **Customer** can search phones and check stock.
* **Admin** can search phones, check stock, and delete phones.

---

## 2. Available Tools

The agent has three tools.

### `search_phone(query)`

Searches for phones by phone name or brand.

### `check_stock(phone_id)`

Checks the current stock quantity of a phone.

### `delete_phone(phone_id)`

Deletes a phone from the system.

This tool is only available to the **admin** role.

---

## 3. Permission Rule

The application has two roles:

| Role     | search_phone | check_stock | delete_phone |
| -------- | ------------ | ----------- | ------------ |
| Customer | Yes          | Yes         | No           |
| Admin    | Yes          | Yes         | Yes          |

Permission is checked in `harness.py` before the tool is executed.

For example, if a customer tries to delete a phone:

```text
Customer
   ↓
delete_phone(phone_id=3)
   ↓
Harness
   ↓
Permission Check
   ↓
PERMISSION_DENIED
```

The phone will not be deleted.

---

## 4. Safety

The application includes several basic safety controls.

### Input Validation

Pydantic schemas validate tool inputs.

For example, the phone ID must be greater than 0.

```text
phone_id = -1
```

will be rejected.

### Error Handling

The tools return controlled error messages instead of crashing the application.

Example:

```text
PHONE_NOT_FOUND
```

when a phone does not exist.

Another example:

```text
PERMISSION_DENIED
```

when a customer tries to delete a phone.

### Tool Call Limit

The agent has a maximum of 3 tool calls.

```python
for _ in range(3):
```

This prevents the agent from running forever.

If the limit is reached, the agent stops and returns:

```text
Agent stopped: maximum tool calls reached.
```

---

## 5. Example Run

### Example 1: Search for a Phone

User:

```text
Find Samsung phones
```

Agent:

```text
search_phone(query="Samsung")
```

The tool returns the matching phones, and the agent provides the final answer.

### Example 2: Multi-Step Request

User:

```text
Find a Samsung phone that is currently in stock.
```

Agent:

```text
search_phone(query="Samsung")
        ↓
Search Result
        ↓
check_stock(phone_id=2)
        ↓
Stock Result
        ↓
Final Answer
```

This demonstrates the agent observing the first tool result and deciding to call another tool.

### Example 3: Failed Search

User:

```text
Find Nokia phones
```

The tool returns an empty result.

The agent should respond that no matching phones were found and should not invent a Nokia phone.

### Example 4: Permission Control

Customer:

```text
Delete phone 3
```

Result:

```text
PERMISSION_DENIED
```

Admin:

```text
Delete phone 3
```

The admin is allowed to use the `delete_phone` tool.

---

## 7. Project Structure

```text
phone-agent/
├── README.md
├── RUN.md
├── main.py
├── agent.py
├── tools.py
├── schemas.py
└── harness.py
```

---

# 8. How to Run the Application

## Step 1: Open the Project

Open a terminal in the project folder:

```bash
cd to the project
```

---

## Step 2: Create a Virtual Environment

### Linux / WSL

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

### Windows PowerShell

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

---

## Step 3: Install Required Packages

Install the required Python packages:

```bash
pip install ollama pydantic
```

---

## Step 4: Check Ollama

Check that Ollama is installed:

```bash
ollama --version
```

Check available models:

```bash
ollama list
```

The project uses:

```text
llama3.2:3b
```

If the model is not installed:

```bash
ollama pull llama3.2:3b
```

Then check again:

```bash
ollama list
```

---

## Step 5: Run the Application

Run:

### Linux / WSL

```bash
python3 main.py
```

### Windows

```powershell
python main.py
```

---

## 10. Application Flow

The complete application works as follows:

```text
User Request
     ↓
main.py
     ↓
agent.py
     ↓
Ollama LLM
     ↓
Choose Tool
     ↓
Harness
     ↓
Permission Check
     ↓
Input Validation
     ↓
Execute Tool
     ↓
Tool Result
     ↓
Ollama LLM
     ↓
Final Answer
```

The agent can repeat the tool-calling process until it has enough information to provide the final answer.
