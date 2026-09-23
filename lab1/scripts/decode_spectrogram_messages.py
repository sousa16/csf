"""Decode visual messages hidden in the stereo side channel of a WAV file.

The Lab 1 audio hides text in the spectrogram of (left - right) / 2, mainly in
18-22 kHz. This script creates an overview followed by readable time tiles.
It never modifies the input audio.
"""

from __future__ import annotations

import argparse
import csv
import wave
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audio", type=Path)
    parser.add_argument("--out", type=Path, default=Path("spectrogram-messages"))
    parser.add_argument("--band-low", type=float, default=18_000.0)
    parser.add_argument("--band-high", type=float, default=22_000.0)
    parser.add_argument("--tile-seconds", type=float, default=50.0)
    parser.add_argument("--start-offset", type=float, default=0.0, help="seconds to skip before the first tile")
    parser.add_argument("--overview-seconds", type=float, default=500.0)
    parser.add_argument("--nfft", type=int, default=16_384)
    parser.add_argument("--hop", type=int, default=4_096)
    parser.add_argument("--vmin", type=float, default=-100.0, help="lower fixed dB limit")
    parser.add_argument("--vmax", type=float, default=-60.0, help="upper fixed dB limit")
    parser.add_argument("--dpi", type=int, default=180)
    return parser.parse_args()


def load_stereo_wav(path: Path) -> tuple[np.ndarray, int]:
    with wave.open(str(path), "rb") as source:
        if source.getnchannels() != 2:
            raise ValueError("Expected stereo audio")
        if source.getsampwidth() != 2:
            raise ValueError("Expected 16-bit PCM audio")
        rate = source.getframerate()
        raw = source.readframes(source.getnframes())

    samples = np.frombuffer(raw, dtype="<i2").reshape(-1, 2).astype(np.float32) / 32768.0
    side = (samples[:, 0] - samples[:, 1]) / 2.0
    return side, rate


def spectrum(samples: np.ndarray, rate: int, nfft: int, hop: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if len(samples) < nfft:
        raise ValueError("The selected interval is shorter than --nfft")
    count = 1 + (len(samples) - nfft) // hop
    starts = np.arange(count)[:, None] * hop
    offsets = np.arange(nfft)[None, :]
    window = np.hanning(nfft)
    frames = samples[starts + offsets] * window[None, :]
    spectrum = np.fft.rfft(frames, axis=1)
    power = np.abs(spectrum) ** 2 / (rate * np.sum(window ** 2))
    power[:, 1:-1] *= 2.0
    power_db = 10.0 * np.log10(np.maximum(power, 1e-14)).T
    frequency = np.fft.rfftfreq(nfft, 1.0 / rate)
    time = (np.arange(count) * hop + nfft / 2) / rate
    return time, frequency, power_db


def render(
    samples: np.ndarray,
    rate: int,
    path: Path,
    title: str,
    low: float,
    high: float,
    nfft: int,
    hop: int,
    vmin: float,
    vmax: float,
    dpi: int,
) -> None:
    time, frequency, power = spectrum(samples, rate, nfft, hop)
    mask = (frequency >= low) & (frequency <= high)
    frequency = frequency[mask]
    power = power[mask]

    figure, axis = plt.subplots(figsize=(18, 7), constrained_layout=True, facecolor="black")
    axis.set_facecolor("black")
    image = axis.pcolormesh(
        time,
        frequency / 1000.0,
        power,
        shading="auto",
        cmap="inferno",
        vmin=vmin,
        vmax=vmax,
    )
    axis.set_title(title)
    axis.set_xlabel("Time (seconds)")
    axis.set_ylabel("Frequency (kHz)")
    axis.set_ylim(low / 1000.0, high / 1000.0)
    figure.colorbar(image, ax=axis, label="Magnitude (dB)")
    figure.savefig(path, dpi=dpi, facecolor="black")
    plt.close(figure)


def main() -> None:
    args = arguments()
    if not 0 < args.band_low < args.band_high:
        raise SystemExit("Require 0 < --band-low < --band-high")
    if args.tile_seconds <= 0 or args.overview_seconds <= 0:
        raise SystemExit("Durations must be positive")

    side, rate = load_stereo_wav(args.audio)
    nyquist = rate / 2.0
    if args.band_high > nyquist:
        raise SystemExit(f"--band-high must not exceed the Nyquist frequency ({nyquist:g} Hz)")

    args.out.mkdir(parents=True, exist_ok=True)
    duration = len(side) / rate
    records: list[dict[str, str]] = []

    overview_end = min(args.overview_seconds, duration)
    overview_path = args.out / f"overview_0000-{overview_end:07.2f}s.png"
    render(
        side[: int(overview_end * rate)],
        rate,
        overview_path,
        f"Spectrograma - SIDE (L - R) / 2 - 0-{overview_end:.2f}s",
        args.band_low,
        args.band_high,
        args.nfft,
        args.hop,
        args.vmin,
        args.vmax,
        args.dpi,
    )
    records.append({"file": overview_path.name, "kind": "overview", "start_s": "0.000", "end_s": f"{overview_end:.3f}"})

    if args.start_offset < 0 or args.start_offset >= duration:
        raise SystemExit("--start-offset must be within the audio duration")

    start = args.start_offset
    tile_number = 0
    while start < duration:
        end = min(start + args.tile_seconds, duration)
        chunk = side[int(start * rate) : int(end * rate)]
        if len(chunk) < args.nfft:
            break
        path = args.out / f"tile_{tile_number:04d}_{start:07.2f}-{end:07.2f}s.png"
        render(
            chunk,
            rate,
            path,
            f"Spectrograma - SIDE (L - R) / 2 - {start:.2f}-{end:.2f}s",
            args.band_low,
            args.band_high,
            args.nfft,
            args.hop,
            args.vmin,
            args.vmax,
            args.dpi,
        )
        records.append({"file": path.name, "kind": "tile", "start_s": f"{start:.3f}", "end_s": f"{end:.3f}"})
        start += args.tile_seconds
        tile_number += 1

    with (args.out / "index.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=["file", "kind", "start_s", "end_s"])
        writer.writeheader()
        writer.writerows(records)

    print(f"side channel: (left - right) / 2")
    print(f"duration: {duration:.3f} s; sample rate: {rate} Hz")
    print(f"overview: {overview_path}")
    print(f"tiles: {tile_number}; index: {args.out / 'index.csv'}")


if __name__ == "__main__":
    main()
