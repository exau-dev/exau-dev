# Finance Afrique — Agents IA

Pipeline d'agents Claude pour la page LinkedIn **Finance Afrique** : veille,
analyse et rédaction de posts, avec file de publication et branchement optionnel
vers l'API LinkedIn.

## Architecture

```
agents/
  research_agent.py   # Veille : web search -> brief d'actualités finance/économie Afrique
  analysis_agent.py   # Analyse : brief -> angle éditorial structuré (insight, tendance, chiffres clés)
  content_agent.py    # Rédaction : angle éditorial -> post LinkedIn (hook, corps, hashtags, CTA)
orchestrator.py        # Enchaîne les 3 agents et enregistre le résultat dans la file
publisher/
  queue.py             # File locale des drafts (data/posts_queue.json)
  linkedin_client.py   # Publication réelle via l'API LinkedIn (Posts API)
scripts/
  run_pipeline.py       # CLI d'exécution
```

Chaque agent est une fonction Python autonome qui appelle l'API Claude
(`claude-opus-5`). Le pipeline est sensiblement plus simple qu'un "agent
autonome" à outils multiples : chaque étape est un appel structuré, ce qui le
rend prévisible et facile à relire.

## Installation

```bash
pip install -r requirements.txt
cp .env.example .env
# Renseigner ANTHROPIC_API_KEY dans .env
```

## Utilisation

```bash
# Veille libre, sujet choisi par l'agent
python -m scripts.run_pipeline

# Sujet précis
python -m scripts.run_pipeline "fintech au Nigeria"

# Génère ET publie directement sur LinkedIn (nécessite la config LinkedIn, voir plus bas)
python -m scripts.run_pipeline "fintech au Nigeria" --publish
```

Chaque exécution ajoute un draft dans `data/posts_queue.json` avec le brief de
veille, l'analyse, le texte du post et son statut (`draft` puis `published`).
Le workflow recommandé est : générer le draft, le relire, puis publier
manuellement sur LinkedIn (copier-coller) ou via `--publish` une fois la
configuration LinkedIn en place.

## Publication LinkedIn

La publication automatique nécessite une app LinkedIn Developer avec accès au
produit **Community Management API** (pour poster au nom d'une page/organisation),
approuvé par LinkedIn — ce n'est pas instantané. Étapes :

1. Créer une app sur [LinkedIn Developer Portal](https://www.linkedin.com/developers/apps).
2. Lier l'app à la page LinkedIn "Finance Afrique" (il faut en être admin).
3. Demander l'accès au produit "Community Management API".
4. Générer un access token OAuth avec le scope `w_organization_social`.
5. Récupérer l'URN de la page (`urn:li:organization:<id>`).
6. Renseigner `LINKEDIN_ACCESS_TOKEN` et `LINKEDIN_AUTHOR_URN` dans `.env`.

Tant que cette configuration n'est pas en place, le pipeline fonctionne quand
même : il génère les drafts, il faut juste les publier à la main.

## Prochaines étapes possibles

- Ajouter un agent de génération de visuels (charts, infographies) pour
  accompagner les posts.
- Historiser les performances des posts publiés pour affiner l'agent
  d'analyse (quels angles génèrent le plus d'engagement).
- Passer à une exécution planifiée (cron) pour une veille quotidienne.
