from django.forms import ModelForm, Textarea
from .models import Data,Query
import os
from .globals import *
# from django.core.files.storage import default_storage
from nltk import tokenize
corpus_embeddings = dict()
class DataForm(ModelForm):
	class Meta:
		model = Data
		fields = ('body', 'document')
	def clean(self):
		cd = self.cleaned_data
		body = (cd.get("body"))
		return cd
	def parse_and_store(self, request):
		body = self.cleaned_data.get("body")
		text = ""

		if len(body) != 0:
			text = body
		else:
			text = request.FILES['document'].read().decode("utf-8") 
		if (len(text) > 0):
			# get sentences, parse the sentences, add too corpuse_embeddings
			print(f"text is {text}")
			sentences = tokenize.sent_tokenize(text)


		from sentence_transformers import SentenceTransformer
		model = SentenceTransformer('all-MiniLM-L6-v2')


		#Sentences are encoded by calling model.encode()
		embeddings = model.encode(sentences)

		#Print the embeddings
		for sentence, embedding in zip(sentences, embeddings):
			# print("Sentence:", sentence)
			# print("Embedding:", embedding)
			# print("")
			print(sentence,embedding)
			corpus_embeddings[sentence] = embedding
		print(f"Text received: {text}")
		
class QueryForm(ModelForm):
	class Meta:
		model = Query
		fields = ('query',)
	def generate_results(self):
		print("generating.....")
		print(corpus_embeddings.keys())
		print("\n\n\n")



		from sentence_transformers import SentenceTransformer, util
		import torch

		embedder = SentenceTransformer('all-MiniLM-L6-v2')
		corpus = list(corpus_embeddings.keys())
		c_e = embedder.encode(list(corpus), convert_to_tensor=True)
		
		query = self.cleaned_data.get("query")

		# Find the closest 2 sentences of the corpus for each query sentence based on cosine similarity
		top_k = min(2, len(corpus))
		print("QUERY", query)
		query_embedding = embedder.encode(query, convert_to_tensor=True)

		# We use cosine-similarity and torch.topk to find the highest 5 scores
		cos_scores = util.cos_sim(query_embedding, c_e)[0]
		top_results = torch.topk(cos_scores, k=top_k)

		print("\n\n======================\n\n")
		print("Query:", query)
		print("\nTop 2 most similar sentences in corpus:")
		print(top_results)
		
		for score, idx in zip(top_results[0], top_results[1]):
			print(corpus[idx], "(Score: {:.4f})".format(score))
		print("\n\n\n")
		print(corpus)

							
					

