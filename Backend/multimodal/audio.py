from pathlib import Path
import json
import os
import shutil

from AI.analyzer import analyze_conversation


model = None


def get_model():
    """Load Whisper only when audio analysis is requested."""
    global model
    if model is None:
        print("[VOICE] loading Whisper model", flush=True)
        try:
            from faster_whisper import WhisperModel
        except ImportError as error:
            raise RuntimeError(
                "Voice transcription is unavailable: faster-whisper is not installed on the server."
            ) from error

        model = WhisperModel(
            os.getenv("WHISPER_MODEL", "tiny"),
            device="cpu",
            compute_type="int8",
        )
        print("[VOICE] Whisper model loaded", flush=True)
    return model


def transcribe_audio(audio_path):
    """
    Transcribe audio using faster-whisper.

    The model automatically detects the spoken language.

    Returns:
        dict: Standardized audio output.
    """

    try:
        print("[VOICE] ffmpeg:", shutil.which("ffmpeg") or "not found; PyAV decoder will be used", flush=True)
        segments, info = get_model().transcribe(
            str(audio_path),
            beam_size=1,
            vad_filter=True,
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

        print("[VOICE] transcription completed", flush=True)
        return {
            "input_type": "audio",
            "text": transcript,
            "language": info.language,
            "language_probability": info.language_probability
        }

    except Exception as error:
        print(f"[VOICE] transcription exception [{type(error).__name__}]: {error}", flush=True)
        return {
            "input_type": "audio",
            "text": "",
            "language": "unknown",
            "error": "Voice transcription failed",
            "detail": str(error),
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
    print("[VOICE] AI analysis started", flush=True)
    analysis = analyze_conversation(text)
    print("[VOICE] AI analysis completed", flush=True)

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
