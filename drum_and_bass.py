import pretty_midi
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def add_instruments_to_melody(input_midi='melody.mid', output_midi='full_song.mid', theme="love", mood="happy", style="pop"):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_midi) or '.', exist_ok=True)

    try:
        logger.debug(f"Loading MIDI from {input_midi} to save as {output_midi} with theme={theme}, mood={mood}, style={style}")
        if not os.path.exists(input_midi):
            logger.error(f"Input MIDI file {input_midi} not found")
            raise FileNotFoundError(f"Input MIDI file {input_midi} not found")
        midi = pretty_midi.PrettyMIDI(input_midi)

        # Bass: Follows melody with realistic phrasing
        bass = pretty_midi.Instrument(program=33 if style == "pop" else 34 if style == "rock" else 35)  # Bass Finger, Fretless, Slap Bass
        verse_chords = [60, 67, 57, 65]  # C, G, Am, F
        chorus_chords = [60, 65, 67, 60]  # C, F, G, C
        beat_duration = 0.5
        total_beats = 120
        time = 0

        # Intro (16 beats): Subtle bass with long notes
        for beat in range(16):
            chord_idx = beat // 4 % 4
            if beat % 4 == 0:
                root = verse_chords[chord_idx]
                velocity = 70 + (beat // 4 * 2)
                note = pretty_midi.Note(velocity=velocity, pitch=root - 12, start=time, end=time + beat_duration * 3)
                bass.notes.append(note)
            time += beat_duration

        # Verse (40 beats): Walking bassline with sync to melody
        for beat in range(40):
            chord_idx = beat // 4 % 4
            root = verse_chords[chord_idx]
            if beat % 4 == 0:
                velocity = 90 + (10 if mood == "energetic" else 0) + (beat % 8 * 2) % 20
                note = pretty_midi.Note(velocity=velocity, pitch=root - 12, start=time, end=time + beat_duration * 1.5)
                bass.notes.append(note)
            elif beat % 4 == 2:
                note = pretty_midi.Note(velocity=velocity - 10, pitch=root - 12 + 2, start=time, end=time + beat_duration)
                bass.notes.append(note)
            elif beat % 4 == 3 and mood != "melancholic":
                note = pretty_midi.Note(velocity=velocity - 15, pitch=root - 12 + 4, start=time, end=time + beat_duration)
                bass.notes.append(note)
            time += beat_duration

        # Chorus (48 beats): Syncopated bass with energy
        for beat in range(48):
            chord_idx = beat // 4 % 4
            root = chorus_chords[chord_idx]
            if beat % 2 == 0:
                velocity = 100 + (20 if mood == "happy" else 0) + (beat % 8 * 3) % 30
                note = pretty_midi.Note(velocity=velocity, pitch=root - 12, start=time, end=time + beat_duration * 1.5)
                bass.notes.append(note)
            elif beat % 4 == 1:
                note = pretty_midi.Note(velocity=velocity - 20, pitch=root - 12 + (2 if beat % 8 == 1 else 0), start=time, end=time + beat_duration)
                bass.notes.append(note)
            time += beat_duration

        # Outro (16 beats): Fade out with sustained notes
        for beat in range(16):
            chord_idx = beat // 4 % 4
            root = verse_chords[chord_idx]
            if beat % 4 == 0:
                velocity = max(50 - (beat * 3), 20)
                note = pretty_midi.Note(velocity=velocity, pitch=root - 12, start=time, end=time + beat_duration * 3)
                bass.notes.append(note)
            time += beat_duration

        # Drums: Realistic patterns synced with melody and bass
        drums = pretty_midi.Instrument(program=0, is_drum=True)
        time = 0
        # Intro (16 beats): Build-up with hi-hat
        for beat in range(16):
            chord_idx = beat // 4 % 4
            if beat % 4 == 0:
                kick = pretty_midi.Note(velocity=70 + (beat // 4 * 5), pitch=36, start=time, end=time + 0.2)
                drums.notes.append(kick)
            if beat % 2 == 0:
                hihat = pretty_midi.Note(velocity=60 + (beat // 4 * 2), pitch=42, start=time, end=time + 0.1)
                drums.notes.append(hihat)
            time += beat_duration

        # Verse (40 beats): Steady groove with fills
        for beat in range(40):
            chord_idx = beat // 4 % 4
            if beat % 4 == 0:  # Kick on downbeat
                kick = pretty_midi.Note(velocity=90 + (10 if mood == "energetic" else 0), pitch=36, start=time, end=time + 0.2)
                drums.notes.append(kick)
            if beat % 4 == 2:  # Snare on 2 and 4
                snare = pretty_midi.Note(velocity=80 + (beat % 8 * 2) % 20, pitch=38, start=time, end=time + 0.2)
                drums.notes.append(snare)
            if beat % 2 == 0:  # Hi-hat
                hihat = pretty_midi.Note(velocity=60, pitch=42, start=time + 0.25, end=time + 0.35)
                drums.notes.append(hihat)
            if beat % 8 == 7 and mood != "melancholic":  # Fill at end of phrase
                tom = pretty_midi.Note(velocity=70, pitch=41, start=time + 0.25, end=time + 0.35)
                drums.notes.append(tom)
            time += beat_duration

        # Chorus (48 beats): Full groove with crash and fills
        for beat in range(48):
            chord_idx = beat // 4 % 4
            if beat % 4 == 0:
                kick = pretty_midi.Note(velocity=100 + (20 if mood == "happy" else 0), pitch=36, start=time, end=time + 0.2)
                drums.notes.append(kick)
                if beat % 8 == 0:
                    crash = pretty_midi.Note(velocity=80, pitch=49, start=time, end=time + 0.3)
                    drums.notes.append(crash)
            if beat % 4 == 2:
                snare = pretty_midi.Note(velocity=90 + (beat % 8 * 3) % 30, pitch=38, start=time, end=time + 0.2)
                drums.notes.append(snare)
            if beat % 2 == 0:
                hihat = pretty_midi.Note(velocity=70 + (10 if mood == "energetic" else 0), pitch=42, start=time + 0.25, end=time + 0.35)
                drums.notes.append(hihat)
            if beat % 8 == 6:
                tom = pretty_midi.Note(velocity=80, pitch=41, start=time + 0.25, end=time + 0.35)
                drums.notes.append(tom)
            time += beat_duration

        # Outro (16 beats): Fade out with sparse hits
        for beat in range(16):
            chord_idx = beat // 4 % 4
            if beat % 4 == 0:
                kick = pretty_midi.Note(velocity=max(40 - (beat * 3), 20), pitch=36, start=time, end=time + 0.2)
                drums.notes.append(kick)
            if beat % 2 == 0:
                hihat = pretty_midi.Note(velocity=max(50 - (beat * 3), 20), pitch=42, start=time, end=time + 0.1)
                drums.notes.append(hihat)
            time += beat_duration

        midi.instruments.append(bass)
        midi.instruments.append(drums)
        midi.write(output_midi)
        logger.debug(f"Saved with bass & drums: {output_midi}")
    except Exception as e:
        logger.error(f"Failed to add instruments: {e}")
        raise Exception(f"Failed to add instruments: {e}")

# Uncomment to test standalone
# if __name__ == "__main__":
#     add_instruments_to_melody("static/melody.mid", "static/full_song.mid", "love", "happy", "pop")