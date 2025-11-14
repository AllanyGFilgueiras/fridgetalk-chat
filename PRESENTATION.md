## Presentation assets & GIF instructions

This file explains how to record a short demo GIF (recommended 4–6 seconds) and optimize it for GitHub and Hugging Face Spaces.

### Recommended flow to record

1. On macOS: open QuickTime Player → File → New Screen Recording.
2. Select the region of the app in your browser (or the whole screen) and record a short flow:
   - Click the ingredients textbox, type: `ovos, tomate, queijo`
   - Click "Gerar receita" and wait for the assistant to respond
   - Stop the recording when the assistant reply is visible (4–6s total recommended)
3. Save the recording as `demo.mov`.

### Convert and optimize with ffmpeg

Install ffmpeg (Homebrew):

```bash
brew install ffmpeg
```

Convert `demo.mov` to GIF optimized for web:

```bash
# Create a 15 fps, scaled GIF (width 800 px) with palette for quality
ffmpeg -y -i demo.mov -vf "fps=15,scale=800:-1:flags=lanczos,palettegen" -y palette.png
ffmpeg -i demo.mov -i palette.png -lavfi "fps=15,scale=800:-1:flags=lanczos[x];[x][1:v]paletteuse" -y demo.gif

# Optionally reduce filesize with gifsicle (brew install gifsicle)
gifsicle -O3 --colors 128 demo.gif -o demo-opt.gif
```

### Tips

- Keep the GIF short (4–6s) to keep filesize small.
- Use 800px width for clarity; smaller widths load faster.
- If the GIF is large, prefer linking to a short MP4 instead — GitHub renders GIFs inline but MP4 is more efficient.

### Adding the GIF to the repo

1. Move the final optimized GIF into `assets/` (e.g., `assets/demo.gif`).
2. Commit and push:

```bash
git add assets/demo.gif
git commit -m "docs(presentation): add demo GIF showing UI flow"
git push origin main
```

After pushing, update `README.md` or `README_en.md` to reference `assets/demo.gif` (replace the placeholder SVG). The hosted Hugging Face Space will pick up the README front-matter and display the README on the Space page.
