# 02 — Objectif du rapport PDF PrivIMU

Ce fichier définit l'objectif, la structure et les règles du rapport final PDF.

---

## 1. Objectif du rapport

Le rapport doit être un document académique court, clair et vérifiable. Il doit accompagner les slides et le repo, pas répéter mot pour mot la soutenance.

Objectif :

> Présenter PrivIMU comme une étude expérimentale de privacy IoT montrant qu'un signal IMU supposé anonyme peut devenir un quasi-identifiant comportemental, puis discuter les défenses possibles.

Longueur cible :

```text
6 à 8 pages hors annexes éventuelles
```

Format :

```text
PDF final : report/PrivIMU_report.pdf
Source recommandé : report/PrivIMU_report.md ou report/PrivIMU_report.tex
```

---

## 2. Ton et niveau attendu

Le ton doit être :

```text
- académique
- précis
- neutre
- défensif / privacy-by-design
- honnête sur les limites
```

Éviter :

```text
- phrases marketing vides
- catastrophisme
- “nous hackons les utilisateurs”
- chiffres non sourcés
- bibliographie fantôme
```

---

## 3. Structure recommandée

### Page 1 — Title + abstract

**Titre** :

```text
PrivIMU: Re-identification Risk in Anonymous Motion Sensor Traces
```

**Sous-titre possible** :

```text
A reproducible IoT privacy study using accelerometer and gyroscope data
```

**Abstract — structure** :

```text
1. IoT systems collect motion traces at scale.
2. These traces are often considered less sensitive than images or audio.
3. We study whether IMU traces can leak identity information.
4. We build a reproducible pipeline on MotionSense.
5. We evaluate top-1/top-3/F1 and entropy leakage.
6. We provide a Streamlit demo and discuss mitigations.
```

Ne pas inclure de chiffres avant de lire `reports/metrics.json`.

---

### Section 1 — Introduction and motivation

Contenu :

```text
- IMU sensors in smartphones/wearables/IoT.
- Privacy misconception: no direct identifier does not imply anonymity.
- Example risk: motion traces reused across apps/services.
- Research question.
- Contributions.
```

Contributions proposées :

```text
C1. A reproducible pipeline for user re-identification from IMU traces.
C2. A measurement of identity leakage using top-k metrics and entropy leakage.
C3. An interactive Streamlit privacy lab showing attack and defense.
C4. A discussion of privacy-by-design mitigations.
```

---

### Section 2 — Background and related work

Objectif : montrer que le sujet est crédible scientifiquement.

Sous-sections :

```text
2.1 Human Activity Recognition with IMU
2.2 Gait and behavioral biometrics
2.3 Sensor privacy leakage
2.4 Defenses: minimization, on-device processing, federated learning, differential privacy, perturbation
```

Inclure une table SOTA :

```text
Paper | Year | Sensor | Task | Model | Dataset | Privacy angle | Difference with PrivIMU
```

Attention : vérifier les références. Le brief contient une liste pressentie, pas une bibliographie finale validée. Ne pas inventer DOI/titres.

---

### Section 3 — Dataset and preprocessing

Contenu :

```text
- MotionSense dataset.
- 24 subjects.
- 6 activities.
- iPhone DeviceMotion.
- channels used: rotationRate.x/y/z + userAcceleration.x/y/z.
- window size: 50 samples.
- step: 25 samples.
- normalization: z-score per window.
```

Inclure un tableau :

```text
Property | Value
Dataset | MotionSense
Subjects | 24
Activities | wlk, jog, ups, dws, sit, std
Sampling | ~50 Hz
Channels | 6 IMU channels
Window | 1 s
Overlap | 50 %
```

---

### Section 4 — Methodology

Contenu :

```text
- Feature extraction.
- Random Forest baseline.
- Optional 1D-CNN if implemented and measured.
- Training/evaluation protocol.
- Metrics.
```

Métriques à définir :

```text
Top-1 accuracy
Top-3 accuracy
Macro-F1
Latency per window
Confusion matrix
Privacy entropy leakage ΔH = log2(N) - H(posterior)
```

Important : aligner le protocole écrit sur le code réel. Vérifier `train.py`. Si le code utilise StratifiedKFold, écrire StratifiedKFold. Si le code implémente LOTO, écrire LOTO.

---

### Section 5 — Implementation and reproducibility

Objectif : vendre l'effort.

Contenu :

```text
- Repo GitHub public.
- Colab notebook.
- Streamlit demo.
- reports/metrics.json as source of truth.
- tests and CI if available.
- Windows-friendly task.ps1.
```

Inclure un bloc commandes :

```powershell
python -m pip install -e ".[dev,app]"
python data/download.py --dest data/raw/motionsense
python -m privimu.train --data-root data/raw/motionsense --model rf --output-dir .
python -m privimu.evaluate --metrics reports/metrics.json
streamlit run streamlit_app.py
```

---

### Section 6 — Results

Cette section doit être générée après le training.

Elle doit contenir :

```text
- Tableau métriques RF, et CNN seulement si disponible.
- Top-1.
- Top-3.
- Macro-F1.
- Latency.
- Privacy leakage.
- Confusion matrix.
- Per-subject F1.
```

Tous les chiffres viennent de :

```text
reports/metrics.json
```

Figures possibles :

```text
reports/confusion_matrix.png
reports/per_subject_f1.png
reports/privacy_entropy_curve.png
screenshot Streamlit defense sweep
```

Si les résultats sont faibles, ne pas mentir. Recentrer :

```text
- top-3 plutôt que top-1
- marche wlk_7 comme démo illustrative
- protocole honnête
- limites et plans de repli
```

---

### Section 7 — Interactive privacy lab

Décrire Streamlit comme artefact pédagogique.

Contenu :

```text
- CSV upload/select.
- Signal plot.
- Top-3 posterior.
- Identity-lock replay.
- Noise defense sweep.
- Evidence card.
```

Inclure capture écran si possible.

Préciser que l'app peut utiliser :

```text
examples/wlk_7/sub_1.csv
```

et lien raw :

```text
https://raw.githubusercontent.com/akiroussama/PrivIMU/main/examples/wlk_7/sub_1.csv
```

---

### Section 8 — Discussion: risks, limitations, mitigations

Risques :

```text
- sensor traces can become behavioral quasi-identifiers
- data sharing with third-party apps
- cross-service linkage risk
```

Limites :

```text
- MotionSense is limited to 24 subjects
- closed-set evaluation
- phone placement and activity dependency
- laboratory/public dataset, not production traffic
- noise defense is pedagogical
```

Mitigations :

```text
- data minimization
- avoid sharing raw IMU traces
- on-device inference
- aggregation before transmission
- federated learning
- differential privacy
- user consent and transparency
- retention limits
```

---

### Section 9 — Conclusion

Conclusion attendue :

```text
PrivIMU shows that motion data can carry identity information and should be treated as potentially privacy-sensitive in IoT systems. The project provides a reproducible pipeline, a live demo, and a discussion of defenses.
```

Ne pas conclure que toute donnée IMU identifie toujours tout le monde. Rester nuancé.

---

## 4. Figures à produire ou intégrer

Priorité haute :

```text
1. Pipeline figure.
2. Example IMU signal.
3. Confusion matrix.
4. Metrics table.
5. Privacy entropy / defense curve.
6. Streamlit screenshot.
```

Si le temps manque : pipeline + metrics table + Streamlit screenshot suffisent.

---

## 5. Bibliographie

Règles :

```text
- Vérifier chaque référence.
- Ne pas inventer DOI.
- Privilégier papier MotionSense original, HAR smartphone, gait biometrics, privacy/differential privacy.
- Utiliser 8 à 15 références propres.
```

Ne pas recopier une liste “pressentie” comme bibliographie finale sans vérification.

---

## 6. Table de correspondance rapport ↔ repo

```text
Introduction -> README.md + brief
Dataset -> data/download.py + examples/wlk_7
Methodology -> src/privimu/features.py + train.py
Results -> reports/metrics.json + reports/*.png
Demo -> streamlit_app.py + docs/STREAMLIT_WOW_FEATURES.md
Ethics -> docs/ETHICS_AND_LIMITS.md
Reproducibility -> notebooks/PrivIMU_MotionSense_Demo.ipynb + tests/
```

---

## 7. Checklist finale du rapport

```text
[ ] PDF dans report/PrivIMU_report.pdf
[ ] Source dans report/PrivIMU_report.md ou .tex
[ ] 6-8 pages
[ ] Abstract clair
[ ] Table dataset
[ ] Pipeline figure
[ ] Métriques issues de metrics.json
[ ] Figures lisibles
[ ] Limites honnêtes
[ ] Défenses privacy-by-design
[ ] Références vérifiées
[ ] Pas de TODO/FIXME
[ ] Pas de chiffre inventé
[ ] Liens repo/Colab/Streamlit corrects
```
