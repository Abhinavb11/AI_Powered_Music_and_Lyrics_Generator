# generate_music.py
import pretty_midi
import random
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def generate_sample_melody(filename="melody.mid", theme="love", mood="happy", style="pop"):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
    
    try:
        logger.debug(f"Starting melody generation for {filename} with theme={theme}, mood={mood}, style={style}")
        midi = pretty_midi.PrettyMIDI(initial_tempo=100 + random.randint(-10, 20) if mood == "energetic" else 120)  # Vary tempo based on mood

        # Choose instrument based on style with random variation
        melody_program = random.choice([0, 1] if style == "classical" else [24, 25, 26] if style == "pop" else [25, 27, 28])  # Piano variations, Guitar variations
        melody_instrument = pretty_midi.Instrument(program=melody_program)

        # Secondary instrument for layering
        secondary_program = random.choice([48, 49] if style == "classical" else [40, 41])  # Strings or Violin
        secondary_instrument = pretty_midi.Instrument(program=secondary_program)

        # Mood-based dynamics
        base_velocity = 70 if mood == "melancholic" else 90 if mood == "happy" else 80

        # Dynamic key and chord selection based on theme and style
        base_note = random.choice([48, 52, 55])  # C2, E2, G2 (lower range to allow octave shifts)
        if theme == "love":
            key_chords = [[0, 4, 7], [7, 11, 14], [5, 8, 12], [3, 7, 10]]  # I, V, iii, vi (C, G, Em, Am)
        elif theme == "adventure":
            key_chords = [[0, 4, 7], [7, 11, 14], [2, 5, 9], [9, 0, 4]]  # I, V, ii, IV (C, G, Dm, F)
        else:  # sadness
            key_chords = [[0, 4, 7], [5, 8, 12], [3, 7, 10], [8, 11, 14]]  # I, iii, vi, iii (C, Em, Am, Em)

        # Convert intervals to absolute MIDI notes
        def get_chord_notes(intervals):
            return [clamp_pitch(base_note + interval) for interval in intervals]

        def clamp_pitch(pitch):
            return max(0, min(127, pitch))

        # Generate random chord progression for each section
        verse_chords = [get_chord_notes(key_chords[i % len(key_chords)]) for i in range(4)]
        chorus_chords = [get_chord_notes(key_chords[(i + 1) % len(key_chords)]) for i in range(4)]
        random.shuffle(verse_chords)  # Randomize order
        random.shuffle(chorus_chords)

        beat_duration = 0.5  # Half-second beats
        total_beats = 120  # 60 seconds
        time = 0

        # Intro (8s = 16 beats): Gentle arpeggio with secondary layer
        for beat in range(16):
            chord = verse_chords[beat // 4 % 4]
            pitch = clamp_pitch(chord[beat % 3] + random.choice([0, 12]))  # Random octave
            logger.debug(f"Intro pitch: {pitch}")  # Debug pitch
            velocity = base_velocity - 20 + (beat // 4 * 2)  # Slight crescendo
            start = time
            end = time + beat_duration * random.uniform(0.8, 1.2)  # Slight rhythm variation
            note = pretty_midi.Note(velocity=velocity, pitch=pitch, start=start, end=end)
            melody_instrument.notes.append(note)
            if beat % 4 == 0:
                for note_pitch in chord:
                    secondary_pitch = clamp_pitch(note_pitch)
                    logger.debug(f"Intro secondary pitch: {secondary_pitch}")  # Debug secondary pitch
                    secondary_note = pretty_midi.Note(velocity=velocity - 30, pitch=secondary_pitch, start=time, end=time + beat_duration * 4)
                    secondary_instrument.notes.append(secondary_note)
            time += beat_duration

        # Verse (20s = 40 beats): Melodic phrasing with randomness
        for beat in range(40):
            chord = verse_chords[beat // 4 % 4]
            if beat % 4 == 0:
                pitch = clamp_pitch(chord[0] + random.choice([12, 24]))  # Random octave
            elif beat % 4 == 2:
                pitch = clamp_pitch(chord[2] + random.choice([0, 12]))
            else:
                pitch = clamp_pitch(random.choice(chord) + random.choice([0, 12, 24]))
            logger.debug(f"Verse pitch: {pitch}")  # Debug pitch
            velocity = base_velocity + random.randint(0, 20)  # Random dynamics
            start = time
            end = time + beat_duration * random.choice([0.5, 1, 1.5])  # Vary note length
            note = pretty_midi.Note(velocity=velocity, pitch=pitch, start=start, end=end)
            melody_instrument.notes.append(note)
            time += beat_duration

        # Chorus (24s = 48 beats): Energetic melody with secondary layer
        for beat in range(48):
            chord = chorus_chords[beat // 4 % 4]
            if beat % 2 == 0:
                pitch = clamp_pitch(chord[0] + random.choice([12, 24]))
            else:
                pitch = clamp_pitch(random.choice(chord) + random.choice([12, 24]))
            logger.debug(f"Chorus pitch: {pitch}")  # Debug pitch
            velocity = base_velocity + 30 + random.randint(0, 30) if mood in ["happy", "energetic"] else base_velocity + 10
            start = time
            end = time + beat_duration * random.choice([1, 1.5, 2])  # Vary note length
            note = pretty_midi.Note(velocity=velocity, pitch=pitch, start=start, end=end)
            melody_instrument.notes.append(note)
            if beat % 4 == 0:
                for note_pitch in chord:
                    secondary_pitch = clamp_pitch(note_pitch)
                    logger.debug(f"Chorus secondary pitch: {secondary_pitch}")  # Debug secondary pitch
                    secondary_note = pretty_midi.Note(velocity=velocity - 40, pitch=secondary_pitch, start=time, end=time + beat_duration * 4)
                    secondary_instrument.notes.append(secondary_note)
            time += beat_duration

        # Outro (8s = 16 beats): Fade out with melody
        for beat in range(16):
            chord = verse_chords[beat // 4 % 4]
            pitch = clamp_pitch(chord[beat % 3] + random.choice([0, 12]))
            logger.debug(f"Outro pitch: {pitch}")  # Debug pitch
            velocity = max(base_velocity - 30 - (beat * 3), 20)
            start = time
            end = time + beat_duration * random.uniform(0.8, 1.2)
            note = pretty_midi.Note(velocity=velocity, pitch=pitch, start=start, end=end)
            melody_instrument.notes.append(note)
            time += beat_duration

        midi.instruments.append(melody_instrument)
        midi.instruments.append(secondary_instrument)
        midi.write(filename)
        logger.debug(f"Melody saved to {filename}")
    except Exception as e:
        logger.error(f"Failed to generate melody: {e}")
        raise Exception(f"Failed to generate melody: {e}")

# Uncomment to test standalone
# if __name__ == "__main__":
#     generate_sample_melody("static/melody.mid", "love", "happy", "pop")