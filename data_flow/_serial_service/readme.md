# Serial Service Readme

## File Nesting

+ **serial_socket** is the main running thread. It spawns a listener for:

   * the control client, and also each serial port configured
   
   * and more
