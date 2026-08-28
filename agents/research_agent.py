"""Agent de veille : recherche l'actualité financière africaine récente via web search."""

import anthropic

from config import ANTHROPIC_API_KEY, MODEL, PAGE_DESCRIPTION

SYSTEM_PROMPT = f"""Tu es l'agent de veille de la page LinkedIn "Finance Afrique".

{PAGE_DESCRIPTION}

Ta mission : utiliser la recherche web pour trouver 3 à 5 actualités récentes et
pertinentes sur la finance, l'économie ou l'investissement en Afrique (croissance,
levées de fonds, fintech, politiques monétaires, partenariats régionaux...).

Pour chaque actualité, donne :
- le titre / sujet
- un résumé en 2-3 phrases
- pourquoi c'est pertinent pour l'audience de la page
- la source (nom + URL)

Réponds en français, sous forme de liste structurée.
"""


def research_finance_africa_news(topic: str | None = None) -> dict:
    """Cherche l'actualité finance/économie Afrique et retourne un brief structuré.

    Args:
        topic: Sujet ou angle précis à approfondir (optionnel). Sans sujet,
            l'agent choisit librement les actualités les plus pertinentes du moment.

    Returns:
        dict avec `brief` (texte du brief de veille) et `sources` (liste d'URLs citées).
    """
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    user_message = (
        f"Fais une veille sur le sujet suivant : {topic}"
        if topic
        else "Fais une veille sur l'actualité finance/économie africaine des derniers jours."
    )

    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        output_config={"effort": "medium"},
        tools=[
            {
                "type": "web_search_20260209",
                "name": "web_search",
                "max_uses": 5,
            }
        ],
        messages=[{"role": "user", "content": user_message}],
    )

    brief_parts = []
    sources = []
    for block in response.content:
        if block.type == "text":
            brief_parts.append(block.text)
        elif block.type == "web_search_tool_result" and isinstance(block.content, list):
            for result in block.content:
                url = getattr(result, "url", None)
                if url and url not in sources:
                    sources.append(url)

    return {"brief": "\n".join(brief_parts).strip(), "sources": sources}
