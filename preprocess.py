import os
import pretty_midi
import numpy as np
import pickle

midi_dir = 'midi'
sequence_length = 50
notes = []

def extract_notes_from_midi(midi_path):
    try:
        midi = pretty_midi.PrettyMIDI(midi_path)
        if not midi.instruments:
            return []
        instrument = midi.instruments[0]
        return [str(note.pitch) for note in instrument.notes]
    except Exception as e:
        print(f"❌ Skipping {midi_path}: {e}")
        return []

# Walk through all subdirectories
print("🔄 Extracting notes from MIDI files...")
file_count = 0
for root, dirs, files in os.walk(midi_dir):
    for file in files:
        if file.endswith('.mid') or file.endswith('.midi'):
            full_path = os.path.join(root, file)
            file_notes = extract_notes_from_midi(full_path)
            if len(file_notes) > sequence_length:
                notes += file_notes
                file_count += 1
                print(f"✅ Processed: {file}")

print(f"\n🎯 Total valid files processed: {file_count}")
if len(notes) == 0:
    raise Exception("No valid MIDI data found! Check your dataset or MIDI file integrity.")

# Create mappings
unique_notes = sorted(list(set(notes)))
note_to_int = {note: num for num, note in enumerate(unique_notes)}
int_notes = [note_to_int[n] for n in notes]

# Create sequences
X, y = [], []
for i in range(0, len(int_notes) - sequence_length):
    X.append(int_notes[i:i + sequence_length])
    y.append(int_notes[i + sequence_length])

# Final data formatting
X = np.reshape(X, (len(X), sequence_length, 1)) / float(len(unique_notes))
y = np.array(y)

# Save
with open("note_to_int.pkl", "wb") as f:
    pickle.dump(note_to_int, f)

np.save("X.npy", X)
np.save("y.npy", y)

print(f"✅ Saved preprocessed data: X.npy shape = {X.shape}, y.npy shape = {y.shape}")