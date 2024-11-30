from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse, JSONResponse, FileResponse
from diffusers import DiffusionPipeline
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import io
import torch
from PIL import Image

# Initialize FastAPI app
app = FastAPI()

# Database setup
DATABASE_URL = "sqlite:///./prompts.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Model for storing prompts and image paths
class PromptHistory(Base):
    __tablename__ = "prompts"
    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(String, nullable=False)
    image_path = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

# Stable Diffusion Pipeline
pipe = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
device = "mps" if torch.backends.mps.is_available() else "cpu"
pipe = pipe.to(device)
pipe.enable_attention_slicing()

# Generate unique folder for storing images
IMAGE_DIR = "./generated_images"
os.makedirs(IMAGE_DIR, exist_ok=True)

# Helper function to save to database
def save_prompt_to_db(prompt: str, image_path: str):
    db = SessionLocal()
    new_entry = PromptHistory(prompt=prompt, image_path=image_path)
    db.add(new_entry)
    db.commit()
    db.close()

@app.get("/")
async def root():
    return {"message": "Welcome to the Text-to-Image API with storage!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "device": device}

@app.get("/generate", response_class=FileResponse)
async def generate_image(prompt: str = Query(..., description="Text prompt for image generation")):
    try:
        # Generate the image
        image = pipe(prompt).images[0]

        # Save the image to disk
        image_path = os.path.join(IMAGE_DIR, f"{prompt.replace(' ', '_')}.png")
        image.save(image_path)

        # Save prompt and image path to the database
        save_prompt_to_db(prompt, image_path)

        # Return the image
        return FileResponse(image_path, media_type="image/png")
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/history")
async def get_history():
    # Fetch all saved prompts and image paths from the database
    db = SessionLocal()
    history = db.query(PromptHistory).all()
    db.close()

    return [
        {"id": entry.id, "prompt": entry.prompt, "image_path": entry.image_path}
        for entry in history
    ]
