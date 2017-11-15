# -*- encoding: utf-8 -*-
import os
import sys
import re
import gensim.models as g
from PyPDF2 import PdfFileReader

os.mkdir("./text_docs")
for i in os.listdir("./papers"):
	# print(i)
	content = ""
	pdf = PdfFileReader("./papers/"+i)
	for j in range(0, pdf.getNumPages()):
		content += pdf.getPage(j).extractText() + "\n"
	# Collapse whitespace
	content = " ".join(content.replace(u"\xa0", " ").strip().split())
	content = str(content.encode("ascii", "ignore"))
	p = re.compile("references",re.IGNORECASE)
	for m in p.finditer(content):
		pos=m.start()
	content = content[:pos]
	content = str.encode(content)
	filename = "./text_docs/"+i
	filename = filename[:len(filename)-3]
	file = open(filename+"txt",'wb')
	file.write(content)
	file.close()

docs = []
for i in os.listdir("./text_docs"):
	docs += g.word2vec.LineSentence("./text_docs/"+i)
m = g.Word2Vec(docs, size=40, alpha=0.025, window=5, min_count=2, sample=1e-5, workers=4, min_alpha=0.0001, sg=1, hs=0, negative=5, iter=100)
m.save("single.bin")
