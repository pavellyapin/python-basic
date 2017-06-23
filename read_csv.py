import csv
import os


##List of errors occured, gets nullified after each load of CSV
error_list = []

##Custom class to handle invalid entries in CSV files, as well as parsing errors and division by zero errors
##This class logs error messages in global list
class BadData(Exception):
    def __init__(self,message):
     error_list.append(message)

##This class is the parent class of BaseballStatRecord and StockStatRecord
##contains 1 member : name
class AbstractClass:
    def __init__(self, name):
        self.name = name

##This class is used to make custom objects from CSV rows
##contains name,salary,games_played,avg as members, and has a custom __str__ function
class BaseballStatRecord(AbstractClass):
    def __init__(self, name,salary,games_played,avg):
        self.name = name
        self.salary = salary
        self.games_played = games_played
        self.avg = avg

    def __str__(self):
        output_string = '{name}({salary},{games_played},{avg})'
        return output_string.format(name = self.name,
                                    salary = self.salary,
                                    games_played = self.games_played,
                                    avg = "{:.2f}".format(self.avg) )

##This class is used to make custom objects from CSV rows
##contains name,exchange_country,price,exchange_rate,shares_outstanding,net_income,market_value_usd,pe_ratio as members, and has a custom __str__ function
class StockStatRecord(AbstractClass):
    def __init__(self, name,company_name,exchange_country,price,exchange_rate,shares_outstanding,net_income,market_value_usd,pe_ratio):
        self.name = name
        self.company_name = company_name
        self.exchange_country = exchange_country
        self.price = price
        self.exchange_rate = exchange_rate
        self.shares_outstanding = shares_outstanding
        self.net_income = net_income
        self.market_value_usd = market_value_usd
        self.pe_ratio = pe_ratio


    def __str__(self):
        output_string = '{name}({company_name},{exchange_country},{price},{exchange_rate},{exchange_rate},{shares_outstanding},{net_income},{market_value_usd},{pe_ratio})'
        return output_string.format(name = self.name,
                                    company_name=self.company_name,
                                    exchange_country = self.exchange_country,
                                    price = "{:.2f}".format(self.price),
                                    exchange_rate = "{:.2f}".format(self.exchange_rate),
                                    shares_outstanding = "{:.2f}".format(self.shares_outstanding),
                                    net_income = "{:.2f}".format(self.net_income),
                                    market_value_usd = "{:.2f}".format(self.market_value_usd),
                                    pe_ratio = "{:.2f}".format(self.pe_ratio))

##This class in parent to BaseballCSVReader and StocksCSVReader
##Takes path to CSV file as an initializer
class AbstractCSVReader:
    def __init__(self, path):
        self.path = path

    #This method will be implemented inside child classes
    def row_to_record(self,row):
        raise NotImplementedError

    ##This method returns a list of custom records, depending on which child class in inheriting the parent class
    def load(self):

        output_list = []
        with open(self.path) as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                try:
                 valid_record = self.row_to_record(row)
                 output_list.append(valid_record)
                except BadData:
                    continue

        return output_list


##This class contains functions that allow program to read an CSV file and output a list of BaseballStatRecord
class BaseballCSVReader (AbstractCSVReader):


    def row_to_record(self,row):

        try: #Validate that all columns exists for row and that none are empty
            player_name = row['PLAYER']
            salary = row['SALARY']
            games_played = row['G']
            avg = row['AVG']

            if min(len(player_name),len(salary),len(games_played),len(avg)) < 1:
                raise KeyError
                return
        except KeyError:
            raise BadData('Missing information, can not create record')
            return
        else:
            try: #Validate that floats and integers are in the proper format
                salary = int(salary)
                games_played = int(games_played)
                avg = float(avg)
            except ValueError:
                raise BadData('Can not convert to float or an integer')
            else: #If validation passes return valid record
                return BaseballStatRecord(player_name,salary,games_played,avg)

##This class contains functions that allow program to read an CSV file and output a list of StockStatRecord
class StocksCSVReader (AbstractCSVReader):

    def row_to_record(self,row):

        try:    #Validate that all columns exists for row and that none are empty
            ticker = row['ticker']
            company_name = row['company_name']
            exchange_country = row['exchange_country']
            price = row['price']
            exchange_rate = row['exchange_rate']
            shares_outstanding = row['shares_outstanding']
            net_income = row['net_income']

            if min(len(ticker),len(company_name),len(exchange_country),len(price),len(exchange_rate),len(shares_outstanding),len(net_income)) < 1:
                raise KeyError
                return
        except KeyError:
            raise BadData('Missing information, can not create record')
            return
        else:
            try:#Validate that floats and integers are in the proper format
                price = float(price)
                exchange_rate = float(exchange_rate)
                shares_outstanding = float(shares_outstanding)
                net_income = float(net_income)
            except ValueError:
                raise BadData('Could not parse to float')
                return
            else:
                try:#Validate that program doesn't attempt to divide by zero
                    market_value_usd = price * exchange_rate * shares_outstanding
                    pe_ratio = price * shares_outstanding/net_income
                except ZeroDivisionError:
                    raise BadData('Can not divide by zero, bad data')
                else: #If validation passes return valid record
                    return StockStatRecord(ticker,company_name,exchange_country,price,exchange_rate,shares_outstanding,net_income,market_value_usd,pe_ratio)



if __name__ == "__main__":
    # execute only if run as a script
    baseball_stat_path = 'MLB2008.csv'
    baseball_stat_list = []
    if not os.path.exists(baseball_stat_path):
        print(baseball_stat_path, " is an invalid file path")
    else:
        baseball_stat_list = BaseballCSVReader(baseball_stat_path).load()

    for record in baseball_stat_list:
        print(record)

    print('************************************************')
    print('Number of rows with bad data in ',baseball_stat_path,':', len(error_list))
    print('************************************************')
    error_list = []

    stock_stat_path = 'StockValuations.csv'
    stock_stat_list =[]
    if not os.path.exists(stock_stat_path):
        print(stock_stat_path, " is an invalid file path")
    else:
        stock_stat_list = StocksCSVReader(stock_stat_path).load()

    for record in stock_stat_list:
        print(record)

    print('************************************************')
    print('Number of rows with bad data in ', stock_stat_path, ':', len(error_list))
    print('************************************************')
    error_list = []
