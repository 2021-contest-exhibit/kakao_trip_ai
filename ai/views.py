from django.shortcuts import render
import requests
from django.http import HttpResponse
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from scipy import spatial
import requests
from modak_server import base

#base.create_base_data()
base_list, intro_list = base.get_base_data()

embedder = SentenceTransformer('distiluse-base-multilingual-cased')

corpus = intro_list
corpus_embeddings = embedder.encode(corpus)
closest_n = 5

print('AI 준비완료')

def index(request):
    request_data = request.GET.get('data')
    query_embedding = embedder.encode([request_data])

    distances = spatial.distance.cdist([query_embedding[0]], corpus_embeddings, "cosine")[0]
    results = zip(range(len(distances)), distances)
    results = sorted(results, key=lambda x: x[1])

    res = ''
    for idx, distance in results[0:closest_n]:
        res += str(corpus[idx].strip()) + str( f'Score : {(1 - distance):4f}' + '<p>')


    return HttpResponse(res)