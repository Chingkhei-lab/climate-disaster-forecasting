import os
from openai import OpenAI, APIError, APIConnectionError
from dotenv import load_dotenv

# 1. Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # Changed variable name

# 2. Gemini Model ID (for Google AI Studio)
MODEL_ID = "gemini-2.0-flash"  # Direct Google model ID

def generate_disaster_report(lat, lon, weather_data, risk_level):
    if not GOOGLE_API_KEY:
        return "⚠️ Error: GOOGLE_API_KEY missing from .env file"

    # 3. Connect to Google AI Studio's OpenAI-compatible endpoint
    client = OpenAI(
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key=GOOGLE_API_KEY,
        timeout=15,  # Slightly higher timeout for direct API
    )

    # Prepare Data
    current = weather_data.get('current', {})
    temp = current.get('temperature_2m', 'N/A')
    rain = current.get('rain', '0')
    wind = current.get('wind_speed_10m', '0')

    prompt = f"""
    Act as a Senior Disaster Response Official.
    
    **SITUATION:**
    - Location: {lat}, {lon}
    - Risk: {risk_level}
    - Weather: {temp}°C, Rain {rain}mm, Wind {wind}km/h.
    
    **MISSION:**
    Write a 3-bullet operational briefing (Threat, Action, Resources).
    Keep it urgent, professional, and under 50 words.
    """

    try:
        completion = client.chat.completions.create(
            model=MODEL_ID,
            messages=[{"role": "user", "content": prompt}],
            # No extra_headers needed for Google AI Studio
        )
        return completion.choices[0].message.content.strip()

    except APIError as e:
        return f"⚠️ API Error: {e.message}"
    except APIConnectionError:
        return "⚠️ Network Error: Could not connect to Google AI"
    except Exception as e:
        return f"⚠️ Unexpected Error: {str(e)}"

# --- TEST THE FUNCTION ---
if __name__ == "__main__":
    test_weather = {'current': {'temperature_2m': 30, 'rain': 5, 'wind_speed_10m': 20}}
    result = generate_disaster_report(24.94, 80.24, test_weather, "HIGH")
    print("\n--- FINAL OUTPUT ---")
    print(result)
