let selecionado = '', prox_semana = 0, semana_atual = 0, replicar = false;

function setSelect2(element, url) {
    element.select2({
        minimumInputLength: 3,
        allowClear: true,
        placeholder: "Digite para buscar",
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

function novaSemana(dados, semana) {
    $(".item[data-id=" + semana + "]").dayScheduleSelector({
        days: [1, 2, 3, 4, 5, 6, 7],
        startTime: '07:00',
        endTime: '23:45',
        interval: 15
    });

    $(".item[data-id=" + semana + "]").data("artsy.dayScheduleSelector").deserialize(dados);
    Object.keys(dados).forEach(function (key) {
        for (evento of dados[key]) {
            var celula = $('.item[data-id="' + semana + '"] .time-slot[data-time="' + evento[0] + '"][data-day="' + key + '"]');
            celula.html(evento[1]+" salas");
            celula.addClass("text-center");
            celula.removeAttr('data-selected');

            if(evento[1] == "0"){
                celula.attr("disabled", "disabled")
            }
        }
    });

    let dias = "" +
        "<tr class='header'>" +
            "<th>-</th>" +
            "<th dia='1' data_semana='" + dados.semana[0] + "'>Segunda-feira <br>(" + dados.semana[0] + ")</th>" +
            "<th dia='2' data_semana='" + dados.semana[1] + "'>Terça-feira <br>(" + dados.semana[1] + ")</th>" +
            "<th dia='3' data_semana='" + dados.semana[2] + "'>Quarta-feira  <br>(" + dados.semana[2] + ")</th>" +
            "<th dia='4' data_semana='" + dados.semana[3] + "'>Quinta-feira  <br>(" + dados.semana[3] + ")</th>" +
            "<th dia='5' data_semana='" + dados.semana[4] + "'>Sexta-Feira  <br>(" + dados.semana[4] + ")</th>" +
            "<th dia='6' data_semana='" + dados.semana[5] + "'>Sábado <br>(" + dados.semana[5] + ")</th>" +
            "<th dia='7' data_semana='" + dados.semana[6] + "'>Domingo <br>(" + dados.semana[6] + ")</th>" +
        "</tr>";

    $('.item[data-id="' + semana + '"] .schedule-header').html(dias);
    $('.schedule-header tr th').addClass("text-center");
};

$(function () {
    let semana = 0;
    novaSemana(eventos, semana);

    setSelect2($("#id_paciente"), url_select2);
    setSelect2($("#id_convidados"), url_select2);
    setSelect2($("#id_profissionais"), url_busca_profissionais);

    $(".select2").css("width", "100%");

    $('#data-hora').on('show.bs.modal', function() {
        $(".time-slot").removeAttr("data-selected");
    });

    $(".select-equipe").click(function(){
        $($(this).find("li")).each(function(){
            console.log($(this).attr("data-id"))
            $("#id_profissionais").append("<option value="+$(this).attr("data-id")+" selected>"+$(this).text()+"</option>");
        });
        $('#selecao-equipe').modal('hide');
    });

    $(document).on('click', '.time-slot', function() {
        console.log("click");
        let index = $(this).index();
        let table = $(this).closest("table");
        let desabilitado = $(this).attr("disabled");

        let data = table.find(".header th").eq(index).attr("data_semana");

        if($(this).attr("data-selected")){
            console.log("terminou agora");
            if($(".time-slot[data-selected='selected'][disabled='disabled']").length > 0){
                $.toast({
                    heading: 'Atenção!',
                    text: 'O horário está reservado',
                    hideAfter: 10000,
                    icon: 'error'
                });
            $(".time-slot").removeAttr("data-selected");
            }
            else{
                var slots_selecionados = $(".time-slot[data-selected='selected']");
                console.log("escolhidos slots para o dia ", data);
                $("#id_data").val(data);
                $("#id_hora_inicio").val(slots_selecionados.eq(0).attr("data-time"));

                var fim = ($(slots_selecionados.last()).parent().next('tr').children().eq(1).attr("data-time"));

                if(fim)
                    $("#id_hora_fim").val(fim);
                else
                    $("#id_hora_fim").val("23:45");

                $('#data-hora').modal('hide');
                console.log("horario inicial ", slots_selecionados.eq(0).attr("data-time"));
                console.log("horario final ", slots_selecionados.last().attr("data-time"));
            }
            
        }
        if (desabilitado === "disabled") {
            $.toast({
                heading: 'Atenção!',
                text: 'O horário está reservado',
                hideAfter: 10000,
                icon: 'error'
            });
        }
    });

    $("#prev").click(function () {
        if (!($('.carousel-inner .item:first').hasClass('active'))) {
            $(".carousel").carousel("prev");
        }
    });

    $('#nova_semana').on('click', function () {
        if ($("div[class='item active']").is(':last-child')) {
            semana += 1;
            $("#weekly-schedule").append("<div class='item' data-id=" + semana + "></div>");

            $.ajax({
                url: "/salas_agendadas/" + semana,
                context: "application/json",
                success: function (data) {
                    novaSemana(data, semana);
                }
            });
        }
        $(".carousel").carousel("next");
    });
})