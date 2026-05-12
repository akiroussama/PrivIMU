# M4 — Live demo

La démo Streamlit est conçue pour rendre l'idée immédiatement visible. À gauche, nous affichons un signal IMU. Il peut venir d'un fichier CSV MotionSense ou d'un exemple embarqué pour tester l'interface. Ce signal ne contient pas de nom, pas d'email et pas de champ identité affiché à l'utilisateur. Pourtant, il contient des variations temporelles produites par le mouvement.

Ensuite, l'application applique le même pipeline que l'expérience : fenêtrage, normalisation, extraction de caractéristiques et passage dans le modèle entraîné. Le résultat n'est pas seulement une classe unique. Nous affichons le top-3 des sujets les plus probables, avec leurs scores de confiance. Cela rend le scénario d'attaque plus réaliste : même si la première prédiction n'est pas toujours correcte, la vraie identité peut apparaître dans les premières hypothèses.

La troisième partie de la démo est le score d'entropie. Avant observation, avec 24 sujets, l'incertitude maximale est log2(24). Après la prédiction, la distribution du modèle devient souvent plus concentrée. La différence entre ces deux entropies représente une fuite d'information : plus elle est élevée, plus le signal réduit l'anonymat.

Enfin, nous avons ajouté un slider de bruit gaussien. Quand on augmente le bruit, on observe que la confiance du modèle peut diminuer et que l'entropie augmente. Ce n'est pas présenté comme une défense parfaite, mais comme une visualisation pédagogique de l'idée : modifier le signal peut réduire l'information identifiable, au prix potentiel d'une perte d'utilité.

Je passe maintenant aux résultats, aux limites et aux implications sécurité IoT.
