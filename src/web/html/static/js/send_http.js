function sendHttp(url, data, getpost, responserequired, alert) {
    // responserequired:
    // 0 = none
    // 1 = text/body of response
    // 2 = success/failure boolean
    try {
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open(getpost, url, false);
        xmlHttp.send(data);
        if (alert){
            if (xmlHttp.status==200){
                var v = document.getElementById('cmd_success')
            } else {
                var v = document.getElementById('cmd_fail')
            }
            v.style.display="block";
            setTimeout(function(){v.style.display="none"}, 2000);
        }
        if (responserequired == 0) {
            return;
        } else if (responserequired == 1) {
            if (xmlHttp.status==200) {return xmlHttp.responseText;} else {return false;}
        } else if (responserequired == 2) {
            if (xmlHttp.status==200) {return true;} else {return false;}
        }
    }
    catch(err) {
        var v = document.getElementById('cmd_fail')
        v.style.display="block";
        setTimeout(function(){v.style.display="none"}, 2000);
        if (responserequired) {return false;}
    }
}