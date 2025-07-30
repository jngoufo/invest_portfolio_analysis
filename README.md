<h1>Analyse de Portefeuille Boursier avec Python et SQL</h1>
Ce projet est un pipeline de données ETL (Extract, Transform, Load) entièrement automatisé, conçu pour extraire, nettoyer, et charger des données de portefeuille boursier dans une base de données MySQL en vue d'analyses SQL avancées.

<h2>🎯 Objectif du Projet</h2>
En tant que professionnel de l'Assurance Qualité Logicielle, j'ai développé ce projet personnel pour :
<ul>
<li><b>Mettre en pratique et valider des compétences SQL</b> en manipulation de données, en automatisation de processus et en gestion de bases de données.</li>
<li><b>Illustrer une approche de travail moderne en utilisant l'IA</b> comme un partenaire de développement pour accélérer la recherche de solutions et la génération de code.</li>
<li><b>Démontrer ma capacité à mener un projet technique de A à Z</b>, de la définition du besoin à la résolution de problèmes complexes.</li>
</ul>
<h2>✨ Fonctionnalités Clés</h2>
<ul>
<li><b>Automatisation du Nettoyage :</b> Un script Python, développé en collaboration avec une IA, nettoie et standardise un fichier CSV brut (gestion des devises multiples, symboles, types de données, etc.).</li>
<li><b>Pipeline ETL Robuste :</b> Le script gère l'extraction (depuis un CSV), la transformation (avec Pandas) et le chargement (avec SQLAlchemy) dans MySQL.</li>
<li><b>Gestion de Données Temporelles :</b> Mise en place d'un système de 12 tables tournantes pour conserver un historique glissant des données sur 3 mois.</li>
<li><b>Sécurité et Configuration :</b> Les informations sensibles (mots de passe) sont externalisées dans un fichier config.ini sécurisé et ignoré par Git.</li>
<li><b>Journalisation (Logging) :</b> Chaque exécution génère un fichier de log horodaté pour un suivi et un débogage faciles.</li>
</ul>
<h2>🛠️ Technologies Utilisées</h2>
<ul>
<li><b>Langage :</b> Python</li>
<li><b>Librairies :</b> Pandas, SQLAlchemy</li>
<li><b>Base de Données :</b> MySQL</li>
<li><b>Gestion de Version :</b> Git & GitHub</li>
<li><b>Environnement :</b> Windows, Git Bash</li>
</ul>
<h2>🚀 Installation et Utilisation</h2>
<ol>
<li><b>Clonez le dépôt :</b></li>
<code>Bash</code>
<code>git clone https://github.com/jngoufo/invest_portfolio_analysis.git</code>
<li><b>Base de Données :</b></li>
<ul>
<li>Assurez-vous d'avoir un serveur MySQL fonctionnel.</li>
<li>Exécutez le script <code>schema.sql</code> pour créer la table de référence <code>portfolio_template.</code></li>
</ul>
<li><b>Configuration :</b></li>
<ul>
<li>Créez un fichier <code>config.ini</code> à la racine du projet et remplissez-le avec vos informations de connexion.</li>
</ul>
<li><b>Données Sources :</b></li>
<ul>
<li>Créez un dossier <code>source/</code>.</li>
<li>Placez votre fichier d'export <code>tipranks_raw.csv</code> à l'intérieur.</li>
</ul>
<li><b>Exécution :</b></li>
<ul>
<li>Lancez le script <code>run_weekly_import.bat</code> pour démarrer le pipeline.</li>
</ul>
</ol>
<h2>🧠 Défis et Apprentissages</h2>
Ce projet a été une excellente opportunité de monter en compétences à travers la <b>résolution de défis concrets</b> :
<ul>
<li><b>Débogage SQL et Permissions :</b> Le contournement des restrictions de <code>LOAD DATA INFILE</code> de MySQL m'a conduit à adopter une méthode de chargement plus moderne et robuste avec SQLAlchemy.</li>
<li><b>Nettoyage de Données Complexes :</b> La gestion de données hétérogènes ("sales data") comme les noms de colonnes dupliqués, les formats mixtes et les lignes vides a été un excellent exercice pratique.</li>
<li><b>Conception de Schéma :</b> La réflexion sur les types de données et l'implémentation de conventions de nommage claires (<code>_pct</code>, <code>_cad</code>) pour rendre la base de données auto-documentée ont été des étapes clés.</li>
</ul>
<h2>🔮 Prochaines Étapes</h2>
Ce projet est évolutif. Les prochaines étapes se concentreront sur l'exploitation des données :
<ul>
<li>Développement d'un ensemble de requêtes SQL pour extraire des indicateurs de performance clés (KPIs).</li>
<li>Création d'un tableau de bord simple pour visualiser les analyses.</li>
</ul>






