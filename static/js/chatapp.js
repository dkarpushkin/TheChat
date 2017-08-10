(function () {
    $('#join_room_btn').click(join_room);
    $('#send_msg_form').submit(send_message);

    function join_room(event) {
        $.post('/joinroom/' + info.room_slug + '/' + info.user.username + '/')
            .done(function (data) {
                $('.join_button').hide()
            })
            .fail(function () {
                // alert(data.errors.join())
            });
    }

    function send_message(event) {
        var form = $(this),
            data = form.serialize(),
            url = form.attr('action'),
            text = form.find('#message-input').val();

        if (typeof(text) === 'undefined' || text.length === 0) {
            alert('Message is empty');
        } else {
            $.post(url, data)
                .done(function (d) {   //  on success
                    return
                })
                .fail(function () {   //  on error
                    alert('You are not joined')
                });
        }

        event.preventDefault();
        event.stopPropagation()
    }

    function render_message(msg_data, is_own) {
        var msg_template = $('.messages-container [hidden]');

        var new_msg = msg_template.clone();
        new_msg.removeAttr('hidden');
        new_msg.find('.username span').text(msg_data['nickname']);
        new_msg.find('.text span').text(msg_data['text']);

        msg_template.parent().prepend(new_msg)
    }

    function render_user(user_data, is_own) {
        var user_template = $('.users-container [hidden]');

        var new_user = user_template.clone();
        new_user.removeAttr('hidden');
        new_user.find('span').text(user_data['nickname']);

        user_template.parent().prepend(new_user);
    }

    run_chat = function (room_slug) {
        var ws;

        function run_ws_chat() {
            ws = new WebSocket(build_wc_url(location.hostname, info.wc_port) + room_slug + "/");

            ws.onmessage = function (event) {
                var msg_data = JSON.parse(event.data);

                switch (msg_data['type']) {
                    case 'user joined':
                        render_user(msg_data);
                        break;
                    case 'message sent':
                        render_message(msg_data);
                        break;
                    default:
                        break;
                }
            };

            ws.onclose = function () {
                // Try to reconnect in 5 seconds
                setTimeout(function () {
                    run_ws_chat()
                }, 5000);
            }
        }

        if ("WebSocket" in window) {
            run_ws_chat()
        } else {
            alert("Browser does not support WebSocket")
        }
    };

    function build_wc_url(hostname, port){
        return 'ws://' + hostname + ':' + port + '/'
    }
})();
