<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Socket test</title>
</head>
<body>
    <h1>Socket test</h1>
    <div id="status">
        Connecting...
    </div>

    <div>
        <input type="text" id="name">
        <button id="btn-send" onclick="sendMessage()">Send</button>
    </div>
    <div id="response">
    </div>

    <script src="/static/js/lib/jquery-3.6.0.min.js"></script>
    <script src="/static/js/lib/socket.io.min.js"></script>
    <script>
        var connected = false;
        var socket;

        $(document).ready(function() {
            socket = io.connect('http://' + document.domain + ':' + location.port);
            socket.on('connect', function() {
                $('#status').html('OK');
                connected = true;
            });

            socket.on('response', function(data) {
                console.log(data);
                $('#response').html(data['data']);
            });
        });

        function sendMessage() {
            console.log('Sent');
            socket.emit('name', {name: $('#name').val()});
        }
    </script>
</body>
</html>