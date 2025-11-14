import re

from app import generate_demo_recipe, chat_with_fridge


def test_generate_demo_recipe_non_empty():
    text = generate_demo_recipe("ovos, tomate")
    assert isinstance(text, str)
    assert len(text) > 0
    assert "Modo de preparo" in text or "Modo de preparo:" in text


def test_chat_with_fridge_demo_override():
    # Force demo mode via override
    out = chat_with_fridge("pão, queijo", demo_override=True)
    assert isinstance(out, str)
    # Should contain a headline-style recipe name
    assert re.search(r"### \w", out)
import os

from app import generate_demo_recipe, chat_with_fridge


def test_generate_demo_contains_sections():
    text = generate_demo_recipe("tomate, queijo")
    assert text
    assert "Modo de preparo" in text or "Modo de preparo:" in text
    assert ("Ingredientes" in text) or ("Ingredientes sugeridos" in text)


def test_chat_with_fridge_demo_env():
    os.environ["DEMO_MODE"] = "1"
    try:
        out = chat_with_fridge("ovo, tomate")
        assert out
        assert "Modo de preparo" in out or "Ingredientes" in out
    finally:
        os.environ.pop("DEMO_MODE", None)
