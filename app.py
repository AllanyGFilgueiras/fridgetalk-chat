import gradio as gr
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_with_fridge(ingredients):
    if not ingredients.strip():
        return "Por favor, digite os ingredientes que você tem. 🍅🥦"

    prompt = f"Crie uma receita criativa e prática usando: {ingredients}. Descreva o modo de preparo passo a passo e dê um nome divertido à receita."

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
        temperature=0.8,
    )

    return response.choices[0].message.content

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
