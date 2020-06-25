function isValidEmail(email){
    var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
    if (reg.test(email) == false) 
    {
        return false;
    }
    return true;
}

function getValues(){

    var username = $('#inputEmail').val();
    if (!isValidEmail(username)){
        username = username + "@call.center";
    }
    var data = {
        "username"    : username,
        "password"    : $('#inputPassword').val(),
        "rememberMe"  : $('#inputRemember').prop('checked')
    }
    return data;
}

function login(){
    if(!singleOperationRestriction){
        singleOperationRestriction = true;
        $.ajax({
            url: login_url,
            method: 'POST',
            async: false,
            dataType: 'json',
            data: getValues(),
            beforeSend: function(){},
            success: function(result){
                if(result.success){
                    $(location).attr('href', index_url);
                }
                else{
                    SoftNotification.show("Error: " + result.message, "danger");
                }
            },
            error: function (result, request, status, error){
                SoftNotification.show("Error: No hay conexión o hubo un fallo en el servidor");
            },
            complete: function(){
                singleOperationRestriction=false
            },
        });
    }
}

$( document ).ready(function() {
    $('#ingresar').click(function(event){
        event.preventDefault();
        login();
    });

    $(window).keydown(function(event){
        if(event.keyCode == 13) {
            event.preventDefault();
            login();
        }
    });
});