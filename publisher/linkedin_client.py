"""Client de publication vers l'API LinkedIn (Posts API).

Nécessite une app LinkedIn Developer avec accès au produit "Community Management
API" (ou "Marketing Developer Platform"), un access token OAuth avec le scope
w_organization_social, et l'URN de la page. Voir README.md > "Publication LinkedIn".
"""

import requests

from config import LINKEDIN_ACCESS_TOKEN, LINKEDIN_AUTHOR_URN

LINKEDIN_API_VERSION = "202601"
POSTS_URL = "https://api.linkedin.com/rest/posts"


class LinkedInNotConfigured(RuntimeError):
    pass


def publish_post(text: str, visibility: str = "PUBLIC") -> str:
    """Publie un post texte sur la page LinkedIn configurée.

    Args:
        text: Contenu du post (le `texte_complet` produit par l'agent de rédaction).
        visibility: "PUBLIC" ou "CONNECTIONS".

    Returns:
        L'URN du post créé (extrait du header `x-restli-id` de la réponse).

    Raises:
        LinkedInNotConfigured: si LINKEDIN_ACCESS_TOKEN / LINKEDIN_AUTHOR_URN
            ne sont pas définis dans l'environnement.
        requests.HTTPError: si l'appel à l'API LinkedIn échoue.
    """
    if not LINKEDIN_ACCESS_TOKEN or not LINKEDIN_AUTHOR_URN:
        raise LinkedInNotConfigured(
            "LINKEDIN_ACCESS_TOKEN et LINKEDIN_AUTHOR_URN doivent être définis "
            "dans .env pour publier automatiquement. Voir README.md."
        )

    response = requests.post(
        POSTS_URL,
        headers={
            "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
            "LinkedIn-Version": LINKEDIN_API_VERSION,
            "X-Restli-Protocol-Version": "2.0.0",
            "Content-Type": "application/json",
        },
        json={
            "author": LINKEDIN_AUTHOR_URN,
            "commentary": text,
            "visibility": visibility,
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": [],
            },
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.headers.get("x-restli-id", "")
