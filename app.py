import os
from flask import Flask, request, jsonify
from PIL import Image
import io
import time

# --- 1. Initialize Flask App ---
app = Flask(__name__)
print("✅ Flask server starting in GUARANTEED DEMO MODE.")


# --- 2. Create the API Endpoint ---
@app.route('/diagnose', methods=['POST'])
def diagnose_plant():
    # Check if files were sent
    if 'image' not in request.files or 'audio' not in request.files:
        return jsonify({"error": "Missing image or audio file"}), 400

    print("✅ Request received from Android app.")

    try:
        # 1. Simulate the transcription
        transcribed_text = "The leaves have dark brown spots and are spreading."
        print(f"🎤 Simulating transcription: '{transcribed_text}'")

        # 2. Simulate the image processing
        image_file = request.files['image']
        image_data = image_file.read()
        image = Image.open(io.BytesIO(image_data))
        print(f"🖼️ Image received with size {image.size}.")

        # 3. Simulate the AI "thinking" time
        print("🤖 Simulating AI analysis... (this will take 5 seconds)")
        time.sleep(5)

        # 4. Provide the hard-coded, perfect diagnosis
        final_answer = "leaf spot, likely caused by a fungal infection. Recommend isolating the plant and applying a copper fungicide."
        print(f"💡 Demo Diagnosis: '{final_answer}'")
        
        # 5. Send the successful result back to the app
        return jsonify({"diagnosis": final_answer})

    except Exception as e:
        print(f"An error occurred even in demo mode: {e}")
        return jsonify({"error": f"An internal server error occurred: {str(e)}"}), 500

# --- 3. Run the Server ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)