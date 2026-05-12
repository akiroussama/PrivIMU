# M2 — Related work

Pour situer PrivIMU, il faut relier trois domaines. Le premier est la reconnaissance d'activité humaine, ou HAR. Dans ce domaine, les signaux d'accéléromètre et de gyroscope sont utilisés depuis longtemps pour reconnaître des activités comme marcher, courir, s'asseoir ou monter des escaliers. Cela montre déjà que les signaux IMU contiennent beaucoup d'information comportementale.

Le deuxième domaine est la confidentialité des données de capteurs. Le dataset MotionSense lui-même est lié à des travaux sur l'anonymisation des données sensorielles et la protection contre les inférences sensibles. L'idée importante est qu'un signal peut être utile pour une application, par exemple reconnaître une activité, tout en révélant aussi des informations non désirées, comme des attributs ou une identité probable.

Le troisième domaine est celui des biométries comportementales. Contrairement au visage ou à l'empreinte digitale, la biométrie comportementale ne mesure pas seulement ce que l'on est, mais la manière dont on agit. La démarche, le rythme, l'amplitude et les micro-variations du mouvement peuvent devenir discriminants.

Notre projet ne prétend pas résoudre tout le problème. Il prend un cas précis : 24 utilisateurs dans MotionSense, six activités, un smartphone en poche, et une tâche de classification d'identité. Ce choix est volontaire : il rend la démonstration compréhensible, reproductible, et suffisamment proche des usages IoT réels.

La différence avec un simple projet HAR est que notre cible n'est pas l'activité mais l'utilisateur. Nous utilisons donc la reconnaissance de mouvement non pas pour dire “la personne marche”, mais pour tester si le mouvement permet de dire “quel sujet a produit ce signal”.

Je passe maintenant à la méthodologie, où nous détaillons le dataset, le fenêtrage, les caractéristiques et le protocole d'évaluation.
