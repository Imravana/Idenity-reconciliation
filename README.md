# identify-reconciliation

This is a FastAPI-based backend service to solve the **Identity Reconciliation** problem for Zamazon.com. The service consolidates user contacts across multiple entries using unique email and phone information.

---
# Clone the repo
git clone https://github.com/riyasinhapat1/identity-reconciliation.git
cd identity-reconciliation

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # For Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
uvicorn main:app --reload

Visit: http://127.0.0.1:8000/docs


## Project structure
identity-reconciliation/
├── main.py
├── crud.py
├── models.py
├── schemas.py
├── database.py
├── requirements.txt
└── README.md

## Author
RIYA SINHA
Email: riyasinhapat1@gmail.com
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






