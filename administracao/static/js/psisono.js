function buscarCPF(cpf) {
    let cpf_unformat = cpf.replace(/_/g, "").replace(/-/g, "").replace(/\./g, '');
    let url = '/buscar/usuario/' + cpf_unformat;

    if (cpf_unformat.length === 11) {
        $.ajax({
            method: 'GET',
            url: url,
            context: "application/json",
            success: function (data) {
                if (data.valido === true) {
                    if (data.existe === true) {
                        let data_nascimento = dataNascimentoFormat(data.data_nascimento)
                        $('#id_nome').val(data.nome);
                        $('#id_data_nascimento').val(data_nascimento);
                        $('#id_telefone').val(data.telefone);
                        $('#id_endereco').val(data.endereco);
                        $('#id_complemento').val(data.complemento);
                        $('#id_email').val(data.email)
                    }
                } else if (data.valido === false) {
                    $(".modal-title").html(data.title);
                    $(".mensagem").html(data.text);
                    $("#profissional-modal").modal({backdrop: 'static', keyboard: true});
                } else {
                    $('#loading').modal({backdrop: 'static', keyboard: false});
                }
            }
        });
    }
}

function dataNascimentoFormat(data_nascimento){
    let data = data_nascimento.split('-');

    return data[2] + '/' + data[1] + '/' + data[0]
}

$(function () {
    // Evento de digitar no campo de CPF
    $("#id_cpf").on('keyup', function () {
        buscarCPF($("#id_cpf").val());
    });

    $('.raca :input').change(function () {
        $(this).each(function () {
            if ($(this).attr('id') === 'id_raca_5' && $(this).prop('checked')) {
                $('#id_raca_outro').show();
            } else {
                $('#id_raca_outro').val('').hide();
                $('#id_raca_5').val('outro')
            }
        })
    });
    if ($('#id_raca_5').prop('checked') === false) {
        $('#id_raca_outro').hide();
    }
    $("#id_raca_outro").on('keyup', function () {
        $('#id_raca_5').val($(this).val())
    });

    $('.situacao :input').change(function () {
        $(this).each(function () {
            if ($(this).attr('id') === 'id_situacao_atual_8' && $(this).prop('checked')) {
                $('#id_situacao_outro').show();
            } else {
                $('#id_situacao_outro').val('').hide();
                $('#id_situacao_atual_8').val('outro')
            }
        })
    });
    if ($('#id_situacao_atual_8').prop('checked') === false) {
        $('#id_situacao_outro').hide();
    }
    $("#id_situacao_outro").on('keyup', function () {
        $('#id_situacao_atual_8').val($(this).val())
    });

    $('.dose-bebida :input').change(function () {
        $(this).each(function () {
            if ($(this).attr('id') === 'id_qtd_bebida_7' && $(this).prop('checked')) {
                $('#id_dose_outro').show();
            } else {
                $('#id_dose_outro').val('').hide();
                $('#id_qtd_bebida_7').val('outro')
            }
        })
    });
    if ($('#id_qtd_bebida_7').prop('checked') === false) {
        $('#id_dose_outro').hide();
    }
    $("#id_dose_outro").on('keyup', function () {
        $('#id_qtd_bebida_7').val($(this).val())
    });

    $('.despertador :input').change(function () {
        $(this).each(function () {
            if ($(this).attr('id') === 'id_despertador_3' && $(this).prop('checked')) {
                $('#id_despertador_outro').show();
            } else {
                $('#id_despertador_outro').hide().val('');
                $('#id_despertador_3').val('outro');
            }
        })
    });
    $('.esquema-trabalho :input').change(function () {
        $(this).each(function () {
            if ($(this).attr('id') === 'id_esquema_trabalho_6' && $(this).prop('checked')) {
                $('#id_esquema_outro').show();
            } else {
                $('#id_esquema_outro').hide().val('');
                $('#id_esquema_trabalho_6').val('outro');
            }
        })
    });

    $('#id_despertador_outro, #id_esquema_outro').hide()

    $("#id_despertador_outro, #id_esquema_outro").on('keyup', function () {
        if ($(this).attr('id') === 'id_despertador_outro') {
            $('#id_despertador_3').val($(this).val());
        } else if ($(this).attr('id') === 'id_esquema_outro') {
            $('#id_esquema_trabalho_6').val($(this).val());
        }
    });

    $('#id_diagnostico_outro').hide()

    $('.diagnostico :input').change(function () {
        if ($(this).attr('id') === 'id_diagnostico_medico_5') {
            if ($(this).prop('checked')) {
                $('#id_diagnostico_outro').show();
            } else {
                $('#id_diagnostico_outro').hide().val('');
                $('#id_diagnostico_medico_5').val('outro');
            }
        }
    })

    $("#id_diagnostico_outro").on('keyup', function () {
        $('#id_diagnostico_medico_5').val($(this).val())
    });

    if ($('#id_profissional_saude').val() !== 'True'){
        $("#consentimentos").hide();
    }

    $('#id_profissional_saude').change(function () {
        if ($(this).val() === 'True') {
            $('#termo-consentimento').modal({backdrop: 'static', keyboard: true}).on('hide.bs.modal', function () {
                $("#consentimentos").show();
            });
        } else if ($(this).val() === 'False'){
            $('#consentimento_profissional').modal({backdrop: 'static', keyboard: true})
        }else {
            if ($("#consentimentos").is(':visible')) {
                $('#consentimentos :input').each(function () {
                    $(this).val('');
                })
                $("#consentimentos").hide();
            }
        }
    })

    $('#id_intervencao_distancia').change(function () {
        if ($(this).val() === 'False') {
            $('#consentimento_intervencao_distancia').modal({backdrop: 'static', keyboard: true});
        }
    })
})