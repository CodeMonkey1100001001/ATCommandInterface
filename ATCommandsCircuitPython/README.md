# ATCommands for Circuit Python

Non blocking with a convenient doOtherStuff(routine)

To add new functionality modify:
```
knownCommands = {
    "+ID": "id",
    "+INFO": "info",
    "+CCLK": "cclk",
    "+RAND": "make_rand",
    "?": "help"
}
```

Expected form is AT+COMMAND where the known commands just gets the extended portion 2nd variable is the function to call.

Example commands for what it knows now:

```
AT+CCLK
at+cclk
+INFO: time requested
+2334.99
OK

AT+ID
+ID: +AT Commands on CircuitPython v20230919.1925
+IDOS: (sysname='samd51', nodename='samd51', release='8.2.1', version='8.2.1 on 2023-07-25', machine='Adafruit Feather M4 Express with samd51j19')
OK

at+rand=100
+Arguments[100]
00
+MaxValue = 100
+MinValue = 0
+Rand = 87
OK

```


