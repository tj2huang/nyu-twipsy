import mysql.connector

from __private import dc_sql_connect


class DataAccess:
    @staticmethod
    def _execute(query_str):
        con = mysql.connector.connect(**dc_sql_connect)
        cur = con.cursor()
        try:
            cur.execute('SET NAMES utf8mb4')
            cur.execute(query_str)
        except mysql.connector.Error as e:
            print(e)
        finally:
            con.close()

    @staticmethod
    def create_table(table_name):
        DataAccess._execute(
            '''CREATE TABLE {} (
            date DATETIME, tweet_id VARCHAR(20), text VARCHAR(1000), lat VARCHAR(20), lon VARCHAR(20),
            label_id INT, predict_id INT);
            '''.format(table_name))

    @staticmethod
    def insert_from_df(df):
        """
        Inserts all the rows of the dataframe into database without labels or prediction
        :param df: pd.DataFrame
        """
        _columns = ['text', 'id', 'created_at', 'lat', 'lon']
        query_vars = dict()
        for index, row in df.iterrows():
            for key in _columns:
                query_vars[key] = row[key] if key in df else 'NULL'
        DataAccess._execute('''INSERT INTO uploaded_tweets (text, tweet_id, date, lat, lon) VALUES ("{}","{}","{}","{}","{}")'''.format(*[query_vars[key] for key in _columns]))
