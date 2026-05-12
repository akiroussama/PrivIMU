# M1 — Introduction and problem

Bonjour. Nous présentons PrivIMU, un projet de sécurité IoT centré sur la confidentialité des données de mouvement. Dans beaucoup d'applications mobiles et IoT, les capteurs inertiels comme l'accéléromètre et le gyroscope sont considérés comme peu sensibles, parce qu'ils ne contiennent pas directement un nom, un numéro de téléphone, une adresse email ou une image du visage. Pourtant, ces capteurs décrivent la manière dont une personne bouge, marche, tient son téléphone, monte les escaliers ou reste immobile.

Notre question est simple : si une trace IMU est anonyme, est-elle vraiment non identifiable ? Pour répondre, nous ne faisons pas une discussion abstraite. Nous construisons une expérience reproductible sur le dataset public MotionSense. Le scénario est celui d'un attaquant qui possède des traces d'entraînement pour plusieurs utilisateurs déjà enrôlés, puis reçoit une nouvelle trace de mouvement sans identifiant. Son objectif est de prédire quel utilisateur a probablement produit cette trace.

Le projet se place donc dans le thème sécurité IoT, avec un angle privacy. Nous voulons montrer que la sécurité ne concerne pas seulement le chiffrement, les attaques réseau ou l'authentification. Elle concerne aussi les données que les objets connectés collectent tous les jours et les inférences que l'on peut faire à partir d'elles.

La contribution de PrivIMU est un mini-laboratoire complet : téléchargement des données, prétraitement, extraction de caractéristiques, entraînement du modèle, évaluation, figures, application Streamlit et discussion des limites. Tous les chiffres finaux doivent venir du fichier metrics.json généré par le code. Cela évite les résultats décoratifs et rend le projet vérifiable par le professeur.

Je passe maintenant à l'état de l'art, qui montre pourquoi cette question est crédible scientifiquement.
