function channelhighlight(chan_no) {
    var all = document.getElementsByTagName("div");
    for (var i = 0; i < all.length; i++)
        {
            if (all[i].id==(chan_no)) {
                document.getElementById(all[i].id).classList.add("chan-highlight");
            }
            else if (all[i].id.startsWith('chan')) {
                document.getElementById(all[i].id).classList.remove("chan-highlight");
            };
        };
}

function channelState(chan_name, chan_logo) {
    //
    document.getElementById("now_viewing").innerHTML=chan_name
    document.getElementById("now_viewing_logo").src="/img/channel/"+chan_logo
    //
}

function getChannel(url, auto) {
    //
    response = sendHttp(url, null, 'GET', 1, false);
    //
    if (response) {
        //
        chan_json = JSON.parse(response);
        //
        chan_no = chan_json.chan_no;
        chan_name = chan_json.chan_name;
        chan_logo = chan_json.chan_logo;
        //
        channelhighlight('chan'+chan_no);
        channelState(chan_name, chan_logo);
        //
    }
    //
    if (auto) {setTimeout(function () {getChannel(url);}, 10000);}
    //
}