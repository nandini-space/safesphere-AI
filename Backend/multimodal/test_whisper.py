from pathlib import Path

from faster_whisper import WhisperModel


# Load a small multilingual Whisper model.
# CPU + int8 keeps the laptop workload reasonable.
model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)


project_folder = Path(__file__).resolve().parents[2]
audio_path = project_folder / "test_audio_hindi.wav"


if not audio_path.exists():
    print(f"Audio not found: {audio_path}")

else:
    print("Transcribing audio...")

    segments, info = model.transcribe(
        str(audio_path),
        beam_size=5
    )

    transcript = " ".join(
        segment.text.strip()
        for segment in segments
    ).strip()

    print("\n===== WHISPER RESULT =====\n")
    print("Detected language:", info.language)
    print("Language probability:", info.language_probability)
    print("Transcript:", transcript)