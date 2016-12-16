$(document).ready(function() {
    $(".dropdown-toggle").dropdown();
});

function hidePopup()
    {
        document.getElementById('message_popup').className = "message viewport_centre hidden";
        if (document.getElementById('msg_title').innerHTML == 'Success') {window.location.href = '/web/home';}
    }