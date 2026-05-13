# 00 — PrivIMU Master Handoff pour Claude local

Ce document est le point d'entrée pour reprendre PrivIMU localement. Il complète `../CLAUDE_LOCAL_HANDOFF.md` et doit être lu avant toute génération de slides, PDF ou modification de code.

---

## A. Identité du projet

```text
Nom : PrivIMU
Repo : https://github.com/akiroussama/PrivIMU
Thème : Sécurité IoT
Angle : Privacy / ré-identification via signaux IMU
Dataset : MotionSense
Démo : Streamlit
Notebook : Google Colab
Objectif qualité : 20/20 avec effet WOW
```

PrivIMU n'est pas un simple devoir de présentation. C'est un projet à vendre comme un mini-lab reproductible : il montre une attaque, mesure la fuite d'information, propose une défense pédagogique et produit des artefacts vérifiables.

---

## B. Contexte humain et pédagogique

Le professeur a demandé un projet sur un thème IoT. Le groupe a choisi le thème Sécurité IoT. Plusieurs sujets étaient possibles, mais le choix final est PrivIMU parce qu'il maximise :

```text
- lien direct avec les capteurs IoT
- faisabilité en 1 semaine
- reproductibilité software-only
- impact narratif fort
- possibilité de démo live
```

Le public de soutenance ne sera pas forcément expert ML. Il faut donc raconter un problème de privacy intuitif, puis l'appuyer par une méthodologie propre.

---

## C. Problème à raconter

Les capteurs IMU sont partout : smartphone, montre connectée, objet de santé, sport tracker, mobilité, applications IoT. Les signaux peuvent sembler anonymes : pas de visage, pas de nom, pas d'email, pas de numéro. Pourtant, la manière de marcher, courir, monter les escaliers ou rester immobile peut contenir des patterns personnels.

PrivIMU pose la question :

> Une trace accéléromètre + gyroscope peut-elle devenir un quasi-identifiant ?

La réponse ne doit pas être seulement théorique. La soutenance doit montrer :

```text
signal -> modèle -> top-3 identité -> entropy leakage -> défense bruitée
```

---

## D. Travaux déjà réalisés par ChatGPT dans ce projet

### D1. Scaffold repo

Un scaffold complet a été préparé avec :

```text
src/privimu/
data/download.py
streamlit_app.py
notebooks/PrivIMU_MotionSense_Demo.ipynb
reports/
slides/
report/
docs/
tests/
.github/workflows/tests.yml
```

### D2. Tests

Des tests unitaires existent. À plusieurs étapes, `pytest -q` a donné :

```text
8 tests passed
```

Claude doit revérifier localement car l'état GitHub peut avoir évolué.

### D3. Notebook Colab

Le notebook Colab existe dans :

```text
notebooks/PrivIMU_MotionSense_Demo.ipynb
```

Lien public attendu :

```text
https://colab.research.google.com/github/akiroussama/PrivIMU/blob/main/notebooks/PrivIMU_MotionSense_Demo.ipynb
```

### D4. Streamlit amélioré

Streamlit a été enrichi avec 3 fonctionnalités WOW :

```text
1. Live identity-lock replay
2. Blue-team defense lab
3. One-click evidence card
```

Un correctif a été préparé pour remplacer les anciens liens CSV cassés par les CSV réels du repo :

```text
examples/wlk_7/sub_*.csv
```

Claude doit vérifier que ce correctif est bien dans `streamlit_app.py`.

### D5. Slides/PDF initiaux

Une première présentation `PrivIMU_final.pptx` et `PrivIMU_final.pdf` a été générée. Elle doit être considérée comme une baseline, pas comme version finale. Le contenu est détaillé dans `01_PRESENTATION_BASELINE_AND_REMAKE_BRIEF.md`.

### D6. Rapport initial

Un squelette de rapport peut exister. Il doit être refait ou renforcé selon `02_REPORT_PDF_OBJECTIVE_AND_OUTLINE.md`.

---

## E. État des décisions

Décisions verrouillées :

```text
- Sujet : PrivIMU, pas un autre projet.
- Thème : Sécurité IoT.
- Dataset : MotionSense.
- Repo : public GitHub akiroussama/PrivIMU.
- Storytelling : académique neutre.
- Métriques : venir de metrics.json.
```

---

## F. Architecture conceptuelle à respecter

```text
MotionSense CSV
  -> load columns rotationRate.* + userAcceleration.*
  -> sliding windows 50 samples, step 25
  -> z-score per window
  -> feature extraction
  -> Random Forest baseline
  -> optional 1D-CNN
  -> metrics.json
  -> figures
  -> Streamlit demo
  -> slides + report
```

---

## G. Artefacts attendus et rôle de chacun

```text
README.md
- vitrine du projet
- quickstart
- liens Colab/Streamlit/release

ARTIFACT_INDEX.md
- page de navigation pour le prof

notebooks/PrivIMU_MotionSense_Demo.ipynb
- reproduction sur Colab

streamlit_app.py
- climax de soutenance

reports/metrics.json
- source unique des chiffres

slides/PrivIMU_final.pptx / .pdf
- soutenance 15 slides

report/PrivIMU_report.pdf
- document académique 6-8 pages

slides/speaker_notes/*.md
- scripts oraux pour 5 membres

docs/ETHICS_AND_LIMITS.md
- posture responsable

docs/SOTA_TABLE.md
- crédibilité scientifique
```

---

## H. Règles anti-erreur

### H1. Interdiction de métriques manuelles

Chaque chiffre doit être traçable.

### H2. Ne pas supprimer les exemples `examples/wlk_7`

Ils servent de source robuste pour Streamlit.

### H3. Ne pas pousser de data lourde

Ne pas committer :

```text
data/raw/
data/processed/
.venv/
__pycache__/
```

### H4. Modèles

Le modèle RF `models/rf.joblib` peut être ajouté s'il reste léger. Sinon fournir instructions et garder la démo fallback, mais ne pas vendre fallback comme résultat réel.

### H5. Colab

Le notebook doit pouvoir reproduire au moins RF + metrics.json.

---

## I. Ordre de travail conseillé à Claude local

1. Lire `CLAUDE_LOCAL_HANDOFF.md`.
2. Vérifier `git status`.
3. Vérifier arborescence.
4. Lancer `pytest -q`.
5. Ouvrir `streamlit_app.py` et vérifier les liens `examples/wlk_7`.
6. Vérifier si `reports/metrics.json` existe.
7. Si non, lancer un run RF rapide ou final selon disponibilité.
8. Refaire les slides à partir du brief de présentation.
9. Refaire le rapport PDF.
10. Vérifier les liens Colab/Streamlit/CSV.
11. Mettre à jour `ARTIFACT_INDEX.md`.
12. Donner un résumé de ce qui a été produit et des tests.

---

## J. Message clé à préserver partout

> Les données de mouvement ne sont pas de simples données techniques. Dans certains contextes, elles peuvent devenir des quasi-identifiants comportementaux. PrivIMU le démontre de manière reproductible et discute les défenses.
