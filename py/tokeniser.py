import click
import csv
import spacy
import regex as re

from lxml import etree


def traitntXpath(xml, requetexpath, nlp, saut=True):
	"""
	Cette fonction tokénise des listes d'éléments collectées via une requête xpath
	"""
	# Pour les éléments dont le contenu est non mixte, comme lem
	for index, n in enumerate(requetexpath):
		if n.text:
			doc = nlp(n.text)
			ligne = [token.text for token in doc]
			chaine = ""
			# On boucle sur chaque token de la ligne
			for token in ligne:
				if saut:
					chaine = f"{chaine}\n<w>{token}</w>"
				else:
					chaine = f"{chaine}<w>{token}</w>"
			# On remplace le contenu de l'élément par la chaine tokénisée
			n.text = chaine
	
	return xml


@click.command()
@click.argument("FICHIER")
def tokeniser(fichier):
	
	xml = etree.parse(fichier)
	nsmap = {'tei': "http://www.tei-c.org/ns/1.0"}

	# On instancie la fonction de tokénisation en français
	nlp = spacy.load("fr_core_news_sm")
	
	# On collecte tous les éléments lem
	lem = xml.xpath("//tei:lem", namespaces=nsmap)
	
	# On collecte les persName qui ne sont pas dasn les rdg
	tousPersNames = xml.xpath("//tei:body//tei:p//tei:persName", namespaces=nsmap)
	selectPersNames = []
	# On boucle sur les persNames pour les trier
	for item in tousPersNames:
		# On récupère le parent du persName
		parent = item.getparent()
		balise = parent.tag[29:]
		# Si la balise n'est pas dans un rdg on l'ajoute à la sélection
		if balise != "rdg":
			selectPersNames.append(item)

	# TOKÉNISATION DES ÉLÉMENTS

	xml = traitntXpath(xml, requetexpath=lem, nlp=nlp)
	xml = traitntXpath(xml, requetexpath=selectPersNames, nlp=nlp, saut=False)

	sortie = fichier.replace(".xml", "-token.xml")
	# On écrit le fichier TEI de sortie
	xml.write(sortie, encoding="utf8", pretty_print=True)

	# On ouvre le fichier TEI au format txt
	with open(sortie) as f:
		contenu = f.read()

	# Transformation des balises écrites précédemment pour les éléments w
	contenu = re.sub("&lt;([\/]?)w&gt;", r"<\1w>", contenu)
	
	# CORRECTION DE L'INDENTATION DU FICHIER TEI
	
	indenter = ["p", "lem", "app", "choice", "corr"]
	
	# On indente les éléments en sautant une ligne avant et une après
	for elt in indenter:
		# On revient à la ligne avant l'élément ouvrant
		contenu = re.sub(f"([^\n])<{elt}>", fr"\1\n<{elt}>", contenu)
		# On revient à la ligne après l'élément ouvrant
		contenu = re.sub(f"<{elt}>([^\n])", fr"<{elt}>\n\1", contenu)
		# On revient à la ligne avant l'élément fermant
		contenu = re.sub(f"([^\n])</{elt}>", fr"\1\n</{elt}>", contenu)
		# On revient à la ligne après l'élément fermant
		contenu = re.sub(f"</{elt}>([^\n])", fr"</{elt}>\n\1", contenu)
	
	# Un persName tokénisé doit être suivi d'un saut de ligne
	# Cette intervention permet que l'indentation permette de prendre en compte le texte autour des persName dans les lem
	contenu = contenu.replace("<persName><w>", "\n<persName><w>")
	contenu = contenu.replace("</w></persName>", "</w></persName>\n")

	# On supprime les espaces en début de ligne
	contenu = re.sub("\n +\n", r"\n", contenu)
	# On indente les remarques
	# On supprime les sauts de ligne
	contenu = re.sub("\n\n", r"\n", contenu)

	
	# BOUCLE POUR L'INDENTATION DES REMARQUES

	contenu = contenu.split("\n")
	nouvContenu = []
	body = False
	p = False
	for ligne in contenu:
		# On détermine si l'on se trouve dans le body et dans les p
		if "<body>" in ligne:
			body = True
		elif "</body>" in ligne:
			body = False
		if "<p>" in ligne:
			p = True
		elif "</p>" in ligne:
			p = False
		# On ne travaille que dans les p du body
		if body and p:
			# Seules les lignes qui ne commencent pas par une balise sont à tokéniser
			if re.search("^ *[^ \<]", ligne):
				ligne = ligne.replace("<!--", "\n<!--")
				ligne = ligne.replace("-->", "-->\n")
				ligne = ligne.split("\n")
				for item in ligne:
					nouvContenu.append(item)
			# Et si une ligne commence par une remarque
			elif "<!--" == ligne[:4]:
				# On indente la suite de la ligne
				ligne = ligne.replace("-->", "-->\n")
				ligne = ligne.split("\n")
				for item in ligne:
					nouvContenu.append(item)
			else:
				nouvContenu.append(ligne)
		else:
			nouvContenu.append(ligne)

	
	# BOUCLE POUR LA TOKÉNISATION

	contenu = nouvContenu
	nouvContenu = []
	body = False
	p = False
	for ligne in contenu:
		# On détermine si l'on se trouve dans le body et dans les p
		if "<body>" in ligne:
			body = True
		elif "</body>" in ligne:
			body = False
		if "<p>" in ligne:
			p = True
		elif "</p>" in ligne:
			p = False
		# On ne travaille que dans les p du body
		if body and p:
			# Seules les lignes qui ne commencent pas par une balise sont à tokéniser
			if re.search("^ *[^ \<]", ligne):
				if not "<" in ligne:
					doc = nlp(ligne)
					ligne = [token.text for token in doc]
					chaine = ""
					# On boucle sur chaque token de la ligne
					for token in ligne:
						if token and token != " ":
							chaine = f"{chaine}\n<w>{token}</w>"	
					# On supprime le premier saut de ligne, inutile
					if chaine[0] == "\n":
						chaine = chaine[1:]
					ligne = chaine
				else:
					print("Non traité : " + ligne)
		nouvContenu.append(ligne)
	contenu = "\n".join(nouvContenu)

	# On écrit le fichier xml de sortie
	with open(sortie, mode="w") as f:
		f.write(contenu)


	# EXPORT DES MOTS

	# On instancie l'arbre xml à partir du fichier tokénisé
	xml = etree.parse(sortie)

	# On collecte tous les éléments w
	words = xml.xpath("//tei:w", namespaces=nsmap)

	mots = []
	txt = ""
	# On boucle sur chaque élément
	for w in words:
		mots.append(w.text)
		txt = txt + w.text + " "

	"""On exporte la liste dans un csv si l'on veut contrôler facilement le nombre de lignes
	destinationCSV = sortie.replace("tei/", "csv/").replace("-token.xml", ".csv")
	with open(destinationCSV, mode="w") as csvf:
		ecriveur = csv.writer(csvf, delimiter="\t", quotechar="|")
		ecriveur.writerow(["form"])
		for item in mots:
			ecriveur.writerow([item])
		print(f"Le fichier {destinationCSV} a été écrit correctement.")
	"""

	# Transformations du texte pour alignement avec pyrrha
	txt = txt.replace("’", "")
	txt = txt.replace("'", "")

	# On exporte le texte dans un fichier txt
	destinationTxt = sortie.replace("tei/", "txt/").replace("-token.xml", ".txt")
	with open(destinationTxt, mode="w") as txtf:
		txtf.write(txt)
		print(f"Le fichier {destinationTxt} a été écrit correctement.")

tokeniser()