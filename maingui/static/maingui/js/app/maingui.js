function logout(){
    if(!singleOperationRestriction){
        singleOperationRestriction = true;
        $.ajax({
            url: logout_url,
            method: 'POST',
            async: false,
            dataType: 'json',
            data: {},
            beforeSend: function(){},
            success: function(result){
                if(result.success){
                    $(location).attr('href', login_url);
                }
                else{
                    SoftNotification.show("Error: Probablemente no deberias de ver este mensaje", "danger");
                }
            },
            error: function (result, request, status, error){
                SoftNotification.show("Error: Hubo un error o no hay conexión con el servidor", "danger");
            },
            complete: function(){
                singleOperationRestriction=false     
            },
        });
    }
}