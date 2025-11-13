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

