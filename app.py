import os
from flask import Flask, request, jsonify
from PIL import Image
import io
import time
from langdetect import detect # Import the language detection library

# --- 1. Initialize Flask App ---
app = Flask(__name__)
print("✅ Flask server starting in MULTILINGUAL DEMO MODE.")

# --- 2. Pre-translated Diagnoses ---
# We store our answers in both English and Malayalam
diagnoses = {
    "en": "leaf spot, likely caused by a fungal infection. Recommend isolating the plant and applying a copper fungicide.",
    "ml": "ഇലപ്പുള്ളി, ഒരു ഫംഗസ് അണുബാധ കാരണമാകാം. ചെടി മാറ്റിനിർത്താനും കോപ്പർ ഫംഗിസൈഡ് പ്രയോഗിക്കാനും ശുപാർശ ചെയ്യുന്നു."
}

# --- 3. Create the API Endpoint ---
@app.route('/diagnose', methods=['POST'])
def diagnose_plant():
    if 'image' not in request.files or 'audio' not in request.files:
        return jsonify({"error": "Missing image or audio file"}), 400

    print("✅ Request received from Android app.")
    
    # Get the typed question from the app
    question_text = request.form.get('prompt', 'Identify the disease on this plant leaf.')
    print(f"❓ Received question: '{question_text}'")

    try:
        # --- Language Detection and Simulation Logic ---
        detected_lang = 'en' # Default to English
        try:
            # Detect the language of the user's typed question
            if len(question_text) > 5: # Make sure there's enough text to detect
                lang_code = detect(question_text)
                if lang_code == 'ml':
                    detected_lang = 'ml'
            print(f"🌍 Language detected: {detected_lang}")
        except Exception as lang_e:
            print(f"⚠️ Language detection failed, defaulting to English. Error: {lang_e}")
            detected_lang = 'en'
            
        # Simulate transcription based on detected language
        if detected_lang == 'ml':
            transcribed_text = "ഇലകളിൽ തവിട്ടുനിറത്തിലുള്ള പാടുകൾ ഉണ്ട്, അത് പടരുന്നു."
        else:
            transcribed_text = "The leaves have dark brown spots and are spreading."
        
        print(f"🎤 Simulating transcription: '{transcribed_text}'")

        # Simulate image processing
        image_file = request.files['image']
        image_data = image_file.read()
        image = Image.open(io.BytesIO(image_data))
        print(f"🖼️ Image received with size {image.size}.")

        # Simulate AI thinking time
        print("🤖 Simulating AI analysis...")
        time.sleep(5)

        # Provide the diagnosis in the detected language
        final_answer = diagnoses.get(detected_lang, diagnoses['en']) # Fallback to English
        print(f"💡 Demo Diagnosis (in {detected_lang}): '{final_answer}'")
        
        # Send the successful result back
        return jsonify({"diagnosis": final_answer})

    except Exception as e:
        print(f"An error occurred in demo mode: {e}")
        return jsonify({"error": f"An internal server error occurred: {str(e)}"}), 500

# --- 4. Run the Server ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)