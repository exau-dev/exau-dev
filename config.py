"""Configuration partagée par les agents Finance Afrique."""

import os

from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-opus-5"

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

LINKEDIN_ACCESS_TOKEN = os.environ.get("LINKEDIN_ACCESS_TOKEN")
LINKEDIN_AUTHOR_URN = os.environ.get("LINKEDIN_AUTHOR_URN")

PAGE_DESCRIPTION = (
    "Finance Afrique est une page LinkedIn dédiée à l'économie et à la finance "
    "du continent africain : croissance économique, investissements, innovation "
    "technologique, entrepreneuriat et développement durable. Le ton est "
    "informatif, engageant et orienté opportunités."
)
