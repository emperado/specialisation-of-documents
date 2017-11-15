from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
import gensim.models as g
import os, sys
import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.cluster.kmeans import KMeansClusterer
from sklearn.cluster import KMeans
from nltk.corpus import stopwords
from scipy.spatial.distance import *

#stemming, symbol

stemmer = nltk.stem.porter.PorterStemmer()
lemma = nltk.wordnet.WordNetLemmatizer()

propernouns={}
corpus_directory='./text_docs1/'
for infile in os.listdir(corpus_directory):
	with open(corpus_directory+infile, 'r') as fin:
		tagged_sent = pos_tag(word_tokenize(fin.read()))
#		propernouns[infile] = [stemmer.stem(word).lower() for word,pos in tagged_sent if pos == 'NNP']
		propernouns[infile] = [lemma.lemmatize(word).lower() for word,pos in tagged_sent if pos == 'NNP']
		propernouns[infile] = set(propernouns[infile])
		propernouns[infile] = list(propernouns[infile])
#		print(propernouns)

for i in os.listdir("./text_docs1"):
	for word in propernouns[i]:
		if (word in stopwords.words('english')) or len(word)==1:
			del propernouns[i][propernouns[i].index(word)]
doc=[]
for i in os.listdir("./text_docs1"):
	f = open("./text_docs1/"+i,'r', encoding="UTF-8")
	doc.append(f.read())
tfidf_vectorizer = TfidfVectorizer()
tfidf = tfidf_vectorizer.fit_transform(doc)
vocab = tfidf_vectorizer.vocabulary_

m = g.Word2Vec.load('./single.bin')

docvec={}
k=0
for i in os.listdir("./text_docs1"):	
	docvec[i] = np.zeros(40)
	for word in propernouns[i]:
		if word in m and word in vocab:
			#print(word)
			docvec[i] += m[word]*tfidf[k,vocab[word]]
	k=k+1

#kmeans = KMeans(n_clusters=7, random_state=0).fit(list(docvec.values()))
kclusterer = KMeansClusterer(7, distance=nltk.cluster.util.cosine_distance, repeats=100)
assigned_clusters = kclusterer.cluster(list(docvec.values()), assign_clusters=True)
labels1={}
l=0
p=list(docvec.keys())
for i in p:
	labels1[i]=assigned_clusters[l]
	l+=1

#print(propernouns)
#print
#print(labels1)
for i in range(0,7):
	print ("Cluster-"+str(i))
	lis=[]
	for x in labels1:
		if labels1[x]==i:
			lis.append(docvec[x])
	for x in labels1:
		if labels1[x]==i:
			print (x,end=", ")
			for j in range(0,len(lis)):
				print ((1-cosine(docvec[x],lis[j])),end=",")
			print()
	print()
