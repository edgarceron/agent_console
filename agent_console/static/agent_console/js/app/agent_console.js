
function getAgentState(agent, previous_state, previous_call){ 
    if(agent != null){
        $.ajax({
            url: agent_state_url,
            method: 'POST',
            async: true,
            dataType: 'json',
            data: {
                'id_agent': agent,
                'previous_state':previous_state,
                'previous_call':previous_call
            },
            success: function(result){
                if(result.update){
                    $('#lblStatus').html(result.status);
                    $('#lblMessage').html(result.message);
                    previous_state = result.previous;
                    if(result.call){
                        previous_call = result.llamada_id;
                        $('#lblPhone').html(result.phone);
                        $('#lblCedula').html(result.cedula);
                        $('#successModal').modal('show');
                        $('#successModal').modal({backdrop:'static', keyboard:false}); 
                        redirectToCrm(
                            result.cedula,
                            result.phone,
                            result.extension,
                            result.llamada_id);
                        setTimeout(function(){ 
                            $('#successModal').modal('hide');
                            $('#lblPhone').html("");
                            $('#lblCedula').html("");
                        }, 5000);
                    }
                }
            },
            complete: function(){
                setTimeout(function(){ 
                    getAgentState(agent, previous_state, previous_call);
                }, 1000);
            },
        });
    }
    else{
        $('#lblStatus').html("No es agente");
        $('#lblMessage').html("No hay un agente ligado a este usuario");
    }
}

function redirectToCrm(cedula, phone, extension, llamada_id){
    $.ajax({
        url: get_crm_url_url,
        method: 'POST',
        async: false,
        dataType: 'json',
        success: function(result){
            if(result.success){
                var documento = "&documento=" + cedula;
                var telefono = "&telefono=" + phone;
                var ext = "&extension=" + extension;
                var llamada = "&llamada_id=" + llamada_id;
                var url = result.url + documento + telefono + ext + llamada;
				console.log(url);
                setTimeout(function(){ 
                    var win = window.open(url, '_blank');
                    if (win) {
                        win.focus();
                    } else {
                        alert('Por favor permita las ventanas emergentes para esta pagina');
                    }
                    //$(location).attr('href', url);
                }, 2000);
            }
            else{
                SoftNotification.show(result.message, "danger");
            }
        },
        error: function (result, request, status, error){
            SoftNotification.show("Ocurrio un error al intentar la redireccion","danger");
        },
    });
}

$( document ).ready(function() {
    setTimeout(function(){ 
        getAgentState(id_agent, -1, "");
    }, 1000);
});