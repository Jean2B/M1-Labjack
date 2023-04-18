# M1-WINDU-Labjack
Signal Labjack T7

## Pré-requis
- Labjack T7
- Par défaut, connexion Ethernet (port 502 pour Modbus) avec un signal sur l'entrée AIN0

## Description
Ce code permet de lire et d'afficher en temps réel une mesure d'entrée analogique provenant d'un LabJack:

- Un handle est ouvert pour le premier LabJack trouvé. Cette opération permet d'initialiser la communication avec le périphérique.
- Les informations sur le périphérique sont récupérées à l'aide de la fonction getHandleInfo() et affichées dans la console.
- Le nom de la mesure à lire est défini ("AIN0").
- Une application PyQt est créée.
- Une fenêtre graphique est créée avec une zone de tracé nommée "Labjack Signal GUI" et une courbe de tracé nommée "curve". Cette courbe est initialisée avec des données nulles.
- La fonction update() est définie pour mettre à jour les données de la courbe avec la dernière valeur lue sur l'entrée analogique.
- La fenêtre est affichée.
- Une boucle infinie est exécutée pour lire en continu la valeur de l'entrée analogique et mettre à jour la courbe.
- L'application Qt est exécutée.

## Paramètres
- `windowWidth` joue sur la durée d'affichage à l'écran (en ms).
- `ptr` correspond au nombre de points. Par exemple, `ptr%20` permet de tracer 20 points à chaque update (sur de hautes fréquences, tracer 1 point par update peut ralentir l'exécution du programme).
- `interval` correspond à l'intervalle entre chaque point (en μs).

## Bibliothèques
- [LJM Library (Labjack)](https://labjack.com/pages/support?doc=/software-driver/ljm-users-guide/ljm-library-overview/) Pour communiquer avec le périphérique.
- [PyQtGraph](https://www.pyqtgraph.org/) Pour tracer le graphe en temps réel.

## Learn More
- [Labjack Documentation](https://labjack.com/products/labjack-t7)