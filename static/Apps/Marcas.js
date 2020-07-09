$(function() {
    'use strinct';
    $("#form-registro-marcas").on('submit',function (event) {
        var post_url = $("#form-registro-marcas").data('post-url');
        var form_data = new FormData(this);
        if (($("#marca").val().length==0)|| ($("#descripcion").val()==0)) {
            if($("#marca").val().length==0){
                $("#marca").addClass('parsley-error');
            }
            else{
                $("#descripcion").addClass('parsley-error');
            }
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
                    console.log(response);
                    alert(response);
                },
            });
        return false;
        }
    });

});
