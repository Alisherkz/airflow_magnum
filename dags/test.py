from airflow.decorators import dag, task
import pendulum
import logging

from io import StringIO
import pandas as pd
import ssl
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
import time


@dag(
    schedule='@hourly',
    start_date=pendulum.datetime(2024, 2, 4, tz='Asia/Almaty'),
    catchup=False,
    tags=['test_python']
)
def test_dag():
    @task
    def get_kurs():
        try:
            ssl._create_default_https_context = ssl._create_stdlib_context

            url = 'https://kurs.kz/'

            opts = FirefoxOptions()
            opts.add_argument("--headless")
            driver = webdriver.Firefox(options=opts)
            driver.get(url)
            time.sleep(5)
            htmlSource = driver.page_source

            dfs = pd.read_html(StringIO(htmlSource))

            dfs[0].to_csv('/opt/airflow/dags/test.csv')
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(e)

    get_kurs()


test_dag()
