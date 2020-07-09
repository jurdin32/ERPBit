$(function() {
    'use strinct';
    $("#form-registro-categorias").on('submit',function (event) {
        var post_url = $("#form-registro-categorias").data('post-url');
        var form_data = new FormData(this);
        if (($("#categoria").val().length==0)|| ($("#descripcion").val()==0))
        {
            if($("#categoria").val().length==0){
                $("#categoria").addClass('parsley-error');
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
                    alert(response);
                },
            });
        return false;
        }
    });
});
