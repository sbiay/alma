import click
import spacy
import regex as re

from lxml import etree


def traitement(xml, requetexpath, nlp, saut=True):
	
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

	xml = traitement(xml, requetexpath=lem, nlp=nlp)
	xml = traitement(xml, requetexpath=selectPersNames, nlp=nlp, saut=False)

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

	contenu = re.sub("\n +\n", r"\n", contenu)
	# On indente les remarques
	# On supprime les sauts de ligne
	contenu = re.sub("\n\n", r"\n", contenu)

	nouvContenu = []
	contenu = contenu.split("\n")
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


	with open(sortie, mode="w") as f:
		f.write(contenu)

tokeniser()