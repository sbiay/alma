import click
import spacy

from lxml import etree

@click.command()
@click.argument("FICHIER")
def tokeniser(fichier):
	
	xml = etree.parse(fichier)
	nsmap = {'tei': "http://www.tei-c.org/ns/1.0"}

	# On cherche les mots à tokéniser dans les éléments :
	# - lem
	# - rdg : pas sûr
	elt = xml.xpath("//tei:lem", namespaces=nsmap)

	nlp = spacy.load("fr_core_news_sm")
	
	for index, n in enumerate(elt):
		if n.text:
			doc = nlp(n.text)
			ligne = [token.text for token in doc]
			if index == 32:
				print(ligne)

tokeniser()