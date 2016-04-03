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
		with open(filename, encoding="utf8") as f:
			# Кол-во всех статей и ссылок (вершин и ребер)
			articles_number, _nlinks = map(int, f.readline().split())
			
			# Массив кол-ва ссылок из каждой статьи
			self._links = array.array('L', [0]*articles_number)
			
			# Массив кол-ва ссылок в каждую статью
			self.external_links = array.array('L', [0]*articles_number)
			
			# Таблица перенаправляющих статей: 1 - перенаправляет, 0 - нет
			self._redirect = array.array('B', [0]*articles_number)
			
			# Таблица перенаправленных статей
			self.external_redirect = array.array('B', [0]*articles_number)
			
			# Массив весов вершин
			self._sizes = array.array('L', [0]*articles_number)
			
			for i in range(articles_number):
				self.titles.append(f.readline().rstrip())
				
				# Вес, флаг перенаправления и кол-во ссылок
				weight, redirect, links_number =  map(int, f.readline().split())
				
				self.offset.append(self.offset[i] + links_number)
				self._sizes[i] = weight
				self._redirect[i] = redirect
				for j in range(links_number):
					link = int(f.readline())
					self.edges.append(link)
					if redirect:
						self.external_redirect[link] += 1
					else:
						self._links[i] = links_number
				# Статья с перенаправлением не считается полноценной статьей, поэтому перенаправления не считаются ссылками
		
		for i in range(articles_number):
			# Кол-во ссылок в i-ую статью = кол-во вхождений этой статьи в грани - кол-во перенаправлений на эту статью
			self.external_links[i] = self.edges.count(i) - self.external_redirect[i]

		print('Граф загружен', '\n')

	def get_number_of_links_from(self, _id): # Кол-во ссылок ИЗ статьи с номером _id
		return self._links[_id]

	def get_links_from(self, _id): # Список статей, на которые ссылается статья с номером _id
		return self.edges[self.offset[_id ]:self.offset[_id + 1]]

	def get_number_of_links_in(self, _id): # Кол-во ссылок В статью с номером _id
		return self.external_links[_id]

	'''def get_links_in(self, _id):
		pass'''

	def get_id(self, title): # Получить идентификатор (номер) статьи по ее названию
		return self.titles.index(title)

	def get_number_of_pages(self): # Кол-во всех статей
		return len(self.titles)

	def is_redirect(self, _id): # Проверить, перенаправляет ли статья с номером _id
		return self._redirect[_id]

	def get_title(self, _id): # Получить название статьи по ее номеру
		return self.titles[_id]

	def get_page_size(self, _id): # Вес статьи
		return self._sizes[_id]


def hist(fname, data, bins, xlabel, ylabel, title, facecolor='green', alpha=0.5, transparent=True, **kwargs):
	plt.clf()
	# TODO: нарисовать гистограмму и сохранить в файл
	
def bfs(G, start, end, nodes = [], wg = None, fired = {}): # Поиск по ширине
	# Аргументы: граф, стартовая вершина, конечная, вершины искомого пути, вики-граф (при первом вызове не нужен), массив пройденных вершин
	nodes.append(end)
	if start == end:
		return nodes
	queue = [start]
	if type(G) == WikiGraph:
		fired[start] = G.get_links_from(G.get_id(start)) # Соседи start (числа)
		while queue:
			current = queue.pop(0) # Взять первую в очереди вершину на обработку
			for neighbour in G.get_links_from(G.get_id(current)): # Соседи current (числа)
				neighbour_name = G.get_title(neighbour)
				if neighbour_name not in fired:
					fired[neighbour_name] = G.get_links_from(neighbour) # Соседи neighbour (числа)
					queue.append(neighbour_name)
				if neighbour_name == end:
					nodes = bfs(fired, start, current, nodes, G)
					return nodes
	else:
		fired[start] = G[start] 
		while queue:
			current = queue.pop(0) # Взять первую в очереди вершину на обработку
			for neighbour in G[current]: # Соседи current (числа)
				neighbour_name = wg.get_title(neighbour)
				if neighbour_name not in fired:
					fired[neighbour_name] = G[neighbour] # Соседи neighbour (числа)
					queue.append(neighbour_name)
				if neighbour_name == end:
					nodes = bfs(fired, start, current, nodes, wg)
					return nodes

def print_path(wg, start = 'Python', end = 'Список_файловых_систем'):
	print('Запускаем поиск в ширину')
	nodes_of_path = bfs(wg, start, end)
	nodes_of_path.reverse()
	print('Поиск закончен. Найден путь:')
	print(' '.join(nodes_of_path))


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
	
	number_of_pages = wg.get_number_of_pages()
	number_of_redirect = wg._redirect.count(1)
	print('Количество статей с перенаправлением:', number_of_redirect)
	
	min_links = min(wg._links)
	max_links = max(wg._links)
	print('МИНимальное количество ссылок ИЗ статьи:', min_links)
	print('Количество статей с МИНимальным количеством ссылок:', wg._links.count(min_links))
	print('МАКСимальное количество ссылок ИЗ статьи:', max_links)
	print('Количество статей с МАКСимальным количеством ссылок:', wg._links.count(max_links))
	print('Статья с наибольшим количеством ссылок:', wg.get_title(wg._links.index(max_links)), '\n')

	average_n_links = sum(wg._links)/(number_of_pages - number_of_redirect)
	print('Среднее количество ссылок ИЗ статьи:', round(average_n_links, 2), '\n')
	
	min_external_links = min(wg.external_links)
	max_external_links = max(wg.external_links)
	print('МИНимальное количество ссылок НА статью (перенаправление не считается внешней ссылкой):', min_external_links)
	print('Количество статей с МИНимальным количеством внешних ссылок:', wg.external_links.count(min_external_links))
	print('МАКСимальное количество ссылок НА статью:', max_external_links)
	print('Количество статей с МАКСимальным количеством внешних ссылок:', wg.external_links.count(max_external_links))
	print('Статья с наибольшим количеством внешних ссылок:', wg.get_title(wg.external_links.index(max_external_links)), '\n')

	average_n_ext_links = sum(wg.external_links)/(number_of_pages - number_of_redirect)
	print('Среднее количество ссылок НА статью:', round(average_n_ext_links, 2))
	print("в тексте лабораторной иное значение возможно потому, что забыто вычитание redirect'ов")
	print('значение совпало с кол-вом ссылок из статьи неслучайно, так и должно быть', '\n')
	
	min_external_redirect = min(wg.external_redirect)
	max_external_redirect = max(wg.external_redirect)
	print('МИНимальное количество перенаправлений на статью:', min_external_redirect)
	print('Количество статей с МИНимальным количеством внешних перенаправлений:', wg.external_redirect.count(min_external_redirect))
	print('МАКСимальное количество перенаправлений на статью:', max_external_redirect)
	print('Количество статей с МАКСимальным количеством внешних перенаправлений:', wg.external_redirect.count(max_external_redirect))
	print('Статья с наибольшим количеством внешних перенаправлений:', wg.get_title(wg.external_redirect.index(max_external_redirect)), '\n')
	
	average_n_ext_redirect = sum(wg.external_redirect)/number_of_pages
	print('Среднее количество внешних перенаправлений на статью:', round(average_n_ext_redirect, 2), '\n')
	
	print_path(wg)