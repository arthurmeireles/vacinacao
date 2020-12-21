$(function() {
    $('#id_periodo_inicial').datepicker({
        format: 'dd/mm/yyyy',
        todayHighlight: true,
        autoclose: true,
        language: 'pt-BR',
    });

    $('#id_periodo_final').datepicker({
        format: 'dd/mm/yyyy',
        todayHighlight: true,
        autoclose: true,
        language: 'pt-BR',
    });

    $(".informacoes").click(function() {
        let id = $(this).data("item-id");

        $.getJSON("/api/logs/" + id + "/", function(result){
            if (result['sucesso']) {
                resultado = '<span class="label label-success">Sucesso</span>';
                mensagem_erro = "Envio bem sucedido"
            } else {
                resultado = '<span class="label label-danger">Falha</span>'
                mensagem_erro = JSON.stringify(result['mensagem_erro'], null, ' ');
            }

            $('#data_submissao').html(result['data_submissao']);
            $('#resposavel').html(result['resposavel']);
            $('#sucesso').html(resultado);
            $('#json_recebido').html(JSON.stringify(result['json_recebido'], null, ' '));
            $('#mensagem_erro').html(mensagem_erro);

            $('pre code').each(function(i, block) {
                hljs.highlightBlock(block);
            });

            $('#info_log').modal('show');
        });
    });

    $('#info_log').on('hidden.bs.modal', function () {
        $("#collapseOne").removeClass("in");
    });
});
