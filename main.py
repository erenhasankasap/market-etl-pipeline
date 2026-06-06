import os
import sqlalchemy

db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")

db_host = "postgres"
db_port = "5432"

# Güvenli bir şekilde f-string ile URI (Connection String) oluşturuyoruz
connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Şimdilik çalıştığını görmek için ekrana basıyoruz (İleride loglama ekleyeceğiz)
print(f"Bağlantı dizesi başarıyla oluşturuldu: {connection_string}")
