function checkListings(url){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open('GET', url, false);
    xmlHttp.send(null);
    if (xmlHttp.status==200) {
        document.getElementById('tvguide-panelbody').innerHTML=xmlHttp.responseText}
    else {setTimeout(function () {checkListings(url);}, 5000);}
}