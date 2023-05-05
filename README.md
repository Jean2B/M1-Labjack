# M1-Labjack
Signaux Labjack T7

## Pré-requis
- Labjack T7
- Par défaut, connexion Ethernet (port 502 pour Modbus) avec un signal sur l'entrée AIN0
- Python 3
- Base de données PostgreSQL

## Installation
- Créer un environnement virtuel (vous pouvez utiliser un logiciel tel qu'Anaconda)
- Installation des packages requis : `pip install -r requirements.txt`
- Exécution : `python graph_ljm.py`

*Note : si vous souhaitez utiliser le LabJack avec une connexion USB, il est nécessaire de télécharger le driver du LabJack, et modifier le type de connexion en passant par exemple de TCP à ANY: `connection_type = "ANY"`* 

## Description
Ce code permet de lire, d'enregistrer en base de données et d'afficher en temps réel une mesure d'entrée analogique provenant d'un LabJack:

- Un `handle` est ouvert pour le premier LabJack trouvé. Cette opération permet d'initialiser la communication avec le périphérique.
- Les informations sur le périphérique sont récupérées à l'aide de la fonction `getHandleInfo()` et affichées dans la console.
- Une connexion à la base de données PostgreSQL est effectuée à l'aide de `dbms_class`.
- Une fenêtre graphique est créée à l'aide de `PyQtGraph` avec une zone de tracé nommée "Labjack Signal GUI" et une courbe de tracé nommée `curve`. Cette courbe est initialisée avec des données nulles.
- La fonction `update()` est définie pour recevoir les données, et fait appel à `insert_db()` et `graph()` pour insérer en base de données les valeurs lues sur les entrées analogiques, et mettre à jour les données de la courbe.
- La fenêtre graphique est affichée.
- Une boucle infinie est exécutée pour lire en continu les valeurs des entrées analogiques, les insérer dans la base de données et mettre à jour la courbe.

## Paramètres
- Informations de connexions à la base de données : `host`, `dbname`, `port`, `user`, `password`.
- `inputs` est la liste des noms des entrées du Labjack à lire (par défaut : AIN0, AIN1, AIN2, AIN3).
- `windowWidth` joue sur la durée d'affichage à l'écran (en ms).
- `ptr` correspond au nombre de points. Par exemple, `ptr%20` permet de tracer 20 points à chaque update (sur de hautes fréquences, tracer 1 point par update peut ralentir l'exécution du programme).
- `interval` correspond à l'intervalle entre chaque point (en μs).

## Bibliothèques
- [LJM Library (Labjack)](https://labjack.com/pages/support?doc=/software-driver/ljm-users-guide/ljm-library-overview/) Pour communiquer avec le périphérique.
- [PyQtGraph](https://www.pyqtgraph.org/) Pour tracer le graphe en temps réel.
- [Psycopg 2](https://www.psycopg.org/) Pour se connecter à la base de données PostgreSQL.

## En savoir plus
- [Labjack Documentation](https://labjack.com/products/labjack-t7)
