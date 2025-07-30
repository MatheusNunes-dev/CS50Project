from flask import Flask, render_template, request, redirect
import db
import sqlite3
import pandas as pd

app = Flask(__name__)


attributes_db = [
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

attributes = [
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
    keys_list = ["id", "name", "Tenure", "SatisfactionScore"]
    clients_list = []
    clients = db.search_clients()
    for client in clients:
        index_key = 0 
        datas = {}
        for data in client: 
            datas[keys_list[index_key]] = data
            index_key += 1
        clients_list.append(datas)     

    return render_template("index.html", clients = clients_list)


@app.route("/register_client", methods=['GET', 'POST'])
def register_client():
    client_data = {field: request.form.get(field) for field in attributes}
    db.insert_client(client_data)
    return redirect("/")


@app.route("/updateDetails", methods=["GET","POST"])
def updateDetails():
    client_data = {field: request.form.get(field) for field in attributes_db}
    id = client_data["id"]
    client_data.pop("id")
    db.update_details(id, client_data )
    return redirect("/")


@app.route("/datails_client", methods=["GET", "POST"])
def datails_client():
    id_client = request.args.get("id_client")
    details = db.get_details(id_client)
    dict_details = {}
    for tuple in details:
        index_key = 0 
        for data in tuple: 
            dict_details[attributes_db[index_key]] = data
            index_key += 1
    return render_template("details_client.html", details = dict_details)

@app.route("/delete_all_clients", methods=["GET", "POST"])
def delete_all_clients():
    db.delete_all_clients()
    return redirect("/")

@app.route("/upload_df", methods=["GET", "POST"])
def upload_df():
    if request.method == "POST":
        file = request.files["df_file"]
        df =  pd.read_excel(file, engine='openpyxl')
        db.insert_df(df)

    return redirect("/")


@app.route("/delete_client", methods=["GET", "POST"])
def delete_client():
    id = request.form.get("id_delete")
    db.delete_client(id)
    return redirect("/")
