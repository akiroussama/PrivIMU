# 04 — Prompt prêt à coller dans Claude local

Copier-coller ce prompt dans Claude une fois placé à la racine du repo `D:\workspace\PrivIMU`.

---

Tu prends la main localement sur le repo PrivIMU.

Contexte : projet de Sécurité IoT nommé PrivIMU, repo `https://github.com/akiroussama/PrivIMU`. Le but est de montrer qu'un signal IMU supposé anonyme peut devenir un quasi-identifiant comportemental. Dataset MotionSense. Démo Streamlit. Notebook Colab. Slides et rapport PDF à finaliser pour viser un rendu 20/20.

Lis d'abord ces fichiers :

```text
CLAUDE_LOCAL_HANDOFF.md
handoff/00_CLAUDE_HANDOFF_MASTER.md
handoff/01_PRESENTATION_BASELINE_AND_REMAKE_BRIEF.md
handoff/02_REPORT_PDF_OBJECTIVE_AND_OUTLINE.md
handoff/03_DELIVERABLES_WOW_CHECKLIST.md
```

Ensuite, fais le travail suivant sans me redemander les éléments déjà fournis :

1. Inspecte le repo : `git status`, arborescence, README, Streamlit, notebook, reports, slides, report.
2. Lance les vérifications minimales :

```powershell
pytest -q
python -m py_compile streamlit_app.py
```

3. Vérifie que Streamlit utilise les CSV réels :

```text
examples/wlk_7/sub_*.csv
https://raw.githubusercontent.com/akiroussama/PrivIMU/main/examples/wlk_7/sub_1.csv
```

et non les anciens liens cassés `demo/sample_motionsense_like.csv`.

4. Vérifie si `reports/metrics.json` existe. Si oui, utilise uniquement ses valeurs pour les résultats. Si non, essaie de le générer par le pipeline RF. Si le run complet est trop long, fais un run rapide pour tester, mais ne mets pas de chiffres de run rapide dans le deck final sans l'indiquer.

5. Refaire complètement la présentation from scratch :

```text
slides/PrivIMU_final.pptx
slides/PrivIMU_final.pdf
```

Contraintes : 15 slides, style professionnel, narration intro -> menace -> dataset -> pipeline -> démo -> résultats -> limites -> conclusion. Slide résultats alimentée par `reports/metrics.json`. Pas de placeholder.

6. Refaire ou finaliser le rapport :

```text
report/PrivIMU_report.pdf
```

Source Markdown ou LaTeX recommandée. 6-8 pages. Ton académique. Chiffres uniquement depuis metrics.json. Références vérifiées. Limites et défenses incluses.

7. Mettre à jour ou créer :

```text
ARTIFACT_INDEX.md
slides/speaker_notes/M1_intro.md
slides/speaker_notes/M2_sota.md
slides/speaker_notes/M3_methodology.md
slides/speaker_notes/M4_demo.md
slides/speaker_notes/M5_results.md
```

8. À la fin, donne un résumé clair :

```text
- fichiers modifiés/créés
- commandes exécutées
- tests réussis/échoués
- métriques utilisées
- éléments restant à faire si certains points n'ont pas pu être complétés
```

Règles non négociables :

```text
- Aucun chiffre inventé.
- Ne pas changer de sujet.
- Ne pas supprimer examples/wlk_7.
- Ne pas committer data/raw ou .venv.
- Ne pas vendre le fallback Streamlit comme résultat scientifique.
- Vérifier les fichiers générés avant d'affirmer qu'ils sont finis.
```
