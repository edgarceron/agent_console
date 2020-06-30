var id;
var errorFields = [];

saveSuccess = function(result){
    if(result.success){
        FormFunctions.resetFormErrors(errorFields);
        errorFields = [];
        SoftNotification.show("Datos actualizados correctamente");
    }
}

function getValues(){
    data = {
        "name"    : $('#nameInput').val(),
        "lastname": $('#lastnameInput').val(),
        "username": $('#usernameInput').val(),
        "password": $('#passwordInput').val(),
        "confirm": $('#passwordConfirmInput').val(),
    }
    return data;
}

function updateData(){
    if(!singleOperationRestriction){
        singleOperationRestriction = true;
        $.ajax({
            url: replace_own_url,
            method: 'PUT',
            async: false,
            dataType: 'json',
            data: getValues(),
            beforeSend: function(){},
            success: function(result){
                saveSuccess(result);
            },
            error: function (request, status, error, result){
                var details = request.responseJSON.Error.details;
                FormFunctions.resetFormErrors(errorFields);
                errorFields = [];
                FormFunctions.setFormErrors(details);
            },
            complete: function(){
                singleOperationRestriction = false;
            }
        });
    }
}

function getData(){
    $.ajax({
        url: get_own_url ,
        method: 'POST',
        async: false,
        dataType: 'json',
        data: {},
        beforeSend: function(){},
        success: function(result){
            var data = result.data;
            var keys = Object.keys(data);
            for(field in keys){
                var inputName = "#" + keys[field] + "Input";
                var input = $(inputName);
                FormFunctions.setValue(input, data[keys[field]]);
            }
        },
        error: function (request, status, error){},
        complete: function(){},
    });
}

function saveFunction(){
    updateData(id);
}

$( document ).ready(function() {
    
    $('#saveButton').click(function(){
        saveFunction();
    });

    $('#profileInput').selectpicker(
        {
            "liveSearch": true
        }
    );


    $('#passwordInput').attr("placeholder", "Ingrese aquí una nueva contraseña");
    $('#passwordConfirmInput').attr("placeholder", "Confirme su nueva contraseña");

    getData();
});