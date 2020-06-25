function deleteUser(user_id){
    if(!singleOperationRestriction){
        singleOperationRestriction = true;
        $.ajax({
            url: delete_url + user_id,
            method: 'DELETE',
            async: false,
            dataType: 'json',
            data: {},
            beforeSend: function(){},
            success: function(result){
                $('#modalMessage').html("El usuario ha sido eliminado con exito");
                $('#successModal').modal('toggle');
                $('#successModal').modal({backdrop:'static', keyboard:false}); 
                setTimeout(function(){ 
                    location.reload();
                }, 2000);
            },
            error: function (result, request, status, error){},
            complete: function(){
                singleOperationRestriction=false
            },
        });
    }
}

function deleteConfirmation(user_id){
    $('#confirm_button').click(function(){
        deleteUser(user_id);
    });
    $('#idi').html(user_id);
    $('#cautionModal').modal('toggle');
}

function toogleUserState(user_id, square_element){
    if(!singleOperationRestriction){
        singleOperationRestriction = true;
        $.ajax({
            url: toggle_url + user_id,
            method: 'POST',
            async: false,
            dataType: 'json',
            data: {},
            beforeSend: function(){},
            success: function(result){
                if(result.success){
                    if(square_element.hasClass('fa-square')){
                        square_element.removeClass('fa-square');
                        square_element.addClass('fa-check-square');
                        SoftNotification.show("Usuario activado con exito");
                    }
                    else if(square_element.hasClass('fa-check-square')){
                        square_element.removeClass('fa-check-square');
                        square_element.addClass('fa-square');
                        SoftNotification.show("Usuario desactivado con exito");
                    }
                }
            },
            error: function (result, request, status, error){},
            complete: function(){
                singleOperationRestriction=false
            },
        });
    }
}

$(document).ready(function() {
    var table = $('#listing').dataTable( {
        "processing": true,
        "serverSide": true,
        "ajax": {
            "type": "POST",
            "processing": true,
            "url": url,
            "dataSrc": "data"
        },

        "createdRow": function ( row, data, index ) {
            var jqobj = $(row);
            for(var i = 0;i < 4;i++){
                $('td', row).eq(i).addClass("row_object_id");
                $('td', row).eq(i).attr('user_id', data.id);
            }
            $('td', row).eq(4).attr('user_id', data.id);
            
            if(data.active){
                $('.fa-square', row).addClass('fa-check-square');
                $('.fa-square', row).removeClass('fa-square');
            }
        },

        "columns": [
            { "data": "id" },
            { "data": "username" },
            { "data": "name" },
            { "data": "lastname" },
            { "data": function(){
                var options = '<i class="fas fa-fw fa-trash text-danger"></i>';
                options += '<i class="far fa-fw fa-square text-primary"></i>';
                return options;
            }}
        ], 

        "lengthMenu": [[3, 10, 25, 50], [3, 10, 25, 50]],

        "drawCallback": function( settings ) {
            $('.row_object_id').dblclick(function(event){
                var target = $(event.delegateTarget);
                var id = target.attr('user_id');
                window.location = update_url + id;
            });

            $('.fa-trash, .fa-square, .fa-check-square').click(function(event){
                var target = event.target;
                var parent = target.parentElement;
                parent = $(parent);
                target = $(target);
                var user_id = parent.attr('user_id');
                if(target.hasClass('fa-trash')){
                    deleteConfirmation(user_id);
                }
                else if(target.hasClass('fa-square') || target.hasClass('fa-check-square')){
                    toogleUserState(user_id, target);
                }
            });

            $('.row_object_id').css('cursor', 'pointer'); 

            $(function () {
                $('[data-toggle="popover"]').popover()
            });
        }
    });

    $('#listing tbody').on( 'click', 'tr', function () {
        $(this).toggleClass('selected');
    });
} );