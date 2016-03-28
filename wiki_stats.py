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
		self.titles = [] # Массив названий статей
		with open(filename) as f:
			articles_number, _nlinks = map(int, f.readline().split()) # Кол-во всех статей и ссылок (вершин и ребер)
			self._links = array.array('L', [0]*articles_number) # Массив кол-ва ссылок из каждой статьи
			self.external_links = array.array('L', [0]*articles_number) # Массив кол-ва ссылок в каждую статью
			self._redirect = array.array('B', [0]*articles_number) # Таблица перенаправляющих статей: 1 - перенаправляет, 0 - нет
			self.external_redirect = array.array('B', [0]*articles_number) # Таблица перенаправленных статей
			self._sizes = array.array('L', [0]*articles_number) # Массив весов вершин
			for i in range(articles_number):
				self.titles.append(f.readline().rstrip())
				weight, redirect, links_number =  map(int, f.readline().split()) # Вес, флаг перенаправления и кол-во ссылок
				self.offset.append(self.offset[i] + links_number)
				self._sizes[i] = weight
				self._redirect[i] = redirect
				self._links[i] = links_number
				for j in range(links_number):
					link = int(f.readline())
					self.edges.append(link)
					if redirect:
						self.external_redirect[link] += 1
		
		for i in range(articles_number):
			self.external_links[i] = self.edges.count(i) - self.external_redirect[i]

		print('Граф загружен')

	def get_number_of_links_from(self, _id):
		return self._links[_id]

	def get_links_from(self, _id):
		return self.edges[self.offset[_id ]:self.offset[_id + 1]]

	def get_number_of_links_in(self, _id):
		return self.external_links[_id]

	'''def get_links_in(self, _id):
		pass'''

	def get_id(self, title):
		return self.titles.index(title)

	def get_number_of_pages(self):
		return len(self.titles)

	def is_redirect(self, _id):
		return self._redirect[_id]

	def get_title(self, _id):
		return self.titles[_id]

	def get_page_size(self, _id):
		return self._sizes[_id]


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
	
	print('Количество статей с перенаправлением:', wg._redirect.count(1))
	
	min_links = min(wg._links)
	max_links = max(wg._links)
	print('МИНимальное количество ссылок ИЗ статьи:', min_links)
	print('Количество статей с МИНимальным количеством ссылок:', wg._links.count(min_links))
	print('МАКСимальное количество ссылок ИЗ статьи:', max_links)
	print('Количество статей с МАКСимальным количеством ссылок:', wg._links.count(max_links))
	print('Статья с наибольшим количеством ссылок:', wg.get_title(wg._links.index(max_links)))
	
	average_n_links = sum(wg._links)/wg.get_number_of_pages()
	print('Среднее количество ссылок в статье:', average_n_links)
	
	min_external_links = min(wg.external_links)
	max_external_links = max(wg.external_links)
	print('МИНимальное количество ссылок НА статью (перенаправление не считается внешней ссылкой):', min_external_links)
	print('Количество статей с МИНимальным количеством внешних ссылок:', wg.external_links.count(min_external_links))
	print('МАКСимальное количество ссылок НА статью:', max_external_links)
	print('Количество статей с МАКСимальным количеством внешних ссылок:', wg.external_links.count(max_external_links))
	print('Статья с наибольшим количеством внешних ссылок:', wg.get_title(wg.external_links.index(max_external_links)))

	average_n_ext_links = sum(wg.external_links)/wg.get_number_of_pages()
	print('Среднее количество ссылок в статье:', average_n_ext_links)

	# TODO: статистика и гистограммы
