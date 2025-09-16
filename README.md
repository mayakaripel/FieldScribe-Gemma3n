# FieldScribe: A Multimodal AI Co-Pilot for Farmers

### 🏆 Official Submission for the Google Gemma 3n Impact Challenge 🏆

---

## Project Overview

FieldScribe is a multimodal diagnostic tool designed to empower farmers in low-connectivity areas, especially those with communication barriers. By combining image recognition, speech-to-text, and advanced language understanding, FieldScribe acts as an expert co-pilot, helping farmers identify crop diseases right in the field.

The project fulfills the "Gemma 3n" vision by building a functional, high-impact application that is "bigger than a simple chatbot." I used Google's **PaliGemma** as the core "eyes and brain" of the system and **OpenAI's Whisper** to provide audio understanding.

---

## 🚀 Key Links

*   **VIDEO DEMO:** [https://youtu.be/T7KEHKBKKqs]
*   **LIVE INTERACTIVE DEMO (Kaggle Notebook):** [https://www.kaggle.com/code/mayakaripel/fieldscribe-interactive-demo1]
*   **LIVE INTERACTIVE DEMO (Kaggle Notebook):** [https://www.kaggle.com/code/mayakaripel/fieldscribe-interactive-demo]

---

## 💡 How It Works

The pipeline, demonstrated in the Kaggle Notebook, proves a true multimodal workflow:
1.  **See:** A farmer uploads a photo of a diseased plant.
2.  **Hear:** The farmer records their observations in their own voice.
3.  **Understand:** FieldScribe uses Whisper to transcribe the audio, combining it with the image and a text prompt.
4.  **Analyze:** Google's PaliGemma model processes all three inputs simultaneously to provide a clear, actionable diagnosis.

## 🛠️ Technology Stack

*   **Vision-Language Model:** Google PaliGemma (`paligemma-3b-mix-448`)
*   **Speech-to-Text:** OpenAI Whisper (`tiny.en`)
*   **Core Libraries:** Hugging Face Transformers, PyTorch, ipywidgets
*   **Platform:** Kaggle Notebooks

## 📂 Repository Contents

*   `FieldScribe-Demo.ipynb`: The main Kaggle Notebook containing all the working code for the live demo.
*   `TECHNICAL_WRITEUP.md`: A detailed paper explaining the architecture, challenges, and design choices.
*   `tomato_leaf.jpg` & `farmer_note.wav`: The asset files used for the pre-loaded demo.

