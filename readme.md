Alma
====

Plan :
1. [Lemmatisation et enrichissement morpho-syntaxique 👍](#t1)
	1. [Tokénisation des éditions TEI ](#t1-1)
	2. [Export des tokens ](#t1-2)
	3. [Lemmatisation à l'aide de Pyrrha ](#t1-3)
	4. [Enrichissement de l'édition TEI à l'aide des données de Pyrrha ](#t1-4)

[comment]: <> (FINET)


Ce dépôt est dédié à l'ingénierie des données et des textes du projet **Alma**, *Wissensnetze in der mittelalterlichen Romania = Knowledge Networks in Medieval Romance Speaking Europe* (Heidelberger Akademie der Wissenschaften, Bayerischen Akademie der Wissenschaften, Akademie der Wissenschaften und der Literatur Mainz).


<a id='t1'/>

# Lemmatisation et enrichissement morpho-syntaxique 👍

Mode d'emploi :

```shell
python3 py/tokeniser.py TEI.xml
```


<a id='t1-1'/>

## Tokénisation des éditions TEI 

On applique les balises `w` sur tous les éléments à tokéniser (y compris la ponctuation de façon provisoire).

Comme on n'a pas réussi à gérer avec **lxml** les éléments `p` en raison de leur contenu mixte, et que l'on souhaite éviter de recourir à **XSLT** en raison de la difficulté de prise en main, on manipule le code par script python, avec lxml pour les éléments ne contenant que du texte et en mode texte pour les éléments mixtes, et ce après rectification de l'indentation.

Exemple de résultat [ici](./tei/TrotulaPr1M_edition-token.xml).

**Questions** :

- Est-il vraiment pertinent de tokéniser les `persName` ? Ils peuvent être composés (ce qui appelle plusieurs `w`)…


<a id='t1-2'/>

## Export des tokens 

On les écrit dans un fichier txt, seul format accepté par Pyrrha.


<a id='t1-3'/>

## Lemmatisation à l'aide de Pyrrha 

La seule différence de comportement observée entre la tokénisation que l'on a appliquée au fichier TEI avec **tokenise.py** et le lemmatiseur Pyrrha est le traitement des apostrophes, que Pyrrha détache du mot et traite à part. Il a suffi de supprimer les apostrophes de l'export `txt` pour obtenir le même nombre de tokens.


<a id='t1-4'/>

## Enrichissement de l'édition TEI à l'aide des données de Pyrrha 

Résultat dans le fichier [./tei/TrotulaPr1M_edition-enrichi.xml](./tei/TrotulaPr1M_edition-enrichi.xml)