# Register bitfield generator for Microchip ATDF files

Writing code for ~~Atmel~~ Microchip AVR Microcontrollers often involves writing directly to registers.

With them using bitfields, single bits or bitgroup got a name and purpose. Knowing "your" CPU one could simply write the decimal or hex value to such a register like:

```c
UCSR0A = 42;
//or
UCSR0A = 0x2A;
```

Which is a bit like writing on a keyboard with blue switches: cool for you but the people around may hate you.

At least avr-gcc supports binary notation, which is - having the datasheet open - a bit easier to read:

```c
UCSR0A = 0b00101010;
```

Anyway, the compiler brings the IO-definitions which are referenced by ```avr/io.h```, so the bit names can be used with zeroes and ones as switches:

```c
UCSR0A = (0<<RXC0) | (0<<TXC0) | (1<<UDRE0) | (0<<FE0) | (1<<DOR0) | (0<<UPE0) | (1<<U2X0) | (0<<MPCM0);
```

If you want to be educational (or if you get paid by LOC), you may even add the descriptions for each bit:

```c
UCSR0A = 
      (0<<RXC0) // USART Receive Complete
    | (0<<TXC0) // USART Transmitt Complete
    | (0<<UDRE0) // USART Data Register Empty
    | (0<<FE0) // Framing Error
    | (0<<DOR0) // Data overRun
    | (0<<UPE0) // Parity Error
    | (0<<U2X0) // Double the USART transmission speed
    | (0<<MPCM0); // Multi-processor Communication Mode
```

Great readability but quite quite a lot of manual labor, right?

Fear not! Everything is already there, just in another format.

# Prerequisite

Get Python 3 and locate your device's ATDF file.

Microchip studio comes with DFP packs which contain those files (typically in <installdir>\packs\atmel\ATmega_DFP\...\atdf\<name>.atdf)

Alternatively, [download the pack](http://packs.download.atmel.com/), despite the extension it's basically a zip-file, you you can extract it with your favorite unpacker.

# Usage

Just run ```atdf_bitfields.py -f <yourfile>.atdf``` to dump all registers and their bitfield to the console in the short format which will look like:

```c
...
/// Module USART - USART
/// Register group USART0 - USART
/// Register UDR0 - USART I/O Data Register 0
UDR0 = ;
/// Register UCSR0A - USART Control and Status Register A
UCSR0A = (0<<RXC0) | (0<<TXC0) | (0<<UDRE0) | (0<<FE0) | (0<<DOR0) | (0<<UPE0) | (0<<U2X0) | (0<<MPCM0);
/// Register UCSR0B - USART Control and Status Register B
...
```

Using the switch ```-d``` prints the detailed descriptions (where available) - so ```atdf_bitfields.py -f <yourfile>.atdf -d``` will output:

```c
...
/// Module USART - USART
/// Register group USART0 - USART
/// Register UDR0 - USART I/O Data Register 0
UDR0 = 
/// Register UCSR0A - USART Control and Status Register A
UCSR0A = 
      (0<<RXC0) // USART Receive Complete
    | (0<<TXC0) // USART Transmitt Complete
    | (0<<UDRE0) // USART Data Register Empty
    | (0<<FE0) // Framing Error
    | (0<<DOR0) // Data overRun
    | (0<<UPE0) // Parity Error
    | (0<<U2X0) // Double the USART transmission speed
    | (0<<MPCM0); // Multi-processor Communication Mode
...
```

That's all for the script's parameters. If you want to have it as a c-file, redirect the output, if you want to only get one register, pipe it to findstr (windows) or grep (linux) - for obvious reasons this only works for the non-detailed output.

# Limitations

The script is not thorougly tested, what was observed so far:

* Doesn't work with structured registers (e.g. ```PORTB.DIRSET```) as used with the XMega and newer XMega2-based AVRs
* Registers without bitfields will generate invalid code
* Some bit names can't be generated properly (seems to be a deficiency in the atdf files)
* Enums for value groups aren't supported yet
