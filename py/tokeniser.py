import click
import spacy
import regex as re

from lxml import etree

@click.command()
@click.argument("FICHIER")
def tokeniser(fichier):
	
	xml = etree.parse(fichier)
	nsmap = {'tei': "http://www.tei-c.org/ns/1.0"}

	# On cherche les mots à tokéniser dans les éléments :
	# - lem
	# - rdg : pas sûr
	lem = xml.xpath("//tei:lem", namespaces=nsmap)
	ps = xml.xpath("//tei:text//tei:body//tei:p/text()", namespaces=nsmap)
	ps2 = xml.xpath("//tei:text//tei:body//tei:p", namespaces=nsmap)
	nlp = spacy.load("fr_core_news_sm")
	
	# Pour le contenu des éléments p, ils forment une seule liste que l'on reforme en chaine
	if ps:
		# On boucle sur chaque partie des éléments p
		for index, p in enumerate(ps):
			#print(p)
			doc = nlp(str(p))
			ligne = [token.text for token in doc]
			chaine = ""
			# On boucle sur chaque token de la ligne
			for token in ligne:
				if token != " " and token:
					chaine = f"{chaine}<w>{token}</w>"
			#print(p)
			#print(chaine)
			ps[index] =  chaine
		#	if index == 0:
		#		print(ligne)
		#		chaine = ""
				# On boucle sur chaque token de la ligne
				#for token in ligne:
				#	chaine = f"{chaine}<w>{token}</w>"
				# On remplace le contenu de l'élément par la chaine tokénisée
				#n.text = chaine

	"""
	for index, n in enumerate(lem):
		if n.text:
			doc = nlp(n.text)
			ligne = [token.text for token in doc]
			if index == 32:
				chaine = ""
				# On boucle sur chaque token de la ligne
				for token in ligne:
					chaine = f"{chaine}<w>{token}</w>"
				# On remplace le contenu de l'élément par la chaine tokénisée
				n.text = chaine
	"""

	sortie = fichier.replace(".xml", "-token.xml")
	# On écrit le fichier TEI de sortie
	xml.write(sortie, encoding="utf8")

	# On ouvre le fichier TEI au format txt
	with open(sortie) as f:
		contenu = f.read()

	contenu = re.sub("&lt;([\/]?)w&gt;", r"<\1w>", contenu)

	with open(sortie, mode="w") as f:
		f.write(contenu)

tokeniser()