
# =================================================================
# FieldScribe: The "Full AI" Production-Intent Backend
# This script loads and runs both Whisper and PaliGemma.
# WARNING: This is very memory-intensive and requires a powerful
# server (e.g., a paid Render plan) or a local machine with ample RAM.
# =================================================================

import os
from flask import Flask, request, jsonify
import torch
from transformers import PaliGemmaForConditionalGeneration, PaliGemmaProcessor
import whisper
from PIL import Image
import io
import numpy as np
import librosa
import gc # Import the garbage collector

# --- 1. Initialize Flask App and Models ---
app = Flask(__name__)

# Disable Dynamo for compatibility
import torch._dynamo
torch._dynamo.disable()

# Check for GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Load PaliGemma Model
model_path = "google/paligemma-3b-mix-448"
print("Loading PaliGemma model...")
paligemma_model = PaliGemmaForConditionalGeneration.from_pretrained(
    model_path,
    dtype=torch.bfloat16,
    device_map=device,
    revision="bfloat16",
).eval()
paligemma_processor = PaliGemmaProcessor.from_pretrained(model_path)
print("✅ PaliGemma model loaded.")

# Load Whisper Model (the multilingual 'base' model)
print("Loading multilingual Whisper model...")
whisper_model = whisper.load_model("base", device=device)
print("✅ Whisper model loaded.")


# --- 2. Create the API Endpoint ---
@app.route('/diagnose', methods=['POST'])
def diagnose_plant():
    if 'image' not in request.files or 'audio' not in request.files:
        return jsonify({"error": "Missing image or audio file"}), 400

    image_file = request.files['image']
    audio_file = request.files['audio']
    question_text = request.form.get('prompt', 'Identify the disease on this plant leaf.')

    try:
        # Manually trigger garbage collection to free up memory before a big task
        gc.collect()
        if device == "cuda":
            torch.cuda.empty_cache()
        print("Memory cleared before analysis.")

        # Step 1: Transcribe the audio in memory
        print("Transcribing audio in memory...")
        audio_data = audio_file.read()
        audio_np, sampling_rate = librosa.load(io.BytesIO(audio_data), sr=16000)
        transcription_result = whisper_model.transcribe(audio_np)
        transcribed_text = transcription_result['text']
        print(f"Transcription: {transcribed_text}")

        # Step 2: Analyze the image and text with PaliGemma
        print("Analyzing with PaliGemma...")
        image_data = image_file.read()
        image = Image.open(io.BytesIO(image_data))
        
        # Aggressively resize the image to save RAM
        image.thumbnail((256, 256)) 
        print(f"Image resized to {image.size} for analysis.")

        # Construct a multilingual-aware prompt
        full_prompt = (
            f"<image> {question_text}\n"
            f"The following notes are from a farmer and may be in their local language (e.g., Malayalam, English).\n"
            f"Farmer's spoken notes: {transcribed_text}"
        )
        
        inputs = paligemma_processor(text=full_prompt, images=image, return_tensors="pt").to(device)
        outputs = paligemma_model.generate(**inputs, max_new_tokens=128)
        
        # Clean the output to get just the answer
        # Note: This cleaning logic might need adjustment depending on the multilingual model's output format
        raw_output_text = paligemma_processor.decode(outputs[0], skip_special_tokens=True)
        # Find where the prompt ends and take the rest of the string
        prompt_end_index = raw_output_text.find(transcribed_text) + len(transcribed_text)
        final_answer = raw_output_text[prompt_end_index:].strip()

        print(f"✅ Diagnosis Complete: {final_answer}")

        return jsonify({"diagnosis": final_answer})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": f"An internal error occurred: {str(e)}"}), 500

# --- 3. Run the Server (for local testing) ---
if __name__ == '__main__':
    # use_reloader=False is crucial to prevent loading the models twice and crashing
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
