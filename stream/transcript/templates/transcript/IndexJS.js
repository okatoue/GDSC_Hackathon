$(document).ready(function() {
    navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
        if (!MediaRecorder.isTypeSupported('audio/webm'))
            return alert('Browser not supported')

        const language = localStorage.getItem('detectedLanguage');
        const rtlLanguages = ['am', 'ur', 'ug', 'ps', 'sd', 'ar', 'he', 'fa'];
        // Check if the detected language is in the rtlLanguages array
        const isRtl = rtlLanguages.includes(language);

        // Set the text direction based on whether the language is RTL or not
        $('#transcript').css('direction', isRtl ? 'rtl' : 'ltr');

        const mediaRecorder = new MediaRecorder(stream, {
            mimeType: 'audio/webm',
        })

        const socket = new WebSocket('ws://localhost:8000/listen')

        socket.onopen = () => {
            document.querySelector('#status').textContent = 'Connected'
            console.log({ event: 'onopen' })
            mediaRecorder.addEventListener('dataavailable', async (event) => {
                if (event.data.size > 0 && socket.readyState == 1) {
                    socket.send(event.data)
                }
            })
            mediaRecorder.start(250)
        }   

        socket.onmessage = (message) => {
            const received = message.data
            if (received) {
                console.log(received)
                const highlightedText = highlightWords(received);
                $('#transcript').html($('#transcript').html() + ' ' + highlightedText);
            }
        }

        socket.onclose = () => {
            console.log({ event: 'onclose' })
        }

        socket.onerror = (error) => {
            console.log({ event: 'onerror', error })
        }

        function highlightWords(text) {
            return text.split(' ').map(word => `<mark>${word} </mark>`).join(' ');
        }

    });
    $('#transcript').on('mouseover', 'mark', function() {
        // This will be the word you're hovering over
        const hoveredWord = $(this).text();
        $('.custom-tooltip').text(hoveredWord).show();
    }).on('mouseout', 'mark', function() {
        // Hide the custom tooltip on mouse out
        $('.custom-tooltip').hide();
    });
});