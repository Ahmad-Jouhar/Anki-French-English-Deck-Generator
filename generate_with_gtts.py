import pandas as pd
from gtts import gTTS
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
# 2️⃣ Process all CSVs in /input
# -------------------------------
csv_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".csv")]

if not csv_files:
    print("\nℹ️ No CSV files found in /input.")
else:
    for csv_file in csv_files:
        deck_name = os.path.splitext(csv_file)[0]
        deck_file = os.path.join(output_dir, f"{deck_name}.apkg")

        # Check if deck already exists
        if os.path.exists(deck_file):
            print(f"\n⚠️ Skipping {csv_file}: Anki deck already exists with name '{deck_name}'")
            continue

        try:
            csv_path = os.path.join(input_dir, csv_file)
            print(f"\n📘 Processing file: {csv_file}")

            # Read CSV
            df = pd.read_csv(csv_path, header=None)
            french_sentences = df.iloc[:, 0].tolist()
            english_sentences = df.iloc[:, 1].tolist()

            # Filter out empty/unwanted lines
            filtered = [
                (fr, en)
                for fr, en in zip(french_sentences, english_sentences)
                if isinstance(fr, str) and fr.strip() not in {",", ""}
            ]
            french_sentences, english_sentences = zip(*filtered) if filtered else ([], [])

            # -------------------------------
            # 3️⃣ Generate audio with gTTS (always overwrite)
            # -------------------------------
            for i, fr in enumerate(french_sentences):
                audio_filename = f"{deck_name}_{i}.mp3"
                audio_path = os.path.join(audio_folder, audio_filename)
                try:
                    tts = gTTS(fr, lang="fr")
                    tts.save(audio_path)
                    # print(f"\n🎧 Saved: {audio_filename}")
                except Exception as e:
                    print(f"\n❌ Error generating {audio_filename}: {e}")

            # -------------------------------
            # 4️⃣ Create Anki deck
            # -------------------------------
            deck_id = abs(hash(deck_name)) % (10**10)
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

            # Add notes (cards)
            for i, (fr, en) in enumerate(zip(french_sentences, english_sentences)):
                audio_filename = f"{deck_name}_{i}.mp3"
                fr_with_audio = f"{fr} [sound:{audio_filename}]"
                note = genanki.Note(model=my_model, fields=[fr_with_audio, en])
                my_deck.add_note(note)

            # -------------------------------
            # 5️⃣ Save deck
            # -------------------------------
            media_files = [
                os.path.join(audio_folder, f"{deck_name}_{i}.mp3")
                for i in range(len(french_sentences))
            ]
            genanki.Package(my_deck, media_files=media_files).write_to_file(deck_file)
            print(f"✅ Deck created: {deck_name}.apkg")

            # -------------------------------
            # 6️⃣ Move processed CSV
            # -------------------------------
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            processed_path = os.path.join(processed_dir, f"{deck_name}_{timestamp}.csv")
            shutil.move(csv_path, processed_path)
            print(f"\n📦 Moved {deck_name}.csv to the Processed folder")

        except Exception as e:
            print(f"❌ Error processing {csv_file}: {e}")

# -------------------------------
# 7️⃣ Clear audio files
# -------------------------------
for filename in os.listdir(audio_folder):
    file_path = os.path.join(audio_folder, filename)
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"\n⚠️ Could not delete {file_path}: {e}")
print("\n🧹 Cleared audio_files folder after deck creation.")

print("\n🎉 All done!")
