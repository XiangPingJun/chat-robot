#!/usr/bin/python
#-*- coding: utf8 -*-
####==================================
#
#    This file is part of the NAER Segmentor  - 
#    Copyright (c) 2016 National Academy for Educational Research
# 
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
# 
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os,time,subprocess,string,re, json
import CRFPP

## set ../Data directory as default model directory 
__default_model_dir__=os.path.abspath(os.path.dirname(__file__)+'/Data')

class POSTagger(object):
	def __init__(self, model_dir=__default_model_dir__):
		self.__model = os.path.join(model_dir,'POSModel200K')
		self.tagger=CRFPP.Tagger("-m "+self.__model) 
		self.separator=re.compile('[\t 　]')

	def __CheckCW(self,word):
		for charC in word:
			if not(charC >= u'\u4e00' and charC <= u'\u9fff'):
				return False
		return True

	def __generateFeatures(self,tokens_list):
		'''generate features for input data'''

		token_features = []
		
		for token in tokens_list:
			
			Features = []
			##===========開始加上各種特徵值===========
			
			##詞的基礎類別 Chinese, Punctuation, or Foreign words

			##character type
			if self.__CheckCW(token):##如果是中文字就直接輸出
				Features.append("AC")
			elif len(token) == 1 and len(token.encode('utf8')) > 1: ##全形符號
				Features.append("PUNC")
			elif len(token.encode('utf8')) == 1 and token in ".,!?;'\"/-":
				Features.append("PUNC")
			else:
				Features.append("Mix")
			
			##last character
			Features.append(token[-1])

			##first character
			Features.append(token[0])

			token_features.append((token,Features))
		return token_features

	def procSents(self, sents):
		L=[]
		for sent in sents:
			L.append(self.procSent(sent))
		return L

	def procSentStr(self, sentStr):
		return self.procSent(self.separator.split(sentStr.strip("\r\n")))
		#return self.procSent(re.split(self.separator,sentStr.strip("\r\n")))

	def _tag_tokens(self, tokens):
		self.tagger.clear()

		##get features for labeling
		token_features = self.__generateFeatures(tokens)
		for fea in token_features:
			x=(fea[0]+" "+string.join(fea[1]," ")).encode("UTF-8")
			self.tagger.add(x)

		self.tagger.parse()

		##start to label
		tagged_tokens=[]

		for i in range(self.tagger.size()):
			tagged_tokens.append([])
			for j in range(self.tagger.xsize()):
				tagged_tokens[-1].append(self.tagger.x(i,j))

			tagged_tokens[-1].append(self.tagger.y2(i))

		return tagged_tokens

	def _assemble_tokens(self, tagged_tokens):
		   
		result=[]
		for data in tagged_tokens:
			result.append((data[0].decode("UTF-8"),data[-1])) 

		return result


	def procSent(self, tokens):
		'''
			given a Chinese string (with space as word boundary)
			output Words with POSs
		'''
		tagged_tokens=self._tag_tokens(tokens)
		result=self._assemble_tokens(tagged_tokens)


		return result


if __name__ == '__main__':

	Tagger = POSTagger()
	result = Tagger.procSentStr(u"這是 一 個 測試 。")
	print " ".join(["%s(%s)" % data for data in result])

	result = Tagger.procSent([u"這是",u"一", u"個", u"測試", u"。"])
	print " ".join(["%s(%s)" % data for data in result])

	result = Tagger.procSents([[u"這是",u"一", u"個", u"測試", u"。"], [u"這是",u"另", u"一", u"個", u"測試", u"。"]])
	for sent in result:
		print " ".join(["%s(%s)" % data for data in sent])
	
