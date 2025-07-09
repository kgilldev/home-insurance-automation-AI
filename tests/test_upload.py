from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.enum.enums import DecisionStatus
from app.routes.claims import router
from pathlib import Path
import zipfile

app = FastAPI()
app.include_router(router)
client = TestClient(app)
PREFIX = Path(__file__).resolve().parent / "files"

class FakeClaim:
        file_name = "sample.pdf"
        structured_claim = {
            "claimant_name": "McLovin",
            "claimant_date": "09-09-2025",
            "claim_summary": "fire but no pants on fire",
            "claim_amount": 2100.00,
            "claim_decision": "ACCEPT",
            "decision_reasoning": "claim accepted by the Gods"
        }
        decision = "ACCEPT"

@patch("app.routes.claims.AsyncSessionLocal")
@patch("app.routes.claims.create_claim", new_callable=AsyncMock)
def test_upload_pdf(mock_create_claim, mock_session_local):
    mock_session = AsyncMock()
    mock_session_local.return_value.__aenter__.return_value = mock_session

    mock_create_claim.return_value = FakeClaim()

    file_path = PREFIX / "sample.pdf"
    with open(file_path, "rb") as f:
        response = client.post(
            "/upload-file",
            files={"file": ("sample.pdf", f, "application/pdf")}
        )

    assert response.status_code == 200

@patch("app.routes.claims.AsyncSessionLocal")
@patch("app.routes.claims.create_claim", new_callable=AsyncMock)
def test_upload_docx(mock_create_claim, mock_session_local):
    mock_session = AsyncMock()
    mock_session_local.return_value.__aenter__.return_value = mock_session

    mock_create_claim.return_value = FakeClaim()

    file_path = PREFIX / "sample.docx"
    with open(file_path, "rb") as doc:
        response = client.post(
            "/upload-file",
            files = {"file": ("sample.docx", doc, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        )
        print("Is zipfile: ", zipfile.is_zipfile("tests/data/sample.docx"))
        
        assert response.status_code == 200

def test_upload_invalid_file_type():
    file_path = PREFIX / "sample.txt"
    with open(file_path, "rb") as txt:
        response = client.post(
            "/upload-file",
            files = {"file": ("sample.txt", txt, "text/plain")}
        )
    assert response.status_code == 400     
    assert "File type not supported" in response.text
