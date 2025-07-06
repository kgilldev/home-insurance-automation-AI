# home-insurance-automation-AI
Using FastAPI to automate home insurance claims with a LLM

High-level Overview:
1. Upload PDF or DOCX
2. LLM parses upload for structured claim
3. LLM makes a decision based off validation rules set
4. Save relevant info into our Postgres DB
5. Client or Escalation Manager gets decision - ACCEPTED | REJECTED | ESCALATED