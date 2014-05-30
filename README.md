smeserver-phpmyadmin
====================
Implementation of phpMyAdmin for Nethserver

see default settings

	config show phpmyadmin

	phpmyadmin=configuration
	access=private
	adminaccess=enabled
	multiaccess=disabled

You have two principal modes to log in phpmyadmin, all combinations are possible. 
You can use adminaccess and multiaccess together or one instead the other.

-mode adminaccess

Access with admin/password (same as the password of server-manager) via: 

	https://yourdomain/phpmyadmin

In this mode you are in a single mode only, no other ways to delegate the DB management to other users.

In order to enable or disable :

	config setprop phpmyadmin adminaccess enabled/disabled
	signal-event nethserver-phpmyadmin-save

-mode multiaccess

In this mode you can delegate the DB management to other users by the user and the password of the database. 
Furthermore this mode is more convenient since the authentication is made with cookies. You can easily close the session.

With the multiaccess mode, the admin account gets a new password which comes from '/etc/my.pwd'. 
Once you retrieve  it, you can change it in the phpmyadmin session for a password more easier to recall.

to retrieve the admin password : cat /etc/my.pwd

You can access via:
 
	https://yourdomain/phpmyadmin-multi 		if adminacces is enabled and multiaccess is enabled

	https://yourdomain/phpmyadmin 			if adminacces is disabled and multiaccess is enabled

In order to enable or disable :

	config setprop phpmyadmin multiaccess enabled/disabled
	signal-event nethserver-phpmyadmin-save

-restrict access (local network or internet)

You can set how the access to phmyadmin is allowed

	public : all internet (can be dangerous)
	private : only your local network

In order to enable or disable :

	config setprop phpmyadmin access public/private
	signal-event nethserver-phpmyadmin-save

