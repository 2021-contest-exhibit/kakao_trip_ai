from django.shortcuts import render
import requests
from django.http import HttpResponse
import numpy as np
from sentence_transformers import SentenceTransformer
from scipy import spatial
import requests
from modak_server import base
import json
from urllib import request, parse

base_list, intro_list = base.get_base_data()

with open('./campings.json', "r") as json_file:
    corpus_embeddings = json.load(json_file)["data"]

embedder = SentenceTransformer('distiluse-base-multilingual-cased')

print("ai 준비완료")

def index(request):
    closest_n = 5
    # base.create_base_data()

    corpus = intro_list
    # corpus_embeddings = embedder.encode(corpus)


    request_data = request.GET.get('data')
    query_embedding = embedder.encode([request_data])

    print([query_embedding[0]])

    distances = spatial.distance.cdist([query_embedding[0]], corpus_embeddings, "cosine")[0]
    results = zip(range(len(distances)), distances)
    results = sorted(results, key=lambda x: x[1])

    res = ''
    for idx, distance in results[0:closest_n]:
        res += str(corpus[idx].strip()) + str( f'Score : {(1 - distance):4f}' + '<p>')


    return HttpResponse(res)

def patch_campings_embedding(req):


    headers = {'Content-Type': 'application/json; chearset=utf-8'}

    for base in base_list:
        intro_embedding = embedder.encode([base.intro])
        res = requests.patch('http://localhost:8080/opendata/base', headers=headers, data=json.dumps({
            'contentId': base.contentId,
            'embedding': str(intro_embedding)
        }).encode('utf-8'))

    return HttpResponse("ok")


def all_camping_to_embedding_json(reqe):
    base_list, intro_list = base.get_base_data()

    embedder = SentenceTransformer('distiluse-base-multilingual-cased')

    corpus = intro_list
    corpus_embeddings = embedder.encode(corpus)

    # headers = {'Content-Type': 'application/json; chearset=utf-8'}
    # data = {'data': corpus_embeddings.tolist()}
    # req = request.Request('http://localhost:8080/ai/all', headers=headers, data=json.dumps(data).encode('utf-8'))
    # res = request.urlopen(req)

    file_path = './campings.json'
    data = {'data': corpus_embeddings.tolist()}

    with open(file_path, 'w') as outfile:
        json.dump(data, outfile)

    return HttpResponse("ok")