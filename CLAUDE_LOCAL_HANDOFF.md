# PrivIMU — Handoff local complet pour Claude

**Date** : 2026-05-13  
**Repo cible** : `https://github.com/akiroussama/PrivIMU`  
**But de ce fichier** : donner à Claude, lancé localement dans le repo, assez de contexte pour reprendre le projet sans perte d'information, refaire la présentation et le PDF proprement, vérifier les livrables, et éviter les erreurs déjà rencontrées.

Ce fichier est volontairement très détaillé. Il doit être lu avant toute modification du repo.

---

## 0. Résumé exécutif en 60 secondes

PrivIMU est un projet de **Sécurité IoT / Privacy** pour le cours FF6 IoT de SUP'COM. L'idée centrale : des données IMU supposées anonymes, issues d'un smartphone ou wearable — accéléromètre + gyroscope — peuvent devenir des quasi-identifiants comportementaux. Le projet montre cela sur le dataset MotionSense, avec un pipeline reproductible : téléchargement/chargement des CSV, fenêtrage 1 seconde, extraction de features, entraînement d'un Random Forest, métriques top-1/top-3/F1/entropy leakage, app Streamlit déployable, notebook Colab, rapport PDF et slides.

Le livrable ne doit pas être vendu comme une simple présentation. Il doit être vendu comme un **mini-laboratoire reproductible de privacy IoT** :

```text
anonymous IMU signal -> sliding windows -> model posterior -> top-3 identity -> privacy leakage score -> defense by Gaussian noise -> evidence card
```

La promesse orale :

> Nous ne disons pas seulement que les capteurs IMU posent un problème de confidentialité. Nous construisons un pipeline qui le montre, le mesure, le visualise et teste une défense simple.

---

## 1. Contexte académique et pédagogique

### 1.1 Cours et thème

- Cours : Formation Doctorale FF6 — IoT, Cloud & Big Data, partie IoT.
- Enseignant : M. Mohamed Ould-Elhassen Aoueileyine, SUP'COM / Université de Carthage.
- Thème choisi : **Sécurité IoT**.
- Sujet retenu : **PrivIMU — ré-identification d'utilisateurs via signaux IMU anonymes**.
- Groupe : 5 membres.
- Soutenance : doit être structurée pour environ 15 minutes, soit environ 3 minutes par membre.

### 1.2 Pourquoi PrivIMU est un bon sujet

PrivIMU coche trois cases importantes :

1. **Sécurité IoT** : la privacy est un pilier de la sécurité. Les données capteurs collectées par les objets connectés ne sont pas forcément anonymes même sans nom, email ou photo.
2. **Smart Sensors** : le sujet est très lié aux capteurs inertiels : accéléromètres, gyroscopes, smartphone, wearable.
3. **WOW effect** : le jury comprend immédiatement le choc narratif : “voici un signal anonyme ; pourtant le modèle propose l'identité probable”.

### 1.3 Ne pas confondre avec d'autres projets

Le brief initial mentionne un ancien pivot SolarPump-Edge et un autre projet parallèle sur l'épilepsie/Raman. Ne pas les réutiliser. Le repo courant est `PrivIMU` et le sujet est uniquement la privacy IMU.

---

## 2. Sujet scientifique

### 2.1 Question principale

Les données IMU partagées avec une application ou un service IoT sont souvent considérées comme anonymes parce qu'elles ne contiennent pas de nom, photo, email ou identifiant direct. La question scientifique est :

> Ces données restent-elles anonymes face à un attaquant qui dispose d'un classifieur ML et de signaux d'entraînement ?

### 2.2 Hypothèse

Un classifieur supervisé entraîné sur des fenêtres d'accéléromètre + gyroscope peut ré-identifier un utilisateur parmi 24 candidats avec une performance très supérieure au hasard.

Baseline aléatoire :

```text
1 / 24 = 4.17 %
```

Cibles initiales du brief :

```text
top-1 >= 65 %
top-3 >= 80 %
F1-macro >= 0.60
```

Attention : ces chiffres sont des cibles. Les chiffres finaux ne doivent jamais être inventés. Ils doivent venir de `reports/metrics.json`.

### 2.3 Dataset

Dataset : MotionSense.

Faits à utiliser :

```text
- 24 sujets
- 6 activités : wlk, jog, ups, dws, sit, std
- capteurs : accelerometer + gyroscope via iPhone DeviceMotion
- fréquence : environ 50 Hz
- fichiers CSV avec colonnes :
  rotationRate.x/y/z
  userAcceleration.x/y/z
  et souvent attitude.*, gravity.*
```

Le repo possède maintenant des CSV de test dans :

```text
examples/wlk_7/sub_*.csv
```

Les liens Streamlit doivent utiliser ces fichiers, pas les anciens liens `demo/sample_motionsense_like.csv` qui ne marchaient pas.

Lien raw principal conseillé :

```text
https://raw.githubusercontent.com/akiroussama/PrivIMU/main/examples/wlk_7/sub_1.csv
```

Lien dossier GitHub visible :

```text
https://github.com/akiroussama/PrivIMU/tree/main/examples/wlk_7
```

---

## 3. État du repo et ce qui a déjà été fait

### 3.1 Repo GitHub

Repo :

```text
https://github.com/akiroussama/PrivIMU
```

Branche principale :

```text
main
```

Le repo a été initialisé avec un scaffold complet comprenant :

```text
README.md
ARTIFACT_INDEX.md
pyproject.toml / requirements.txt
Makefile
task.ps1
data/download.py
src/privimu/
notebooks/PrivIMU_MotionSense_Demo.ipynb
streamlit_app.py
reports/
slides/
report/
docs/
tests/
.github/workflows/tests.yml
examples/wlk_7/sub_*.csv
```

### 3.2 Tests

Les tests unitaires initiaux passaient :

```powershell
pytest -q
# 8 tests passed
```

Quand Claude reprend localement, première commande obligatoire :

```powershell
cd D:\workspace\PrivIMU
pytest -q
```

Ne pas modifier les slides/PDF avant de vérifier l'état du repo.

### 3.3 Windows / PowerShell

Le Makefile ne marche pas nativement sur Windows PowerShell si `make` n'est pas installé. Un script `task.ps1` a été préparé pour remplacer les commandes `make`.

Commandes prévues :

```powershell
.\task.ps1 download
.\task.ps1 train-rf
.\task.ps1 evaluate
.\task.ps1 demo
```

Si PowerShell bloque :

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### 3.4 Google Colab

Notebook dans le repo :

```text
notebooks/PrivIMU_MotionSense_Demo.ipynb
```

Lien Colab direct après push :

```text
https://colab.research.google.com/github/akiroussama/PrivIMU/blob/main/notebooks/PrivIMU_MotionSense_Demo.ipynb
```

Problème rencontré : `data/download.py` avait téléchargé le repo MotionSense global au lieu de préparer directement `A_DeviceMotion_data/`. Le training cherchait :

```text
data/raw/motionsense/A_DeviceMotion_data/
```

Fix recommandé : `data/download.py` doit télécharger ou extraire `A_DeviceMotion_data.zip` pour créer ce dossier. Vérifier que le fix est bien dans le repo. Sinon le notebook Colab plantera à l'étape `python -m privimu.train`.

### 3.5 Streamlit

Fichier :

```text
streamlit_app.py
```

Fonctionnalités initiales attendues par le brief :

```text
1. Upload ou sélection d'un CSV MotionSense-like.
2. Visualisation IMU Plotly.
3. Top-3 identités probables.
4. Privacy entropy score.
5. Slider de bruit gaussien pour montrer une défense.
```

Trois fonctionnalités WOW ont été ajoutées :

```text
WOW #1 — Live identity-lock replay
- Le modèle analyse fenêtre par fenêtre.
- Courbe top-1 confidence.
- Courbe privacy leakage ΔH.
- Détection du moment où l'identité devient stable.

WOW #2 — Blue-team defense lab
- Sweep automatique de sigma, bruit gaussien.
- Graphique top-1 confidence vs leakage vs signal preservation proxy.
- Recommandation d'un niveau de bruit.

WOW #3 — One-click evidence card
- Téléchargement JSON.
- Téléchargement Markdown.
- Résumé : source, top-3, entropy, leakage, noise sigma, identity lock.
```

Dernière correction demandée : utiliser les CSV réels du repo dans `examples/wlk_7` au lieu des anciens liens `demo/*.csv`.

Streamlit doit afficher :

```text
- source sélectionnable : examples/wlk_7/sub_1.csv, sub_2.csv, etc.
- lien GitHub raw vers sub_1.csv
- lien dossier examples/wlk_7
- upload CSV toujours disponible
- fallback synthétique seulement si aucun CSV local n'est disponible
```

### 3.6 Slides et PDF déjà générés

Une première version de présentation a été générée :

```text
slides/PrivIMU_final.pptx
slides/PrivIMU_final.pdf
```

Elle était volontairement propre mais pas finale :

- 15 slides.
- Style sombre/cyber/privacy.
- Narration : intro -> menace -> dataset -> pipeline -> démo -> résultats -> défenses.
- Slide 13 contient des placeholders `run train-rf` car les vraies métriques de `reports/metrics.json` n'étaient pas encore générées.

Claude doit refaire la présentation localement from scratch, mais peut utiliser le fichier séparé `handoff/01_PRESENTATION_BASELINE_AND_REMAKE_BRIEF.md` comme description du contenu de base.

### 3.7 Rapport PDF

Un squelette de rapport existe possiblement dans :

```text
report/PrivIMU_report.md
```

Le PDF final doit être écrit proprement, 6–8 pages, avec chiffres issus uniquement de `reports/metrics.json`. Le fichier séparé `handoff/02_REPORT_PDF_OBJECTIVE_AND_OUTLINE.md` donne l'objectif détaillé.

---

## 4. Règles non négociables

### 4.1 Pas de métriques inventées

Tous les chiffres affichés dans :

```text
slides
report PDF
README
abstract
conclusion
```

doivent venir de :

```text
reports/metrics.json
```

ou d'un fichier généré par script dans `reports/`.

Interdit :

```text
"Notre modèle atteint 86 %" sans preuve.
"Top-1 = 65 %" si ce n'est pas dans metrics.json.
"CNN meilleur que RF" sans résultat généré.
```

Autorisé :

```text
"La baseline aléatoire est 1/24 = 4.17 %."
"Les résultats finaux sont dans reports/metrics.json."
"La démo Streamlit peut fonctionner en fallback UI mode avant entraînement, mais ce mode est pédagogique et non mesuré."
```

### 4.2 Scope verrouillé

Ne pas changer le sujet vers IDS, adversarial TinyML ou fingerprinting réseau. Le sujet est :

```text
Ré-identification / privacy leakage via IMU MotionSense.
```

### 4.3 Ton attendu

Ton académique, neutre, défensif :

```text
- Pas alarmiste.
- Pas hacker show-off.
- Montrer l'attaque ET les défenses.
- Insister sur privacy-by-design.
- Reconnaitre les limites du dataset et du protocole.
```

### 4.4 Éthique

Ne pas encourager une attaque contre des personnes réelles. Le dataset est public, contrôlé, et l'objectif est pédagogique/défensif.

### 4.5 Vérifications avant toute déclaration

Avant de dire “c'est fini” :

```powershell
pytest -q
python -m py_compile streamlit_app.py
python -m privimu.evaluate --metrics reports/metrics.json
streamlit run streamlit_app.py
```

Pour slides/PDF : ouvrir les fichiers produits et vérifier :

```text
- pas de placeholders oubliés
- pas de métriques non sourcées
- pas de lien cassé
- pas de texte illisible
- pas de slide surchargée
```

---

## 5. Commandes de reproduction recommandées

### 5.1 Installation locale Windows

```powershell
cd D:\workspace\PrivIMU
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev,app]"
pytest -q
```

### 5.2 Préparation dataset

```powershell
python data/download.py --dest data/raw/motionsense --force
```

Vérification :

```powershell
Get-ChildItem -Recurse data/raw/motionsense | Select-String "sub_1.csv"
```

ou simplement vérifier l'existence :

```text
data/raw/motionsense/A_DeviceMotion_data/wlk_7/sub_1.csv
```

### 5.3 Entraînement RF

Run rapide :

```powershell
python -m privimu.train --data-root data/raw/motionsense --model rf --output-dir . --window-size 50 --step-size 25 --n-splits 3 --n-estimators 50 --activities wlk --max-files 24
```

Run final RF :

```powershell
python -m privimu.train --data-root data/raw/motionsense --model rf --output-dir . --window-size 50 --step-size 25 --n-splits 5 --n-estimators 200
```

### 5.4 Évaluation

```powershell
python -m privimu.evaluate --metrics reports/metrics.json
```

### 5.5 Streamlit

```powershell
streamlit run streamlit_app.py
```

---

## 6. Ce que Claude doit refaire localement

### 6.1 Présentation

Refaire le deck from scratch :

```text
slides/PrivIMU_final.pptx
slides/PrivIMU_final.pdf
```

Contraintes :

```text
- 15 slides.
- 5 membres, 3 slides/membre environ.
- Style pro, moderne, clair.
- Pas de surcharge.
- Mettre QR code repo + Colab + Streamlit si liens disponibles.
- Slide résultats : uniquement metrics.json.
- Inclure la démo Streamlit comme climax.
```

Le contenu de base est dans :

```text
handoff/01_PRESENTATION_BASELINE_AND_REMAKE_BRIEF.md
```

### 6.2 Rapport PDF

Créer ou refaire :

```text
report/PrivIMU_report.pdf
```

Optionnel mais recommandé : source markdown ou LaTeX :

```text
report/PrivIMU_report.md
```

Objectif détaillé :

```text
handoff/02_REPORT_PDF_OBJECTIVE_AND_OUTLINE.md
```

### 6.3 Livrables

Vérifier et compléter :

```text
README.md
ARTIFACT_INDEX.md
notebooks/PrivIMU_MotionSense_Demo.ipynb
streamlit_app.py
reports/metrics.json
slides/PrivIMU_final.pptx
slides/PrivIMU_final.pdf
slides/speaker_notes/*.md
report/PrivIMU_report.pdf
docs/ETHICS_AND_LIMITS.md
docs/SOTA_TABLE.md
docs/STREAMLIT_WOW_FEATURES.md
examples/wlk_7/*.csv
```

Checklist complète :

```text
handoff/03_DELIVERABLES_WOW_CHECKLIST.md
```

---

## 7. La stratégie de soutenance

### 7.1 Message principal

> Même anonymisées, les traces de mouvement peuvent contenir une signature comportementale. PrivIMU le montre via un pipeline reproductible et une démo interactive.

### 7.2 Moment WOW

Le moment le plus fort doit être dans la démo :

```text
1. Le prof voit un CSV IMU sans identité visible.
2. L'app trace le signal.
3. L'app affiche Top-3 identité probable.
4. L'app montre ΔH, la fuite d'information.
5. L'app ajoute du bruit et la confiance baisse.
6. L'app télécharge une evidence card.
```

### 7.3 Ce que le professeur doit comprendre

```text
- Le projet est dans le thème Sécurité IoT.
- Les capteurs ne sont pas juste des capteurs innocents.
- Le pipeline est reproductible.
- Les chiffres sont générés par code.
- Le groupe a pensé attaque, défense, limites et éthique.
```

---

## 8. Pièges déjà identifiés

### 8.1 `make` sous Windows

Erreur rencontrée :

```text
make : Le terme 'make' n'est pas reconnu...
```

Solution : utiliser `task.ps1` ou les commandes Python directes.

### 8.2 Colab download MotionSense

Erreur rencontrée :

```text
FileNotFoundError: Could not find A_DeviceMotion_data under data/raw/motionsense
```

Cause : ZIP mauvais niveau. Solution : extraire/télécharger `A_DeviceMotion_data.zip`.

### 8.3 Liens CSV cassés dans Streamlit

Anciens liens :

```text
https://raw.githubusercontent.com/akiroussama/PrivIMU/main/demo/sample_motionsense_like.csv
https://raw.githubusercontent.com/akiroussama/PrivIMU/main/demo/motionsense_like_sample.csv
```

Ne pas les utiliser.

Nouveaux liens :

```text
https://raw.githubusercontent.com/akiroussama/PrivIMU/main/examples/wlk_7/sub_1.csv
https://github.com/akiroussama/PrivIMU/tree/main/examples/wlk_7
```

### 8.4 Fallback UI mode

Streamlit peut fonctionner sans `models/rf.joblib` avec un fallback synthétique. Ne pas vendre ce fallback comme résultat scientifique. Il est utile pour tester l'interface avant entraînement.

### 8.5 Slides résultats

Ne jamais laisser `run train-rf`, `TODO`, `TBD`, `placeholder`, `à mesurer` dans le deck final.

---

## 9. Prompt conseillé à donner à Claude local

Un fichier prêt à coller est fourni :

```text
handoff/04_CLAUDE_LOCAL_PROMPT.md
```

Version courte :

> Lis `CLAUDE_LOCAL_HANDOFF.md`, puis refais la présentation PPTX/PDF et le rapport PDF de PrivIMU. Vérifie le repo, utilise uniquement les métriques de `reports/metrics.json`, mets à jour les liens vers `examples/wlk_7`, produis les fichiers finaux et donne les commandes/test results.

---

## 10. Critère final de réussite

PrivIMU est prêt lorsque :

```text
- Le README donne repo + Colab + Streamlit + quickstart.
- Le notebook Colab s'exécute jusqu'à metrics.json.
- Streamlit s'ouvre et utilise un CSV examples/wlk_7.
- reports/metrics.json existe et contient les métriques finales.
- slides/PrivIMU_final.pptx et .pdf sont propres.
- report/PrivIMU_report.pdf est propre, 6-8 pages.
- Chaque chiffre du deck/rapport vient de metrics.json.
- pytest -q passe.
- Une release ou au moins un commit final propre existe.
```

La note visée n'est pas “projet qui marche à peu près”. La note visée est :

> projet reproductible + démo live + storytelling clair + chiffres vérifiés + posture éthique.
