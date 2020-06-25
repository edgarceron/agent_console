var id;
var listing_url;
var errorFields = [];
var singleOperationRestriction = false;

function getValues(){
    
    var data = {
        'nombres': $('#nombresInput').val(),
        'primer_apellido': $('#primer_apellidoInput').val(),
        'segundo_apellido': $('#segundo_apellidoInput').val(),
        'fecha_nacimiento': $('#fecha_nacimientoInput').val(),
        'tipo_documento': $('#tipo_documentoInput').val(),
        'identificacion': $('#identificacionInput').val(),
        'telefono': $('#telefonoInput').val(),
        'email': $('#emailInput').val(),
        'direccion': $('#direccionInput').val(),
        'departamento': $('#departamentoInput').val(),
        'barrio': $('#barrioInput').val(),
        'municipio': $('#municipioInput').val(),
        'tipo_servicio':  $('#tipo_servicioInput').val(),
    }
    return data;
}

function addData(){
    if(!singleOperationRestriction){
        singleOperationRestriction = true;
        $.ajax({
            url: add_url,
            method: "POST",
            async: false,
            dataType: "json",
            data: getValues(),
            beforeSend: function(){

            },
            success: function(result){
                if(result.success){
                    FormFunctions.resetFormErrors(errorFields);
                    errorFields = [];
                    $('#successModal').modal('toggle');
                    $('#successModal').modal({backdrop:'static', keyboard:false}); 
                    setTimeout(function(){ 
                        $(location).attr('href', listing_url);
                    }, 2000);
                }
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

function updateData(profile_id){
    $.ajax({
        url: replace_url + profile_id,
        method: 'PUT',
        async: false,
        dataType: 'json',
        data: getValues(),
        beforeSend: function(){},
        success: function(result){
            if(result.success){
                FormFunctions.resetFormErrors(errorFields);
                errorFields = [];
                $('#successModal').modal('toggle');
                $('#successModal').modal({backdrop:'static', keyboard:false}); 
                setTimeout(function(){ 
                    $(location).attr('href', listing_url);
                }, 2000);
            }
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

function getData(datos_id){
    $.ajax({
        url: get_url + datos_id,
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
                setValue(input, data[keys[field]])
            }
            var actions = result.actions;
            loadActionCheboxes(actions);
        },
        error: function (request, status, error){},
        complete: function(){},
    });
}

function setValue(input, value){
    if(typeof(value) == 'boolean'){
        input.prop("checked", value);
    }
    else{
        input.val(value);
    }
}


function saveFunction(){
    if(id == 0){
        addData();
    }
    else{
        updateData(id);
    }
}

function loadActionCheboxes(actions){
    actions.forEach(element => {
        var action = element.action;
        var permission = element.permission;
        var element_id = "#actionInput" + action;
        $(element_id).prop('checked', permission);
    });
}

$( document ).ready(function() {
    $('#saveButton').click(function(){
        saveFunction();
    });
});