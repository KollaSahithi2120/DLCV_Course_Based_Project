# ImaginAItion: Text-to-Image Generator with FastAPI and Streamlit

ImaginAItion is a web application that combines the power of **FastAPI** and **Streamlit** to generate stunning images from text prompts using **Stable Diffusion**. The app also stores generated images and prompts in a database for easy access to your creative history.

---

## Features

- **Text-to-Image Generation**: Enter a text prompt to create AI-generated visuals.
- **Prompt History**: Browse previously generated images and their corresponding prompts.
- **Service Health Check**: Monitor the backend status from the Streamlit frontend.
- **Interactive UI**: User-friendly interface for generating and viewing images.
- **Persistent Storage**: Stores prompts and image paths in an SQLite database.

---

## Installation

### Prerequisites

1. Python 3.8 or higher.
2. A machine with `torch` support (e.g., MPS for macOS, CPU fallback if unavailable).

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/your-repo/imaginAItion.git
   cd imaginAItion
