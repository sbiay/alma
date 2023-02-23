---
title: Alma
subtitle: Feulle de route
---

# Tokéniser les textes

1. On applique les balises `w` sur tous les éléments tokénisés

	- Impossible à gérer par py pour les chaînes des éléments `p` en raison de leur contenu mixte
	
	- On réindente
		- Les `p` pour pouvoir parser seulement dedans
		- Les `app` ont toujours un saut de ligne avant et un saut de ligne après
		- Les `lem` fermant on un saut de ligne après

	- xslt…

2. On récolte tous les éléments `w` du document

3. On les écrit dans un fichier