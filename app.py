import gradio as gr
from openai import OpenAI
import os

# Initialize OpenAI client (reads OPENAI_API_KEY from env if provided)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_with_fridge(ingredients):
    if not ingredients.strip():
        return "Por favor, digite os ingredientes que você tem. 🍅🥦"

    prompt = f"Crie uma receita criativa e prática usando: {ingredients}. Descreva o modo de preparo passo a passo e dê um nome divertido à receita."

    # Try preferred model first, then fallback to a more broadly available model.
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

            # The SDK may return different shapes; handle common cases.
            try:
                # Newer SDKs: response.choices[0].message.content
                return response.choices[0].message.content
            except Exception:
                try:
                    # Older/alternative shape: choices[0]["message"]["content"]
                    return response.choices[0]["message"]["content"]
                except Exception:
                    try:
                        # Fallback: choices[0].text
                        return response.choices[0].text
                    except Exception:
                        return str(response)

        except Exception as e:
            # Log to container logs so we can inspect in HF Spaces UI.
            print(f"OpenAI call failed for model={model}: {e}")
            import traceback

            traceback.print_exc()
            last_exception = e
            # try next model
            continue

    # If we reach here, all attempts failed.
    print("All OpenAI model attempts failed.")
    if last_exception:
        print(repr(last_exception))

    return "Erro ao gerar a receita. Verifique a configuração da chave OpenAI no Space ou tente novamente mais tarde."

# UI moderna com Gradio
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("## 🧊 FridgeTalk — Converse com sua geladeira e descubra receitas!")
    gr.Markdown("Digite os ingredientes que você tem em casa e veja o que o FridgeTalk cria 🍳")

    ingredients = gr.Textbox(label="Ingredientes disponíveis", placeholder="Ex: ovos, tomate, queijo, pão...")
    chat = gr.Chatbot(height=400)
    send = gr.Button("Gerar receita 🍽️")

    def respond(ingredients, chat_history):
        recipe = chat_with_fridge(ingredients)
        chat_history.append(("👩‍🍳 Você", ingredients))
        chat_history.append(("🤖 FridgeTalk", recipe))
        return "", chat_history

    send.click(respond, [ingredients, chat], [ingredients, chat])

demo.launch()
