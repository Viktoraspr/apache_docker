"""
For getting metal prices using API request.

# XAU - Gold
# XAG - Silver
# PA - Palladium
# PL - Platinum
"""

from typing import Dict, Tuple
from random import uniform

import requests

from src.config.config import WEB_URL, HEADERS
from src.database.db_management import DBManagement


class Metal(DBManagement):

	def __init__(self, web_url=WEB_URL, headers=HEADERS):
		super().__init__()
		self.url = web_url
		self.headers = HEADERS

	def send_request(self) -> Dict:
		"""
		Send API requests.
		:return: Live metal prices in dictionary
		"""
		try:
			metal_response = requests.get(url=self.url, headers=self.headers)
		except Exception:
			print("It was error when tried to get data from metal's prices portal")
			raise Exception('It was error')
		metal_response = metal_response.json()
		return metal_response

	@staticmethod
	def __get_mock_prices() -> Dict:
		"""
		For creating mock prices.
		:return: Metal prices in dictionary
		"""
		metal_response = {
			'rates':
				{
					'XAU': uniform(1815, 1819),
					'XAG': uniform(20, 22),
					'PA': uniform(920, 925),
					'PL': uniform(790, 795),
				}
		}
		return metal_response

	def get_prices(self, mock_prices=True) -> Tuple:
		"""
		Method, where you choose what prices you want to get - mock or real
		:return: prices in tuple format
		"""
		if mock_prices:
			prices = self.__get_mock_prices()['rates']
		else:
			prices = self.send_request()['rates']

		return prices['XAU'], prices['XAG'], prices['PA'], prices['PL']

	def run(self, mock_prices=True) -> None:
		"""
		Runs API request and to DB.
		:param mock_prices: "True" for mock prices, False - for real prices
		:return: None
		"""
		self.add_values_to_metal_prices_table(self.get_prices(mock_prices=mock_prices))
