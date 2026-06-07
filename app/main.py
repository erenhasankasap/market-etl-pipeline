import os
import sqlalchemy
from sqlalchemy import create_engine, text, Column, Integer, String, Float, Date, BigInteger
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import OperationalError

db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")

db_host = "postgres"
db_port = "5432"

connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(connection_string)

print("Connecting to the database...")

try:
    with engine.connect() as connection: #Secure pipelines
        result = connection.execute(text("SELECT 1;")) #Test query to check connection
        pong = result.scalar()
        if pong == 1:
            print("Successfully connected to the database!")
except OperationalError as e:
    print(f"Failed to connect to the database: {e}")


base = declarative_base()  #Base class for ORM models

class MarketData(base):
    __tablename__ = "market_data"
    
    # Rows of table
    id = Column(Integer, primary_key=True, autoincrement=True, index=True) #Unique identifier for each record
    ticker = Column(String, nullable=False, index=True) #Symbol of the stock
    date = Column(Date, nullable=False, index=True) #Date of the market data
    open_price = Column(Float, nullable=False) #Opening price of the stock
    high_price = Column(Float, nullable=False) #Highest price of the stock
    low_price = Column(Float, nullable=False) #Lowest price of the stock
    close_price = Column(Float, nullable=False) #Closing price of the stock
    volume = Column(BigInteger, nullable=False) #Volume of stocks traded


print("Database schema defined successfully!")

