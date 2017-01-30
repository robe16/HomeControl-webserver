# Home Control - Web Server

Client to run alongside the main server - intention to have both run 24/7 on a Raspberry Pi.

A web interface  that will dynamically be created on the fly when requested, and will allow for commands to be sent to the server for controlling devices.

<h4>Bundles that have been developed:</h4>

<p>Devices</p>
- LG TV control
- Virgin Media TiVo control

<p>Accounts</p>
- Nest (thermostat & smoke detectors)

<p>Info Services</p>
- Weather forecast
- TV Listings

<img src="https://github.com/robe16/HomeControl-documentation/blob/master/img_interfaces_webserver-server.jpg">
<h5>Figure: Interfaces between server and devices/accounts/info sources</h5>

<hr>
<h3>API Guide</h3>
<p>
<code>GET</code> <code>/web/{page}</code>
<br>Returns a HTML page dependant on the variable {page}. Pages include home, tvguide and about.</p>
<br><p>
<code>GET</code> <code>/web/device/{room_id}/{device_id}</code>
<br>Returns a HTML page created for the particular device as requested by the {room_id} and {device_id} variables.
</p><br>
<code>GET</code> <code>/web/account/{account_id}</code>
<br>Returns a HTML page created for the particular account as requested by the {account_id} variable.
</p><br>

<strike><p>
<code>GET</code> <code>/web/preferences/{page}</code>
<br>Only one value available at present for {page} - tvguide. Returns a page for the logged in user to choose their favourite channels for showing in channel lists.
</p></strike>

<br><p>
<code>GET</code> <code>/web/static/{folder}/{filename}</code>
<br>Returns static files such as css, js and fonts/glyphicons.
</p><br><p>
<code>GET</code> <code>/data/device/{room_id}/{device_id}/{resource_requested}</code>
<br>relay request for data to the main server for/from a particular device as requested by the {room_id} and {device_id} variables. {resource_requested} indicates the resource requested from the device. Further documentation to be produced for this.
</p><br><p>
<code>GET</code> <code>/data/account/{account_id}/{resource_requested}</code>
<br>relay request for data to the main server for/from a particular account as requested by the {account_id} variable. {resource_requested} indicates the resource requested from the device. Further documentation to be produced for this.
</p><br><p>
<code>POST/GET</code> <code>/command/device/{room_id}/{device_id}</code>
<br>Relay commands to the main server for relaying to the particular device as requested by the {room_id} and {device_id} variables. Query parameters identify the command to be sent (<code>command</code>) and others that are device or command specific. Further documentation to be produced for this.
</p><br><p>
<code>POST/GET</code> <code>/command/account/{account_id}</code>
<br>relay commands to the main server for relaying to the particular account as requested by the {account_id} variable. Query parameters identify the command to be sent (<code>command</code>) and others that are device or command specific. Further documentation to be produced for this.
</p><br>

<strike><p>
<code>POST</code> <code>/preferences/{category}</code>
<br>Used to submit and save the user preferences via a json payload.
</p><br></strike>

<p>
<code>GET</code> <code>/favicon.ico</code>
<br>Returns favicon for HTML pages.
</p><br><p>
<code>GET</code> <code>/img/{category}/{filename:re:.*\.png}</code>
<br>Returns image as defined by pre-set HTML pages.
</p><br><p>
<code>GET</code> <code>/web/login</code>
<br>Present login screen for user selection and logging in.
<code>GET</code> <code>/web/logout</code>
<br>Logs user out by deleting session cookie.
</p><br>

<hr>

<h3>Required python packages</h3>
<p>The following python packages require installation on the target system:
<br>
bottle:
<code>http://bottlepy.org/docs/dev/index.html</code>
<br>
requests:
<code>http://docs.python-requests.org/en/master/</code>
</p>
