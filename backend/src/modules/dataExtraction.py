#Data Extraction for ETL process
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)

def download_tickers(tickers: list[str], start_date, end_date, period, interval='1d') -> pd.DataFrame:
    """Funçao para extrair dados de ação no Yahoo Finance

    Args:
        ticker (str): explica o que é ticker
        start_date (str): Data inicial para a consulta
        end_date (str): Data final para a consulta
        period (str): Periodo que seja que seja agrupado as informacoes
        interval (str, optional): Intervalo para consulta. Defaults to '1d'.

    Returns:
        DataFrame: DataFrame com os dados consultados
    """
    
    if not period:

        logging.info(f"Using start date: {start_date}, end date: {end_date}, and interval: {interval}")

        if not start_date:
            start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d') # Default to 3 months ago if no start date is provided
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
    else:
        start_date = None
        end_date = None
        logging.info(f"Using period: {period} and interval: {interval}")


    
    for ticker in tickers: 
        if yf.Ticker(ticker):
            pass
        else:
            logging.error(f"Ticker {ticker} is not valid or does not exist in Yahoo Finance.")
            tickers.remove(ticker)  # Remove invalid tickers from the list
    
    try:
        data = yf.download(         # Download historical data for the ticker
            tickers,
            start=start_date,
            end=end_date,
            period=period,
            interval=interval,
            auto_adjust=True,
        )
       
    except Exception as e:
        logging.error(f"Failed to download data for {ticker} from Yahoo Finance: {e}")
        return None
    
    df = pd.DataFrame(data)  # Convert the data to a DataFrame
    
    if df.empty:
        logging.warning(f"No data found for {ticker} in the specified date range.")
        return None
    else:
        return df

