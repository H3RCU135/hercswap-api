from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Header
from fastapi.responses import FileResponse
import uuid, os, shutil, json
from pydantic import BaseModel

app = FastAPI()
API_KEYS_FILE = "database.json"
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def load_keys():
    with open(API_KEYS_FILE, "r") as f:
        return json.load(f)["keys"]

def validate_key(api_key: str):
    keys = load_keys()
    return api_key in keys

@app.post("/api/face-swap")
async def face_swap(
    original: UploadFile = File(...),
    target: UploadFile = File(...),
    hd: bool = Form(False),
    x_api_key: str = Header(None)
):
    if not validate_key(x_api_key):
        raise HTTPException(status_code=403, detail="Invalid API key")

    # Save uploads
    uid = str(uuid.uuid4())
    original_path = f"{UPLOAD_DIR}/{uid}_original.jpg"
    target_path = f"{UPLOAD_DIR}/{uid}_target.jpg"
    result_path = f"{UPLOAD_DIR}/{uid}_result.jpg"

    with open(original_path, "wb") as f:
        f.write(await original.read())
    with open(target_path, "wb") as f:
        f.write(await target.read())

    # Here you'd call your face swap logic
    shutil.copyfile(original_path, result_path)  # 🔁 Placeholder for swap result

    return FileResponse(result_path, media_type="image/jpeg")

@app.post("/api/video-face-swap")
async def video_face_swap(
    video: UploadFile = File(...),
    face: UploadFile = File(...),
    hd: bool = Form(False),
    x_api_key: str = Header(None)
):
    if not validate_key(x_api_key):
        raise HTTPException(status_code=403, detail="Invalid API key")

    uid = str(uuid.uuid4())
    video_path = f"{UPLOAD_DIR}/{uid}_video.mp4"
    face_path = f"{UPLOAD_DIR}/{uid}_face.jpg"
    result_path = f"{UPLOAD_DIR}/{uid}_result.mp4"

    with open(video_path, "wb") as f:
        f.write(await video.read())
    with open(face_path, "wb") as f:
        f.write(await face.read())

    # Placeholder logic – use actual swap logic here
    shutil.copyfile(video_path, result_path)

    return FileResponse(result_path, media_type="video/mp4")