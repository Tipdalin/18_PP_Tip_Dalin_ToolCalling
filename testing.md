# Sample Testing Flow

## 1. Search Phone

### Input

```text
Find Samsung phones
```

### Agent Flow

```text
User
 ↓
Agent
 ↓
search_phone(query="Samsung")
 ↓
Tool Result
 ↓
Agent
 ↓
Final Answer
```

### Expected Result

```text
Galaxy S25 Ultra
Brand: Samsung
Price: $1299
Stock: 7
```

---

## 2. Multi-Step Agent Flow

### Input

```text
Find a Samsung phone that is currently in stock.
```

### Agent Flow

```text
User
 ↓
Agent
 ↓
search_phone(query="Samsung")
 ↓
Search Result: Galaxy S25 Ultra
 ↓
Agent observes result
 ↓
check_stock(phone_id=2)
 ↓
Stock: 7
 ↓
Agent
 ↓
Final Answer
```

### Expected Result

```text
Galaxy S25 Ultra is currently in stock with 7 units available.
```

This test demonstrates the main agent loop:

```text
Decision → Action → Observation → Decision → Final Answer
```

---

## 3. Failed Search

### Input

```text
Find Nokia phones
```

### Agent Flow

```text
User
 ↓
Agent
 ↓
search_phone(query="Nokia")
 ↓
Tool Result: []
 ↓
Agent observes empty result
 ↓
Final Answer
```

### Expected Result

```text
Sorry, I couldn't find any phones matching "Nokia".
```

The agent should not invent a Nokia phone.

---

## 4. Check Stock

### Input

```text
Check the stock of phone 2.
```

### Agent Flow

```text
User
 ↓
Agent
 ↓
check_stock(phone_id=2)
 ↓
Tool Result
 ↓
Final Answer
```

### Expected Result

```text
Galaxy S25 Ultra has 7 units in stock.
```

---

## 5. Customer Permission Test

### Role

```text
customer
```

### Input

```text
Delete phone 3.
```

### Flow

```text
User
 ↓
Agent
 ↓
delete_phone(phone_id=3)
 ↓
Harness
 ↓
Permission Check
 ↓
PERMISSION DENIED
 ↓
Tool is NOT executed
```

### Expected Result

```text
Role 'customer' is not allowed to use 'delete_phone'.
```

The phone should remain in the list.

---

## 6. Admin Permission Test

### Role

```text
admin
```

### Input

```text
Delete phone 3.
```

### Flow

```text
User
 ↓
Agent
 ↓
delete_phone(phone_id=3)
 ↓
Harness
 ↓
Permission Check
 ↓
Allowed
 ↓
Tool executes
 ↓
Phone deleted
```

### Expected Result

```text
Phone 'Pixel 9 Pro' was deleted.
```

---

## 7. Invalid Input Test

### Input

```text
Check the stock of phone -1.
```

### Flow

```text
User
 ↓
Agent
 ↓
check_stock(phone_id=-1)
 ↓
Schema Validation
 ↓
INVALID_PHONE_ID
```

### Expected Result

```text
Validation error
Phone ID must be greater than 0.
```

---

## 8. Phone Not Found Test

### Input

```text
Check the stock of phone 999.
```

### Flow

```text
User
 ↓
Agent
 ↓
check_stock(phone_id=999)
 ↓
Tool
 ↓
PHONE_NOT_FOUND
 ↓
Final Answer
```

### Expected Result

```text
Phone with ID 999 was not found.
```

---

## 9. To Exit Application

### Input

```text
q
```

or:

```text
exit
```

### Expected Result

```text
Goodbye!
```

---

# Recommended Demo Order

For a classroom demonstration, use these tests:

```text
1. Find Samsung phones
        ↓
2. Find a Samsung phone that is currently in stock.
        ↓
3. Find Nokia phones
        ↓
4. Delete phone 3 as customer
        ↓
5. Delete phone 3 as admin
```

These demonstrate:

* Tool calling
* Multi-step agent loop
* Failed search
* Permission control
* Admin action
* Final answers
* Safety controls
