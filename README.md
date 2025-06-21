# identify-reconciliation

This is a FastAPI-based backend service to solve the **Identity Reconciliation** problem for Zamazon.com. The service consolidates user contacts across multiple entries using unique email and phone information.

---
##  Features

- Accepts JSON input with `email` and/or `phoneNumber`
- Identifies matching contact records
- Creates new primary or secondary contact entries
- Returns consolidated contact data including:
  - `primaryContactId`
  - all associated `emails`
  - all associated `phoneNumbers`
  - `secondaryContactIds`

---

##  API Endpoint

### POST `/identify`

**Request Body:**

```json
{
  "email": "riyasinhapat1@gmail.com",
  "phoneNumber": "1234567890"
}
