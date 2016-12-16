function buildList()
    {
        //
        errorFound = false;
        //
        var inptChans = document.getElementsByName('user-channel');
        //
        list = '[';
        //
        for (var i = 0; i < inptChans.length; i++)
            {
                //
                roomNum = i + 1;
                //
                if (inptChans[i].checked)
                    {
                        //
                        if (list=='[')
                            {list += '"' + inptChans[i].id + '"';}
                        else
                            {list += ', "' + inptChans[i].id + '"';}
                        //
                    }
                //
            }
        //
        list += ']'
        //
        return list;
        //
    }


function sendUpdate()
    {
    listChans = buildList();
    if (listChans && sendHttp('/preferences/tvguide', listChans, 'POST', 2, true))
        {
            document.getElementById('msg_title').innerHTML = 'Success';
            document.getElementById('msg_txt').innerHTML = 'User preferences have been successfully sent to the server';
            document.getElementById('message_popup').className = 'message viewport_centre visible';
        }
    else
        {
            document.getElementById('msg_txt').innerHTML = 'An error has been encountered.';
            document.getElementById('msg_title').innerHTML = 'Error';
            document.getElementById('message_popup').className = 'message viewport_centre visible';
        }
    }

function hidePopup()
    {
        document.getElementById('message_popup').className = "message viewport_centre hidden";
        if (document.getElementById('msg_title').innerHTML == 'Success') {window.location.href = '/web/home';}
    }