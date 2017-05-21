#encoding=utf-8
from __future__ import unicode_literals
import sys
sys.path.append("../")
from firebase import firebase
import sentences
import random
import re
import string
import seg

firebase = firebase.FirebaseApplication('https://live-2-0-131ee.firebaseio.com', None)
chats = None
chats_key = None
said_keyword = ['泳裝','男人','小本子','消夜']
random.shuffle(sentences.sentences)
sentences_idx = 0

def getUser(keyword):
    name = ''
    for j in chats_key:
        if chats[j]['text'].find(keyword) < 0 or u'系統' == chats[j]['name']:
            continue
        name = chats[j]['name']
    simple_name = seg.replaceSymbol(name, u'')
    if not simple_name:
        simple_name = name
    if not simple_name:
        simple_name = getRandUser()
    if len(simple_name) < 2:
        simple_name += u'網友'
    return simple_name

def getRandUser():
    users = []
    for key in chats:
        if u'系統' == chats[key]['name'] or 'effect' in chats[key]:
            continue
        users.append(chats[key]['name'])
    name = random.choice(users)
    if u'系統' == name:
        return u'祥平君'
    if len(name) < 2:
        name += u'網友'
    return name

def hasStopWords(str):
    stopWords = [u'晚安', u'說話', u'條件', u'講話', u'關係', u'系統']
    for stop in stopWords:
        if 0 == str.find(stop):
            if str == stop:
                return True
        elif str.find(stop) > 0:
            return True
    return False

def replaceKeyword(sentence, input, pos):
    global said_keyword
    candidate = []
    for keyword in seg.getNoun(input):
        if hasStopWords(keyword):
            continue
        if not keyword in said_keyword:
            candidate.append(keyword)
    random.shuffle(said_keyword)
    for i, keyword in enumerate(candidate + said_keyword):
        idx = '[n' + str(i+1) + ']'
        if sentence.find(idx) < 0:
            break
        sentence = sentence.replace(idx, keyword)
        said_keyword.append(keyword)
        name = getUser(keyword)
        sentence = sentence.replace('[u]', name)
    sentence = sentence.replace('[u]', getRandUser())
    return sentence

def saySomething():
    global sentences_idx
    if sentences_idx >= len(sentences.sentences):
        random.shuffle(sentences.sentences)
        sentences_idx = 0
    text = sentences.sentences[sentences_idx]
    sentences_idx += 1
    text = replaceKeyword(text, getMixedSentence(), 'n')
    idx = re.search('^(\d+)', chats_key[-1]).group(1)
    idx = int(idx) + 1
    attr = str(idx) + '　sysmsg'
    data = {'color':'black','text':text,'name':'系統'}
    firebase.put('/chat', name=attr, data=data)

def getChats():
    global chats
    global chats_key
    chats = firebase.get('/chat', None)
    chats_key = sorted(chats.keys())

def getMixedSentence():
    mixed_sentence = ''
    mixed_sentence_count = 0
    for key in reversed(chats_key):
        if u'系統' == chats[key]['name'] or u'effect' in chats[key]:
            continue
        text = chats[key]['text']
        text = re.sub(u'\[.*\]',u'。', text)
        text = re.sub(u'[.;:!\(\)]',u'。', text)
        text = text.replace(u'台',u'臺')
        if not text:
            continue
        mixed_sentence += text + '。'
    return mixed_sentence
