import logging
import os
import random
import typing

import gradio as gr
from openai import OpenAI


# Configure a simple logger for clearer runtime diagnostics (goes to container logs)
logger = logging.getLogger("fridgetalk")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)


def generate_demo_recipe(ingredients: str) -> str:
    """Return a realistic, formatted demo recipe string.

    This function provides deterministic-ish demo content for presentation purposes
    when the real AI backend is not available.
    """
    examples = [
        {
            "name": "Tortinha Rápida de Tomate e Queijo",
            "ingredients": ["tomate", "queijo", "ovo", "pão"],
            "steps": [
                "Pré-aqueça a frigideira em fogo médio.",
                "Pique o tomate e rale o queijo.",
                "Bata o ovo e misture com o queijo e tomate.",
                "Coloque a mistura sobre fatias de pão e toste por 2-3 minutos cada lado.",
                "Sirva quente com ervas frescas por cima."
            ],
        },
        {
            "name": "Omelete Tropical",
            "ingredients": ["ovo", "manga", "cebola", "pimenta"],
            "steps": [
                "Bata dois ovos com sal e pimenta.",
                "Refogue cebola até dourar, acrescente pedaços de manga.",
                "Adicione os ovos batidos e cozinhe até firmar.",
                "Dobre a omelete e sirva com salsa."
            ],
        },
        {
            "name": "Macarrão Improvisado com Alho e Azeite",
            "ingredients": ["macarrão", "alho", "azeite", "pimenta"],
            "steps": [
                "Cozinhe o macarrão conforme instruções da embalagem.",
                "Em uma frigideira, doure alho fatiado no azeite.",
                "Misture o macarrão cozido com o azeite e tempere.",
                "Finalize com pimenta e queijo ralado se disponível."
            ],
        },
    ]

    # Choose an example based on a hash of ingredients for variety
    seed = sum(ord(c) for c in (ingredients or ""))
    random.seed(seed)
    ex = random.choice(examples)

    result = [f"### {ex['name']}", ""]
    result.append(f"Ingredientes sugeridos: {', '.join(ex['ingredients'])}")
    result.append("")
    result.append("Modo de preparo:")
    for i, step in enumerate(ex["steps"], start=1):
        result.append(f"{i}. {step}")

    result.append("")
    result.append("Dica: ajuste os temperos ao seu gosto e substitua ingredientes conforme necessário.")
    return "\n".join(result)


def chat_with_fridge(ingredients: str, demo_override: typing.Optional[bool] = None) -> str:
    """Main entry point used by the UI and tests.

    Behavior:
    - If DEMO_MODE env var is set to a truthy value, or demo_override is True, return demo recipe.
    - Otherwise try OpenAI (with model fallback). On errors, return a user-friendly message and a demo recipe.
    """
    if not ingredients or not ingredients.strip():
        return "Por favor, digite os ingredientes que você tem. Ex: 'ovos, tomate, queijo'. 🍅🥦"

    # Demo mode via environment variable or function override
    env_demo = os.getenv("DEMO_MODE", "0").lower() in ("1", "true", "yes")
    if demo_override or env_demo:
        return generate_demo_recipe(ingredients)

    prompt = f"Crie uma receita criativa e prática usando: {ingredients}. Descreva o modo de preparo passo a passo e dê um nome divertido à receita."

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        # Friendly message for end users with a demo fallback suggestion
        logger.info("OPENAI_API_KEY not set; returning demo recipe for presentation")
        demo_text = generate_demo_recipe(ingredients)
        return (
            "No momento não temos acesso ao provedor de IA. "
            "Para ver o funcionamento, use o modo demo ou adicione uma chave OpenAI nas configurações.\n\n" + demo_text
        )

    try:
        client = OpenAI(api_key=api_key)
    except Exception as e:
        logger.exception("Failed to initialize OpenAI client")
        demo_text = generate_demo_recipe(ingredients)
        return (
            "Encontramos um problema ao inicializar o serviço de IA. "
            "Verifique a chave nas configurações do Space. Enquanto isso, veja uma sugestão:\n\n" + demo_text
        )

    models_to_try = ["gpt-4o-mini", "gpt-3.5-turbo"]
    last_exception = None

    for model in models_to_try:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.8,
            )

            # Handle a few possible shapes
            try:
                return response.choices[0].message.content
            except Exception:
                try:
                    return response.choices[0]["message"]["content"]
                except Exception:
                    try:
                        return response.choices[0].text
                    except Exception:
                        return str(response)

        except Exception as e:
            logger.warning("OpenAI call failed for model=%s: %s", model, e)
            logger.debug("Exception details", exc_info=True)
            last_exception = e
            continue

    logger.info("All OpenAI model attempts failed.")
    if last_exception:
        logger.info(repr(last_exception))

    # Return friendly message + demo fallback
    demo_text = generate_demo_recipe(ingredients)
    return (
        "No momento o serviço de IA está indisponível. Abaixo há uma sugestão de receita de demonstração. "
        "Se quiser usar IA real, confira a chave nas configurações do Space e tente novamente.\n\n" + demo_text
    )


# UI com Gradio
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("## 🧊 FridgeTalk — Converse com sua geladeira e descubra receitas!")
    gr.Markdown(
        "Digite os ingredientes que você tem em casa e veja sugestões práticas. "
        "Se o serviço de IA não estiver disponível, use o modo demo para ver exemplos." 
    )

    with gr.Row():
        ingredients = gr.Textbox(label="Ingredientes disponíveis", placeholder="Ex: ovos, tomate, queijo, pão...", elem_id="ingredients")
        demo_toggle = gr.Checkbox(label="Usar modo demo (sem IA)", value=False)

    chat = gr.Chatbot(elem_id="chatbot", height=420)
    with gr.Row():
        send = gr.Button("Gerar receita 🍽️")
        demo_button = gr.Button("Gerar receita de demonstração")

    def respond(ingredients_text, chat_history, use_demo):
        recipe = chat_with_fridge(ingredients_text, demo_override=use_demo)
        # Append messages in a clear semantic way: user then assistant
        chat_history = chat_history or []
        chat_history.append(("Você", ingredients_text))
        chat_history.append(("FridgeTalk", recipe))
        # Clear the input textbox and return updated history
        return "", chat_history

    send.click(respond, inputs=[ingredients, chat, demo_toggle], outputs=[ingredients, chat])
    # demo_button forces demo mode
    demo_button.click(lambda i, h: respond(i, h, True), inputs=[ingredients, chat], outputs=[ingredients, chat])


if __name__ == "__main__":
    demo.launch()
