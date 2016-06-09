import csv

potbyblock = dict()
with open('potholes.csv') as f:
    for row in csv.DictReader(f):
        addr = row['STREET ADDRESS'] 
        try:
            num = int(row['NUMBER OF POTHOLES FILLED ON BLOCK'])
        except ValueError:
            num = 0
        addparts = addr.split()
        #Simplify the number part of street address (1246 -> 1200, 36 -> 0)
        try:
            addparts[0] = str(int(addparts[0])//100*100)
        except IndexError:
            print('No address:', addr)
        except ValueError:
            addparts.insert(0, '0')
        addr = ' '.join(addparts)
        if addr in potbyblock:
            potbyblock[addr] += num
        else:
            potbyblock[addr] = num

lastblock = None
laststreet = None
blockrun = 0
blocklen = 0
biggestrun = 0
for b in sorted((k.split() for k in potbyblock.keys()), key=lambda x: (x[1:], x[0])):
    thisstreet = ' '.join(b[1:])
    blocknum = int(b[0])
    if thisstreet != laststreet:
        blockrun = 0
    

