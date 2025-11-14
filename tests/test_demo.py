import re

from app import chat_with_fridge, generate_demo_recipe


def test_generate_demo_recipe_has_expected_sections():
    text = generate_demo_recipe("ovos, tomate")
    assert text
    assert "###" in text
    assert "Modo de preparo" in text
    assert "Ingredientes" in text


def test_chat_with_fridge_requires_input():
    out = chat_with_fridge("")
    assert "Por favor, digite os ingredientes" in out


def test_chat_with_fridge_demo_override():
    out = chat_with_fridge("pão, queijo", demo_override=True)
    assert isinstance(out, str)
    assert re.search(r"### \w", out)


def test_chat_with_fridge_demo_env(monkeypatch):
    monkeypatch.setenv("DEMO_MODE", "1")
    out = chat_with_fridge("ovo, tomate")
    assert "Modo de preparo" in out


def test_chat_with_fridge_without_api_key_returns_friendly_message(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    out = chat_with_fridge("tomate, queijo")
    assert "No momento não temos acesso ao provedor de IA." in out
    assert "Modo de preparo" in out
