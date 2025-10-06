# 🇫🇷 French Sentence Deck Generator

This project lets you **automatically create Anki decks** with **French sentences, English translations, and audio**.  

You can choose between two versions:

- **Local voice (pyttsx3)** — Works offline using your system’s French voice  
- **Online voice (gTTS)** — Uses Google Translate TTS (more natural, but slower and rate-limited)

---

## 🗂 Folder Structure

Run either python file once to generate the 4 folders needed to use the program.

Your project folder should look like this:

```

French-Deck-Generator/

├── input/          # Put your .csv files here

├── output/         # Generated .apkg decks appear here

├── processed/      # Processed CSVs get moved here

├── audio\_files/    # All generated .mp3 files go here

│

├── generate\_with\_pyttsx3.py   # Offline version (local voice)

├── generate\_with\_gtts.py      # Online version (Google TTS)

└── README.md

```

## ⚙️ Setup

1. **Install Python 3.9 or later**  
   - [Download here](https://www.python.org/downloads/)

2. **Install dependencies**  

```bash
pip install pandas pyttsx3 gTTS genanki
```

3. **(For pyttsx3 only)**

Ensure you have a **French (France)** voice installed on your system (Windows example):

  - Open **Settings → Time \& Language → Speech**
  - Under **Manage voices**, click **Add voices**
  - Choose **French (France)** and install it

---

## 🧾 CSV Format

Each `.csv` file in the `input/` folder should have **two columns**, with **no header row**:

French Sentence | English Translation
----------------|-------------------
Bonjour !       | Hello!
Comment ça va ? | How are you?

---

## 🚀 How to Use

Run either python file once to generate the 4 folders needed to use the program.

1. Place your `.csv` sheets in the **input** folder  
2. Run one of the scripts (either by double-clicking or from the terminal)  
3. The generated decks will appear in the **output** folder  
4. Processed `.csv` files will be moved automatically to the **processed** folder  

---

### 🗣 Local Voice (pyttsx3)

- Works **offline**  
- Requires the **French (France)** voice to be installed  
- Speed depends on your computer  

Run:

python generate_with_pyttsx3.py

---

### 🌐 Google TTS (gTTS)

- Requires an **internet connection**  
- Audio sometimes sounds a bit **unnatural**  
- May **freeze or stop** if there are too many audio files to generate  

Run:

python generate_with_gtts.py

---

## 🧠 Notes

- The program automatically prevents overwriting existing audio or decks.  
- If a deck with the same name already exists, a warning will be made by the program and the file will stay in the input folder untouched.  
- Each CSV generates its own `.apkg` deck with all related audio included.


