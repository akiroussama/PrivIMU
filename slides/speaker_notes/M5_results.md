# M5 — Results and conclusion

Les résultats finaux sont lus depuis reports/metrics.json. Nous présentons d'abord la top-1 accuracy, qui mesure la proportion de fenêtres où le modèle prédit directement le bon sujet. Ensuite, nous présentons la top-3 accuracy, qui mesure si le bon sujet apparaît parmi les trois candidats les plus probables. Cette métrique est importante pour la privacy, car un attaquant n'a pas toujours besoin d'être certain : réduire fortement la liste des candidats est déjà une fuite d'information.

Nous analysons aussi le F1-macro, qui donne le même poids à chaque sujet. Cela évite de cacher une performance faible sur certains individus derrière une moyenne globale. La matrice de confusion montre quelles identités sont confondues. Le graphe de F1 par sujet permet de voir si certains utilisateurs sont beaucoup plus identifiables que d'autres.

Sur le plan sécurité IoT, la conclusion est claire : une donnée sans identifiant direct peut rester sensible. Les traces IMU doivent donc être traitées comme des données de privacy, surtout lorsqu'elles sont collectées en continu par des objets personnels. Les défenses possibles incluent la minimisation des données, le traitement local, le partage de caractéristiques moins sensibles, la confidentialité différentielle et l'apprentissage fédéré.

Nous reconnaissons aussi les limites : MotionSense contient 24 sujets, le scénario est closed-set, le téléphone est en poche, et le bruit gaussien n'est pas une garantie formelle. Mais ces limites ne détruisent pas le message principal. Elles montrent au contraire que même dans un cadre contrôlé et modeste, il existe une fuite mesurable.

Notre contribution n'est donc pas seulement une présentation. C'est un mini-lab reproductible qui permet de télécharger les données, entraîner le modèle, vérifier les métriques, visualiser l'attaque et discuter les défenses.
