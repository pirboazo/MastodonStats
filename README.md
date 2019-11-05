# MastodonStats

----

**Avertissement Important**: Ce script est prévu pour un usage personnel,
Les résultats du scripts sont des statistiques sur vos pouets, même s'il contient principalement vos informations personnelles, il peut donner des informations sur vos conversations avec d'autres personnes,ce qui peut leur poser problème.
Le script ne permets pas sans modification de publier des informations privées

Si vous voulez publier ces données, considérez d'abord l'impact potentiel et demandez leur accord.

----
# Installation 

## Pre-requis

### Logiciel - packages

1.pyhton  : 3.5

2.Télécharger le script (git clone git@framagit.org:pirboazo/MastodonStats.git)

3.Installer les packages :
 - docopt ( pip install docopt )
 - schema ( pip install schema )


### Données
Une extraction de votre archive à télécharger depuis votre compte
`https://domainedevotreinstance.tld/settings/export`

## Utilisation

* ouvrez un terminal dans le dossier contenant le script (executable)

usage :
>mastodonStats.py  PATH FILE... [--hashtag=N]  [--mention=N]

> *Arguments*:

>    FILE     input file

>    PATH     out directory


> Options:

>   --hashtag=N   Valeur du filtre nombre de citation entre 1 & 10

>   --mention=N Filtre mention % de citation entre 1 & 10

>   -v --version

>   -h --help


* * *

## Exemple 

### Statistiques globales uniquement

> ~/src/masto3/MastodonStats-master$ python mastodonStats.py   ./ ./archive/pirboazo/archive-20180810152630-024fb72a5631f5e60f0b8086cb934ffc/outbox.json 

>Statistiques sur une archive de @pirboazo@mastodon.social
 
> Nombre de messages 

> total : 1278 (100%) 

>  publics : 395 (30.9%);

>  non listés : 256 (20.0%); 

>  privés : 318 (24.9%); 

>  directs : 44 (3.4%); 

> repouets : 260 (20.3%) ; 

>  MentionFail : 5 (0.4%)
 
> Hashtag utilisés : 45
  
>  Pseudos mentionnés : 837


### Statistiques globales plus hastag

> ~/src/masto3/MastodonStats-master$ python mastodonStats.py   ./ ./archive/pirboazo/archive-20180810152630-024fb72a5631f5e60f0b8086cb934ffc/outbox.json --hashtag=5

> Statistiques sur une archive de @pirboazo@mastodon.social

> Nombre de messages 

> total : 1278 (100%) 
 
> publics : 395 (30.9%); 

> non listés : 256 (20.0%); 

> privés : 318 (24.9%); 

> directs : 44 (3.4%); 

> repouets : 260 (20.3%) ; 

> MentionFail : 5 (0.4%) 

>Hashtag utilisés : 45

> Hashtag utilisés (par quantité décroissante):

> nxt : 11 (24.4%)

> vendredilecture : 10 (22.2%)

> cryptocoin : 7 (15.6%)


> Pseudos mentionnés : 837

### Statistiques globales plus mentions

>~/src/masto3/MastodonStats-master$ python mastodonStats.py   ./ ./archive/pirboazo/archive-20180810152630-024fb72a5631f5e60f0b8086cb934ffc/outbox.json --mention=4

> Statistiques sur une archive de @pirboazo@mastodon.social

> Nombre de messages 

> total : 1278 (100%) 

> publics : 395 (30.9%); 

> non listés : 256 (20.0%); 

> privés : 318 (24.9%); 

> directs : 44 (3.4%); 

> repouets : 260 (20.3%) ; 

> MentionFail : 5 (0.4%) 

>Hashtag utilisés : 45

>Pseudos mentionnés : 837

>Pseudos mentionnés (par quantité décroissante):

>@SXXXXXX@mamot.fr : 64 (7.6%)

>@NNNNNNN@mamot.fr : 38 (4.5%)

>@YYYYYYY@mastodon.xyz : 35 (4.2%)

