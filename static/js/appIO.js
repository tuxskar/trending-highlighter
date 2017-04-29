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

    var room = 'cars', username, users, manualSend = false;

    $('#manual-send').change(function (e) {
        manualSend = $(this).is(':checked');
    });

    function sendRandomSentence() {
        if (manualSend) return;
        var randomSentences = ['que no quiero que sigas a lo tuyo', 'vale', '¿como estas?', 'no planches más',
                '¿vemos una peli?'],
            selectedIdx = Math.floor((Math.random() * randomSentences.length)),
            msg = randomSentences[selectedIdx];
        $('#send-msg-data').val(msg);

        setTimeout(function () {
            //do what you need here
            $('form#send-msg').submit();
        }, 1000);
    }

    var autoSendFunc = setInterval(sendRandomSentence, 3000);

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

        if (data.words) {
            $('.word-cloud').jQCloud(data.words, {
                autoResize: true,
                shape: 'rectangular'
            })
        }

        if (data.roomMessages && data.roomMessages && data.roomMessages.length > 0) {
            $.each(data.roomMessages, function (idx, x) {
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
        addMsgToChat(msg)
    });

    socket.on('newWordUpdate', function (words) {
        $('.word-cloud').jQCloud('update', words);
    });

    socket.on('userCnt', function (data) {
        if (!data) return;
        var cnt = data.cnt;
        $('#user-cnt').text(cnt);
    });


    // Handlers for the different forms in the page.
    // These accept data from the user and send it to the server in a
    // variety of ways
    $('form#send-msg').submit(function (event) {
        var $msgInput = $('#send-msg-data'),
            msg = $msgInput.val();
        $msgInput.val('');
        socket.emit('newMsg', {room: room, data: msg, username: username});
        return false;
    });

});