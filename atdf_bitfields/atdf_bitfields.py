import sys
import argparse
import xml.etree.ElementTree as ET

def countsetbits(var):
    cnt = 0
    while var:
        cnt += var & 1
        var >>= 1
    return cnt

def convert_atdf(file, detailed=False):

    tree = ET.parse(file)
    root = tree.getroot()

    modules = root.findall("modules/module")

    for md in modules:
        print("/// Module %s - %s" % (md.get("name"), md.get("caption")))

        reggroups = md.findall("register-group")

        for reggroup in reggroups:
            print("/// Register group %s - %s" % (reggroup.get("name"), reggroup.get("caption")))

            regs = reggroup.findall("register")

            for reg in regs:
                print("/// Register %s - %s" % (reg.get("name"), reg.get("caption")))

                bitfields = reg.findall("bitfield")

                if detailed:
                    print("%s = " % (reg.get("name")))

                    for bitfield in bitfields:
                        last = ";" if bitfield == bitfields[-1] else ""
                        first = " " if bitfield == bitfields[0] else "|"

                        mask = int(bitfield.get("mask"), 16)
                        bits = countsetbits(mask)
                        if bits > 1:
                            bitnames = []
                            lsb = bitfield.get("lsb")
                            if lsb is None:
                                lsb = 0
                            else:
                                lsb = int(lsb)
                            for bit in range(bits):
                                
                                bitnames.append("(0<<%s%u)" % (bitfield.get("name"), bits - bit - 1 + lsb))
                            print("    %s %s%s // %s" % (first, " | ".join(bitnames), last, bitfield.get("caption")))
                        else:
                            print("    %s (0<<%s)%s // %s" % (first, bitfield.get("name"), last, bitfield.get("caption")))
                else:
                    chunks = []
                    for bitfield in bitfields:
                        lsb = bitfield.get("lsb")
                        if lsb is None:
                            lsb = 0
                        else:
                            lsb = int(lsb)
                        mask = int(bitfield.get("mask"), 16)
                        bits = countsetbits(mask)
                        if bits > 1:
                            for bit in range(bits):
                                chunks.append("(0<<%s%u)" % (bitfield.get("name"), bits - bit - 1 + lsb))
                        else:
                            chunks.append("(0<<%s)" % bitfield.get("name"))
                    print("%s = %s;" % (reg.get("name"), " | ".join(chunks)))

def main():
    parser = argparse.ArgumentParser(description="Convert ATDF files to Register assignements")
    parser.add_argument("-f", "--file", required=True,
                        help="ATDF file to be converted")
    parser.add_argument("-d", "--detailed", required=False, action="store_true",
                    help="print bitfields per line with description")

    args = parser.parse_args(sys.argv[1:])

    convert_atdf(args.file, args.detailed)

if __name__ == "__main__":
    main()