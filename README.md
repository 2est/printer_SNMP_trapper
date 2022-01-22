# printer_SNMP_trapper

What is it?
-----------
Script for intercepting SNMP traffic from printers and converting it into a readable format.

How it work?
-----------
To work you will need:
- Setting your devices for send SNMP alert on broadcast address or IP of computer where running printer_SNMP_trapper
- time package
- pysnmp.entity package
- pysnmp.carrier.asyncore.dgram package
- pysnmp.entity.rfc3413 package

After using the script, you can see the received data in the received_traps20210923.log file.
