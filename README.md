## Présentation

Le projet KivyPyRobots vise à rendre WebPyRobots [lien] plus ergonomique pour les utilisateurs mobiles. Ainsi, la connexion à Internet n'est pas requise et l'application est utilisable sur n'importe quel système, que ce soit mobile ou ordinateur. Elle reproduit donc les grandes fonctionnalités du site : maintenir un tank, lui fournir un pilote artificiel codé en python pour pouvoir le faire combattre contre d'autres. Contrairement au site, on ne battra pas contre les pilotes des autres utilisateurs, mais contre des pilotes prédéfinis sous forme de niveaux à passer, et cela pour permettre une indépendance à la connexion. 



## État des lieux

Il reste beaucoup de travail à faire. L'affichage des batailles est notamment améliorable. La bataille affichée est une bataille par défaut et non un bataille enregistrée dans la base de données. On pourra aussi par exemple afficher les balles tirées, faire en sorte d'utiliser des textures, qu'il s'adapte aux redimensionnements. 

L'éditeur de code est fonctionnel et testé, mais un bug subsiste. Lorsqu'on clique sur un bouton de suggestion, l'entrée du code perd le focus et ne peux donc pas sélectionner la partie à changer. Donner le focus à un TextInput (ou un CodeInput dans ce cas) est un bug connu de kivy, et il semblerait que le hack trouvé pour contourner le problème ne permette pas la sélection. 



## Dépendances

Python >= 3.5

Cythpon == 0.23

Kivy >= 1.9



## Installation

L’application est développée avec python et kivy, et donc pour la faire tourner il va falloir installer quelques trucs.
Tout d’abord kivy a besoin d’une version de python 3.5 ou plus récente, il faut donc vérifier votre version de python si vous l’avez, sinon je vous invite à télécharger et à installer python.
### Installation sur Windows
Pour être sûr, vous pouvez vérifier la version de python ; pour cela il faut aller dans le répertoire de python, ouvrir le terminal de python, et faire:

    python –version

Installez pip et Wheel :

    python -m pip install –upgrade pip wheel setuptools
Installez les dépendences :

    python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
    
Installer Kivy :

    python -m pip install kivy


### Installation sous Linux 
Dans le terminal tapez :

    $ sudo apt-get install python-kivy

Ensuite tapez les commandes suivantes : 

    $ sudo  pip install pygments docutils
    
    $ sudo apt-get install python-setuptools python-pygame python-opengl \
    python-gst0.10 python-enchant gstreamer0.10-plugins-good python-dev \
    build-essential libgl1-mesa-dev-lts-quantal libgles2-mesa-dev-lts-quantal\
    
    python-pip

Kivy a besoin d’une version recente de Cython, donc c’est mieux d’utiliser la dernière version  :

    $ sudo pip install –upgrade Cython==0.27.3
    
### Installation sous OS X

Sans utiliser brew, vous pouvez installer les dépendances pour kivy en exécutant manuellement les commandes suivantes:

                    curl –O -L https://www.libsdl.org/release/SDL2-2.0.4.dmg                				        curl -O -L https://www.libsdl.org/projects/SDL_image/release/SDL2_image-2.0.1.dmg 		        curl -O -L https://www.libsdl.org/projects/SDL_mixer/release/SDL2_mixer-2.0.1.dmg		        curl -O -L https://www.libsdl.org/projects/SDL_ttf/release/SDL2_ttf-2.0.13.dmg		        curl -O -L http://gstreamer.freedesktop.org/data/pkg/osx/1.7.1/gstreamer-1.0-1.7.1-x86_64.pkg    												        curl -O -L http://gstreamer.freedesktop.org/data/pkg/osx/1.7.1/gstreamer-1.0-devel -1.7.1-x86_64.pkg        												        hdiutil attach SDL2-2.0.4.dmg 								        sudo cp -a /Volumes/SDL2/SDL2.framework /Library/Frameworks/

Cela devrait vous demander votre mot de passe root, vous devez le fournir, puis executer les lignes suivantes:
             
                     hdiutil attach SDL2_image-2.0.1.dmg     							       sudo cp -a /Volumes/SDL2_image/SDL2_image.framework/Library/Frameworks/   		       hdiutil attach SDL2_ttf-2.0.13.dmg 								       sudo cp -a /Volumes/SDL2_ttf/SDL2_ttf.framework /Library/Frameworks/ 			       hdiutil attach SDL2_mixer-2.0.1.dmg   							       sudo cp -a /Volumes/SDL2_mixer/SDL2_mixer.framework/Library/Frameworks/   		       sudo installer -package gstreamer-1.0-1.7.1-x86_64.pkg -target /  				       sudo installer -package gstreamer-1.0-devel-1.7.1-x86_64.pkg -target /  			       pip install --upgrade --user cython pillow

Maintenant que vous avez toutes les dépendances pour kivy, vous devez vous assurer que les outils de ligne de commande sont installés:

               	xcode-select --install
Pour vérifier si kivy est installé, tapez la commande suivante dans votre terminal:

        		python -c “import kivy”

Et voilà, vous pouvez à présent coder avec kivy. Pour lancer notre application vous devez aller dans le répertoire GUI et lancer la classe main.


## Utilisation

Le fichier à lancer est main.py. On pourra aussi lancer les modules individuellement dans le cadre de tests


## Architecture 

Le projet est divisé en deux modules indépendants : editor et fight, ainsi qu'un module Menu pour lier les deux. 

__Explication des fichiers__

* editor.py -> Description du comportement de l'éditeur. Renseigne notament les suggestion, l'autoindentation, la sauvegarde et le chargement du code utilisateur.

* suggestion.py -> Renferme les informations concernant les suggestions de l'éditeur. On y retrouve le texte à afficher, le texte à insérer au clic, et la zone de sélection après l'insertion. 

* fight.py -> Affichage de la bataille. Contient aussi les classes de récupération dans la base de données et l'interface avec le fonctionnement du jeu.

* Game.py -> Fonctionnement du jeu récupéré de WebPyRobots. 

* Data/kivy.db -> Base de données SQLite.

* GUI/main.py -> Initialisation des menus. Penser à inclure le screen que l'on veut rajouter même si PyCharm le considère comme non utilisé.

* GUI/kivy.kv -> Description de la hiérarchie de la GUI. 
