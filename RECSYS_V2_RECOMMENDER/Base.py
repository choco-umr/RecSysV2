from abc import ABC, abstractmethod


class Recommender(ABC):
	@abstractmethod
	def fit(self, data):
		pass


	@abstractmethod
	def recommend(self, query):
		pass