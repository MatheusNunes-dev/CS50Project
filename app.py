from flask import Flask, render_template, request, redirect, jsonify
import db
import sqlite3
import pandas as pd

app = Flask(__name__)

ALL_DATABASE_COLUMNS = [
    "id",
    "name",
    "Tenure",
    "PreferredLoginDevice",
    "CityTier",
    "WarehouseToHome",	
    "PreferredPaymentMode",	
    "Gender",	
    "HourSpendOnApp",	
    "NumberOfDeviceRegistered",	
    "PreferedOrderCat",  
    "SatisfactionScore",	
    "MaritalStatus",	
    "NumberOfAddress",	
    "Complain",	
    "OrderAmountHikeFromlastYear",	
    "CouponUsed",	
    "OrderCount",	
    "DaySinceLastOrder",	
    "CashbackAmount",
    "email",
    "phone", 
    "prob_churn",
    "pred_churn"
]


USER_INPUT_COLUMNS = [
    "name",
    "Tenure",
    "PreferredLoginDevice",
    "CityTier",
    "WarehouseToHome",	
    "PreferredPaymentMode",	
    "Gender",	
    "HourSpendOnApp",	
    "NumberOfDeviceRegistered",	
    "PreferedOrderCat", 
    "SatisfactionScore",	
    "MaritalStatus",	
    "NumberOfAddress",	
    "Complain",	
    "OrderAmountHikeFromlastYear",	
    "CouponUsed",	
    "OrderCount",	
    "DaySinceLastOrder",	
    "CashbackAmount",
    "email",
    "phone"
]

@app.route("/")
def index():
    display_columns = ["id", "name", "Tenure", "SatisfactionScore", "pred_churn"]
    client_records = db.search_clients()
    clients_data = [dict(zip(display_columns, client)) for client in client_records]
    return render_template("index.html", clients=clients_data)

@app.route("/register_client", methods=['GET', 'POST'])
def register_client():
    form_data = {field: request.form.get(field) for field in USER_INPUT_COLUMNS}
    db.insert_client(form_data)
    print(form_data)
    return redirect("/")

@app.route("/update_client_details", methods=["GET","POST"])
def update_client_details():
    form_data = {field: request.form.get(field) for field in ALL_DATABASE_COLUMNS}
    client_id = form_data["id"]
    form_data.pop("id")
    db.update_client_details(client_id, form_data)
    return redirect("/")

@app.route("/details_client", methods=["GET", "POST"])
def show_client_details():
    client_id = request.args.get("id_client")
    client_details = db.get_client_details(client_id)
    client_data = dict(zip(ALL_DATABASE_COLUMNS, client_details[0]))
    return render_template("details_client.html", details=client_data)

@app.route("/delete_all_clients", methods=["GET", "POST"])
def delete_all_clients():
    db.delete_all_clients()
    return redirect("/")

@app.route("/upload_dataframe", methods=["GET", "POST"])
def upload_excel_file():
    if request.method == "POST":
        uploaded_file = request.files["df_file"]
        dataframe = pd.read_excel(uploaded_file, engine='openpyxl')
        db.insert_dataframe(dataframe)
    return redirect("/")

@app.route("/delete_client", methods=["GET", "POST"])
def delete_single_client():
    client_id = request.form.get("id_delete")
    db.delete_client(client_id)
    return redirect("/")

@app.route('/client_registration')
def show_client_registration():
    return render_template('client_registration.html')

@app.route('/churn_analysis')
def show_churn_analysis():
    churn_display_columns = ["name", "email", "phone", "prob_churn"]
    total_clients_count, predicted_churn_count = db.predict_churn_statistics()
    high_risk_clients = db.get_high_risk_clients()
    high_risk_clients_data = [dict(zip(churn_display_columns, client)) for client in high_risk_clients]
    print(high_risk_clients_data)
    return render_template("churn.html", 
                         total_clients=total_clients_count, 
                         churn_predicts=predicted_churn_count,
                         clients_high_proba_list=high_risk_clients_data)

@app.route("/city_churn_data")
def get_city_churn_data():
    tier1_churn, tier2_churn, tier3_churn = db.get_city_churn_statistics()
    city_churn_counts = [tier3_churn, tier2_churn, tier1_churn]
    return jsonify({'values': city_churn_counts})

if __name__ == '__main__':
    app.run()