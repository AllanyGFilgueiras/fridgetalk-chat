# FridgeTalk — Smart Recipe Assistant

Demonstration-ready Gradio app that turns a list of ingredients into a practical recipe.

## Overview

FridgeTalk accepts a quick list of ingredients and returns a suggested recipe with a name and step-by-step instructions. This repository is prepared for interview demos: it includes a demo-mode fallback so reviewers can see the UI and user flow even without an AI key.

## Highlights

- Clean, responsive Gradio interface
- Demo-mode fallback (works offline, no API key required)
- Clear, user-facing error messages and guidance for reviewers
- Unit tests and CI to demonstrate engineering best practices

## Quick start (local)

```bash
git clone <your-repo-url>
cd fridge-talk
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://localhost:7860 in your browser.

## Demo mode

- Toggle "Usar modo demo" in the UI to generate sample recipes without any API key.
- Or set the environment variable:

```bash
export DEMO_MODE=1
python app.py
```

## Enable AI provider (optional)

To enable OpenAI, set `OPENAI_API_KEY` in your environment or add it to your Hugging Face Space Secrets. The app will automatically fall back to demo mode if the provider is unavailable or the key is not present.

## Presentation materials

- `assets/screenshot-placeholder.svg` — replace with a real screenshot
- `assets/gif-placeholder.svg` — placeholder for a short demo GIF. See `PRESENTATION.md` for instructions on how to record and optimize a GIF for GitHub and the HF Space.

## Contributing

See `CONTRIBUTING.md` for contribution guidelines and project conventions.

## License

MIT — see `LICENSE`
