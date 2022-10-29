from prefect import flow, get_run_logger, task
import pandas as pd
from typing import Union

# this flow is a test for processing 800 mb CSV
# I load it here:
# https://www3.stats.govt.nz/2018census/Age-sex-by-ethnic-group-grouped-total-responses-census-usually-resident-population-counts-2006-2013-2018-Censuses-RC-TA-SA2-DHB.zip?_ga=2.68486545.1860860682.1666167942-1295392051.1666167942


@task
def read_the_DataFrame(path_to_csv: str) -> pd.DataFrame:
    return pd.read_csv(path_to_csv, skiprows=0)


@task
def get_average_age(df: pd.DataFrame) -> pd.DataFrame:
    # in dataset there is columns:
    # Index(['Year', 'Age', 'Ethnic', 'Sex', 'Area', 'count'], dtype='object')

    return df["Age"].mean()


@task
def get_average_age(df: pd.DataFrame) -> Union[pd.DataFrame, int]:
    return df["Age"].mean()


@task
def count_wrong_values(df: pd.DataFrame):
    return df.loc[lambda x: x['Age'] > 120]['Age'].count()


@flow
def DataFrame_processing(path_to_csv: str):
    df = read_the_DataFrame(path_to_csv)
    avr_age = get_average_age(df)
    if avr_age > 120:
        # too much immortal peoples
        wrong_rows = count_wrong_values(df)
        get_run_logger().error(f'Wrong rows in the dataset based on the Age column: {wrong_rows}')
    # or do something else


if __name__ == "__main__":
    
    path_to_csv = 'path/to/your/csv'
    
    DataFrame_processing(path_to_csv)
