from DataPersitenceService import DBMS


DBMS_ = DBMS()

# DBMS_.DDL()

print(DBMS_.read("SELECT * FROM information_schema.tables WHERE table_schema = 'ckb'"))
