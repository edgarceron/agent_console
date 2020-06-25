# dashboardcti

# Requirements
- Memcached server (https://memcached.org/) or docker (https://hub.docker.com/_/memcached).

# Instalation

- Run the next commands in the Issabel call_center database, replace 'IP Server' with the IP Address of the current applications server and 'password' with the password you want for the user:
```
 CREATE TABLE `cedula_llamada` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `uniqueid` varchar(32) DEFAULT NULL,
  `cedula` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE USER 'manticore'@'IP Server' IDENTIFIED BY 'password';
GRANT SELECT, INSERT, UPDATE ON call_center.* TO 'manticore'@'IP Server';
FLUSH PRIVILEGES;
```
- Create a context number in the pbx server for this example we are using the number 400.
- Add the database credentials to the isabel/agi_cedula.php file.
- Copy the isabel/agi_cedula.php into the folder /var/lib/asterisk/agi-bin in the Isabel server.
- Create the next context in the folder etc/asterisk/extension-custom.conf on the Isabel server: 
```
[cedula] 
exten => 400,1,AGI(agi_cedula.php, ${UNIQUEID})  
exten => 400,2,Hangup 
```
- Include the context at the top in from-internal-custom:
```
[from-internal-custom]	
....
....
....
include => cedula
```
- Create a custom destination in the IVR menu in the Isabel web app (See isabel/custom_destination_example_1 and isabel/custom_destination_example_2).
- Alter the settings for the databases (default and call_center).
- Alter the settings for the memcache server address.
- Run makemigrations, then migrate and then run the command appregistration.

# Testing
Any test running on mysql server (call_center database) must be runned using the SimpleTestCase Class and the tables used in the test must be defined on the test setup.