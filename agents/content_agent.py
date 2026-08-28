"""Agent de rédaction : transforme un angle éditorial en post LinkedIn prêt à publier."""

import json

import anthropic

from config import ANTHROPIC_API_KEY, MODEL, PAGE_DESCRIPTION

SYSTEM_PROMPT = f"""Tu es le rédacteur de la page LinkedIn "Finance Afrique".

{PAGE_DESCRIPTION}

Écris des posts en français, avec :
- une accroche (hook) qui capte l'attention dans les 2 premières lignes
- un corps de texte clair, informatif, avec des retours à la ligne pour l'aération
- 3 à 5 hashtags pertinents (finance, Afrique, secteur concerné)
- un appel à la discussion (question ou invitation à commenter) en fin de post

Longueur cible : 800 à 1200 caractères. Pas d'emojis excessifs (1 à 3 maximum).
"""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "hook": {"type": "string"},
        "corps": {"type": "string"},
        "hashtags": {"type": "array", "items": {"type": "string"}},
        "appel_discussion": {"type": "string"},
    },
    "required": ["hook", "corps", "hashtags", "appel_discussion"],
    "additionalProperties": False,
}


def draft_linkedin_post(analysis: dict, sources: list[str] | None = None) -> dict:
    """Rédige un post LinkedIn à partir d'un angle éditorial analysé.

    Args:
        analysis: dict retourné par `analyze_research_brief` (sujet_retenu,
            insight_principal, tendance_de_fond, chiffres_cles, angle_editorial).
        sources: URLs des sources à mentionner en fin de post (optionnel).

    Returns:
        dict avec `hook`, `corps`, `hashtags`, `appel_discussion` et `texte_complet`
        (le post assemblé, prêt à publier).
    """
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    user_message = (
        "Rédige un post LinkedIn à partir de cet angle éditorial :\n\n"
        f"{json.dumps(analysis, ensure_ascii=False, indent=2)}"
    )

    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        output_config={
            "effort": "medium",
            "format": {"type": "json_schema", "schema": OUTPUT_SCHEMA},
        },
        messages=[{"role": "user", "content": user_message}],
    )

    text = next(b.text for b in response.content if b.type == "text")
    post = json.loads(text)

    hashtags_line = " ".join(post["hashtags"])
    texte_complet = (
        f"{post['hook']}\n\n{post['corps']}\n\n{post['appel_discussion']}\n\n{hashtags_line}"
    )
    if sources:
        texte_complet += "\n\nSources : " + " | ".join(sources)

    post["texte_complet"] = texte_complet
    return post
