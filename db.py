import sqlite3
import pandas as pd
import numpy as np
from joblib import load

model = pd.read_pickle("ecommerce_pipeline.pkl")
pipeline_model = model["Model"]
features = model["features"]

def search_clients():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, Tenure, SatisfactionScore  FROM Clientes")
        return cursor.fetchall()
    
def insert_client(client_data):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        predict, proba = get_churn(client_data)
        cursor.execute("""
            INSERT INTO Clientes (
                name, Tenure, PreferredLoginDevice, CityTier, WarehouseToHome, PreferredPaymentMode, Gender,
                HourSpendOnApp, NumberOfDeviceRegistered, PreferedOrderCat, SatisfactionScore, MaritalStatus,
                NumberOfAddress, Complain, OrderAmountHikeFromlastYear, CouponUsed, OrderCount,
                DaySinceLastOrder, CashbackAmount, email, phone, prob_churn, pred_churn
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            client_data['name'],
            client_data['Tenure'],
            client_data['PreferredLoginDevice'],
            client_data['CityTier'],
            client_data['WarehouseToHome'],
            client_data['PreferredPaymentMode'],
            client_data['Gender'],
            client_data['HourSpendOnApp'],
            client_data['NumberOfDeviceRegistered'],
            client_data['PreferedOrderCat'],
            client_data['SatisfactionScore'],
            client_data['MaritalStatus'],
            client_data['NumberOfAddress'],
            client_data['Complain'],
            client_data['OrderAmountHikeFromlastYear'],
            client_data['CouponUsed'],
            client_data['OrderCount'],
            client_data['DaySinceLastOrder'],
            client_data['CashbackAmount'],
            client_data['email'],
            client_data['phone'],
            proba,
            predict
        ))
        conn.commit()


def get_details(id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
                SELECT id, name, Tenure, PreferredLoginDevice, CityTier, WarehouseToHome, PreferredPaymentMode, Gender,
                HourSpendOnApp, NumberOfDeviceRegistered, PreferedOrderCat, SatisfactionScore, MaritalStatus,
                NumberOfAddress, Complain, OrderAmountHikeFromlastYear, CouponUsed, OrderCount,
                DaySinceLastOrder, CashbackAmount, email, phone, prob_churn, pred_churn from Clientes WHERE id = ?;
                       """, (id,))
        return cursor.fetchall()
    

def delete_all_clients():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Clientes")
        conn.commit()
    return

def insert_df(df):
    with sqlite3.connect("database.db") as conn:
        df_db = get_churn_df(df)
        df_db.to_sql('Clientes', conn, if_exists='append', index=False)
    return

def delete_client(id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Clientes WHERE id = ?;", (id,))
        conn.commit()
    return

def update_details(id, client):
    predict, proba = get_churn(client)
    client_data = (
        client["name"], client["Tenure"], client["PreferredLoginDevice"], 
        client["CityTier"], client["WarehouseToHome"], client["PreferredPaymentMode"], 
        client["Gender"], client["HourSpendOnApp"], client["NumberOfDeviceRegistered"], 
        client["PreferedOrderCat"], client["SatisfactionScore"], client["MaritalStatus"], 
        client["NumberOfAddress"], client["Complain"], client["OrderAmountHikeFromlastYear"], 
        client["CouponUsed"], client["OrderCount"], client["DaySinceLastOrder"], 
        client["CashbackAmount"], client["email"], client["phone"], proba, predict, int(id)
    )
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
                UPDATE Clientes
                SET
                    name = ?, 
                    Tenure = ?, 
                    PreferredLoginDevice = ?, 
                    CityTier = ?, 
                    WarehouseToHome = ?, 
                    PreferredPaymentMode = ?, 
                    Gender = ?, 
                    HourSpendOnApp = ?, 
                    NumberOfDeviceRegistered = ?, 
                    PreferedOrderCat = ?, 
                    SatisfactionScore = ?, 
                    MaritalStatus = ?, 
                    NumberOfAddress = ?, 
                    Complain = ?, 
                    OrderAmountHikeFromlastYear = ?, 
                    CouponUsed = ?, 
                    OrderCount = ?, 
                    DaySinceLastOrder = ?, 
                    CashbackAmount = ?,
                    email = ?,
                    phone = ?,
                    prob_churn = ?,
                    pred_churn = ?
                WHERE id = ?;
                """, client_data)
        return
    

def get_churn(datas):
    datas_client = {
            "Tenure": [datas["Tenure"]],
            "PreferredLoginDevice" : [datas["PreferredLoginDevice"]],
            "CityTier" : [datas["CityTier"]],
            "WarehouseToHome" : [datas["WarehouseToHome"]],
            "PreferredPaymentMode" : [datas["PreferredPaymentMode"]],
            "Gender" :	[datas["Gender"]],
            "HourSpendOnApp" : [datas["HourSpendOnApp"]],
            "NumberOfDeviceRegistered" : [datas["NumberOfDeviceRegistered"]],
            "PreferedOrderCat" : [datas["PreferedOrderCat"]],
            "SatisfactionScore" : [datas["SatisfactionScore"]],
            "MaritalStatus" : [datas["MaritalStatus"]],
            "NumberOfAddress" : [datas["NumberOfAddress"]],
            "Complain" : [datas["Complain"]],
            "OrderAmountHikeFromlastYear" : [datas["OrderAmountHikeFromlastYear"]],
            "CouponUsed" : [datas["CouponUsed"]],
            "OrderCount" : [datas["OrderCount"]],
            "DaySinceLastOrder" : [datas["DaySinceLastOrder"]],
            "CashbackAmount" : [datas["CashbackAmount"]]
            }

    df = pd.DataFrame(data = datas_client)
    proba = pipeline_model.predict_proba(df)
    predict = pipeline_model.predict(df)
    predict = int(predict[0])
    proba = proba[0][1]
    return predict, proba


def get_churn_df(df):
    df_db = df.copy()
    predict =  pipeline_model.predict(df[features])
    proba =  pipeline_model.predict_proba(df[features])
    df_db["pred_churn"] = predict[0]
    df_db["prob_churn"] = proba[0][1]
    return df_db
