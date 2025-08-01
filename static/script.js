
function back_to_dashboard(){
    
}

function editDetails(){
    const inputs = document.querySelectorAll("#form-details [disabled]");
    const btnSave = document.querySelector(".btn-saveDetails")
    btnSave.style.display = "block"
    inputs.forEach(input => input.disabled = false);
}

function open_client_registration(){
    window.location.href = "/client_registration"
}

function open_home(){
    window.location.href = "/"
}

function open_churn(){
    window.location.href = "/churn"
}
