import os
import sqlite3
import read_csv
import collections

##This class is the parent class of BaseballStatsDAO and StockStatsDAO
##contains 1 member : db_name
class AbstractDAO:
    def __init__(self, db_name):
        self.db_name = db_name

    # This method will be implemented inside child classes
    def insert_records(self, records):
            raise NotImplementedError

    # This method will be implemented inside child classes
    def select_all(self):
        raise NotImplementedError

    # This method returns a sqllite connection depending on the type of DAO
    def connect(self):

        rtn_conn = sqlite3.connect(self.db_name)

        return rtn_conn

##This class extends AbstractDAO and implements methods: insert_records(records) , select_all()
class BaseballStatsDAO (AbstractDAO):

    ##This method takes a list of BaseballStatRecord records and insert the valid records into DB table baseball_stats
    def insert_records(self, records):

        a_connection = self.connect()
        a_cursor = a_connection.cursor()

        for record in records:
            creation_str = 'INSERT INTO baseball_stats VALUES (?,?,?,?)'

            try:
                row = record.name,\
                      record.games_played,\
                      record.avg,\
                      record.salary
                try:
                    a_cursor.execute(creation_str, row)
                except sqlite3.OperationalError:
                    print("Error inserting into baseball_stats")
            except AttributeError:
                print("Invalid BaseballStatRecord")

        a_connection.commit()
        a_connection.close()

    ##This method connects to the database configured for this class and selects all rows from baseball_stats
    ##Returns a list of BaseballStatRecord records
    def select_all(self):

        a_connection = self.connect()
        a_cursor = a_connection.cursor()

        baseball_queue = collections.deque()
        result_list = []

        try:
            a_cursor.execute('SELECT name,games_played,average,salary FROM baseball_stats')
            result_list = a_cursor.fetchall()
        except sqlite3.OperationalError:
            print("Error retrieving data from database:", self.db_name)

        for row in result_list:
            name,games_played,average,salary = row
            baseball_record = read_csv.BaseballStatRecord(name,
                                                                           salary,
                                                                           games_played,
                                                                           average)
            baseball_queue.append(baseball_record)

        a_connection.close()

        return baseball_queue

##This class extends AbstractDAO and implements methods: insert_records(records) , select_all()
class StockStatsDAO (AbstractDAO):

    ##This method takes a list of StockStatRecord records and insert the valid records into DB table stock_stats
    def insert_records(self, records):

        a_connection = self.connect()
        a_cursor = a_connection.cursor()

        for record in records:
            creation_str = 'INSERT INTO stock_stats VALUES (?,?,?,?,?,?,?,?,?)'
            try:
                row = record.name, \
                      record.company_name, \
                      record.exchange_country,\
                      record.price,\
                      record.exchange_rate,\
                      record.shares_outstanding,\
                      record.net_income,\
                      record.market_value_usd,\
                      record.pe_ratio
                try:
                    a_cursor.execute(creation_str,row)
                except sqlite3.OperationalError:
                    print("Error inserting into stock_stats")
            except AttributeError:
                print("Invalid StockStatRecord")

        a_connection.commit()  # save changes
        a_connection.close()

    ##This method connects to the database configured for this class and selects all rows from stock_stats
    ##Returns a list of StockStatRecord records
    def select_all(self):

        a_connection = self.connect()
        a_cursor = a_connection.cursor()

        stocks_queue = collections.deque()
        result_list = []

        try:
            a_cursor.execute('SELECT ticker,company_name,country,price,exchange_rate,shares_outstanding,net_income,market_value,pe_ratio FROM stock_stats')
            result_list = a_cursor.fetchall()
        except sqlite3.OperationalError:
            print("Error retrieving data from database:" , self.db_name)

        for row in result_list:
            ticker,company_name,country,price,exchange_rate,shares_outstanding,net_income,market_value,pe_ratio = row
            stock_record = read_csv.StockStatRecord(ticker,
                                                                     company_name,
                                                                     country,
                                                                     price,
                                                                     exchange_rate,
                                                                     shares_outstanding,
                                                                     net_income,
                                                                     market_value,
                                                                     pe_ratio)
            stocks_queue.append(stock_record)

        a_connection.close()

        return stocks_queue


if __name__ == "__main__":
    # execute only if run as a script
    baseball_stat_path = 'MLB2008.csv'
    baseball_stat_list = []
    if not os.path.exists(baseball_stat_path):
        print(baseball_stat_path, " is an invalid file path")
    else:
        baseball_stat_list = read_csv.BaseballCSVReader(baseball_stat_path).load()

    BaseballStatsDAO('baseball.db').insert_records(baseball_stat_list)
    baseball_list = BaseballStatsDAO('baseball.db').select_all()
    avg_list = []

    print("********************************************")
    print("Average salary by batting average:")
    print("********************************************")
    for item in baseball_list:
        avg_list.append(item.avg)

    for avg in set(avg_list):
        salary_sum = 0
        player_count = 0
        for record in baseball_list:
            if record.avg == avg:
                salary_sum+= record.salary
                player_count+=1
        print(avg,":",round(salary_sum/player_count,3))

    print("********************************************")


    stock_stat_path = 'StockValuations.csv'
    stock_stat_list = []
    if not os.path.exists(stock_stat_path):
        print(stock_stat_path, " is an invalid file path")
    else:
        stock_stat_list = read_csv.StocksCSVReader(stock_stat_path).load()

    StockStatsDAO('stocks.db').insert_records(stock_stat_list)
    stocks_list = StockStatsDAO('stocks.db').select_all()
    country_list = []

    print("********************************************")
    print("Number of tickers per country code:")
    print("********************************************")

    for item in stocks_list:
        country_list.append(item.exchange_country)

    for country in set(country_list):
        print(country,':',country_list.count(country))

    print("********************************************")


