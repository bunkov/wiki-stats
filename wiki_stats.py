#!/usr/bin/python3

import os
import sys
import math

import array

import statistics

from matplotlib import rc
rc('font', family='Droid Sans', weight='normal', size=14)

import matplotlib.pyplot as plt


class WikiGraph:

	def load_from_file(self, filename):
		print('Загружаю граф из файла: ' + filename)
		self.edges = array.array('L', [])
		self.offset = array.array('H', [0])
		self.titles = []
		with open(filename) as f:
			articles_number, _nlinks = map(int, f.readline().split())
			for i in range(articles_number):
				self.titles.append(f.readline().rstrip())
				weight, redirect, links_number =  map(int, f.readline().split())
				self.offset.append(self.offset[i] + links_number)
				for j in range(links_number):
					self.edges.append(int(f.readline()))
		'''
		self._sizes = array.array('L', [0]*n)
		self._links = array.array('L', [0]*_nlinks)
		self._redirect = array.array('B', [0]*n)
		self._offset = array.array('L', [0]*(n+1))'''

			# TODO: прочитать граф из файла

		print('Граф загружен')

	def get_number_of_links_from(self, _id):
		pass

	def get_links_from(self, _id):
		pass

	def get_id(self, title):
		return self.titles.index(title)

	def get_number_of_pages(self):
		pass

	def is_redirect(self, _id):
		pass

	def get_title(self, _id):
		return self.titles[_id]

	def get_page_size(self, _id):
		pass


def hist(fname, data, bins, xlabel, ylabel, title, facecolor='green', alpha=0.5, transparent=True, **kwargs):
	plt.clf()
	# TODO: нарисовать гистограмму и сохранить в файл


if __name__ == '__main__':

	if len(sys.argv) != 2:
		print('Использование: wiki_stats.py <файл с графом статей>')
		sys.exit(-1)

	if os.path.isfile(sys.argv[1]):
		wg = WikiGraph()
		wg.load_from_file(sys.argv[1])
	else:
		print('Файл с графом не найден')
		sys.exit(-1)

	# TODO: статистика и гистограммы
