import click
import csv
from lxml import etree

@click.command()
@click.argument("TEI")
@click.argument("PYRRHA")
def enrichitTEI(tei, pyrrha):

	# On récupère le contenu du fichier TSV Pyrrha
	donnees = []
	with open(pyrrha) as csvf:
		lecteur = csv.reader(csvf, delimiter="\t", quotechar="|")
		etiquettes = []
		for index, ligne in enumerate(lecteur):
			if index == 0:
				etiquettes = ligne
			else:
				enregistrement = {}
				for index, etiquette in enumerate(etiquettes):
					enregistrement[etiquette] = ligne[index]
				donnees.append(enregistrement)

	# On instancie l'arbre du fichier TEI
	xml = etree.parse(tei)
	nsmap = {'tei': "http://www.tei-c.org/ns/1.0"}

	# On collecte tous les éléments w
	words = xml.xpath("//tei:w", namespaces=nsmap)
	# On vérifie le nombre de tokens
	if len(words) != len(donnees):
		return print("Le nombre de lignes de tableau diffère du nombre d'élément w dans le fichier tei")

	# ENRICHISSEMENT DES ÉLÉMENTS W DU FICHIER TEI
	for index, w in enumerate(words):
		for etiquette in etiquettes:
			w.attrib[etiquette] = donnees[index][etiquette]

	# On écrit le fichier TEI de sortie
	sortie = tei.replace("-token.xml", "-enrichi.xml")
	xml.write(sortie, encoding="utf8", pretty_print=True)

enrichitTEI()