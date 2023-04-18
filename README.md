# M1-WINDU-Labjack
Signal Labjack T7

## Pré-requis
- Labjack T7
- Par défaut, connexion Ethernet (port 502 pour Modbus) avec un signal sur l'entrée AIN0

## Paramètres
- `windowWidth` joue sur la durée d'affichage à l'écran (en ms).
- `ptr` correspond au nombre de points. Par exemple, `ptr%20` permet de tracer 20 points à chaque update (sur de hautes fréquences, tracer 1 point par update peut ralentir l'exécution du programme).
- `interval` correspond à l'intervalle entre chaque point (en μs).

## Bibliothèques
- [LJM Library (Labjack)](https://labjack.com/pages/support?doc=/software-driver/ljm-users-guide/ljm-library-overview/)
- [PyQtGraph](https://www.pyqtgraph.org/)
