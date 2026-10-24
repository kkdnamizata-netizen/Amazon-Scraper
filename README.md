 Amazon.fr High-Tech Scraper

 1. Description

Ce projet récupère automatiquement des produits de la catégorie High-Tech d'Amazon.fr et les enregistre dans des fichiers exploitables.

Pour chaque produit, le programme essaie d'extraire :

 le nom (titre)
 le prix
 la couleur (si elle existe)
 la description et les points clés
 jusqu'à 3 images téléchargées
 l'identifiant Amazon (ASIN) et l'URL propre du produit

Les résultats sont enregistrés en CSV et en Excel, et un rapport HTML global résume l'exécution (durée, nombre de produits, erreurs).

Le projet a été réalisé en Python avec Selenium et BeautifulSoup. Il a été testé sur Windows avec Python 3.13.15 et Visual Studio Code Insiders.

2. Prérequis

 Windows 11
 Python 3.13.15
 Visual Studio Code 
 Google Chrome installé
 Une connexion internet

3. Installation (étape par étape)

Toutes les commandes se tapent dans le terminal PowerShell, depuis le dossier du projet.

 Étape 1 : ouvrir le dossier du projet

Ouvrir le dossier amazon_scraper_mvc dans Visual Studio Code . Ce dossier contient notamment README.md, requirements.txt, controllers, models et views.

Dans le terminal, se placer dans ce dossier :

powershell
cd chemin\vers\amazon_scraper_mvc

Remplacer le chemin par l'emplacement réel du dossier sur l'ordinateur.

 Étape 2 : créer l'environnement virtuel

Cette commande est à exécuter une seule fois, si l'environnement virtuel n'existe pas déjà :

powershell
python -m venv venv


L'environnement virtuel permet d'installer les bibliothèques nécessaires au projet sans les mélanger avec les autres projets Python.

 Étape 3 : activer l'environnement virtuel

À refaire à chaque nouvelle fenêtre PowerShell :

powershell
venv\Scripts\activate


Le début de la ligne de commande doit afficher (venv) lorsque l'environnement est activé.

Si PowerShell refuse d'exécuter le script, taper la commande suivante une seule fois :

powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned


Puis recommencer l'étape 3.

 Étape 4 : installer les bibliothèques

Avec l'environnement virtuel activé, exécuter :

powershell
python -m pip install --upgrade pip
pip install -r requirements.txt


Le fichier requirements.txt contient les bibliothèques utilisées par le programme, notamment Selenium, BeautifulSoup, pandas, requests, openpyxl et lxml.


 4. Lancer le script

Depuis le dossier du projet, avec (venv) actif, exécuter :

powershell
python -m controllers.main


Ce qui se passe :

 Chrome s'ouvre 
 Le programme charge la page de recherche des ordinateurs portables sur Amazon.fr.
 Il recherche les liens des produits
 il traite au maximum une sous-catégorie
 Il tente d'extraire jusqu'à 5 produits
 Il affiche sa progression dans le terminal
 Il enregistre les résultats et génère un rapport HTML

À la fin, le terminal affiche le chemin du dossier des résultats. Appuyer sur Entrée  dans le terminal pour terminer le script.

Pendant le scraping, Chrome navigue automatiquement entre les pages. C'est normal. Il vaut mieux éviter de cliquer dans la fenêtre Chrome ou de la fermer pendant l'exécution.

Amazon peut afficher un CAPTCHA ou empêcher le chargement de certaines pages. Dans ce cas, le scraping peut être partielle. Il est possible de réessayer plus tard.

 5. Résultats

Tout est enregistré dans le dossier output_amazon_technologies.

Le dossier est organisé de la manière suivante :

output_amazon_technologies/
    extraction_report.html   
    <nom de la sous-catégorie>/
        <nom>.csv
        <nom>.xlsx(pour ouvrir: click droit, reveal in file .Le dossier contenant le fichier s'ouvrira dans l'Explorateur de fichiers Windows.)
        images/


Les fichiers CSV et Excel sont générés lorsque des produits ont été extraits.

Pour ouvrir le rapport depuis le dossier du projet :

powershell
start output_amazon_technologies\extraction_report.html

 6. Réglages

Les réglages se trouvent au début du fichier controllers/scraper.py.

HEADLESS = False : Chrome reste visible pendant le scarping
MAX_PAGES = 1 nombre de pages de résultats par sous-catégorie  MAX_PRODUCTS = 5 nombre de produits par sous-catégorie	

Le nombre de sous-catégories traitées se règle dans controllers/main.py, sur la ligne :

for name, link in subcats[:1]:

Le nombre 1 limite le traitement à une seule sous-catégorie. Il est possible de modifier cette valeur pour en traiter davantage.

Conseil : commencer avec les limites actuelles, puis les augmenter progressivement si nécessaire. Chaque produit demande environ 8 secondes. Aller trop vite ou trop loin augmente le risque d'être bloqué par Amazon. 

 7. Conception du projet
 7.1 Architecture MVC

Le code est séparé en trois parties, selon le modèle MVC (Modèle Vue Contrôleur).

L'organisation principale du projet est la suivante :

amazon_scraper_mvc/
    controllers/
        main.py
point d'entrée : orchestre l'exécution
        scraper.py
logique de scraping (Selenium + BeautifulSoup)
    models/
        product.py
classe Product : structure d'un produit
    views/
        saver.py
sauvegarde des produits en CSV et Excel
        reporter.py
génération du rapport HTML
    requirements.txt
liste des bibliothèques Python
    README.md            
ce fichier

controllers/main.py : lance le programme et organise les étapes.
controllers/scraper.py : ouvre les pages Amazon et récupère les informations des produits.
models/product.py : contient la classe Product, qui représente un produit.
views/saver.py : enregistre les données en CSV et Excel.
 views/reporter.py : crée le rapport HTML.
 requirements.txt : contient la liste des bibliothèques nécessaires.
 README.md : explique l'installation, l'utilisation et le fonctionnement du projet.

models: représente les informations d'un produit, views: s'occupe des résultats et controllers: organise l'exécution.

Cette organisation permet de séparer les différentes parties du programme et de faciliter les modifications.

 7.2 Technologies utilisées

Les principales bibliothèques utilisées sont :

 selenium : piloter Chrome et charger les pages web.
 webdriver-manager : installer automatiquement le pilote Chrome adapté.
 beautifulsoup4 : rechercher les informations dans le HTML des pages.
 lxml : analyser le HTML avec BeautifulSoup.
 requests : télécharger les images.
 pandas : organiser les données sous forme de tableau.
 openpyxl : enregistrer les fichiers Excel.

 7.3 Déroulement du programme

1. main.py crée le dossier de sortie et lance Chrome avec create_driver.
2. find_subcategories charge la page de recherche définie dans TECH_CATEGORY_URL et recherche les liens des sous-catégories.
3. scrape_subcategory parcourt les résultats en respectant les limites définies.
4. extract_product_links_from_search récupère les liens des produits et les normalise au format https://www.amazon.fr/dp/ASIN.
5. parse_product ouvre la fiche du produit et essaie d'extraire le titre, le prix, la couleur, la description, les points clés et les images.
6. Le programme essaie de télécharger les trois premières images du produit.
7. Saver.save_products enregistre les données dans les fichiers CSV et Excel.
8. Reporter.generate_report crée le rapport HTML avec le résumé de l'exécution et les erreurs rencontrées.

 7.4 Choix techniques

 Des pauses aléatoires entre les pages pour limiter les blocages. 
Les erreurs rencontrées sont enregistrées dans la liste errors et peuvent apparaître dans le rapport.
 La couleur est recherchée dans la zone de sélection de couleur ou dans le tableau des caractéristiques.
 Pour la description, le programme utilise la description classique si elle existe, sinon le contenu enrichi, puis les points clés si nécessaire.
   pourles images uniquement les photos du produit, en grande taille, et non toutes les images de la page.
 Le programme tente de télécharger jusqu'à trois images par produit.
 Chrome est lancé avec l'option detach, ce qui permet de le laisser ouvert après la fin du script.

Les informations récupérées dépendent du contenu des pages Amazon. Certains produits peuvent ne pas avoir toutes les informations disponibles.

 8. Problèmes courants

requirements.txt introuvable : vérifier que le terminal est ouvert dans le dossier du projet avec cd et dir.

No module named controllers : vérifier que le terminal est placé dans le dossier amazon_scraper_mvc, puis lancer le programme avec python -m controllers.main.

(venv) absent : activer l'environnement virtuel avec venv\Scripts\activate.

Erreur de pilote Chrome : vérifier que Chrome est installé et que la connexion internet fonctionne.

Le terminal semble bloqué : le programme peut être en train de charger une page. Attendre un peu ou utiliser Ctrl + C pour arrêter l'exécution.

Page CAPTCHA dans Chrome : l'extraction peut être bloquée. Réessayer plus tard si nécessaire.

0 liens produits trouvés : vérifier la page chargée dans Chrome. Amazon peut ne pas afficher les résultats attendus.

Caractères bizarres dans le terminal : cela peut être un problème d'affichage de PowerShell et ne signifie pas forcément que les fichiers de résultats sont incorrects.

Erreur DLL load failed lors de l'importation de pandas : vérifier que les bibliothèques sont installées dans l'environnement virtuel du projet. Si l'erreur persiste, réinstaller NumPy et Pandas avec les versions compatibles :

powershell
python -m pip install --force-reinstall numpy==2.2.6 pandas==2.3.3


