import sqlite3

##This method creates a sqllite database with the name as parameter inputed if doesn't exist yet. returns sqllite connection and cursor
def create_db(a_db_name):

    rtn_conn = sqlite3.connect(a_db_name)
    rtn_cursor = rtn_conn.cursor()
    return rtn_conn, rtn_cursor

##Takes sqllite connection, cursor, table name, list of field names with their corresponding types.
##Creates table in database
def createTable(a_connection, a_cursor, a_table_name, list_num_fields):

    creation_str = 'CREATE TABLE ' + a_table_name + ' ('
    for i in range(0, len(list_num_fields) - 1):
        field = list_num_fields[i]
        name = field["name"]
        type = field["type"]
        creation_str+= name + ' ' + type    + ','


    field = list_num_fields[len(list_num_fields)-1]
    name = field["name"]
    type = field["type"]
    creation_str += name + ' ' + type + ')'
    print(creation_str)
    a_cursor.execute(creation_str)
    a_connection.commit() # save changes
    print('table ' + a_table_name + ' created')

##creare baseball schema
a_connection,a_cursor = create_db('baseball.db')
createTable(a_connection,a_cursor,'baseball_stats',[{'name':'name','type':'text'},
                                                    {'name':'games_played','type':'real'},
                                                    {'name':'average','type':'real'},
                                                    {'name':'salary','type':'real'}])
##create stocks schema
a_connection,a_cursor = create_db('stocks.db')
createTable(a_connection,a_cursor,'stock_stats',[{'name':'ticker','type':'text'},
                                                 {'name':'company_name','type':'text'},
                                                 {'name':'country','type':'text'},
                                                 {'name':'price','type':'real'},
                                                 {'name':'exchange_rate', 'type':'real'},
                                                 {'name':'shares_outstanding', 'type': 'real'},
                                                 {'name':'net_income', 'type': 'real'},
                                                 {'name':'market_value', 'type': 'real'},
                                                 {'name':'pe_ratio', 'type': 'real'}])
