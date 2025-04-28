import google.generativeai as genai

# ✅ DIRECTLY SET YOUR GEMINI API KEY HERE
genai.configure(api_key="AIzaSyC3gCVc0LbnzbV_vozigQHYV9aY64PmIwQ")  # Replace with your real key

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-flash-latest")

def generate_lyrics(theme="love", mood="happy", style="pop"):
    try:
        prompt = f"""
        Write original song lyrics in English about '{theme}' in a '{mood}' mood and '{style}' style.
        The lyrics should include a chorus and at least two verses.
        """
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating lyrics: {e}"

# Test
if __name__ == "__main__":
    lyrics = generate_lyrics("dreams", "hopeful", "indie")
    print(lyrics)
