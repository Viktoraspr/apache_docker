from datetime import datetime
from typing import List
import re
from pathlib import Path
from sktime.forecasting.arima import ARIMA

from src.config.config import DB_URL
from src.database.db_management import DBManagement


class Model(DBManagement):
    def __init__(self, tickers: List[str] = None, url: str = DB_URL) -> None:
        super().__init__(url=url)
        if tickers is None:
            self.tickers = ["XAU", "XAG", "PA", "PL"]
        else:
            self.tickers = tickers
        self.models: dict[str, ARIMA] = {}

    def train(self, /, use_generated_data: bool = False) -> None:
        if use_generated_data:
            data = self.get_values_for_machine_learning_project()
        else:
            raise NotImplementedError

        for ticker in self.tickers:
            dataset = data[ticker].values
            model = ARIMA(order=(1, 1, 0), with_intercept=True, suppress_warnings=True)
            model.fit(dataset)
            self.models[ticker] = model

    def save(self, path_to_dir) -> None:
        date = str(datetime.now())
        date = re.sub(r'[. :-]', '_', date)
        path_to_dir = Path(f'{path_to_dir}/{date}')
        path_to_dir.mkdir(parents=True, exist_ok=True)
        for ticker in self.tickers:
            full_path = path_to_dir / ticker
            self.models[ticker].save(full_path)

    def run(self, path_to_dir=None, use_generated_data: bool = True):
        self.train(use_generated_data=use_generated_data)
        self.save(path_to_dir=path_to_dir)
