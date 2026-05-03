#!/usr/bin/env python3
"""Minimal local Supertonic desktop TTS app for Linux (GNOME-friendly)."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import threading
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

DEFAULT_VOICES = ["F1", "M1", "F2", "M2", "M3", "M4", "M5", "F3", "F4", "F5"]


class TTSApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Supertonic TTS")
        self.root.geometry("560x380")

        self.voice_var = tk.StringVar(value=os.environ.get("SUPERTONIC_VOICE", "F1"))
        self.status_var = tk.StringVar(value="Ready")

        container = ttk.Frame(root, padding=12)
        container.pack(fill="both", expand=True)

        voice_row = ttk.Frame(container)
        voice_row.pack(fill="x", pady=(0, 8))
        ttk.Label(voice_row, text="Voice:").pack(side="left")

        self.voice_box = ttk.Combobox(voice_row, textvariable=self.voice_var, values=DEFAULT_VOICES, width=8, state="readonly")
        self.voice_box.pack(side="left", padx=(8, 0))

        self.text_box = tk.Text(container, wrap="word", height=14)
        self.text_box.pack(fill="both", expand=True)

        controls = ttk.Frame(container)
        controls.pack(fill="x", pady=(8, 0))

        self.play_button = ttk.Button(controls, text="Play", command=self.on_play)
        self.play_button.pack(side="left")
        ttk.Label(controls, textvariable=self.status_var).pack(side="right")

    def on_play(self) -> None:
        text = self.text_box.get("1.0", "end").strip()
        if not text:
            messagebox.showwarning("No text", "Please enter some text first.")
            return

        self.play_button.configure(state="disabled")
        self.status_var.set("Synthesizing...")
        threading.Thread(target=self._synthesize_and_play, args=(text,), daemon=True).start()

    def _play_wav(self, wav_path: Path) -> None:
        players = [
            ["paplay", str(wav_path)],
            ["aplay", str(wav_path)],
            ["ffplay", "-nodisp", "-autoexit", "-loglevel", "error", str(wav_path)],
        ]
        for cmd in players:
            if shutil.which(cmd[0]):
                subprocess.run(cmd, check=True, capture_output=True, text=True)
                return
        raise FileNotFoundError("paplay/aplay/ffplay")

    def _synthesize_and_play(self, text: str) -> None:
        wav_path: Path | None = None
        try:
            voice = self.voice_var.get().strip() or "F1"
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                wav_path = Path(tmp.name)

            subprocess.run(["supertonic", "tts", text, "--voice", voice, "-o", str(wav_path)], check=True, capture_output=True, text=True)
            self._play_wav(wav_path)
            self.root.after(0, lambda: self.status_var.set("Done"))
        except FileNotFoundError as exc:
            self.root.after(0, lambda: messagebox.showerror("Missing dependency", f"Missing command: {exc}\n\nInstall dependencies from README and try again."))
            self.root.after(0, lambda: self.status_var.set("Error"))
        except subprocess.CalledProcessError as exc:
            err = (exc.stderr or exc.stdout or str(exc)).strip()
            self.root.after(0, lambda: messagebox.showerror("TTS failed", err[:1200]))
            self.root.after(0, lambda: self.status_var.set("Error"))
        finally:
            if wav_path and wav_path.exists():
                try:
                    wav_path.unlink()
                except OSError:
                    pass
            self.root.after(0, lambda: self.play_button.configure(state="normal"))


def main() -> None:
    root = tk.Tk()
    TTSApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
