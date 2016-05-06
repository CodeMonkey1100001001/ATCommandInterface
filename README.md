# ATCommandInterface
Allows an Arduino to respond to at commands as if it were a modem.


This is a very basic version with only a hand full of demo commands as examples.


Examples:

AT+HELO
Helo AT Reader
OK


AT+RAND
+RAND=7
AT+RAND=999
+RAND=438
OK

AT+NULL
OK

AT+STAT
+STATUS=A OK!
AT+STA
A OK!
