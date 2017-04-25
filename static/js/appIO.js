/**
 * Created by tuxskar on 4/24/17.
 */
$(document).ready(function () {
    // Use a "/test" namespace.
    // An application can open a connection on multiple namespaces, and
    // Socket.IO will multiplex all those connections on a single
    // physical channel. If you don't care about multiple channels, you
    // can set the namespace to an empty string.
    var namespace = '';

    var room = 'cars', username, users;

    // Connect to the Socket.IO server.
    // The connection URL has the following format:
    //     http[s]://<domain>:<port>[/<namespace>]
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

    // Event handler for new connections.
    // The callback function is invoked when a connection with the
    // server is established.
    socket.on('connect', function () {
        console.log('connect!')
        socket.emit('join', {room: room})
    });

    socket.on('message', function (data) {
        console.log('got message:', data);

        if (data.username) {
            username = data.username;
            $('#username-place-holder').text(toTitleCase(username));
        }

        if (data.users) {
            users = data.users;
        }

        if (data.roomMessages && data.roomMessages[room] && data.roomMessages[room].length > 0) {
            $.each(data.roomMessages[room], function (idx, x) {
                addMsgToChat(x)
            })
        }
        console.log(data)
    });

    function toTitleCase(str) {
        return str.replace(/\w\S*/g, function (txt) {
            return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
        });
    }

    function addMsgToChat(msg) {
        console.log('addMsgToChat', msg)
        var roomMsgs = $('#room-msgs'),
            color = users[msg.username];

        var $time = $('<time/>').addClass('timeago').attr('datetime', msg.timestamp).text(msg.timestamp);
        roomMsgs.prepend($('<div/>').append(
            $('<div/>').append(
                $time,
                $('<span/>').addClass('username').text(toTitleCase(msg.username))),
            $('<span/>').addClass('msg-text').text(msg.msg)
            ).css('color', color)
        );
        $time.timeago();
    }

    socket.on('newMsg', function (msg) {
        console.log('newMsg')
        addMsgToChat(msg)
    });


    // Handlers for the different forms in the page.
    // These accept data from the user and send it to the server in a
    // variety of ways
    $('form#send-msg').submit(function (event) {
        var $msgInput = $('#send-msg-data'),
            msg = $msgInput.val();
        $msgInput.val('');
        console.log('Sending new msg: ', msg);
        socket.emit('newMsg', {room: room, data: msg, username: username});
        return false;
    });

});