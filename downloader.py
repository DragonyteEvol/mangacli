from web_scrapy import *

print("Exribe la url del manga")
url = input("url: ")
print("Escribe un rango de capitulos")
from_chapter = input("Desde:")
to_chapter = input("Hasta: ")

scrapTumangaonline(str(url),generateCaps(int(from_chapter),int(to_chapter)))
