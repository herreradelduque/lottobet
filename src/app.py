"""Module providing utilities for LaPrimitiva bets"""
import logging
import pandas as pd
from pandas import DataFrame

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def df_acquisition() -> DataFrame:
    """This function returns a df with the last LaPrimitiva lottery results

    Args:
        param (None): This function gets no param

    Returns:
        DataFrame: DataFrame with LaPrimitiva results"""

    logging.info(
        'Getting LaPrimitiva results from: https://lawebdelaprimitiva.com/Primitiva/')

    return pd.read_csv(
        'https://lawebdelaprimitiva.com/Primitiva/descarga_historico/2023/csv.html',
        index_col=1,
        header=6,
        sep=';',
    ).reset_index()


if __name__ == '__main__':
    df = df_acquisition()
    print(df)
    logging.info('Step 1: Acquire data: DONE!')
