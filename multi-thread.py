##Name: Pavel Lyapin
##Class: CS 521
##Date: October 17th, 2016
##This program uses multi-threading to extract rows from an excel sheet and made them into custom python objects


import csv
import os
import threading
from queue import Queue
from read_csv import StockStatRecord


##List of errors occured, gets nullified after each load of CSV
error_list = []

##Custom class to handle invalid entries in CSV files, as well as parsing errors and division by zero errors
##This class logs error messages in global list
class BadData(Exception):
    def __init__(self,message):
     error_list.append(message)

##This method validates each row to be a valid StockStatRecord, if invalid returns nothing
def validate_record(row):

    try:  # Validate that all columns exists for row and that none are empty
        ticker = row['ticker']
        company_name = row['company_name']
        exchange_country = row['exchange_country']
        price = row['price']
        exchange_rate = row['exchange_rate']
        shares_outstanding = row['shares_outstanding']
        net_income = row['net_income']

        if min(len(ticker), len(company_name), len(exchange_country), len(price), len(exchange_rate),
               len(shares_outstanding), len(net_income)) < 1:
            raise KeyError
            return
    except KeyError:
        raise BadData('Missing information, can not create record')
        return
    else:
        try:  # Validate that floats and integers are in the proper format
            price = float(price)
            exchange_rate = float(exchange_rate)
            shares_outstanding = float(shares_outstanding)
            net_income = float(net_income)
        except ValueError:
            raise BadData('Could not parse to float')
            return
        else:
            try:  # Validate that program doesn't attempt to divide by zero
                market_value_usd = price * exchange_rate * shares_outstanding
                pe_ratio = price * shares_outstanding / net_income
            except ZeroDivisionError:
                raise BadData('Can not divide by zero, bad data')
            else:  # If validation passes return valid record
              return StockStatRecord(ticker, company_name, exchange_country, price, exchange_rate,
                                                   shares_outstanding, net_income, market_value_usd, pe_ratio)


##Global queues to be used by threads
stocks_rows = Queue()
stocks_records = Queue()

##This is a callable class, used for extracting rows from global queue stocks_rows , and inserting them as StockStatRecords into stocks_records
class Runnable():
    def __call__(self, *args, **kwargs):

        timeout = 0

        for key, value in kwargs.items():
            if (key == 'timeout'):
                timeout = value

        while True:
            try:
                 if stocks_rows.empty():
                     return
                 row = stocks_rows.get(timeout)
                 print('{worker_id} working hard!!'.format(worker_id=id(self)))
                 stocks_records.put(validate_record(row))
            except BadData:
                continue

##This class loads data from an excel sheet
##It then uses several threads to turn the data into StockStatRecords
class FastStocksCSVReader():
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):

        with open(self.file_path) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                 stocks_rows.put(row)

        threads = []
        for i in range(0,4):
            new_thread = threading.Thread(target=Runnable(),kwargs={'timeout': 1})
            new_thread.start()
            threads.append(new_thread)

        for thread in threads:
            thread.join()

        output_list = []

        while not stocks_records.empty():
            output_list.append(stocks_records.get())

        return output_list



if __name__ == "__main__":
    # execute only if run as a script

    stock_stat_path = 'StockValuations.csv'
    stock_stat_list =[]
    if not os.path.exists(stock_stat_path):
        print(stock_stat_path, " is an invalid file path")
    else:
        stock_stat_list = FastStocksCSVReader(stock_stat_path).load()

    for record in stock_stat_list:
        print(record)

    print('************************************************')
    print('Number of rows with bad data in ', stock_stat_path, ':', len(error_list))
    print('************************************************')
    error_list = []






