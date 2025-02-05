import re
import psycopg2

# PostgreSQL Connection Config
DB_CONFIG = {
    "dbname": "trade_logs",
    "user": "trade_user",
    "password": "securepassword",
    "host": "localhost",
    "port": "5432"
}

# FIX message pattern
FIX_PATTERN = r"11=(?P<order_id>\d+).*?55=(?P<symbol>\w+).*?44=(?P<price>[\d.]+).*?39=(?P<status>\d+)"

FIX_STATUS = {
    "0": "New",
    "1": "Partially Filled",
    "2": "Filled",
    "4": "Canceled",
    "8": "Rejected"
}

def parse_fix_log(file_path):
    trade_data = []
    with open(file_path, "r") as file:
        for line in file:
            match = re.search(FIX_PATTERN, line.replace("|", " "))
            if match:
                order_id = match.group("order_id")
                symbol = match.group("symbol")
                price = float(match.group("price"))
                status = FIX_STATUS.get(match.group("status"), "Unknown")

                if status == "Rejected":
                    print(f"⚠️ ALERT: Order {order_id} for {symbol} was REJECTED!")

                trade_data.append((order_id, symbol, price, status))
    
    return trade_data

def save_to_database(trade_data):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        insert_query = """
        INSERT INTO trades (order_id, symbol, price, status)
        VALUES (%s, %s, %s, %s)
        """
        cur.executemany(insert_query, trade_data)
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Trade data saved to PostgreSQL.")
    except Exception as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    trade_log = "sample_fix_log.txt"
    parsed_trades = parse_fix_log(trade_log)
    save_to_database(parsed_trades)

