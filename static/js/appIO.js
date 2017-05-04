/**
 * Created by tuxskar on 4/24/17.
 */
$(document).ready(function () {

    // Connect to the Socket.IO server.
    // The connection URL has the following format:
    //     http[s]://<domain>:<port>[/<namespace>]
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);


    var room = window.location.pathname.slice(1), username, users, manualSend = true, randomSentences;

    if (['cats', 'dogs'].indexOf(room) === -1) room = 'cats';

    // event handlers
    socket.on('connect', function () {
        socket.emit('join', {room: room})
    });

    socket.on('message', function (data) {
        if (data.username) {
            username = data.username;
            $('#username-place-holder').text(toTitleCase(username));
        }

        if (data.users) users = data.users;

        if (data.sentences) randomSentences = data.sentences;

        if (data.words)
            $('.word-cloud').jQCloud(data.words, {
                autoResize: true,
                delay: 5,
                shape: 'rectangular'
            });

        if (data.room) {
            room = data.room;
            $('#room-name').text(data.roomName);
        }

        if (data.roomMessages && data.roomMessages && data.roomMessages.length > 0) {
            $.each(data.roomMessages, function (idx, x) {
                addMsgToChat(x)
            })
        }
    });


    socket.on('newMsg', function (msg) {
        addMsgToChat(msg)
    });

    socket.on('newWordUpdate', function (words) {
        $('.word-cloud').jQCloud('update', words);
    });

    socket.on('userCnt', function (data) {
        if (!data) return;
        $('#user-cnt').text(data.cnt);
    });


    // submit and change events
    $('form#send-msg').submit(function (event) {
        var $msgInput = $('#send-msg-data'),
            msg = $msgInput.val();
        $msgInput.val('');
        socket.emit('newMsg', {room: room, data: msg, username: username});
        return false;
    });

    $('#manual-send').change(function (e) {
        manualSend = $(this).is(':checked');
    });

    // extra functions
    function toTitleCase(str) {
        return str.replace(/\w\S*/g, function (txt) {
            return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
        });
    }

    function addMsgToChat(msg) {
        var roomMsgs = $('#room-msgs'),
            color = users[msg.username];

        var d = new Date(msg.timestamp), timeTxt = d.toLocaleTimeString(),
            $time = $('<time/>').text(timeTxt).attr('title', msg.timestamp).addClass('time');
        roomMsgs.prepend($('<div/>').append(
            $('<div/>').append(
                $time,
                $('<span/>').addClass('username').text(toTitleCase(msg.username))),
            $('<div/>').addClass('msg-text').text(msg.msg)
            ).css('color', color)
        );
        roomMsgs.find('div').slice(30).remove()
    }

    function sendRandomSentence() {
        if (manualSend) return;
        var selectedIdx = Math.floor((Math.random() * randomSentences.length)),
            msg = randomSentences[selectedIdx];
        $('#send-msg-data').val(msg);

        setTimeout(function () {
            $('form#send-msg').submit();
        }, 1000);
    }

    // JS ready initializations
    setInterval(sendRandomSentence, 3000);

    $('#manual-send').attr('checked', manualSend);
    $('#room-name').text(room);
});