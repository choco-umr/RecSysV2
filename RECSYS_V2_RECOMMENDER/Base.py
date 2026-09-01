from abc import ABC, abstractmethod


class recommender(ABC):
	@abstractmethod
	def fit(self, data):
		pass


	@abstractmethod
	def recommend(self, query):
		pass