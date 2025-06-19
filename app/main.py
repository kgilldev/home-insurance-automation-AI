from fastapi import FastAPI, UploadFile, File, HTTPException

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):

    if not file.filename or not (file.filename.endswith(".pdf") or file.filename.endswith(".docx")):
        raise HTTPException(status_code=400, detail=f"File type not supported {file.filename}, must be a PDF or DOCX")
    
    try:
        file_content = await file.read()
        return {
            "file_name": file.filename, 
            "file_size": len(file_content)
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {file.filename} {e}")
    finally:
        await file.close()

