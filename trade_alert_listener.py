import psycopg2
import psycopg2.extras
import select

DB_CONFIG = {
    "dbname": "trade_logs",
    "user": "trade_user",
    "password": "securepassword",
    "host": "localhost",
    "port": "5432"
}

# Alert conditions
ALERT_THRESHOLD = 100000  # Example: Alert if trade value > $100,000
REJECTED_STATUS = "Rejected"

def process_trade(trade):
    """Handle trade alert logic."""
    order_id = trade["order_id"]
    symbol = trade["symbol"]
    price = float(trade["price"])
    status = trade["status"]

    print(f"🔔 New Trade Alert: Order {order_id} | {symbol} | ${price} | {status}")

    if status == REJECTED_STATUS:
        print(f"⚠️ ALERT: Order {order_id} for {symbol} was REJECTED!")

    if price >= ALERT_THRESHOLD:
        print(f"🚨 HIGH VALUE TRADE: {symbol} traded at ${price}!")

def listen_for_trades():
    """Listen for new trade notifications."""
    conn = psycopg2.connect(**DB_CONFIG)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Listen for PostgreSQL notifications
    cur.execute("LISTEN new_trade;")
    print("👂 Listening for new trade alerts...")

    try:
        while True:
            if select.select([conn], [], [], 5) == ([], [], []):
                continue
            conn.poll()
            while conn.notifies:
                notify = conn.notifies.pop(0)
                trade = eval(notify.payload)  # Convert JSON string to dict
                process_trade(trade)
    except KeyboardInterrupt:
        print("🛑 Stopping listener...")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    listen_for_trades()

