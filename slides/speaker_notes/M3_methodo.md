# M3 — Methodology

La méthodologie part du dataset MotionSense. Nous utilisons les fichiers de DeviceMotion, qui contiennent notamment les vitesses de rotation du gyroscope et l'accélération utilisateur. Le signal est échantillonné à 50 Hz. Nous segmentons donc les séries temporelles en fenêtres d'une seconde, soit 50 échantillons, avec un recouvrement de 50 %. Ce choix donne suffisamment de contexte temporel tout en gardant une latence compatible avec une démo interactive.

Pour chaque fenêtre, nous appliquons une normalisation z-score par fenêtre et par canal. Ensuite, nous extrayons 60 caractéristiques : dix descripteurs pour chacun des six canaux. Les caractéristiques incluent par exemple la moyenne, l'écart-type, le RMS, le minimum, le maximum, la médiane, l'IQR, l'asymétrie, la kurtosis et l'entropie spectrale. L'objectif est de capturer à la fois l'intensité, la variabilité et une partie de la structure fréquentielle du mouvement.

Le modèle principal est une Random Forest. Ce choix est important : il est robuste, rapide sur CPU et facile à défendre à l'oral. Nous avons aussi prévu une extension 1D-CNN pour apprendre directement depuis les fenêtres brutes, mais le projet reste solide même si la Random Forest est le modèle final.

L'évaluation est group-aware : le script évite de mélanger des fenêtres du même groupe activité-essai entre l'entraînement et le test. Les métriques sont top-1, top-3, F1-macro, matrice de confusion, F1 par sujet, latence et fuite d'entropie privacy.

La règle la plus importante est que les résultats ne sont jamais saisis à la main. Ils sont générés par le script d'entraînement et écrits dans reports/metrics.json. C'est ce fichier qui sert de source unique pour le rapport et les slides.

Je passe maintenant à la démo live, qui montre concrètement l'attaque et l'effet d'une défense simple.
