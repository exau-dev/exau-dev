"""Enchaîne veille -> analyse -> rédaction pour produire un draft de post LinkedIn."""

from agents.analysis_agent import analyze_research_brief
from agents.content_agent import draft_linkedin_post
from agents.research_agent import research_finance_africa_news
from publisher.queue import add_draft


def run_pipeline(topic: str | None = None) -> dict:
    """Exécute le pipeline complet et enregistre le résultat dans la file de publication.

    Args:
        topic: Sujet ou angle précis à couvrir (optionnel, sinon veille libre).

    Returns:
        dict du draft enregistré (voir `publisher.queue.add_draft`).
    """
    research = research_finance_africa_news(topic)
    analysis = analyze_research_brief(research["brief"])
    post = draft_linkedin_post(analysis, sources=research["sources"])

    draft = add_draft(
        {
            "topic": topic,
            "research_brief": research["brief"],
            "sources": research["sources"],
            "analysis": analysis,
            "post": post,
        }
    )
    return draft
