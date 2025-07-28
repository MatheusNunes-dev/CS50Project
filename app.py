from flask import Flask, render_template, request
import db

app = Flask(__name__)


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
    "CashbackAmount"
]

@app.route("/")
def index():
    return render_template("index.html", clients = db.search_clients())


@app.route("/register_client", methods=['GET', 'POST'])
def register_client():
    client_data = {field: request.form.get(field) for field in [
        "name", "Tenure", "PreferredLoginDevice", "CityTier", "WarehouseToHome",
        "PreferredPaymentMode", "Gender", "HourSpendOnApp", "NumberOfDeviceRegistered",
        "PreferedOrderCat", "SatisfactionScore", "MaritalStatus", "NumberOfAddress",
        "Complain", "OrderAmountHikeFromlastYear", "CouponUsed", "OrderCount",
        "DaySinceLastOrder", "CashbackAmount"
    ]}
    db.insert_client(client_data)
    return "NICE!"