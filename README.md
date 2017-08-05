# Home Control - Web Server

<strong>Full documentation can be found at https://github.com/robe16/HomeControl-documentation/wiki/HomeControl-Webserver</strong>

Client to run alongside the main server - intention to have both run 24/7 on a Raspberry Pi.

A web interface that will dynamically be created on the fly when requested, and will allow for commands to be sent to the server for controlling devices.

<h4>Bundles that have been developed:</h4>

<p>Devices</p>
<ul>
<li>LG TV control</li>
<li>Virgin Media TiVo control</li>
<li>Nest (thermostat & smoke detectors)</li>
</ul>

<p>Info Services</p>
<ul>
<li>Weather forecast</li>
<li>TV Listings</li>
</ul>

<img src="https://github.com/robe16/HomeControl-documentation/blob/master/images/interfaces/img_interfaces_webserver-server.jpg">
<h5>Figure: Interfaces between HomeControl-webserver and HomeControl-server</h5>

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
