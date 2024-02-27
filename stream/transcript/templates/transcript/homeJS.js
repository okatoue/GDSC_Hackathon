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

    document.querySelector('#sendButton').onclick = function() {
        // Check if both dropdowns have selections
        var dropdownFrom = document.getElementById('dropdown1').value;
        var dropdownTo = document.getElementById('dropdown2').value;

        if (dropdownFrom !== "" && dropdownTo !== "") {
            // Send data through WebSocket
            websocket.send(JSON.stringify({
                'dropdown1': dropdownFrom,
                'dropdown2': dropdownTo
            }));
            localStorage.setItem('detectedLanguage', dropdownTo);
            window.location.href = 'index.html';
        } else {
            alert('Please select options from both dropdowns.');
        }
    };

});

