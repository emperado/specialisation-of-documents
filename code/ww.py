# -*- encoding: utf-8 -*-
from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os, re
import sys, getopt

reload(sys)  
sys.setdefaultencoding('utf8')

#converts pdf, returns its text content as a string
def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)
    print(fname)
    #infile = file(fname, 'rb')
    with open(fname,'r') as infile:
    	for page in PDFPage.get_pages(infile, pagenums):
    	    interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text

# print(convert('./papers/Joint Naïve Bayes and LDA for Unsupervised Sentiment Analysis.pdf'))

os.mkdir("./text_docs1")
for i in os.listdir("./papers"):
    print(i)
    content = convert("./papers/"+i)
    # content = " ".join(content.replace(u"\xa0", " ").strip().split())
    content = str(content.encode("ascii", "ignore"))
    p = re.compile("references",re.IGNORECASE)
    for m in p.finditer(content):
        pos=m.start()
    content = content[:pos]
    content = str.encode(content)
    filename = "./text_docs1/"+i
    filename = filename[:len(filename)-3]
    file = open(filename+"txt",'wb')
    file.write(content)
    file.close()
