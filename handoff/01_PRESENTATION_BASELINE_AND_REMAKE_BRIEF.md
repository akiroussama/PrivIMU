# 01 — Contenu de la présentation baseline + consignes pour refaire le deck

Ce fichier décrit la présentation que ChatGPT a déjà produite, ainsi que les consignes pour la refaire localement from scratch. Claude doit s'en servir comme brief narratif, pas comme contrainte graphique rigide.

---

## 1. Objectif de la présentation finale

Créer une présentation de soutenance qui donne au professeur l'impression d'un projet complet, sérieux et reproductible.

Le deck final doit :

```text
- être compréhensible par un jury non spécialiste ML ;
- être crédible pour un enseignant IoT/sécurité ;
- avoir une démo comme climax ;
- montrer les résultats réels issus de reports/metrics.json ;
- rappeler les limites et défenses ;
- donner envie de visiter le repo GitHub.
```

Durée cible : 15 minutes. Groupe de 5 personnes. Environ 3 minutes par personne.

Nombre de slides cible : 15.

---

## 2. Style recommandé

Style initial utilisé : sombre, cyber/privacy, high-tech, mais lisible.

Pour refaire from scratch, garder :

```text
- fond sombre ou clair très propre, au choix ;
- typographie grande ;
- peu de texte par slide ;
- 1 idée par slide ;
- visuels : pipeline, signaux, matrices, cards, gauges ;
- couleur accent pour privacy/security ;
- aucun texte minuscule ;
- aucune métrique placeholder en version finale.
```

Éviter :

```text
- slides surchargées ;
- bullet lists longues ;
- images décoratives sans valeur ;
- chiffres non vérifiés ;
- ton alarmiste ;
- “hackers”, skulls, cyber clichés excessifs.
```

---

## 3. Structure globale baseline

La présentation baseline a 15 slides :

```text
1. Title — PrivIMU
2. IMU in IoT
3. Scientific question
4. Threat model
5. Related work positioning
6. MotionSense dataset
7. Reproducible pipeline
8. Preprocessing / features / models
9. Evaluation protocol
10. Demo architecture
11. Live attack
12. Noise defense
13. Results from metrics.json
14. Limits and mitigations
15. Takeaway + QR links
```

---

## 4. Répartition orale 5 membres

```text
M1 — Slides 1 à 3 : introduction, contexte, problème
M2 — Slides 4 à 5 : threat model + état de l'art
M3 — Slides 6 à 9 : dataset + pipeline + méthode + évaluation
M4 — Slides 10 à 12 : démo Streamlit + attaque + défense
M5 — Slides 13 à 15 : résultats + limites + conclusion
```

Chaque membre doit avoir un rôle défendable. Le prof doit sentir que le groupe entier maîtrise.

---

## 5. Détail slide par slide

### Slide 1 — Title

**Titre proposé** :

```text
PrivIMU
Motion data are not automatically anonymous
```

**Sous-titre** :

```text
A reproducible IoT privacy lab using accelerometer and gyroscope traces
```

**Contenu visuel** :

```text
- icône smartphone / wearable
- petit flux : IMU -> ML -> identity risk
- nom du cours / groupe / repo GitHub
```

**Message oral** :

Nous allons montrer que des signaux de mouvement apparemment anonymes peuvent contenir des signatures comportementales exploitables par un modèle ML.

**À ne pas faire** : afficher un score type 86 % dès la slide 1 si non prouvé.

---

### Slide 2 — IMU in IoT

**Titre** :

```text
IMU sensors are everywhere in IoT
```

**Message** :

Les capteurs inertiels sont présents dans les smartphones, montres, trackers santé, sports, applications de mobilité et objets connectés. Ils sont souvent collectés parce qu'ils semblent moins sensibles qu'une caméra ou un micro.

**Bullets courts** :

```text
- Smartphones and wearables
- Health, sport, mobility, smart environments
- Low-cost, continuous, high-frequency data
- Often perceived as “anonymous”
```

**Visuel** :

Carte d'écosystème IoT avec IMU au centre.

---

### Slide 3 — Scientific question

**Titre** :

```text
Anonymous does not mean non-identifiable
```

**Question affichée** :

```text
Can accelerometer + gyroscope traces identify a user without direct identifiers?
```

**Baseline à afficher** :

```text
Random guess among 24 subjects = 4.17 %
```

**Message** :

Le problème n'est pas l'identifiant direct. Le problème est le signal comportemental latent.

**Transition** :

Pour comprendre l'attaque, nous définissons d'abord le modèle de menace.

---

### Slide 4 — Threat model

**Titre** :

```text
Threat model: motion traces as quasi-identifiers
```

**Attacker story** :

```text
1. An app collects IMU traces.
2. Direct identifiers are removed.
3. The attacker has reference traces from known users.
4. A classifier predicts the most likely subject.
```

**Visuel** :

Diagramme 4 blocs : user -> IoT app -> anonymized IMU -> ML attacker -> top-3 identity.

**Important** :

Préciser que c'est un cadre académique, dataset public, pas une attaque contre des personnes réelles.

---

### Slide 5 — Related work positioning

**Titre** :

```text
From activity recognition to identity leakage
```

**Message** :

La littérature HAR montre qu'on peut reconnaître l'activité. PrivIMU déplace la question : peut-on reconnaître la personne ?

**Axes à afficher** :

```text
- Human Activity Recognition
- Gait / behavioral biometrics
- Sensor privacy leakage
- Defenses: noise, minimization, edge learning, DP/federated learning
```

**Visuel** :

Mini-tableau SOTA 4 colonnes ou timeline.

**Attention** :

Les références du rapport doivent être vérifiées. Ne pas inventer de DOI.

---

### Slide 6 — MotionSense dataset

**Titre** :

```text
Dataset: MotionSense
```

**Faits** :

```text
- 24 subjects
- iPhone DeviceMotion in pocket
- 50 Hz sampling
- 6 activities: walking, jogging, upstairs, downstairs, sitting, standing
- channels used: rotationRate + userAcceleration
```

**Visuel** :

Carte dataset + six activités + six canaux.

**Message oral** :

MotionSense est adapté parce qu'il contient des données capteurs réelles, publiques et structurées.

---

### Slide 7 — Reproducible pipeline

**Titre** :

```text
A reproducible privacy pipeline
```

**Pipeline** :

```text
CSV -> windows -> normalization -> features -> model -> metrics.json -> Streamlit demo
```

**Message** :

Chaque chiffre affiché dans le rapport et les slides doit pouvoir être régénéré.

**Visuel** :

Pipeline horizontal avec `reports/metrics.json` en bloc central.

**Phrase clé** :

```text
metrics.json is the source of truth.
```

---

### Slide 8 — Preprocessing, features, models

**Titre** :

```text
How the signal becomes evidence
```

**Contenu** :

```text
Windowing:
- 1 second = 50 samples
- 50 % overlap = step 25

Features:
- mean, std, rms, min, max
- spectral / entropy descriptors

Models:
- Random Forest baseline
- optional 1D-CNN extension
```

**Visuel** :

Signal découpé en fenêtres + feature vector.

---

### Slide 9 — Evaluation protocol

**Titre** :

```text
Evaluation: avoid inflated results
```

**Métriques** :

```text
- Top-1 accuracy
- Top-3 accuracy
- Macro-F1
- Confusion matrix
- Per-subject F1
- Latency per window
- Privacy entropy leakage ΔH
```

**Protocole** :

Utiliser le split implémenté dans le code. Si le code n'est pas réellement LOTO, ne pas écrire LOTO. Vérifier `train.py` avant finalisation. Si la version actuelle utilise `StratifiedKFold`, écrire honnêtement `stratified cross-validation`.

**Point critique** :

La présentation doit être alignée sur le code réel.

---

### Slide 10 — Demo architecture

**Titre** :

```text
Live demo: from CSV to privacy risk
```

**Flux** :

```text
Upload/select CSV -> plot signal -> predict top-3 -> compute ΔH -> test noise defense -> export evidence card
```

**Visuel** :

Screenshot Streamlit ou mockup.

**Message** :

La démo est le cœur du projet, pas un bonus.

---

### Slide 11 — Live attack

**Titre** :

```text
WOW #1: identity-lock replay
```

**Contenu** :

```text
- Window-by-window posterior
- Confidence curve
- Identity lock time
- Top-3 identities
```

**Visuel** :

Capture de la courbe top-1 confidence + leakage.

**Phrase orale** :

Nous ne montrons pas seulement une prédiction finale. Nous montrons quand l'identité devient stable.

---

### Slide 12 — Noise defense

**Titre** :

```text
WOW #2: blue-team defense lab
```

**Contenu** :

```text
- Gaussian noise slider
- Noise sweep
- Leakage decreases
- Utility/privacy trade-off
```

**Visuel** :

Courbe sigma vs top-1 confidence / leakage.

**Message** :

Le projet ne s'arrête pas à l'attaque. Il montre aussi une mitigation pédagogique.

---

### Slide 13 — Results from metrics.json

**Titre** :

```text
Results: measured, not hand-written
```

**Contenu final attendu** :

```text
Random Forest:
- Top-1: value from metrics.json
- Top-3: value from metrics.json
- Macro-F1: value from metrics.json
- Latency: value from metrics.json
- Privacy leakage: value from metrics.json
```

**Visuel** :

Carte de métriques + confusion matrix miniature.

**État baseline** :

La première version du deck affichait `run train-rf` parce que les métriques n'étaient pas encore générées. Claude doit remplacer cela par les vraies valeurs.

**Règle** :

Si `reports/metrics.json` n'existe pas, mettre la slide en mode “protocol ready, metrics pending” uniquement pour draft interne, jamais dans le PDF final.

---

### Slide 14 — Limits and mitigations

**Titre** :

```text
Limits and privacy-by-design mitigations
```

**Limites** :

```text
- Dataset limited to 24 subjects
- Closed-set classification
- Phone position and activity dependence
- Public benchmark not production environment
- Noise defense is pedagogical, not a complete guarantee
```

**Mitigations** :

```text
- Data minimization
- On-device processing
- Federated learning
- Differential privacy
- Feature-level sharing instead of raw traces
- User consent and transparency
```

**Message** :

Une bonne soutenance gagne des points en reconnaissant ses limites.

---

### Slide 15 — Takeaway + QR links

**Titre** :

```text
Takeaway: motion data can be privacy-sensitive
```

**Trois takeaways** :

```text
1. IMU traces can contain behavioral identity signals.
2. Privacy leakage can be measured, not only discussed.
3. IoT systems should treat motion data as potentially sensitive.
```

**Liens** :

```text
GitHub repo
Google Colab
Streamlit demo
Report PDF
```

**Visuel** :

QR codes ou cards de liens.

---

## 6. Design des QR codes

À générer si les liens sont stables :

```text
Repo: https://github.com/akiroussama/PrivIMU
Colab: https://colab.research.google.com/github/akiroussama/PrivIMU/blob/main/notebooks/PrivIMU_MotionSense_Demo.ipynb
Streamlit: URL exacte de l'app déployée
CSV: https://github.com/akiroussama/PrivIMU/tree/main/examples/wlk_7
```

Si Streamlit n'est pas encore déployé, ne pas afficher un faux QR. Mettre “Live demo from repo” ou laisser le lien à compléter seulement dans un draft.

---

## 7. Speaker notes attendues

Créer ou mettre à jour :

```text
slides/speaker_notes/M1_intro.md
slides/speaker_notes/M2_sota.md
slides/speaker_notes/M3_methodology.md
slides/speaker_notes/M4_demo.md
slides/speaker_notes/M5_results.md
```

Chaque script :

```text
- 450 à 520 mots
- ton oral naturel
- transition vers le membre suivant
- aucun chiffre non sourcé
- rôle individuel clair
```

---

## 8. Checklist de validation du deck

Avant export final :

```text
[ ] 15 slides maximum ou très proche.
[ ] Pas de placeholder.
[ ] Pas de métrique inventée.
[ ] Slide 13 alimentée par metrics.json.
[ ] Liens GitHub/Colab/Streamlit corrects.
[ ] Style cohérent.
[ ] Le deck est lisible en PDF.
[ ] Le deck raconte attaque + défense + éthique.
[ ] Les scripts des 5 membres existent.
[ ] Le fichier PPTX et le PDF sont dans slides/.
```
