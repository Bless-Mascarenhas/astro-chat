# ✦ AstroChat — Cosmic AI Astrology Guide

A beautiful AI-powered astrology chatbot that runs **100% locally** using [Ollama](https://ollama.com) and `qwen3.5:4b`.

![AstroChat UI](https://img.shields.io/badge/Model-qwen3.5%3A4b-a78bfa?style=for-the-badge&logo=ollama)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-f472b6?style=for-the-badge)

---

## Features

- 🔮 **Cosmic dark UI** with nebula background, floating animations & purple gradients
- 🤖 **Powered by qwen3.5:4b** running locally via Ollama — no API keys needed
- 💬 **Real-time streaming** responses
- ♈–♓ **Astrology-focused** system prompt (birth charts, zodiac, transits, compatibility, etc.)
- 📜 **Scrollable chat history** with styled scrollbar
- 🚀 **Quick suggestion buttons** to get started instantly
- 🌐 **Optional public sharing** via Cloudflare Tunnel

---

## Requirements

- [Python 3.8+](https://python.org)
- [Ollama](https://ollama.com/download) installed and running
- `qwen3.5:4b` model pulled

---

## Quick Start

### 1. Install Ollama & pull the model
```bash
# Download Ollama from https://ollama.com/download
ollama pull qwen3.5:4b
```

### 2. Clone this repo
```bash
git clone https://github.com/YOUR_USERNAME/astro-chat.git
cd astro-chat
```

### 3. Start the app
**Option A — Double-click `start.bat`** (Windows, recommended)

**Option B — Manual:**
```bash
# Terminal 1: start Ollama
ollama serve

# Terminal 2: start the web server
python server.py
```

### 4. Open in browser
```
http://localhost:8080
```

---

## Share Publicly (Optional)

To share with others using Cloudflare Tunnel (free, no account needed):

```bash
# Download cloudflared from https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
cloudflared tunnel --url http://localhost:8080
```

You'll get a public URL like: `https://random-name.trycloudflare.com`

---

## Project Structure

```
astro-chat/
├── index.html      # Full chatbot UI (HTML + CSS + JS)
├── server.py       # Python proxy server (serves UI + forwards to Ollama)
├── start.bat       # One-click launcher for Windows
└── README.md
```

---

## How It Works

```
Browser → http://localhost:8080
           ↓ POST /api/chat
       server.py (Python proxy)
           ↓ forwards to
       Ollama (localhost:11434)
           ↓ runs
       qwen3.5:4b (local model)
```

The proxy server eliminates CORS issues and keeps the model call fully local.

---

## License

MIT — free to use, modify, and share.
