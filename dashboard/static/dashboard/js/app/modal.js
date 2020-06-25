var repeat;
var id;
var update_url;
function getTextData(datos_id){
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
                var inputName = "#" + keys[field] + "Text";
                var input = $(inputName);
                setValue(input, data[keys[field]])
            }
        },
        error: function (request, status, error){},
        complete: function(){},
    });
}

function getLlamadas(){
    $.ajax({
        url: get_llamadas_url,
        method: 'POST',
        async: false,
        dataType: 'json',
        data: {},
        beforeSend: function(){},
        success: function(result){
            if(result.phone !== null){
                $("#phoneText").html(result.phone);
                $("#phoneText2").html(result.phone);
                repeat = false;
                if(result.data !== null){
                    var data = result.data;
                    var keys = Object.keys(data);
                    update_url = update_url + data['id'];
                    for(field in keys){
                        var inputName = "#" + keys[field] + "Text";
                        var input = $(inputName);
                        setValue(input, data[keys[field]]);
                        
                        $('#successModal').modal('toggle');
                        $('#successModal').modal({backdrop:'static', keyboard:false}); 
                    }
                }
                else{
                    $('newModal').modal('toggle');
                    $('#newModal').modal({backdrop:'static', keyboard:false}); 
                }
            }
        },
        error: function (request, status, error){},
        complete: function(){},
    });
}

function buscarCedula(){
    $.ajax({
        url: get_cedula_url,
        method: 'POST',
        async: false,
        dataType: 'json',
        data: {
            'cedula':$('#cedulaInput').val()
        },
        beforeSend: function(){},
        success: function(result){
            $('#newModal').modal('hide');
            repeat = false;
            if(result.data !== null){
                var data = result.data;
                var keys = Object.keys(data);
                update_url = update_url + data['id'];
                for(field in keys){
                    var inputName = "#" + keys[field] + "Text";
                    var input = $(inputName);
                    setValue(input, data[keys[field]]);
                    
                    $('#successModal').modal('toggle');
                    $('#successModal').modal({backdrop:'static', keyboard:false}); 
                }
            }
            else{
                alert("No hay datos para esta cedula");
                $('newModal').modal('toggle');
                $('#newModal').modal({backdrop:'static', keyboard:false}); 
            }
            
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
        input.html(value);
    }
}