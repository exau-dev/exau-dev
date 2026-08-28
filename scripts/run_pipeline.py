"""CLI : génère un draft de post LinkedIn, et publie optionnellement.

Usage :
    python -m scripts.run_pipeline
    python -m scripts.run_pipeline "fintech au Nigeria"
    python -m scripts.run_pipeline "fintech au Nigeria" --publish
"""

import argparse
import sys

from orchestrator import run_pipeline
from publisher.linkedin_client import LinkedInNotConfigured, publish_post
from publisher.queue import mark_published


def main() -> None:
    parser = argparse.ArgumentParser(description="Pipeline Finance Afrique")
    parser.add_argument("topic", nargs="?", default=None, help="Sujet ou angle à couvrir")
    parser.add_argument(
        "--publish", action="store_true", help="Publie directement sur LinkedIn après génération"
    )
    args = parser.parse_args()

    draft = run_pipeline(args.topic)

    print(f"Draft {draft['id']} créé.\n")
    print(draft["post"]["texte_complet"])

    if args.publish:
        try:
            urn = publish_post(draft["post"]["texte_complet"])
        except LinkedInNotConfigured as exc:
            print(f"\n{exc}", file=sys.stderr)
            sys.exit(1)
        mark_published(draft["id"], linkedin_post_urn=urn)
        print(f"\nPublié sur LinkedIn : {urn}")
    else:
        print(f"\nDraft en attente de relecture dans data/posts_queue.json (id: {draft['id']}).")


if __name__ == "__main__":
    main()
