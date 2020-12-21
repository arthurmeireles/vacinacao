v4h_api = new V4H();

const audit_url_base = 'http://v4h.telessaude.ufrn.br';

$(document).ready(function() {
  $("#finalizar").hide();
    v4h_api.login('telessaude_ufrn', 'lais@tele123');
    fetch(audit_url_base + '/auth', {
        method: 'POST', 
        headers: {'Content-Type': 'application/json'}, 
        body: JSON.stringify({'username': 'telessaude_ufrn', 'password': 'lais@tele123'})
  }).then(result => {
    console.log("esse é o resultado ", result);
    startVideoConf();
  });
});

function startVideoConf() {
    $("#div_sala").removeClass("hidden");
    $("#iniciar").hide();
    console.log("Chamando resquestConference()");
    v4h_api.joinConference("teleconsultaPRODUCAO"+sessionID, document.querySelector('#meet'));
    v4h_api.requestConference("teleconsultaPRODUCAO"+sessionID).then(function (sessionId) {
        v4h_api.startConference("teleconsultaPRODUCAO"+sessionID, document.querySelector('#meet'));
        v4h_api.registerEndedListener(conferenceEnded);
    });
    $("#finalizar").show();
}

function getConfUrl() {
    v4h_api.getGuestUrl(v4h_api.sessionId, 'Jose', 'http://servidor.com/avatar/joao').then(function (data) {
        console.log('conference url is ' + data['url'])
        document.getElementById("url").innerHTML = "<a href=" + '"' + data['url'] + '"' + ">Click to Open Link</a>"
    });
}

function conferenceEnded(mySessionId) {
  $("#div_sala").addClass("hidden");
  $("#finalizar").trigger("click");
  }

function getStorageUrl(sessionId, rowNumber) { 
    fetch(audit_url_base + '/get-url/' + sessionId, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
      'Authorization': 'Bearer ' + v4h_api.token['access']
    }}).then(function (response) {
        return response.text().then(function (url) {
      url = url.replace(/['"]+/g, '');
      console.log('playing conference ' + sessionId + ' from url ' + url);
      var table = document.getElementById("example");
      table.rows[rowNumber].cells[5].innerHTML = "<a href='#' onclick='openVideo(" + '"' + url + '"' + ")'>Link</a><br />";
        });
    });
}

function openVideo(url) {
  document.getElementById("meet").innerHTML = "<video id='playback' width='960' height='960' controls>";
  let conf = document.getElementById('playback');
  let source = document.createElement('source');
  source.setAttribute('src', url);
  conf.appendChild(source);
  conf.load();
  conf.play();
}

function getAllConfs() {
  console.log(v4h_api.token['access']);
      // Efetua login na API de audição
    fetch(audit_url_base + '/get-all-conferences', {
    method: 'GET', 
    headers: {
      'Accept': 'application/json',
      'Authorization': 'Bearer ' + v4h_api.token['access']
    }
  }).then(function(response) {
    response.json().then(function(data) {
      console.log(data);
      var table = document.getElementById("example");
      for(var i = 0; i < data.length; ++i) {
        var row = table.insertRow(i+1);
        row.insertCell(0).innerHTML = data[i].sessionId;
        row.insertCell(1).innerHTML = data[i].owner;
        row.insertCell(2).innerHTML = data[i].requested;
        row.insertCell(3).innerHTML = data[i].started;
        row.insertCell(4).innerHTML = data[i].joined;
        if(data[i].storageToken != '') {
          getStorageUrl(data[i].sessionId, i);
        } else {
          row.insertCell(5).innerHTML = "";
        }
      }
    })
  });
}