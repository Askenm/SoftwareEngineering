"""
The purpose of this is to write all the functionality required to edit the main database
"""
from sqlalchemy import create_engine, text
import pandas as pd


query_catalog = {'init':{"create_tournament_table":"""CREATE TABLE ckb.tournaments (
                                                        tid SERIAL PRIMARY KEY,
                                                        tournament_name VARCHAR(255) NOT NULL,
                                                        creator VARCHAR(255),
                                                        create_date DATE DEFAULT CURRENT_DATE,
                                                        end_date DATE DEFAULT NULL
                                                        );""",
                         "create_battle_table":"""CREATE TABLE ckb.battles (
                                                        bid SERIAL PRIMARY KEY,
                                                        battle_name VARCHAR(255) NOT NULL,
                                                        tournament_id INT,
                                                        github_repo VARCHAR(255) NOT NULL,
                                                        creator VARCHAR(255),
                                                        create_date DATE DEFAULT CURRENT_DATE,
                                                        end_date DATE
                                                        );"""
                        },
                 'write':{},
                 'read':{}}


class DBMS():
    def __init__(self):
        user="ckbAdmin"
        password="CodeKataBattles$"
        host="ckb.postgres.database.azure.com"
        port=5432
        database="postgres"
        DBMS_connection_string = 'postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, database)

        self.engine = create_engine(DBMS_connection_string)


    def DDL(self):
        for query_name,query in query_catalog['init'].items():
            print(f'EXECUTING {query_name}')
            with self.engine.connect() as connection:
                query = text(query)
                connection.execute(query)
        

    def write(self,data,table):
        pass

    def read(self,query):
        
        dataDF = pd.read_sql(query, self.engine)

        return dataDF



