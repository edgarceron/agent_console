
function getValues(){
    var values={
        'REDIRECT_TIME':$('#REDIRECT_TIMEInput').val(),
        'CRM_URL':$('#CRM_URLInput').val(),
    }
    return values;
}

function updateData(){
    if(!singleOperationRestriction){
        singleOperationRestriction = true;
        $.ajax({
            url: replace_options_agent_console_url,
            method: 'PUT',
            async: false,
            dataType: 'json',
            data: getValues(),
            beforeSend: function(){},
            success: function(result){
                if(result.success){
                    SoftNotification.show("Opciones guardadas con exito");
                }
            },
            error: function (request, status, error, result){
            },
            complete: function(){
                singleOperationRestriction = false;
            }
        });
    }
}

function getData(user_id){
    $.ajax({
        url: get_options_agent_console_url,
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

function autoGenerateUsers(){
    $.ajax({
        url: auto_generate_users_url,
        method: 'POST',
        async: false,
        dataType: 'json',
        data: {},
        beforeSend: function(){},
        success: function(result){
            if(result.success){
                SoftNotification.show(result.message);
            }
            else{
                SoftNotification.show(result.message, "danger");
            }
        },
        error: function (request, status, error){},
        complete: function(){},
    });
}


$( document ).ready(function() {
    $('#saveButton').click(function(){
        updateData();
    });

    $('#generateButton').click(function(){
        autoGenerateUsers();
    });

    getData();
});