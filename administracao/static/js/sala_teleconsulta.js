$(function () {
    function atualizaAnexosEncaminhamentos() {
        $.ajax({
            url: url_anexos_encaminhamentos + "?encaminhamentos=" + $("#meus_encaminhamentos").val() + "&condutas=" + $("#minhas_condutas").val(),
        })
            .done(function (data) {
                anexos_profissional = JSON.parse(data["anexos_profissional"]);
                anexos_paciente = JSON.parse(data["anexos_paciente"]);
                encaminhamentos = data["encaminhamentos"];
                escala = JSON.parse(data["escala_funcional"]);

                $("#anexos-profissional").html("");
                $("#anexos-paciente").html("");
                $("#encaminhamentos-profissionais").html("");
                $("#condutas-profissionais").html("");
                $.each(anexos_profissional, function (key, anexo) {
                    $("#anexos-profissional").append(
                        "<li><a href='/media/" + anexo["fields"]["arquivo"] + "' target='_blank'>" + anexo["fields"]["arquivo"] + "</a></li>")
                });
                $.each(anexos_paciente, function (key, anexo) {
                    $("#anexos-paciente").append(
                        "<li><a href='/media/" + anexo["fields"]["arquivo"] + "' target='_blank'>" + anexo["fields"]["arquivo"] + "</a></li>")
                });
                encaminhamentos.forEach(function (item) {
                    if (item[1] != null) {
                        $("#encaminhamentos-profissionais").append(
                            '<div class="col-md-12">' +
                            '<p><strong>Encaminhamentos de ' + item[0] + '</strong></p>' +
                            '<div class="box">' +
                            '<p>' + item[1] + '</p>' +
                            '</div></div>'
                        )
                    }
                    if (item[2] != null) {
                        $("#condutas-profissionais").append(
                            '<div class="col-md-12">' +
                            '<p><strong>Condutas de ' + item[0] + '</strong></p>' +
                            '<div class="box">' +
                            '<p>' + item[2] + '</p>' +
                            '</div></div>'
                        )
                    }
                });

                Object.keys(escala[0]["fields"]).forEach(function(key) {
                    console.log(key, escala[0]["fields"][key]);
                    $("#id_"+key).val(escala[0]["fields"][key]);
                });
            });
    }

    atualizaAnexosEncaminhamentos();
    setInterval(atualizaAnexosEncaminhamentos, 10000);

    $("#anexos").submit(function (event) {
        event.preventDefault(); //prevent default action 
        var post_url = $(this).attr("action"); //get form action url
        var request_method = $(this).attr("method"); //get form GET/POST method
        var form_data = new FormData(this); //Creates new FormData object
        $.ajax({
            url: post_url,
            type: request_method,
            data: form_data,
            contentType: false,
            cache: false,
            processData: false
        }).done(function (response) { //
            atualizaAnexosEncaminhamentos();
            $.toast({
                heading: 'Salvo!',
                text: 'Anexo enviado com sucesso',
                hideAfter: 2000,
                icon: 'success'
            });
        });
    });

    $("#meus_encaminhamentos, #minhas_condutas").on("input", function () {
        if ($(this).val().length % 50 == 0) {
            atualizaAnexosEncaminhamentos();
        }
    });

    $("#force_atualizar").on("click", function () {
        atualizaAnexosEncaminhamentos();
        $.toast({
            heading: 'Salvo!',
            text: 'Encaminhamentos e Condutas salvos',
            hideAfter: 2000,
            icon: 'success'
        });
    });

    $("#finalizar").on("click", function () {
        Swal.fire({
            title: 'Qual o status da teleconsulta?',
            type: 'question',
            input: 'select',
            inputOptions: {
                'finalizada': "Respondida e Finalizada",
                'cancelada': "Cancelada",
            },
            showCancelButton: true
        }).then(
        result => {
            if (result.value != undefined){
                if ($("#minhas_condutas").val().length > 1) {
                    window.location.href = url_atualizar+"?status="+result.value+"&encaminhamentos="+$("#meus_encaminhamentos").val()+"&condutas="+$("#minhas_condutas").val();
                }
                else{
                    Swal.fire({
                        type: 'error',
                        title: 'Condutas/Evolução',
                        text: 'Preencha a aba de condutas/evolução para finalizar a Teleconsulta',
                      })
                }
            }
        }
        );
    });

    $('#bulbar :input').change(function () {
        let totalBubar = 0;
        $('.form-group .bulbar').each(function () {
            let selectVal = $(this).val();
            if ($.isNumeric(selectVal)) {
                totalBubar += parseInt(selectVal);
            }
        });
        $('#id_bulbar_total').val(totalBubar);
    });

    $('#maos_bracos :input').change(function () {
        let totalMaosBracos = 0;
        $('.form-group .maos_bracos').each(function () {
            let selectVal = $(this).val();
            if ($.isNumeric(selectVal)) {
                totalMaosBracos += parseInt(selectVal);
            }
        });
        $('#id_bracos_total').val(totalMaosBracos);

    });

    $('#tronco_mmii :input').change(function () {
        let totalTrcoMMII = 0;
        $('.form-group .tronco_mmii').each(function () {
            let selectVal = $(this).val();
            if ($.isNumeric(selectVal)) {
                totalTrcoMMII += parseInt(selectVal);
            }
        });
        $('#id_tronco_total').val(totalTrcoMMII);
    });

    $('#respiratorio :input').change(function () {
        let totalRespiratorio = 0;
        $('.form-group .respiratorio').each(function () {
            let selectVal = $(this).val();
            if ($.isNumeric(selectVal)) {
                totalRespiratorio += parseInt(selectVal);
            }
        });
        $('#id_respiratorio_total').val(totalRespiratorio);
    });

    $('#escala_funcional').change(function () {
        let total = 0;
        $('.subtotal').each(function () {
            let inputVal = $(this).val();
            if ($.isNumeric(inputVal)){
                total += parseInt(inputVal);
            }
        });
        $('#id_total').val(total);
    });

    $('#id_total').css('width', '4.8em')

    $("#escala_funcional").submit(function (event) {
        event.preventDefault(); //prevent default action
        var post_url = $(this).attr("action"); //get form action url
        var request_method = $(this).attr("method"); //get form GET/POST method
        var form_data = new FormData(this); //Creates new FormData object
        $.ajax({
            url: post_url,
            type: request_method,
            data: form_data,
            contentType: false,
            cache: false,
            processData: false
        }).done(function (response) { //
            atualizaAnexosEncaminhamentos();
            $.toast({
                heading: 'Salvo!',
                text: 'Escala Funcional salvo com sucesso',
                hideAfter: 2000,
                icon: 'success'
            });
        });
    });
});