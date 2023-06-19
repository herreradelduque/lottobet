"""Module providing utilities for La Primitiva bets"""
import logging
from typing import List, Set, Any
import itertools
import random
import pandas as pd
from pandas import DataFrame

# import requests
# from datetime import date
import streamlit as st


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


# def csv_acquisition() -> None:
#    logging.info(
#        'Downloading LaPrimitiva results from: https://lawebdelaprimitiva.com/Primitiva/')
#    url = 'https://lawebdelaprimitiva.com/Primitiva/descarga_historico/2023/csv.html'
#    req = requests.get(url)
#    url_content = req.content
#    today = date.today().strftime('%Y%m%d')

#    with open(f'../data/{today}.csv', 'wb') as f:
#        f.write(url_content)


#    return None
def df_acquisition() -> DataFrame:
    """This function returns a df with the last LaPrimitiva lottery results

    Args:

    Returns:
        DataFrame: DataFrame with LaPrimitiva results"""

    logging.info(
        'Getting LaPrimitiva results from: https://lawebdelaprimitiva.com/Primitiva/'
    )

    return pd.read_csv(
        'https://lawebdelaprimitiva.com/Primitiva/descarga_historico/2023/csv.html',
        header=6,
        sep=';',
    )


def last_n_draws(
        df_arg: DataFrame, recent: int = 0, last_n: int = 10
) -> DataFrame:
    """This function returns the last n recent draws from the n recent.

    Args:
        df_arg: df with all the draws.
        recent: the n recent draw
        last_n: number of draws

    Returns:
        The return a df

    """
    df_arg = df_arg.iloc[recent:last_n, :7]
    col_names = ['N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'C']
    df_arg.columns = col_names

    return df_arg


def split_df(df_arg: DataFrame) -> tuple[DataFrame, DataFrame]:
    """This function splits the df into numbers and complimentary.

    Args:
        df_arg: df with all the draws.

    Returns:
        The return 2 df's: one with the numbers and other one with the complimentary numbers

    """
    return df_arg.iloc[:, :-1], df_arg.iloc[:, -1:]


def row_list_f(df_arg: DataFrame) -> Set[Any]:
    """This function returns a list with all the numbers

    Args:
        df_arg: df with all the draws.

    Returns:
        The return a list

    """
    # Create an empty list
    row_list_arg = []

    # Iterate over each row
    for _, rows in df_arg.iterrows():
        for number in rows:
            row_list_arg.append(number)
    return set(row_list_arg)


def row_list_com_f(df_arg: DataFrame) -> List[int]:
    """This function returns a list with all the complement

    Args:
        df_arg: df with all the draws.

    Returns:
        The return a list

    """
    # Create an empty list
    row_list_com_arg = []

    # Iterate over each row
    for _, rows in df_arg.iterrows():
        for number in rows:
            row_list_com_arg.append(number)
    return row_list_com_arg


def get_all_combinations(
    my_list: Set[int], num_elements: int
) -> list[tuple[int, ...]]:
    """This function calculates all the possible combinations.

    Args:
        my_list: List with all the numbers
        num_elements: number of elements in the combionations

    Returns:
        The return a list of tuples

    """
    if len(my_list) < num_elements:
        raise ValueError('Number of elements exceeds the length of the list.')

    combinations = [
        tuple(combination)
        for combination in itertools.combinations(my_list, num_elements)
    ]

    return combinations


def get_n_bets_f(
    all_combinations_arg: list[tuple[int, ...]], get_n_bets_arg: int
) -> list[tuple[int, ...]]:
    """This function returns a list with random combinations.

    Args:
        all_combinations_arg: list with all possible combinations
        get_n_bets_arg: number of bets

    Returns:
        The return a list

    """
    return random.sample(all_combinations_arg, get_n_bets_arg)


if __name__ == '__main__':
    last_n_draws_arg = st.number_input(
        'Insert a number of draws',
        min_value=int(2),
        max_value=int(9),
        value=int(5),
        step=1,
    )

    number_of_bets = st.number_input(
        'Insert a number of bets',
        min_value=int(0),
        max_value=int(50),
        value=int(2),
        step=1,
    )
    # st.write(f'You are going to get {number_of_bets} combinations')

    # logging.info('Step 2: Acquire data: DONE!')
    # csv_acquisition()

    if st.button('Obtener apuestas'):
        logging.info('Step 1: Download csv: DONE!')
        df = df_acquisition()

        st.write(f'Downloading last {last_n_draws_arg} draws...')
        df_10 = last_n_draws(df_arg=df, recent=0, last_n=last_n_draws_arg)

        st.dataframe(df_10)

        df_10_nums, df_10_com = split_df(df_10)

        row_list = row_list_f(df_10_nums)
        st.write('Calculating all possible combinations...')
        all_combinations = get_all_combinations(row_list, 6)
        st.write(
            f'{len(all_combinations)} possible combinations with {len(set(row_list))} different numbers.'
        )
        st.write('Your bets are here...:')

        my_n_bets = get_n_bets_f(all_combinations, number_of_bets)

        st.dataframe(my_n_bets)

        row_list_com = row_list_com_f(df_10_com)
        st.write('Calculating all possible complimentary numbers...')
        com_number = random.choice(row_list_com)
        st.write(
            f'{len(row_list_com)} possible combinations with {len(set(row_list_com))} different numbers.'
        )

        com_number_df = pd.DataFrame(
            {'Complimentary': [com_number]}
        ).reset_index(drop=True)['Complimentary']
        st.dataframe(com_number_df)

    else:
        st.write('')
