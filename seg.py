#encoding=utf-8
import json
from Segmentor import *
from POSTagger import *
import re

segmenter = Segmentor()

def getNoun(text):
    words = segmenter.segment(text)
    temp = []
    for item in words:
        item = replaceSymbol(item, u'。')
        item = re.sub(u'\w', u'。', item)
        split = []
        for sp in item.split(u'。'):
            if sp:
                split.append(sp)
        if len(split) > 0:
            for sp in split:
                temp.append(sp)
        else:
            temp.append(u'。')
    words = temp
    seg = POSTagger().procSent(words)
    nouns = []
    seperated = True
    for item in seg:
        if 'Na' != item[1]: # and 'Nb' != item[1] and 'Nc' != item[1]:
            seperated = True
            continue
        if seperated:
            nouns.append(item[0])
        else:
            nouns[-1] += item[0]
        seperated = False
    # sort by frequency
    candidate = []
    for noun in nouns:
        found = False
        i = 0
        for cand in candidate:
            if noun.find(cand[0]) >= 0:
                candidate[i][0] = noun
            if cand[0].find(noun) >= 0 or noun.find(cand[0]) >=0:
                candidate[i][1] += 1
                found = True
                break
            i += 1
        if not found:
            candidate.append([noun, 1])    
    def compareTerm(a, b):
        if a[1] > b[1]:
            return -1
        elif a[1] == b[1]:
            return 0
        else:
            return 1
    candidate.sort(compareTerm)
    result = []
    for cand in candidate:
        result.append(cand[0])
    return result

def replaceSymbol(text, replace):
    return re.sub(u'[^\w\u4e00-\u9fa5\u3105-\u3129\u02CA\u02C7\u02CB\u02D9]', replace, text)
