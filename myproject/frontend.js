document.addEventListener('DOMContentLoaded', (event) => {
    // Establish a WebSocket connection to the server
    const socket = new WebSocket('ws://localhost:6789');
    
    // Get the transcript element where text will be displayed
    const transcriptElement = document.getElementById('transcript');

    // Listen for messages from the WebSocket server
    socket.onmessage = function(event) {
        // Append the received message (transcription) to the transcript element
        // You can customize this as needed, e.g., appending as new lines or new elements
        transcriptElement.textContent += event.data + "\n";
    };

    socket.onerror = function(error) {
        // Handle any errors that occur during the connection
        console.error('WebSocket Error: ', error);
    };

    socket.onopen = function(event) {
        // Optional: Handle when the connection to the WebSocket server is opened
        console.log('WebSocket connection established');
    };

    socket.onclose = function(event) {
        // Optional: Handle when the WebSocket connection is closed
        console.log('WebSocket connection closed', event.reason);
    };
});
