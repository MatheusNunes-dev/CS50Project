function open_register_client(){
    const form = document.querySelector(".register-information")
    const dashboard = document.querySelector(".dashboard")
    const spreadsheet = document.querySelector(".add-spreadsheet")
    form.style.display = "flex" 
    dashboard.style.display = "none"
    spreadsheet.style.display = "none"
}

function back_to_dashboard(){

}

function editDetails(){
    const inputs = document.querySelectorAll("#form-details [disabled]");
    const btnSave = document.querySelector(".btn-saveDetails")
    btnSave.style.display = "block"
    inputs.forEach(input => input.disabled = false);
}