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
from django.http import JsonResponse

base_list, intro_list = base.get_base_data()
closest_n = 5
with open('./campings.json', "r") as json_file:
    corpus_embeddings = json.load(json_file)["data"]

with open('./camping.json', "r") as json_file:
    camping_embedding_dict = json.load(json_file)


print("ai 준비완료")

def index(request):
    embedder = SentenceTransformer('distiluse-base-multilingual-cased')
    # base.create_base_data()

    corpus = intro_list
    # corpus_embeddings = embedder.encode(corpus)


    request_data = request.GET.get('data')
    query_embedding = embedder.encode([request_data])

    print(len(query_embedding[0]), query_embedding[0].shape)

    print(query_embedding[0])

    distances = spatial.distance.cdist([query_embedding[0]], corpus_embeddings, "cosine")[0]
    results = zip(range(len(distances)), distances)
    results = sorted(results, key=lambda x: x[1])

    res = ''
    for idx, distance in results[0:closest_n]:
        res += str(corpus[idx].strip()) + str( f'Score : {(1 - distance):4f}' + '<p>')


    return HttpResponse(res)

def recommend(req):
    if req.method == "POST":
        contentId_list = json.loads(req.body)["contentIdList"]
        contentId_list.sort()
        print(contentId_list)
        base_embedding = [camping_embedding_dict[str(contentId)] for contentId in contentId_list ]
        distances = spatial.distance.cdist(base_embedding,corpus_embeddings, "cosine")[0]
        results = zip(range(len(distances)), distances)
        results = sorted(results, key=lambda x: x[1])



        res = []
        for idx, distance in results:
            # res += str(intro_list[idx].strip()) + str(f'Score : {(1 - distance):4f}' + '<p>')
            if len(res) >= closest_n:
                break

            if base_list[idx].contentId not in contentId_list:
                res.append(base_list[idx].contentId)

        data = { 'data' : res}

        return JsonResponse(data)

def patch_campings_embedding(req):
    embedder = SentenceTransformer('distiluse-base-multilingual-cased')
    file_path = './camping.json'
    data = {}

    for base in base_list:
        intro_embeddings = embedder.encode([base.intro])
        data[str(base.contentId)] = intro_embeddings[0].tolist()


    with open(file_path, 'w') as outfile:
        json.dump(data, outfile)


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