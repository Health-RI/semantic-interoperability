from pathlib import Path
import re
import sys
import wave


# If you run this script from the parent folder, it will use ./audio-wav.
# If you run it from inside audio-wav, it will use the current folder.
AUDIO_DIR_NAME = "audio-wav"

OUTPUT_AUDIO = Path("combined_audio.wav")
SILENCE_SECONDS = 0.30
ADD_SILENCE_AFTER_LAST = True


def detect_audio_dir() -> Path:
    current = Path(".")

    if (current / AUDIO_DIR_NAME).is_dir():
        return current / AUDIO_DIR_NAME

    if list(current.glob("slide *.wav")):
        return current

    sys.exit(
        "Error: could not find WAV files.\n"
        "Run this script either:\n"
        "  1. from the parent folder containing ./audio-wav, or\n"
        "  2. from inside the audio-wav folder."
    )


def slide_number(path: Path) -> int:
    match = re.fullmatch(r"slide (\d+)\.wav", path.name, flags=re.IGNORECASE)

    if not match:
        raise ValueError(f"Unexpected filename: {path.name}")

    return int(match.group(1))


def find_ordered_wav_files(audio_dir: Path) -> list[Path]:
    wav_files = list(audio_dir.glob("slide *.wav"))

    if not wav_files:
        sys.exit(f"Error: no WAV files found in {audio_dir.resolve()}")

    numbered_files = sorted(
        [(slide_number(path), path) for path in wav_files],
        key=lambda item: item[0],
    )

    numbers = [number for number, _ in numbered_files]
    expected_numbers = list(range(1, len(numbers) + 1))

    if numbers != expected_numbers:
        found = ", ".join(f"{n:02d}" for n in numbers)
        expected = ", ".join(f"{n:02d}" for n in expected_numbers)

        sys.exit(
            "Error: slide audio files are not consecutively numbered.\n"
            f"Found:    {found}\n"
            f"Expected: {expected}\n"
            "Check for missing or incorrectly named files."
        )

    return [path for _, path in numbered_files]


def get_wav_params(path: Path):
    with wave.open(str(path), "rb") as wav:
        return wav.getparams()


def get_wav_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as wav:
        return wav.getnframes() / wav.getframerate()


def validate_compatible_wavs(wav_files: list[Path]) -> wave._wave_params:
    first_params = get_wav_params(wav_files[0])

    for path in wav_files[1:]:
        params = get_wav_params(path)

        if (
            params.nchannels != first_params.nchannels
            or params.sampwidth != first_params.sampwidth
            or params.framerate != first_params.framerate
            or params.comptype != first_params.comptype
        ):
            sys.exit(
                "Error: WAV files do not all have the same audio format.\n\n"
                f"First file: {wav_files[0].name}\n"
                f"  {first_params}\n\n"
                f"Different file: {path.name}\n"
                f"  {params}\n\n"
                "Reconvert all files using the same settings before concatenating."
            )

    if first_params.comptype != "NONE":
        sys.exit(
            "Error: WAV files are compressed. This script expects uncompressed PCM WAV files."
        )

    return first_params


def concatenate_with_silence(
    wav_files: list[Path],
    output_path: Path,
    silence_seconds: float,
    add_silence_after_last: bool,
) -> None:
    params = validate_compatible_wavs(wav_files)

    silence_frames = round(silence_seconds * params.framerate)
    silence_bytes = b"\x00" * silence_frames * params.nchannels * params.sampwidth

    with wave.open(str(output_path), "wb") as output:
        output.setparams(params)

        for index, wav_path in enumerate(wav_files, start=1):
            with wave.open(str(wav_path), "rb") as source:
                frames = source.readframes(source.getnframes())
                output.writeframes(frames)

            is_last = index == len(wav_files)

            if add_silence_after_last or not is_last:
                output.writeframes(silence_bytes)


def main() -> None:
    audio_dir = detect_audio_dir()
    wav_files = find_ordered_wav_files(audio_dir)

    print(f"Audio folder: {audio_dir.resolve()}")
    print(f"Files found: {len(wav_files)}")
    print(f"Safeguard after each slide: {SILENCE_SECONDS:.2f} seconds")
    print(f"Add safeguard after last slide: {ADD_SILENCE_AFTER_LAST}")
    print()

    durations = [get_wav_duration(path) for path in wav_files]

    for index, (path, duration) in enumerate(zip(wav_files, durations), start=1):
        print(f"Slide {index:02d}: {path.name} = {duration:.2f}s")

    number_of_silences = (
        len(wav_files) if ADD_SILENCE_AFTER_LAST else len(wav_files) - 1
    )
    expected_duration = sum(durations) + number_of_silences * SILENCE_SECONDS

    concatenate_with_silence(
        wav_files=wav_files,
        output_path=OUTPUT_AUDIO,
        silence_seconds=SILENCE_SECONDS,
        add_silence_after_last=ADD_SILENCE_AFTER_LAST,
    )

    actual_duration = get_wav_duration(OUTPUT_AUDIO)

    print()
    print(f"Expected duration: {expected_duration:.2f} seconds")
    print(f"Actual duration:   {actual_duration:.2f} seconds")
    print(f"Difference:        {actual_duration - expected_duration:+.3f} seconds")
    print()
    print(f"Done: {OUTPUT_AUDIO.resolve()}")


if __name__ == "__main__":
    main()
