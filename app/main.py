import os
import sqlalchemy
import yfinance as yf
from sqlalchemy import create_engine, text, Column, Integer, String, Float, Date, BigInteger
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import OperationalError

db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")

db_host = "postgres"
db_port = "5432"

connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(connection_string)

print("Connecting to the database...")

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

base.metadata.create_all(engine) #Create tables in the database based on the defined models

try:
    with engine.connect() as connection: #Secure pipelines
        result = connection.execute(text("SELECT 1;")) #Test query to check connection
        pong = result.scalar()
        if pong == 1:
            print("Successfully connected to the database!")
except OperationalError as e:
    print(f"Failed to connect to the database: {e}")


# ---ETL: Extract, Transform, Load; Extract Phase---

ticker_symbol = "AAPL"
print(f"Extracting market data for {ticker_symbol}...")
df = yf.download(ticker_symbol, period='5d') #Download historical market data for Apple Inc. from Yahoo Finance
df.columns = df.columns.get_level_values(0) #Flatten the column index if it is a MultiIndex
print(f"Extracted {len(df)} rows of market data for {ticker_symbol}.")
print("\n Data that extracted:")
print(df)

print("Database tables created successfully!")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #Create a session factory for database interactions

session = SessionLocal() #Create a new session for database operations

print("---ETL: Extract, Transform, Load; Transform and Load Phase---")

try:
    for index, row in df.iterrows(): #Iterate through each row of the DataFrame
        market_data_record = MarketData(
            ticker=ticker_symbol,
            date=index.date(),
            open_price=float(row["Open"]),
            high_price=float(row["High"]),
            low_price=float(row["Low"]),
            close_price=float(row["Close"]),
            volume=int(row["Volume"])
        ) #Create a new MarketData object for each row of data
        session.add(market_data_record) #Add the MarketData object to the session for insertion into the database


    session.commit() #Commit the transaction to save changes to the database
    print("Market data loaded into the database successfully!")

except Exception as e:
    session.rollback() #Rollback the transaction in case of an error
    print(f"Failed to load market data into the database: {e}")

finally:
    session.close() #Close the session to free up resources

