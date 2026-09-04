from pathlib import Path
import json

from faster_whisper import WhisperModel

from Backend.AI.analyzer import analyze_conversation


# Load Whisper once when the module starts.
# "small" gives a good balance between accuracy and speed.
model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)


def transcribe_audio(audio_path):
    """
    Transcribe audio using faster-whisper.

    The model automatically detects the spoken language.

    Returns:
        dict: Standardized audio output.
    """

    try:
        segments, info = model.transcribe(
            str(audio_path),
            beam_size=5
        )

        # Combine all transcript segments
        transcript = " ".join(
            segment.text.strip()
            for segment in segments
        ).strip()

        if not transcript:
            return {
                "input_type": "audio",
                "text": "",
                "language": "unknown",
                "error": "No speech could be transcribed from the audio"
            }

        return {
            "input_type": "audio",
            "text": transcript,
            "language": info.language,
            "language_probability": info.language_probability
        }

    except Exception as error:
        return {
            "input_type": "audio",
            "text": "",
            "language": "unknown",
            "error": f"Audio transcription failed: {error}"
        }


def analyze_audio(audio_path):
    """
    Transcribe audio, detect its language automatically,
    and send the transcript to the SafeSphere AI analyzer.
    """

    # Step 1: Audio → transcript
    transcription = transcribe_audio(audio_path)

    if transcription.get("error"):
        return transcription

    text = transcription["text"]

    # Step 2: Send transcript to Member 2
    analysis = analyze_conversation(text)

    # Step 3: Return standardized SafeSphere result
    return {
        "input_type": "audio",
        "extracted_text": text,
        "language": transcription.get("language", "unknown"),
        "language_probability": transcription.get(
            "language_probability",
            0
        ),
        "analysis": analysis
    }


if __name__ == "__main__":
    project_folder = Path(__file__).resolve().parents[2]

    # Change this filename whenever you want to test
    # a different audio file. No language code is required.
    audio_path = project_folder / "test_audio_hindi.wav"

    if not audio_path.exists():
        print(f"Audio not found: {audio_path}")

    else:
        result = analyze_audio(audio_path)

        print("\n===== AUDIO PIPELINE OUTPUT =====\n")
        print(json.dumps(result, indent=4, ensure_ascii=False))