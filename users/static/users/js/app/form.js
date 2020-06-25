//TODO
//Ajax webservice usuarios
var id;
var listing_url;
var errorFields = [];
var singleOperationRestriction = false;

saveSuccess = function(result){
    if(result.success){
        FormFunctions.resetFormErrors(errorFields);
        errorFields = [];
        $('#successModal').modal('toggle');
        $('#successModal').modal({backdrop:'static', keyboard:false}); 
        setTimeout(function(){ 
            $(location).attr('href', listing_url);
        }, 2000);
    }
}

function addData(){
    if(!singleOperationRestriction){
        singleOperationRestriction = true;
        $.ajax({
            url: add_url,
            method: "POST",
            async: false,
            dataType: "json",
            data: {
                "name"    : $('#nameInput').val(),
                "lastname": $('#lastnameInput').val(),
                "username": $('#usernameInput').val(),
                "password": $('#passwordInput').val(),
                "active"  : $('#activeInput').prop('checked'),
                "profile" : $('#profileInput').val()
            },
            beforeSend: function(){

            },
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

function updateData(user_id){
    if(!singleOperationRestriction){
        singleOperationRestriction = true;
        $.ajax({
            url: replace_url + user_id,
            method: 'PUT',
            async: false,
            dataType: 'json',
            data: {
                "name"    : $('#nameInput').val(),
                "lastname": $('#lastnameInput').val(),
                "username": $('#usernameInput').val(),
                "password": $('#passwordInput').val(),
                "active"  : $('#activeInput').prop('checked'),
                "profile" : $('#profileInput').val()
            },
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

function getData(user_id){
    $.ajax({
        url: get_url + user_id,
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
                if(inputName == "#profileInput"){
                    getProfileData(data[keys[field]]);
                }
                FormFunctions.setValue(input, data[keys[field]]);
            }
        },
        error: function (request, status, error){},
        complete: function(){},
    });
}


function saveFunction(){
    if(id == 0){
        addData();
    }
    else{
        updateData(id);
    }
}

function updatePicker(pickerName, resultados){
    var input = $(pickerName);
    input.html('');
    var opVal;
    var opText;
    for(let data of resultados){
        opVal = data.id;
        opText = data.name;
        addOption(input, opVal, opText);
    }
    input.selectpicker("refresh");
}

function addOption(input, val, text){
    var option = `<option value="${val}">${text}</option>`;
    input.append(option);
}

function getProfileData(id_profile){ 
    if(id_profile != null){
        $.ajax({
            url: get_profile_url + id_profile,
            method: 'POST',
            async: false,
            dataType: 'json',
            success: function(result){
                if(result.success){
                    profile = [result.data];
                    if(profile != null){
                        pickerName = '#profileInput';
                        updatePicker(pickerName, profile);
                    }
                }
            }
        });
    }
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

    if(id != 0){
        getData(id);
        $('#passwordInput').attr("placeholder", "Ingrese aquí una nueva contraseña temporal");
    }

    FormFunctions.setAjaxLoadPicker('#profileInput', picker_search_profile_url, updatePicker);
});