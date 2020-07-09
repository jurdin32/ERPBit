function Tablas(idTabla) {
    var table=$(idTabla).dataTable({
        dom: 'flirtBp',
        // "dom": '<"top"i>rt<"bottom"flp><"clear">',
        paging: true,
        searching: true,
        select: true,

        lengthMenu: [
            [50, 100, 150, -1, 5, 10, 15, 20, 25 ],
            ['50', '100', '150', 'Todos','5','10','15','20', '25'],
        ],
        buttons: [
                'copyHtml5',
                'excelHtml5',
                'csvHtml5',
                'pdfHtml5','print',
        ],
        autoFill: true,
        language: {
            "sProcessing": "Procesando...",
            "sLengthMenu": "Mostrar _MENU_ registros",
            "sZeroRecords": "No se encontraron resultados",
            "sEmptyTable": "Ningun dato disponible en esta tabla",
            "sInfo": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
            "sInfoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
            "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
            "sInfoPostFix": "",
            "sSearch": "Buscar: ",
            "sUrl": "",
            "sInfoThousands": ",",
            "sLoadingRecords": "Cargando...",
            "oPaginate": {
                "sFirst": "Pri.",
                "sLast": "Ult.",
                "sNext": "Sig.",
                "sPrevious": "Ant."
            },
            "oAria": {
                "sSortAscending": ": Activar para ordenar la columna de manera ascendente",
                "sSortDescending": ": Activar para ordenar la columna de manera descendente"
            }
        }

    });
    $('input').css('border-radius', '5px');
    $('select').css('border-radius', '5px');
}

function Tablas2(idTabla,leng) {
    var table=$(idTabla).dataTable({
        dom: 'flirtp',
        // "dom": '<"top"i>rt<"bottom"flp><"clear">',
        paging: true,
        searching: true,
        select: true,

        lengthMenu:leng,
        autoFill: true,
        language: {
            "sProcessing": "Procesando...",
            "sLengthMenu": "Mostrar _MENU_ registros",
            "sZeroRecords": "No se encontraron resultados",
            "sEmptyTable": "Ningun dato disponible en esta tabla",
            "sInfo": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
            "sInfoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
            "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
            "sInfoPostFix": "",
            "sSearch": "Buscar: ",
            "sUrl": "",
            "sInfoThousands": ",",
            "sLoadingRecords": "Cargando...",
            "oPaginate": {
                "sFirst": "Pri.",
                "sLast": "Ult.",
                "sNext": "Sig.",
                "sPrevious": "Ant."
            },
            "oAria": {
                "sSortAscending": ": Activar para ordenar la columna de manera ascendente",
                "sSortDescending": ": Activar para ordenar la columna de manera descendente"
            }
        }

    });
    $('input').css('border-radius', '5px');
    $('select').css('border-radius', '5px');
}