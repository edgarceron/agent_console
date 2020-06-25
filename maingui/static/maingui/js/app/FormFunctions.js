class FormFunctions{
    static resetFormErrors(errorFields){
        for (const key in errorFields) {
            if (errorFields.hasOwnProperty(key)) {
                const field = errorFields[key];
                const invalid = "#" + field + "Invalid";
                const input   = "#" + field + "Input";
                $(invalid).html("");
                $(input).removeClass("is-invalid");
            }
        }
    }

    static setFormErrors(details){
        for (var key in details) {
            if (details.hasOwnProperty(key)) {
                const field   = details[key].field;
                errorFields.push(field);
                const message = details[key].message;
                const invalid = "#" + field + "Invalid";
                const input   = "#" + field + "Input";
                $(invalid).html(message);
                $(input).addClass("is-invalid");
            }
        }
    }

    static setAjaxLoadPicker(input, url, updateFunction){
        $(input).siblings().find("input[type='text']").keyup(
            function(event){
                var target = $(event.target);
                var text = target.val();
                if(text.length > 0){
                    $.ajax({
                        url: url,
                        method: 'POST',
                        async: true,
                        dataType: 'json',
                        data: {'value': text},
                        beforeSend: function(){},
                        success: function(result){
                            if(result.success){
                                var resultados = result.result;
                                var pickerName = input;
                                updateFunction(pickerName, resultados);
                            }
                        },
                        error: function (result, request, status, error){
                            SoftNotification.show("Ocurrio un error al cargar el picker " + input, 'danger');
                        },
                        complete: function(){
                            singleOperationRestriction=false
                        },
                    });
                }
            }
        )
    }

    static setValue(input, value){
        if(typeof(value) == 'boolean'){
            input.prop("checked", value);
        }
        else{
            input.val(value);
        }
    }
}