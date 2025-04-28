from flask import Flask, render_template, request, send_file
import os
from generate_music import generate_sample_melody
from drum_and_bass import add_instruments_to_melody
from lyrics_generator import generate_lyrics
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables (if any)
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    theme = request.form['theme']
    mood = request.form['mood']
    style = request.form['style']

    # Generate lyrics
    try:
        logger.debug(f"Generating lyrics for theme={theme}, mood={mood}, style={style}")
        lyrics = generate_lyrics(theme, mood, style)
        logger.debug("Lyrics generated successfully")
    except Exception as e:
        logger.error(f"Error generating lyrics: {e}")
        return f"Error generating lyrics: {e}", 500

    # Ensure static directory exists
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    if not os.path.exists(static_dir):
        logger.debug(f"Creating static directory at {static_dir}")
        os.makedirs(static_dir)

    # Generate music with absolute paths and user input
    melody_path = os.path.join(static_dir, 'melody.mid')
    full_song_path = os.path.join(static_dir, 'full_song.mid')

    try:
        logger.debug(f"Generating melody at {melody_path} with theme={theme}, mood={mood}, style={style}")
        generate_sample_melody(melody_path, theme, mood, style)
        if not os.path.exists(melody_path):
            logger.error(f"Melody MIDI file not created at {melody_path}")
            raise Exception(f"Melody MIDI file not created at {melody_path}")
        logger.debug(f"Melody file created at {melody_path}")
    except Exception as e:
        logger.error(f"Error in generate_sample_melody: {e}")
        return f"Error in generate_sample_melody: {e}", 500

    try:
        logger.debug(f"Adding instruments, input={melody_path}, output={full_song_path}, theme={theme}, mood={mood}, style={style}")
        add_instruments_to_melody(melody_path, full_song_path, theme, mood, style)
        if not os.path.exists(full_song_path):
            logger.error(f"Full song MIDI file not created at {full_song_path}")
            raise Exception(f"Full song MIDI file not created at {full_song_path}")
        logger.debug(f"Full song file created at {full_song_path}")
    except Exception as e:
        logger.error(f"Error in add_instruments_to_melody: {e}")
        return f"Error in add_instruments_to_melody: {e}", 500

    # Final verification before rendering
    if not os.path.exists(full_song_path):
        logger.error(f"Final check failed: Full song MIDI file not found at {full_song_path}")
        return f"Error: Final check failed, MIDI file not found at {full_song_path}", 500

    # Pass the MIDI file for download
    download_link = "static/full_song.mid"
    logger.debug(f"Returning template with download_link={download_link}")
    return render_template('index.html', lyrics=lyrics, download_link=download_link)

@app.route('/download')
def download():
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    full_song_path = os.path.join(static_dir, 'full_song.mid')
    if not os.path.exists(full_song_path):
        logger.error(f"MIDI file not found for download at {full_song_path}")
        return "Error: MIDI file not found for download.", 404
    logger.debug(f"Sending file for download: {full_song_path}")
    return send_file(full_song_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)