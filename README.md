---
title: "FridgeTalk Chat"
emoji: "🧊"
colorFrom: yellow
colorTo: purple
sdk: gradio
app_file: app.py
pinned: false
---
---

# 🧊 FridgeTalk Chat

FridgeTalk sugere receitas práticas com base nos ingredientes que você tem disponível. O foco é simplicidade, clareza e uma experiência agradável para o usuário.

Visão geral
- Entrada: texto com ingredientes (ex.: ovos, tomate, queijo)
- Saída: nome da receita e modo de preparo passo a passo
- Comportamento: tenta usar um provedor de IA quando configurado; caso contrário, usa o modo demo local

Recursos principais
- 🎛️ Interface única com sugestões de ingredientes e dicas rápidas
- 🔁 Fallback automático para modo demo quando a IA não está disponível
- 🧪 Testes unitários básicos para validar fluxo demo e mensagens ao usuário

Imagem
![Screenshot](assets/demo.png)

Como executar localmente
```bash
git clone <seu-repo-url>
cd fridgetalk-chat
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Abra http://localhost:7860 no navegador.

Executar testes
```bash
python3 -m pytest -q
```

Modo demo
- Marque "Usar modo demo" na interface para gerar receitas locais sem necessidade de chaves.
- Ou defina a variável de ambiente:

```bash
export DEMO_MODE=1
python app.py
```

Usando provedor de IA (opcional)
- Para habilitar chamadas reais ao OpenAI, defina `OPENAI_API_KEY` como variável de ambiente ou adicione como Secret na Hugging Face Space.
- O aplicativo faz fallback automático para o modo demo quando o provedor não está disponível.

Estrutura do repositório
- `app.py` — aplicação Gradio com fallback demo e mensagens de erro amigáveis
- `requirements.txt` — dependências (Gradio, OpenAI, pytest)
- `tests/` — testes unitários (pytest)
- `assets/` — imagens e placeholders
- `.github/workflows/ci.yml` — workflow básico de CI (testes)
- `LICENSE` — MIT

Deploy na Hugging Face Space
- O front matter acima já está pronto para Spaces (SDK Gradio e `app.py`).
- Adicione `OPENAI_API_KEY` e demais variáveis necessárias em **Settings → Variables & secrets**.
- Use `PRESENTATION.md` como guia para gravar um GIF/MP4 curto e atualize `assets/demo.png` ou adicione um GIF otimizado se quiser animação.
- Caso esteja em macOS com Python 3.14+, instale `libjpeg` (via `brew install jpeg`) antes de `pip install -r requirements.txt` para permitir a compilação do Pillow.

Boas práticas para apresentação
- Ao apresentar, abra a Space ou rode localmente.
- Use o modo demo para garantir resposta imediata.
- Se for demonstrar a IA, mostre como a integração muda o comportamento ao adicionar `OPENAI_API_KEY`.

Contribuições
- Veja `CONTRIBUTING.md`.

Licença
- MIT — consulte `LICENSE`
