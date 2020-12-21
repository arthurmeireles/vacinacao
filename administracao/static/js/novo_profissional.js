function buscarProfissional(cpf) {
    let cpf_unformat = cpf.replace(/_/g, "").replace(/-/g, "").replace(/\./g, '');
    let url = '/admin/usuarios/buscar/' + cpf_unformat;

    if (cpf_unformat.length === 11) {
        $.ajax({
            url: url,
            context: "application/json",
            success: function (data) {
                if (data.local === 1) {
                    $(".mensagem").html("O <strong>CPF " + cpf + "</strong> está cadastrado no nome de " + data.nome + ". Deseja alterar a senha?");
                    $(".editar").attr("href", "/admin/usuario/" + data.id + "/editar/").css('display', '');
                    $("#profissional-modal").modal({backdrop: 'static', keyboard: true});
                } else if (data.valido === false) {
                    $(".modal-title").html(data.title);
                    $(".mensagem").html(data.text);
                    $("#profissional-modal").modal({backdrop: 'static', keyboard: true});
                    $(".editar").css('display', 'none')
                } else {
                    $('#loading').modal({backdrop: 'static', keyboard: false});
                    setTimeout(function () {
                        $('#loading').modal('hide')
                    }, 2000)
                }
            }
        });
    }
}

function setSelect2(element, url) {
    element.select2({
        minimumInputLength: 3,
        allowClear: true,
        placeholder: "Select a State",
        ajax: {
            url: url,
            dataType: 'json',
            type: "GET",
            quietMillis: 150,
            processResults: function (data) {
                return {
                    results: data
                };
            },
        }
    });
}


$(function () {
    // Adicionando mascara para campos de CPF e celular
    $("#id_cpf").mask("999.999.999-99");

    // Setando select2 para campos de perfil de área temática
    $("#id_perfil").select2({
        width: 'resolve',
        language: "pt-BR",
        placeholder: 'Selecione os perfis do profissional',
    });

    $("#id_especialista_tipo_solicitacao").select2({
        width: 'resolve',
        language: "pt-BR",
        placeholder: 'Selecione os tipos de teleconsultoria que podem ser encaminhadas',
    });

    $("#id_regulador_area_tematica").select2({
        width: 'resolve',
        language: "pt-BR",
        placeholder: 'Selecione uma ou mais áreas temáticas',
    });

    // Escondendo campos especificos
    // camposEspecificosPerfil();

    // $("#id_perfil").change(function() {
    //     camposEspecificosPerfil();
    // });

    // Setando senha caso o CPF esteja preenchido
    let cpf_unmask = $("#id_cpf").data($.mask.dataName);
    $("#id_username").val(cpf_unmask);

    // Evento de Ctrl+V no campo de CPF
    $("#id_cpf").on('paste', function (event) {
        // Preenchendo campo do login com cpf digitado
        let text = event.originalEvent.clipboardData.getData('Text').replace(".", "").replace(".", "").replace("-", "");
        $("#id_username").val(text);

        buscarProfissional(text);
    });

    // Evento de digitar no campo de CPF
    $("#id_cpf").on('keypress', function (event) {
        // Preenchendo campo do login com cpf digitado
        let cpf_unmask = $("#id_cpf").data($.mask.dataName);
        $("#id_username").val(cpf_unmask);

        buscarProfissional($("#id_cpf").val());
    });

    $(".select2").css("width", "100%");
});
