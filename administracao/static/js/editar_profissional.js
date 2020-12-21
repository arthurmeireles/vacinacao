function camposEspecificosPerfil() {
    $(".regulador").hide();
    $(".especialista").hide();
    $(".regulador-cr").hide();
    $(".administracao-ubs").hide();

    $('#id_perfil :selected').each(function() {
        if ($(this).text() === "Regulador") {
            $(".regulador").show();
        }
        if ($(this).text() === "Especialista") {
            $(".especialista").show();
        }
        if ($(this).text() === "ReguladorCR") {
            $(".regulador-cr").show();
        }
        if ($(this).text() === "AdministracaoUBS") {
            $(".administracao-ubs").show();
        }
    });
}

function setSelect2(element, url) {
    element.select2({
        minimumInputLength: 3,
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


$(function() {
    $("#id_cpf").mask("999.999.999-99");
    $("#id_telefone").mask("(99) 99999-9999");

    $("#id_perfil").select2({
        width: 'resolve',
        language: "pt-BR",
        placeholder: 'Selecione os perfis do profissional',
    });

    $("#id_especialista_tipo_solicitacao").select2({
        width: 'resolve',
        language: "pt-BR",
        placeholder: 'Selecione os tipos de teleconsultoria que podem ser encaminhadas'
    });

    $("#id_regulador_area_tematica").select2({
        width: 'resolve',
        language: "pt-BR",
        placeholder: 'Selecione uma ou mais áreas temáticas',
    });

    camposEspecificosPerfil();

    $("#id_perfil").change(function() {
        camposEspecificosPerfil();
    });

    $(".select2").css("width", "100%");
});
