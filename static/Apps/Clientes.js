$(function() {
    'use strinct';
    $("#form-registro-clientes").on('submit',function (event) {
        var post_url = $("#form-registro-clientes").data('post-url');
        var form_data = new FormData(this);
        if ($("#ruc").hasClass('parsley-error')) {
            event.preventDefault();
        }
        else
        {
            $.ajax({
                url: post_url,
                type: 'POST',
                data: form_data,
                processData: false,
                contentType: false,
                success: function (response) {
                    alert(response);
                    $("#Alerta").html("<p>"+response+"</p>")
                },
            });
        return false;
        }
    });

});