# Supertonic Desktop TTS (Linux/GNOME)

A dead-simple local desktop app: type text, press **Play**, hear speech.

## One-time setup (Fedora 43)

### 1) Install required packages

```bash
sudo dnf install -y python3 python3-tkinter pulseaudio-utils alsa-utils git
```

> Why no `ffmpeg` here: on some Fedora 43 systems with RPM Fusion, `ffmpeg` can conflict with installed `ffmpeg-free` packages. This app works without ffmpeg by using `paplay`/`aplay`.

### 2) Create virtual environment + install Supertonic

```bash
cd /path/to/supertonic-desktop-linux
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install supertonic
```

### 3) Download model assets one time

```bash
supertonic assets download
```

After this, synthesis runs locally/offline.

### 4) Install GNOME launcher (click-to-run)

```bash
cd /path/to/supertonic-desktop-linux
mkdir -p ~/.local/share/applications
APP_DIR="$(pwd)"
sed "s|__APP_DIR__|$APP_DIR|g" supertonic-tts.desktop > ~/.local/share/applications/supertonic-tts.desktop
chmod +x run-supertonic-tts.sh
update-desktop-database ~/.local/share/applications >/dev/null 2>&1 || true
```

Now launch from GNOME app grid/search: **Supertonic TTS**.

## Everyday usage (zero terminal)

1. Open GNOME app grid (or press Super key and search).
2. Open **Supertonic TTS**.
3. Enter text.
4. Press **Play**.

## Notes

- Fully local runtime: no cloud API calls from this app.
- No telemetry or background service.
- Voice dropdown includes common voice IDs (`F1`, `M1`, `F2`, ...). If a voice is unavailable, the app shows an error dialog.
