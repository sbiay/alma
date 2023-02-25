title: Alma
====

Plan :

1. [Lemmatisation et enrichissement morpho-syntaxique](#t1)
	1. [Tokénisation des éditions TEI ⌛](#t1-1)
	2. [Export des mots et de la ponctuation](#t1-2)

[comment]: <> (FINET)


Ce dépôt est dédié à l'ingénierie des données et des textes du projet **Alma**, *Wissensnetze in der mittelalterlichen Romania = Knowledge Networks in Medieval Romance Speaking Europe* (Heidelberger Akademie der Wissenschaften, Bayerischen Akademie der Wissenschaften, Akademie der Wissenschaften und der Literatur Mainz).


<a id='t1'/>

# Lemmatisation et enrichissement morpho-syntaxique


<a id='t1-1'/>

## Tokénisation des éditions TEI ⌛

On applique les balises `w` sur tous les éléments à tokéniser (y compris la ponctuation de façon provisoire).

Comme il est impossible de gérer par py pour les chaînes des éléments `p` en raison de leur contenu mixte, et que l'on souhaite éviter de recourir à XSLT en raison de la difficulté de prise en main. On manipule le code par script python.

Eléments par encore traités par le script :

```xml
<p>Mais pour ce ke les femes sunt 
<choice><sic>et</sic><corr/></choice> et à mouteplier 
et ount <!-- VM : à voir s'il ne vaut mieux utiliser une typologie de valeurs plus fines pour les fautes de copie, cf. Roncaglia--> greignor travail 
<persName>Ypocras</persName> à traiter ainsi : <w><persName>Ypocras</persName></w>
.</p>
```


<a id='t1-2'/>

## Export des mots et de la ponctuation

1. On les écrit dans un fichier csv

2. On les écrit dans un fichier txt