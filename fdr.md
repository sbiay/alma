---
title: Alma
subtitle: Feulle de route
---

# Tokéniser les textes

1. On applique les balises `w` sur tous les éléments tokénisés

	- Impossible à gérer par py pour les chaînes des éléments `p` en raison de leur contenu mixte
	- xslt… aurait été compliqué
	
	- **Manipulation du code**
		- Traiter la question des balises internes aux `p` (et qui peuvent intervenir potentiellement dans les `lem`)
		- Placer les remarques <!----> après un retour à la ligne

2. On récolte tous les éléments `w` du document

3. On les écrit dans un fichier