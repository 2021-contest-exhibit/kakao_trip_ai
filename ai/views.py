from django.shortcuts import render
import requests
from django.http import HttpResponse
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from scipy import spatial


embedder = SentenceTransformer('distiluse-base-multilingual-cased')

corpus = ['aaaa','bbbb','ccccc','ddddd','ttttt']
corpus_embeddings = embedder.encode(corpus)
closest_n = 5

def index(request):
    query_embedding = embedder.encode(['test5'])

    distances = spatial.distance.cdist([query_embedding[0]], corpus_embeddings, "cosine")[0]
    results = zip(range(len(distances)), distances)
    results = sorted(results, key=lambda x: x[1])

    res = ''
    for idx, distance in results[0:closest_n]:
        res += str(corpus[idx].strip()) + str( f'Score : {(1 - distance):4f}')


    return HttpResponse(res)