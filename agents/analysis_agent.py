"""Agent d'analyse : extrait les insights et l'angle éditorial d'un brief de veille."""

import json

import anthropic

from config import ANTHROPIC_API_KEY, MODEL, PAGE_DESCRIPTION

SYSTEM_PROMPT = f"""Tu es l'agent d'analyse de la page LinkedIn "Finance Afrique".

{PAGE_DESCRIPTION}

À partir d'un brief de veille, identifie l'actualité la plus porteuse pour un post
LinkedIn et structure ton analyse : insight principal, tendance de fond, chiffres
clés à citer, et angle éditorial (le point de vue ou la question qui donnera du
relief au post).
"""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "sujet_retenu": {"type": "string"},
        "insight_principal": {"type": "string"},
        "tendance_de_fond": {"type": "string"},
        "chiffres_cles": {"type": "array", "items": {"type": "string"}},
        "angle_editorial": {"type": "string"},
    },
    "required": [
        "sujet_retenu",
        "insight_principal",
        "tendance_de_fond",
        "chiffres_cles",
        "angle_editorial",
    ],
    "additionalProperties": False,
}


def analyze_research_brief(brief: str) -> dict:
    """Analyse un brief de veille et retourne un angle éditorial structuré.

    Args:
        brief: Texte du brief produit par l'agent de veille.

    Returns:
        dict validé selon OUTPUT_SCHEMA (sujet_retenu, insight_principal,
        tendance_de_fond, chiffres_cles, angle_editorial).
    """
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        output_config={
            "effort": "medium",
            "format": {"type": "json_schema", "schema": OUTPUT_SCHEMA},
        },
        messages=[{"role": "user", "content": f"Brief de veille :\n\n{brief}"}],
    )

    text = next(b.text for b in response.content if b.type == "text")
    return json.loads(text)
