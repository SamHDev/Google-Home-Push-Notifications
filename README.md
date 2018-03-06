# Google-Home-Push-Notifications
Allows you to send push a notification to a google home using webhooks!


The the server or Computers Public local IPV4 Adress or domain

If you Wish to use this with IFTTT remember to port forward. Its default port is 8093


Current Methods:

/devices (GET) Returns the friendlay names of all devices found (No Args Required)

/push (GET) Pushes a Notoication. (Posible Args: device* , text* , slow , vol)

*required
