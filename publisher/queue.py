"""File locale des drafts de posts, en attente de relecture puis de publication."""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

QUEUE_PATH = Path(__file__).resolve().parent.parent / "data" / "posts_queue.json"


def _load() -> list[dict]:
    if not QUEUE_PATH.exists():
        return []
    return json.loads(QUEUE_PATH.read_text(encoding="utf-8"))


def _save(drafts: list[dict]) -> None:
    QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
    QUEUE_PATH.write_text(json.dumps(drafts, ensure_ascii=False, indent=2), encoding="utf-8")


def add_draft(content: dict) -> dict:
    """Ajoute un draft à la file avec statut "draft" et retourne l'entrée créée."""
    drafts = _load()
    draft = {
        "id": str(uuid.uuid4()),
        "status": "draft",
        "created_at": datetime.now(timezone.utc).isoformat(),
        **content,
    }
    drafts.append(draft)
    _save(drafts)
    return draft


def list_drafts(status: str | None = None) -> list[dict]:
    """Liste les drafts, filtrés par statut si précisé (ex: "draft", "published")."""
    drafts = _load()
    if status is None:
        return drafts
    return [d for d in drafts if d["status"] == status]


def mark_published(draft_id: str, linkedin_post_urn: str | None = None) -> dict:
    """Marque un draft comme publié et enregistre l'URN du post LinkedIn créé."""
    drafts = _load()
    for draft in drafts:
        if draft["id"] == draft_id:
            draft["status"] = "published"
            draft["published_at"] = datetime.now(timezone.utc).isoformat()
            draft["linkedin_post_urn"] = linkedin_post_urn
            _save(drafts)
            return draft
    raise ValueError(f"Draft introuvable : {draft_id}")
