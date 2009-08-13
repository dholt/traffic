#!/usr/bin/env python

import urllib2
import xml.parsers.expat

class Traffic:
	def __init__(self, yahooApiKey, zipcode, radius):
		self.url = 'http://local.yahooapis.com/MapsService/V1/trafficData?appid=%s&zip=%s&radius=%s' % (yahooApiKey, zipcode, radius)
		self.info = []
		self.inTag = 0
		self.count = 0
		self.current = ""

		self.__update()

	def __update(self):
		p = xml.parsers.expat.ParserCreate()
		p.StartElementHandler = self.__start_element
		p.EndElementHandler = self.__end_element
		p.CharacterDataHandler = self.__char_data
		
		page = urllib2.urlopen(self.url)
		p.Parse(page.read(), 1)
		page.close()
		

	def __start_element(self, name, attrs):
		name = name.encode('utf-8')
		if name == 'Result':
			self.inTag = 1
			for x in attrs:
				self.info.append({})
				self.info[self.count][x.encode('utf-8')] = attrs[x].encode('utf-8')
		elif self.inTag == 1:
			self.current = name
	
	def __end_element(self, name):
		if name == 'Result':
			self.inTag = 0
			self.count = len(self.info)

	def __char_data(self, data):
		if self.inTag == 1:
			self.info[self.count][self.current] = data.encode('utf-8')

	def getTraffic(self):
		return self.info
	
if __name__ == '__main__':
	from config import *
	t = Traffic(yahooApiKey, zipcode, radius)
	for item in t.getTraffic():
		print item['Title'], "(%s [%s])" % (item['type'], item['Severity'])
		print item['Description']
		print item
