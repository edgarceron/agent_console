/**
 * Scripts here may replace things from the users form.js
 */
var user_id; 
function getUserAgentValues(){
    var data = {
        'user': id,
        'agent': $('#agentInput').val()
    }
    return data;
}

saveSuccess = function(result){
    singleOperationRestriction = false;
    if(result.success){
        FormFunctions.resetFormErrors(errorFields);
        errorFields = [];
        id = result.user_id;
        setUserAgent();
    }
}

function setUserAgent(){
    if(!singleOperationRestriction){
        singleOperationRestriction = true;
        $.ajax({
            url: set_user_agent_url,
            method: 'POST',
            async: false,
            dataType: 'json',
            data: getUserAgentValues(),
            beforeSend: function(){},
            success: function(result){
                if(result.success){
                    $('#successModal').modal('toggle');
                    $('#successModal').modal({backdrop:'static', keyboard:false}); 
                    setTimeout(function(){ 
                        $(location).attr('href', listing_url);
                    }, 2000);
                }
                else{
                    SoftNotification.show(result.message, 'danger');
                }
            },
            error: function (result, request, status, error){
                var details = request.responseJSON.Error.details;
                FormFunctions.resetFormErrors(errorFields);
                errorFields = [];
                FormFunctions.setFormErrors(details);
            },
            complete: function(){
                singleOperationRestriction=false
                
            },
        });
    }
}

function getAgentData(id_user){ 
    if(id_user != null){
        $.ajax({
            url: get_agent_url + id_user,
            method: 'POST',
            async: false,
            dataType: 'json',
            success: function(result){
                if(result.success){
                    profile = [result.data];
                    if(profile != null){
                        pickerName = '#agentInput';
                        updatePicker(pickerName, profile);
                    }
                }
            }
        });
    }
}

function updatePickerAgent(pickerName, resultados){
    var input = $(pickerName);
    input.html('');
    var opVal;
    var opText;
    for(let data of resultados){
        opVal = data.id;
        opText = "" + data.number + " " + data.name;
        addOption(input, opVal, opText);
    }
    input.selectpicker("refresh");
}

 $( document ).ready(function() {

    $('#agentInput').selectpicker(
        {
            "liveSearch": true
        }
    );

    if(id != 0){
        getAgentData(id);
    }

    FormFunctions.setAjaxLoadPicker('#agentInput', pircker_search_agent_url, updatePickerAgent);
});