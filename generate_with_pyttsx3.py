import pandas as pd
import pyttsx3
import genanki
import os
import shutil
from datetime import datetime

# -------------------------------
# 1️⃣ Setup folders
# -------------------------------
base_dir = os.path.dirname(os.path.abspath(__file__))
input_dir = os.path.join(base_dir, "input")
output_dir = os.path.join(base_dir, "output")
processed_dir = os.path.join(base_dir, "processed")
audio_folder = os.path.join(base_dir, "audio_files")

for folder in [input_dir, output_dir, processed_dir, audio_folder]:
    os.makedirs(folder, exist_ok=True)

# -------------------------------
# 2️⃣ Prepare TTS engine
# -------------------------------
engine = pyttsx3.init()
voices = engine.getProperty("voices")
french_voice = None
for v in voices:
    if "fr" in v.id.lower() or "french" in v.name.lower():
        french_voice = v.id
        break
if french_voice:
    engine.setProperty("voice", french_voice)
print(f"✅ Using voice: {french_voice}")

# -------------------------------
# 3️⃣ Process CSVs and queue audio
# -------------------------------
# -------------------------------
# 3️⃣ Process CSVs and queue audio
# -------------------------------
csv_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".csv")]
if not csv_files:
    print("ℹ️ No CSV files found in /input.")
else:
    decks_info = []  # store deck info for later
    for csv_file in csv_files:
        deck_name = os.path.splitext(csv_file)[0]
        deck_file_path = os.path.join(output_dir, f"{deck_name}.apkg")

        # Check if the deck already exists
        if os.path.exists(deck_file_path):
            print(f"\n⚠️ Skipping {csv_file}: Anki deck already exists with name '{deck_name}'")
            continue

        try:
            csv_path = os.path.join(input_dir, csv_file)
            print(f"\n📘 Processing file: {csv_file}")

            # Read CSV
            df = pd.read_csv(csv_path, header=None)
            french_sentences = df.iloc[:, 0].tolist()
            english_sentences = df.iloc[:, 1].tolist()

            # Filter
            filtered = [
                (fr, en) for fr, en in zip(french_sentences, english_sentences)
                if isinstance(fr, str) and fr.strip() not in {",", ""}
            ]
            french_sentences, english_sentences = zip(*filtered) if filtered else ([], [])

            # Queue audio for all sentences
            for i, fr in enumerate(french_sentences):
                audio_path = os.path.join(audio_folder, f"{deck_name}_{i}.mp3")
                engine.save_to_file(fr, audio_path)
                # print(f"🎧 Queued audio: {deck_name}_{i}.mp3")

            # Store deck info to create later
            decks_info.append({
                "csv_file": csv_file,
                "french_sentences": french_sentences,
                "english_sentences": english_sentences
            })

        except Exception as e:
            print(f"\n❌ Error queuing audio for {csv_file}: {e}")


# -------------------------------
# 4️⃣ Generate all audio at once
# -------------------------------
if decks_info:
    print("\n🔊 Generating all audio files in a single batch...")
    engine.runAndWait()
    engine.stop()
    print("\n✅ All audio generation complete.")

# -------------------------------
# 5️⃣ Create decks
# -------------------------------
for deck in decks_info:
    csv_file = deck["csv_file"]
    french_sentences = deck["french_sentences"]
    english_sentences = deck["english_sentences"]

    deck_name = os.path.splitext(csv_file)[0]
    deck_id = abs(hash(deck_name)) % (10**10)
    deck_file = os.path.join(output_dir, f"{deck_name}.apkg")

    my_deck = genanki.Deck(deck_id, deck_name)

    my_model = genanki.Model(
        1607392319,
        'Simple Model with Audio',
        fields=[{'name': 'French'}, {'name': 'English'}],
        templates=[{
            'name': 'Card 1',
            'qfmt': """
                <div style="text-align: center; font-size: 32px;">
                    {{French}}
                </div>
            """,
            'afmt': """
                {{FrontSide}}
                <hr id="answer">
                <div style="text-align: center; font-size: 32px;">
                    {{English}}
                </div>
            """,
        }],
    )

    for i, (fr, en) in enumerate(zip(french_sentences, english_sentences)):
        audio_filename = f"{os.path.splitext(csv_file)[0]}_{i}.mp3"
        fr_with_audio = f"{fr} [sound:{audio_filename}]"
        note = genanki.Note(model=my_model, fields=[fr_with_audio, en])
        my_deck.add_note(note)

    # Save deck
    media_files = [
        os.path.join(audio_folder, f"{os.path.splitext(csv_file)[0]}_{i}.mp3")
        for i in range(len(french_sentences))
    ]
    genanki.Package(my_deck, media_files=media_files).write_to_file(deck_file)
    print(f"✅ Deck created: {deck_name}.apkg")

    # Move CSV to processed
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    processed_path = os.path.join(processed_dir, f"{deck_name}_{timestamp}.csv")
    shutil.move(os.path.join(input_dir, csv_file), processed_path)
    print(f"\n📦 Moved {deck_name}.csv to the Processed folder")

# Clear audio folder after deck
for filename in os.listdir(audio_folder):
    file_path = os.path.join(audio_folder, filename)
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"\n⚠️ Could not delete {file_path}: {e}")
print("\n🧹 Cleared audio_files folder after deck creation.")

print("\n🎉 All done!")
