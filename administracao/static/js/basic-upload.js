$(function () {
    $("#novo-arquivo").click(function () {
        $('#modal-progress').modal('toggle');
    });

    $(".js-upload-photos").click(function () {
        if ($('#gallery tbody tr').length + 1 <= 12) {
            $("#fileupload").click();
        }
        else {
            alert("Não é possível submeter mais que 12 arquivos");
        }
    });

    $("#fileupload").fileupload({
        dataType: 'json',
        sequentialUploads: true, /* 1. SEND THE FILES ONE BY ONE */
        acceptFileTypes: /(\.|\/)(txt)$/i,
        start: function (e) {  /* 2. WHEN THE UPLOADING PROCESS STARTS, SHOW THE MODAL */
            $("#modal-progress").modal("show");
        },
        stop: function (e) {  /* 3. WHEN THE UPLOADING PROCESS FINALIZE, HIDE THE MODAL */
            $('#modal-progress').modal('hide');
        },
        progressall: function (e, data) {  /* 4. UPDATE THE PROGRESS BAR */
            let progress = parseInt(data.loaded / data.total * 100, 10);
            let strProgress = progress + "%";
            $(".progress-bar").css({"width": strProgress});
            $(".progress-bar").text(strProgress);
        },
        done: function (e, data) {
            if (data.result.is_valid) {
                if ($('#gallery tbody tr').length == 1 && $('#gallery tr:last').attr('id') == "empty") {
                    $('#gallery tr:last').remove();
                }
                $("#gallery tbody").prepend(
                    "<tr><td><a href='" + data.result.url + "'>" + data.result.name + "</a></td></tr>"
                );
            }
        }

    });

    $(".confirm").click(function(event) {
        event.preventDefault();

        if (confirm("Deseja realmente continuar?")) {
            window.location.href = $(this).attr("href");
        }
    });
});