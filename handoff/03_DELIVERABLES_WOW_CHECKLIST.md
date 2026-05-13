# 03 — Livrables PrivIMU et checklist WOW effect

Ce fichier liste tous les livrables attendus, leur rôle, leur état probable et les critères de validation.

---

## 1. Philosophie du livrable

Le projet doit être présenté comme un écosystème complet :

```text
repo public + code reproductible + notebook Colab + demo Streamlit + metrics.json + slides + report + evidence + ethics
```

Le professeur doit sentir que le groupe a produit plus qu'un exposé : un laboratoire de privacy IoT.

---

## 2. Livrables principaux

| # | Livrable | Chemin / lien | Rôle | Validation |
|---|---|---|---|---|
| 1 | Repo GitHub | `https://github.com/akiroussama/PrivIMU` | Source principale | public, propre, README clair |
| 2 | README | `README.md` | vitrine | contient pitch, quickstart, liens |
| 3 | Artifact index | `ARTIFACT_INDEX.md` | navigation prof | liste repo, Colab, Streamlit, PDF, slides |
| 4 | Colab | `notebooks/PrivIMU_MotionSense_Demo.ipynb` | reproduction rapide | ouvre depuis GitHub, exécute training/eval |
| 5 | Streamlit | `streamlit_app.py` | démo live | fonctionne local + cloud |
| 6 | CSV exemples | `examples/wlk_7/sub_*.csv` | test upload/demo | liens raw fonctionnent |
| 7 | Training code | `src/privimu/train.py` | génération modèle/métriques | produit reports/metrics.json |
| 8 | Metrics | `reports/metrics.json` | source des chiffres | lu par slides/rapport |
| 9 | Figures | `reports/*.png` | résultats visuels | lisibles et sourcés |
| 10 | Slides PPTX | `slides/PrivIMU_final.pptx` | soutenance | 15 slides propres |
| 11 | Slides PDF | `slides/PrivIMU_final.pdf` | partage facile | PDF lisible |
| 12 | Rapport PDF | `report/PrivIMU_report.pdf` | document académique | 6-8 pages |
| 13 | Speaker notes | `slides/speaker_notes/*.md` | oral 5 membres | 450-520 mots chacun |
| 14 | Ethics | `docs/ETHICS_AND_LIMITS.md` | posture responsable | limites + usage défensif |
| 15 | SOTA | `docs/SOTA_TABLE.md` | crédibilité scientifique | refs vérifiées |
| 16 | Tests | `tests/` | qualité logicielle | `pytest -q` OK |
| 17 | GitHub Actions | `.github/workflows/tests.yml` | badge qualité | CI verte si possible |
| 18 | Demo video | `demo/PrivIMU_demo_90s.mp4` | backup | utile si Wi-Fi tombe |
| 19 | Release | GitHub release `v1.0-submission` | gel version | contient PDF/slides/metrics |

---

## 3. Livrables à vérifier immédiatement

Claude doit vérifier :

```powershell
git status
pytest -q
python -m py_compile streamlit_app.py
```

Puis :

```text
[ ] Le repo contient bien examples/wlk_7/sub_1.csv.
[ ] streamlit_app.py ne référence plus demo/sample_motionsense_like.csv comme lien principal.
[ ] reports/metrics.json existe ou peut être généré.
[ ] le notebook Colab pointe vers le bon repo.
[ ] slides/ et report/ existent.
```

---

## 4. WOW effect attendu

### WOW #1 — Démo self-contained

Le prof ouvre Streamlit et peut choisir un CSV déjà dans le repo.

Message implicite :

```text
La démo ne dépend pas d'un fichier caché sur notre machine.
```

### WOW #2 — Identity-lock replay

La démo montre la révélation progressive de l'identité.

Message implicite :

```text
Ce n'est pas juste un tableau ; on visualise la fuite d'information dans le temps.
```

### WOW #3 — Defense lab

La démo montre comment le bruit réduit la fuite.

Message implicite :

```text
Nous avons pensé comme attaquants et comme défenseurs.
```

### WOW #4 — Evidence card

La démo permet de télécharger un JSON/Markdown de l'expérience.

Message implicite :

```text
La démo produit une preuve, pas seulement un effet visuel.
```

### WOW #5 — metrics.json

Les chiffres du deck viennent d'un fichier généré.

Message implicite :

```text
Notre présentation est vérifiable.
```

---

## 5. Checklist présentation finale

```text
[ ] 15 slides.
[ ] 5 blocs oraux clairs.
[ ] Slide 13 alimentée par metrics.json.
[ ] QR repo.
[ ] QR Colab.
[ ] QR Streamlit si app déployée.
[ ] Démo Streamlit mentionnée comme climax.
[ ] Limites honnêtes.
[ ] Défenses mentionnées.
[ ] Pas de métrique manuelle.
[ ] PPTX + PDF générés.
```

---

## 6. Checklist rapport final

```text
[ ] 6-8 pages.
[ ] Abstract.
[ ] Dataset table.
[ ] Pipeline.
[ ] Méthode.
[ ] Résultats.
[ ] Streamlit lab.
[ ] Limites.
[ ] Défenses.
[ ] Références vérifiées.
[ ] PDF généré.
```

---

## 7. Checklist déploiement Streamlit

Paramètres Streamlit Cloud :

```text
Repository: akiroussama/PrivIMU
Branch: main
Main file path: streamlit_app.py
```

Vérifier :

```text
[ ] requirements.txt installe le package local si nécessaire.
[ ] imports privimu OK.
[ ] examples/wlk_7 est disponible dans le repo.
[ ] l'app démarre sans model avec fallback.
[ ] l'app utilise model RF si models/rf.joblib existe.
[ ] liens CSV affichés fonctionnent.
```

---

## 8. Checklist Colab

```text
[ ] Le notebook clone ou utilise le repo GitHub.
[ ] pip install -e . fonctionne.
[ ] data/download.py prépare A_DeviceMotion_data.
[ ] train-rf fonctionne.
[ ] reports/metrics.json est lu.
[ ] figures s'affichent.
```

---

## 9. Commit final conseillé

Après génération finale :

```powershell
git add README.md ARTIFACT_INDEX.md streamlit_app.py notebooks docs slides report reports examples handoff

git commit -m "feat: finalize PrivIMU reproducible privacy lab" `
  -m "Verified-By: pytest -q" `
  -m "Verified-By: python -m py_compile streamlit_app.py" `
  -m "Verified-By: python -m privimu.evaluate --metrics reports/metrics.json" `
  -m "Refs: PRIVIMU_BRIEF.md"

git push
```

Si `metrics.json` n'existe pas, ne pas utiliser la ligne `evaluate` dans `Verified-By`.

---

## 10. Formulation à utiliser devant le prof

Phrase courte :

> PrivIMU est un mini-lab reproductible de privacy IoT : on charge un signal IMU, on mesure la fuite d'identité, on visualise le risque, puis on teste une défense par bruit.

Phrase plus académique :

> Notre objectif n'était pas seulement de classifier des signaux. Nous voulions vérifier si une trace capteur supposée anonyme peut devenir un quasi-identifiant comportemental, puis documenter l'attaque et les mitigations dans un pipeline reproductible.
