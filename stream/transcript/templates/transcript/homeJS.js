document.addEventListener('DOMContentLoaded', function() {
    var websocket = new WebSocket('ws://localhost:8000/ws/path/');

    document.querySelector('#sendButton').onclick = function() {
        var value1 = document.querySelector('#dropdown1').value;
        var value2 = document.querySelector('#dropdown2').value;
        websocket.send(JSON.stringify({
            'dropdown1': value1,
            'dropdown2': value2
        }));
    };
});