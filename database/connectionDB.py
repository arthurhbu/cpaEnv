from pymongo import (
    MongoClient,
    errors)
from database.pythonMongoConfig import read_db_config

def connection(db_config):
    """
    Realiza a conexão com o banco de dados

    :param db_config: contém informações do host e usuário para realizar a conexão
    :type db_config: Dict
    :return: Retorna o MongoClient 
    :rtype: MongoClient
    """
    try:
        print("Connecting to mongoDB database...")
        Mclient = MongoClient(
        db_config['host'],
        username=db_config['username'],
        password=db_config['password']
    )
    except errors as err:
        return print(err)
    return Mclient

def connectToDatabase(databaseName):
    db_config = read_db_config()
    client = connection(db_config)
    print("Connection Established with MongoDB")
    filterDBName = databaseName.replace(" ", "")
    filterDBName = filterDBName.replace(".csv", "")
    database = client[filterDBName]

    return database