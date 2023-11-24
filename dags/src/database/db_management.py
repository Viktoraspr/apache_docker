"""
This file is for creating connection with DB. It injects, retrieves data as well.

Metal constants:
XAU - Gold
XAG - Silver
PA - Palladium
PL - Platinum
"""
from datetime import datetime, timedelta
from typing import Tuple

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from src.config.config import DB_URL
from src.database.models import Price


class DBManagement:
    def __init__(self, url=DB_URL):
        self.url = url
        self.engine = create_engine(self.url)

    def add_values_to_metal_prices_table(self, prices: Tuple[float, ...]) -> None:
        """
        Adds prices to table price
        :param prices: metal prices.
        :return: None
        """

        price = Price(
            XAU_price_Eur=prices[0],
            XAG_price_Eur=prices[1],
            PA_price_Eur=prices[2],
            PL_price_Eur=prices[3],
        )

        with Session(self.engine) as session:
            session.add(price)
            session.commit()

    def create_last_12_hours(self):
        """
        Creates view last 12 hours prices
        :return: None
        """
        data_now = datetime.now() - timedelta(hours=12)

        sql_query = f"""
        CREATE OR REPLACE VIEW prices_last_12 AS
        select *
        FROM prices
        WHERE timestamp > '{data_now}';
        """
        with self.engine.connect() as con:
            con.execute(text(sql_query))

    def get_values_for_machine_learning_project(self) -> pd.DataFrame:
        """
        Extracts data from view 'prices_last_12'
        :return: return prices in pandas DataFrame format.
        """
        sql_query = f"""
                select *
                FROM prices_last_12;
                """

        with self.engine.connect() as con:
            values = con.execute(text(sql_query))

        columns = ['XAU_price_Eur', 'XAG_price_Eur', 'PA_price_Eur', 'PL_price_Eur']
        data_frame = pd.DataFrame(data=values)[columns]

        columns = {
            "XAU_price_Eur": "XAU",
            "XAG_price_Eur": "XAG",
            "PA_price_Eur": "PA",
            "PL_price_Eur": "PL",
        }
        data_frame.rename(columns=columns, inplace=True)

        return data_frame
