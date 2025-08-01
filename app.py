from flask import Flask, render_template, request, redirect, jsonify
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
    keys_list = ["id", "name", "Tenure", "SatisfactionScore", "pred_churn" ]
    clients_list = []
    clients = db.search_clients()
    print(clients)
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


@app.route('/client_registration')
def client_registration():
    return render_template('client_registration.html')


@app.route('/churn')
def info_churn():
    keys_dict = ["name", "email", "phone", "prob_churn"]
    clients_high_proba_list = []
    total_clients, churn_predicts = db.get_details_churns()
    clients_high_proba = db.get_clients_high_proba()
    for person in clients_high_proba:
        clients_high_proba_dict = {}
        index_key = 0
        for data in person:
            clients_high_proba_dict[keys_dict[index_key]] = data
            index_key += 1
        clients_high_proba_list.append(clients_high_proba_dict)    
        
    return render_template("/churn.html", total_clients = total_clients, churn_predicts = churn_predicts, 
                            clients_high_proba_list = clients_high_proba_list
                            )


@app.route("/city_datas")
def city_datas():
    city_1, city_2, city_3 = db.get_details_city()
    cities = [city_3, city_2, city_1]
    return jsonify({'values' : cities})