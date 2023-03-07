Alma
====

Plan :
1. [Lemmatisation et enrichissement morpho-syntaxique](#t1)
	1. [Tokénisation des éditions TEI ](#t1-1)
	2. [Export des mots et de la ponctuation](#t1-2)

[comment]: <> (FINET)


Ce dépôt est dédié à l'ingénierie des données et des textes du projet **Alma**, *Wissensnetze in der mittelalterlichen Romania = Knowledge Networks in Medieval Romance Speaking Europe* (Heidelberger Akademie der Wissenschaften, Bayerischen Akademie der Wissenschaften, Akademie der Wissenschaften und der Literatur Mainz).


<a id='t1'/>

# Lemmatisation et enrichissement morpho-syntaxique

Mode d'emploi :

```shell
python3 py/tokeniser.py TEI.xml
```


<a id='t1-1'/>

## Tokénisation des éditions TEI 👍

On applique les balises `w` sur tous les éléments à tokéniser (y compris la ponctuation de façon provisoire).

Comme on n'a pas réussi à gérer avec **lxml** les éléments `p` en raison de leur contenu mixte, et que l'on souhaite éviter de recourir à **XSLT** en raison de la difficulté de prise en main, on manipule le code par script python, avec lxml pour les éléments ne contenant que du texte et en mode texte pour les éléments mixtes, et ce après rectification de l'indentation.

Exemple de résultat [ici](./tei/TrotulaPr1M_edition-token.xml).

**Questions** :

- Est-il vraiment pertinent de tokéniser les `persName` ? Ils peuvent être composés de toponymes…


<a id='t1-2'/>

## Export des mots et de la ponctuation

1. On les écrit dans un fichier csv

2. On les écrit dans un fichier txt