import sqlite3

def search_clients():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, Tenure, SatisfactionScore  FROM Clientes")
        return cursor.fetchall()
    
def insert_client(client_data):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Clientes (
                name, Tenure, PreferredLoginDevice, CityTier, WarehouseToHome, PreferredPaymentMode, Gender,
                HourSpendOnApp, NumberOfDeviceRegistered, PreferedOrderCat, SatisfactionScore, MaritalStatus,
                NumberOfAddress, Complain, OrderAmountHikeFromLastYear, CouponUsed, OrderCount,
                DaySinceLastOrder, CashbackAmount
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, tuple(client_data.values()))
        return 


