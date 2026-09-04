from pathlib import Path
import json

from AI.analyzer import analyze_conversation


model = None


def get_model():
    """Load Whisper only when audio analysis is requested."""
    global model
    if model is None:
        try:
            from faster_whisper import WhisperModel
        except ImportError as error:
            raise RuntimeError(
                "Voice analysis is not configured on this server. Install faster-whisper to enable it."
            ) from error

        model = WhisperModel("small", device="cpu", compute_type="int8")
    return model


def transcribe_audio(audio_path):
    """
    Transcribe audio using faster-whisper.

    The model automatically detects the spoken language.

    Returns:
        dict: Standardized audio output.
    """

    try:
        segments, info = get_model().transcribe(
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
            "error": str(error) if "not configured" in str(error) else "We could not transcribe this recording. Please try a clearer audio file."
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
