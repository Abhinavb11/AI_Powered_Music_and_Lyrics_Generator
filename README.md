# 🎵 AI-Powered Music and Lyrics Generator

> Generate **original melodies, lyrics, drums, and bass** instantly using **Deep Learning** and **Generative AI**.  
> Create mood-based songs and download your music — all through a simple web interface!

---

## 📜 Project Overview

Creating original music traditionally demands both creativity and technical expertise.  
Our project **democratizes music creation** by enabling anyone — regardless of musical background — to **compose complete songs** using AI.

**This system automatically**:
- Generates melodies with deep learning (LSTM models)
- Creates lyrics with Google Gemini API
- Adds drum and bass layers based on mood and style
- Lets users download their generated songs in `.mid` format

---

## 🎯 Key Features

- 🎶 **Melody Generation**: LSTM model predicts a sequence of musical notes.
- ✍️ **Lyrics Generation**: Gemini AI generates original lyrics matching your theme, mood, and style.
- 🥁 **Drums and Bass Tracks**: Rule-based system layers rhythmic instruments dynamically.
- 🌐 **Flask Web App**: Simple, user-friendly interface for real-time music and lyrics creation.
- 📥 **Download Option**: Users can download the final MIDI song directly.

---

## 🧠 Tech Stack

| Technology             | Purpose                                    |
|------------------------|--------------------------------------------|
| **Python**             | Core programming language                  |
| **Flask**              | Backend web server                         |
| **PrettyMIDI**         | MIDI file parsing, creation, editing       |
| **TensorFlow**         | LSTM-based melody generation model         |
| **Google Gemini API**  | AI lyrics generation                       |
| **HTML/CSS**           | Frontend rendering                         |
| **NumPy**              | Numerical computations                     |

---

## 📚 Dataset Used

- **Lakh MIDI Dataset**  
  > 176,581 MIDI files containing melodies, chords, and full songs.

- **Preprocessing**:
  - MIDI parsing with `pretty_midi`
  - Extract note sequences and encode them as integers
  - Normalize and structure data for LSTM input

---

## 🛠 How It Works

1. User selects **Theme**, **Mood**, and **Style** on the web app.
2. Flask backend:
   - 🎵 Generates a melody (LSTM).
   - ✍️ Generates lyrics (Gemini API).
   - 🥁 Adds drums and bass tracks (rule-based).
3. The full song is created as a MIDI file.
4. User sees generated lyrics and can **download the music**!

---

## 📂 Project Structure

```
AI-Music-Generator/
├── app.py                  # Main Flask app
├── generate_music.py       # Melody generation
├── drum_and_bass.py        # Adding drum and bass layers
├── lyrics_generator.py     # Lyrics generation via Gemini API
├── static/
│   └── full_song.mid       # Generated MIDI files
├── templates/
│   └── index.html          # Frontend HTML
├── models/
│   ├── melody_model_fast.h5 # Trained LSTM model
│   ├── note_to_int.pkl     # Note-to-integer mapping
│   ├── X.npy               # Preprocessed sequences
│   └── y.npy
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## 🧩 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/AI-Music-Generator.git
cd AI-Music-Generator
```

### 2. Install the required Python packages
```bash
pip install -r requirements.txt
```

### 3. Set up Google Gemini API
- Get an API key from [Google Generative AI](https://ai.google.dev/)
- Add your key in `lyrics_generator.py`:
```python
genai.configure(api_key="YOUR-API-KEY-HERE")
```

### 4. Run the Flask app
```bash
python app.py
```

### 5. Open your browser
Visit: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## ⚙️ Requirements

- Python 3.8+
- TensorFlow 2.x
- Flask
- PrettyMIDI
- NumPy
- Google Generative AI SDK
- dotenv

(Already listed in `requirements.txt`)

---

## 🎯 Future Improvements

- Host live version (Render, PythonAnywhere)
- Add more realistic instruments with GANs or Transformers
- Add real-time audio playback (not just MIDI download)
- Mobile app version for instant music creation
- Collaborative music sessions between users

---

## 🏆 Members

- Rabeeh N
- Abhinav B


## 🙏 Acknowledgements

- [Lakh MIDI Dataset](https://colinraffel.com/projects/lmd/)
- [PrettyMIDI Library](https://github.com/craffel/pretty-midi)
- [Google Generative AI (Gemini)](https://ai.google.dev/)
- [Flask Framework](https://flask.palletsprojects.com/)

---

# 🎶 Ready to create your own AI-generated songs?  
Clone the project, run the app, and **start making music instantly!** 🎹🎤
