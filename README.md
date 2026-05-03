# Supertonic Desktop TTS (Linux/GNOME)

A dead-simple local desktop app: type text, press **Play**, hear speech.

- Fully local (no cloud APIs, no telemetry)
- Python + Tkinter GUI
- Uses official `supertonic` package locally (ONNX Runtime under the hood)

## Files

- `app.py` - the GUI app
- `run-supertonic-tts.sh` - click-friendly launcher script
- `supertonic-tts.desktop` - GNOME launcher entry

---

## One-time setup (Fedora 43)

### 1) Install system packages

```bash
sudo dnf install -y python3 python3-tkinter ffmpeg git
```

### 2) Create virtual environment and install Supertonic

From this project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install supertonic
```

### 3) Download Supertonic model assets once

Use the official package helper (it will place assets locally for offline use afterward):

```bash
supertonic assets download
```

> After this step, everyday TTS is local/offline.

### 4) Install clickable GNOME launcher

```bash
mkdir -p ~/.local/share/applications
cp supertonic-tts.desktop ~/.local/share/applications/
chmod +x run-supertonic-tts.sh
```

Edit `~/.local/share/applications/supertonic-tts.desktop` and set:

- `Exec=` to your real project path + `/run-supertonic-tts.sh`
- `Path=` to your real project path

(Optional) Trust launcher in GNOME file manager if prompted.

---

## Everyday usage (no terminal)

- Open GNOME app grid/search
- Launch **Supertonic TTS**
- Type or paste text
- Click **Play**

That is it.

---

## Optional voice selection

The dropdown includes common voice IDs (`F1`, `M1`, `F2`, `M2`, ...).
If an unavailable voice is selected, the app shows an error dialog.

---

## Privacy / network behavior

- Runtime synthesis is fully local.
- No telemetry/analytics/background service is added by this app.
- Only one-time setup may require network (installing packages + model assets).
