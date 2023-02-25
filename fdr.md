---
title: Alma
subtitle: Feulle de route
---

# Tokéniser les textes

1. On applique les balises `w` sur tous les éléments tokénisés (y compris la ponctuation de façon provisoire)

	- Impossible à gérer par py pour les chaînes des éléments `p` en raison de leur contenu mixte
	- xslt… aurait été compliqué
	
	- **Manipulation du code**
		- Traiter la question des balises internes aux `p` (et qui peuvent intervenir potentiellement dans les `lem`)
		- Placer les remarques <!----> après un retour à la ligne
		- Autres éléments à tokéniser
			- <p>Mais pour ce ke les femes sunt 
			- <choice><sic>et</sic><corr/></choice> et à mouteplier 
			- et ount <!-- VM : à voir s'il ne vaut mieux utiliser une typologie de valeurs plus fines pour les fautes de copie, cf. Roncaglia--> greignor travail 
			- <persName>Ypocras</persName> à traiter ainsi : <w><persName>Ypocras</persName></w>
			- .</p>

2. On récolte tous les éléments `w` du document

3. On les écrit dans un fichier csv

4. On les écrit dans un fichier txt