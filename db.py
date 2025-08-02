import sqlite3
import pandas as pd
import numpy as np
from joblib import load
from typing import Dict, List, Tuple, Optional

DATABASE_PATH = "database.db"
TABLE_NAME = "Clientes"
MODEL_PATH = "ecommerce_pipeline.pkl"

model_data = pd.read_pickle(MODEL_PATH)
pipeline_model = model_data["Model"]
model_features = model_data["features"]




ML_FEATURE_COLUMNS = [
    "Tenure", "PreferredLoginDevice", "CityTier", "WarehouseToHome",
    "PreferredPaymentMode", "Gender", "HourSpendOnApp", "NumberOfDeviceRegistered",
    "PreferedOrderCat", "SatisfactionScore", "MaritalStatus", "NumberOfAddress",
    "Complain", "OrderAmountHikeFromlastYear", "CouponUsed", "OrderCount",
    "DaySinceLastOrder", "CashbackAmount"
]


def get_database_connection():
    return sqlite3.connect(DATABASE_PATH)

def search_clients() -> List[Tuple]:
    query = """
        SELECT id, name, Tenure, SatisfactionScore, pred_churn 
        FROM Clientes 
    """
    try:
        with get_database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()
    except sqlite3.Error:
        return []

def insert_client(client_data: Dict) -> bool:
    try:
        churn_prediction, churn_probability = predict_churn(client_data)
        
        query = """
            INSERT INTO Clientes (
                name, Tenure, PreferredLoginDevice, CityTier, WarehouseToHome, 
                PreferredPaymentMode, Gender, HourSpendOnApp, NumberOfDeviceRegistered, 
                PreferedOrderCat, SatisfactionScore, MaritalStatus, NumberOfAddress, 
                Complain, OrderAmountHikeFromlastYear, CouponUsed, OrderCount,
                DaySinceLastOrder, CashbackAmount, email, phone, prob_churn, pred_churn
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        

        values = (
            client_data['name'],                                    
            int(client_data['Tenure']),                            
            client_data['PreferredLoginDevice'],                   
            int(client_data['CityTier']),                          
            int(client_data['WarehouseToHome']),                   
            client_data['PreferredPaymentMode'],                   
            client_data['Gender'],                                 
            int(client_data['HourSpendOnApp']),                    
            int(client_data['NumberOfDeviceRegistered']),         
            client_data['PreferedOrderCat'],                     
            int(client_data['SatisfactionScore']),                 
            client_data['MaritalStatus'],                       
            int(client_data['NumberOfAddress']),                   
            int(client_data['Complain']),                          
            int(client_data['OrderAmountHikeFromlastYear']),       
            int(client_data['CouponUsed']),                        
            int(client_data['OrderCount']),                        
            int(client_data['DaySinceLastOrder']),                 
            float(client_data['CashbackAmount']),                  
            client_data['email'],                                 
            client_data['phone'],                                  
            churn_probability,                                     
            churn_prediction                                      
        )
        
        with get_database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            return True
            
    except Exception as e:
        print(f"Erro ao inserir cliente: {e}")
        return False



def get_client_details(client_id: int) -> List[Tuple]:
    query = """
        SELECT *
        FROM Clientes 
        WHERE id = ?
    """
    
    try:
        with get_database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (client_id,))
            return cursor.fetchall()
    except sqlite3.Error:
        return []

def delete_all_clients() -> bool:
    try:
        with get_database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {TABLE_NAME}")
            conn.commit()
            return True
    except sqlite3.Error:
        return False

def insert_dataframe(dataframe: pd.DataFrame) -> bool:
    try:
        df_with_predictions = generate_churn_predictions_for_dataframe(dataframe)
        
        with get_database_connection() as conn:
            df_with_predictions.to_sql(TABLE_NAME, conn, if_exists='append', index=False)
            return True
            
    except Exception:
        return False

def delete_client(client_id: int) -> bool:
    try:
        with get_database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE id = ?", (client_id,))
            conn.commit()
            return True
    except sqlite3.Error:
        return False

def update_client_details(client_id: int, updated_data: Dict) -> bool:
    try:
        churn_prediction, churn_probability = predict_churn(updated_data)
        
        query = """
            UPDATE Clientes SET
                name = ?, Tenure = ?, PreferredLoginDevice = ?, CityTier = ?, 
                WarehouseToHome = ?, PreferredPaymentMode = ?, Gender = ?, 
                HourSpendOnApp = ?, NumberOfDeviceRegistered = ?, PreferedOrderCat = ?, 
                SatisfactionScore = ?, MaritalStatus = ?, NumberOfAddress = ?, 
                Complain = ?, OrderAmountHikeFromlastYear = ?, CouponUsed = ?, 
                OrderCount = ?, DaySinceLastOrder = ?, CashbackAmount = ?,
                email = ?, phone = ?, prob_churn = ?, pred_churn = ?
            WHERE id = ?
        """
        
        values = (
            updated_data['name'],
            updated_data['Tenure'],
            updated_data['PreferredLoginDevice'],
            updated_data['CityTier'],
            updated_data['WarehouseToHome'],
            updated_data['PreferredPaymentMode'],
            updated_data['Gender'],
            updated_data['HourSpendOnApp'],
            updated_data['NumberOfDeviceRegistered'],
            updated_data['PreferedOrderCat'],
            updated_data['SatisfactionScore'],
            updated_data['MaritalStatus'],
            updated_data['NumberOfAddress'],
            updated_data['Complain'],
            updated_data['OrderAmountHikeFromlastYear'],
            updated_data['CouponUsed'],
            updated_data['OrderCount'],
            updated_data['DaySinceLastOrder'],
            updated_data['CashbackAmount'],
            updated_data['email'],
            updated_data['phone'],
            churn_probability,
            churn_prediction,
            client_id
        )
        
        with get_database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            return True
            
    except Exception:
        return False

def predict_churn(client_data: Dict) -> Tuple[int, float]:
    try:
        prediction_data = {
            feature: [client_data[feature]] 
            for feature in model_features
        }
        
        df = pd.DataFrame(prediction_data)
        df.head()
        probability_scores = pipeline_model.predict_proba(df)
        predictions = pipeline_model.predict(df)
        
        churn_prediction = int(predictions[0])
        churn_probability = float(probability_scores[0][1])
        print(churn_prediction, churn_probability)
        return churn_prediction, churn_probability
        
    except Exception:
        return 0, 0.0




def generate_churn_predictions_for_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    try:
        df_with_predictions = dataframe.copy()
        
        predictions = pipeline_model.predict(dataframe[model_features])
        probabilities = pipeline_model.predict_proba(dataframe[model_features])[:, 1]
        
        df_with_predictions["pred_churn"] = predictions
        df_with_predictions["prob_churn"] = probabilities
        df_with_predictions["prob_churn"] = df_with_predictions["prob_churn"].apply(
            lambda x: format(x, ".6f")
        )
        
        return df_with_predictions
        
    except Exception as e:
        raise e

def predict_churn_statistics() -> Tuple[int, int]:
    try:
        with get_database_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute(f"SELECT COUNT(id) FROM {TABLE_NAME}")
            total_clients = cursor.fetchone()[0]
            
            cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE pred_churn = 1")
            churn_predictions = cursor.fetchone()[0]
            
            return total_clients, churn_predictions
            
    except sqlite3.Error:
        return 0, 0

def get_city_churn_statistics() -> Tuple[int, int, int]:
    try:
        with get_database_connection() as conn:
            cursor = conn.cursor()
            
            queries = [
                f"SELECT COUNT(CityTier) FROM {TABLE_NAME} WHERE CityTier = 1 AND pred_churn = 1",
                f"SELECT COUNT(CityTier) FROM {TABLE_NAME} WHERE CityTier = 2 AND pred_churn = 1",
                f"SELECT COUNT(CityTier) FROM {TABLE_NAME} WHERE CityTier = 3 AND pred_churn = 1"
            ]
            
            results = []
            for query in queries:
                cursor.execute(query)
                results.append(cursor.fetchone()[0])
            
            return tuple(results)
            
    except sqlite3.Error:
        return 0, 0, 0

def get_high_risk_clients(limit: int = 10) -> List[Tuple]:
    query = f"""
        SELECT name, email, phone, prob_churn 
        FROM {TABLE_NAME} 
        ORDER BY prob_churn DESC 
        LIMIT ?
    """
    
    try:
        with get_database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (limit,))
            return cursor.fetchall()
    except sqlite3.Error:
        return []