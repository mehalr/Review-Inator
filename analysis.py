import requests
import json
import os
from expertai.nlapi.cloud.client import ExpertAiClient
from decouple import config
from secrets import secrets

os.environ["EAI_USERNAME"] = config('USERNAME')
os.environ["EAI_PASSWORD"] = config('PASSWORD')

client = ExpertAiClient()

# success code - 200
language = 'en'


def getReviews(url):
    headers = {
        "apikey": config('API_KEY')
    }

    params = (
        ("url", url),
        ("amount", "25"),
    )

    response = requests.get('https://app.reviewapi.io/api/v1/reviews', headers=headers, params=params)
    obj = json.loads(response.text)

    all_reviews = ""
    for review in obj['reviews']:
        if review['text']:
            all_reviews += review['text']

    return(all_reviews)

def sentiments(all_reviews):

    output3 = client.specific_resource_analysis(body={"document": {"text": all_reviews}},
                                                params={'language': 'en', 'resource': 'sentiment'})

    # print("Output overall sentiment:")
    # print(output3.sentiment.positivity)
    # print(output3.sentiment.negativity)
    # print(output3.sentiment.overall)
    return(output3.sentiment.positivity,abs(output3.sentiment.negativity))

def words_sentences(all_reviews):
    output = client.specific_resource_analysis(body={"document": {"text": all_reviews}},
                                               params={'language': language, 'resource': 'relevants'})
    words = []
    sentences = []
    for lemma in output.main_lemmas:
        words.append(lemma.value)

    for sent in output.main_sentences:
        sentences.append(sent.value)
    return(words,sentences)

def emotional_traits(all_reviews):
    output2 = client.classification(body={"document": {"text": all_reviews}},
                                    params={'taxonomy': 'emotional-traits', 'language': 'en'})
    emotion = []
    score = []
    if output2:
        for category in output2.categories:
            emotion.append(category.label)
            score.append(category.score)
            print(category.id_, category.label, category.hierarchy, category.score, sep="\t")
    return(emotion, score)


if __name__=='__main__':
    all_reviews = getReviews("https://www.amazon.in/New-Apple-iPhone-XR-64GB/dp/B08L8BK9V6")
    print(all_reviews)
    p, n= sentiments(all_reviews)
    print(p,n)
    w ,s = words_sentences(all_reviews)
    print(w,s)
    e , sc = emotional_traits(all_reviews)
    print(e, sc)


# response = requests.get('https://app.reviewapi.io/api/v1/reviews', headers=headers, params=params);
# obj = json.loads(response.text)
# print(obj)
#
# all_reviews = ""
# for review in obj['reviews']:
#     if review['text']:
#         all_reviews += review['text']
#
# print(all_reviews)
#
# output = client.specific_resource_analysis(body={"document": {"text": all_reviews}}, params={'language': language, 'resource': 'relevants'})
#
#
# # Main lemmas
#
# print("Main lemmas:")
#
# for lemma in output.main_lemmas:
#     print(lemma.value)
#
# for lemma in output.main_sentences:
#     print(lemma.value)
# # print(obj['login'])
#
# output2 = client.classification(body={"document": {"text": all_reviews}}, params={'taxonomy': 'emotional-traits', 'language': 'en'})
#
# if output2:
#     for category in output2.categories:
#
#            print(category.id_, category.label, category.hierarchy, category.score,sep="\t")
#
# output3 = client.specific_resource_analysis(body={"document": {"text": all_reviews}}, params={'language': 'en', 'resource': 'sentiment'})
#
# print("Output overall sentiment:")
#
# print(output3.sentiment.positivity)
# print(output3.sentiment.negativity)
# print(output3.sentiment.overall)