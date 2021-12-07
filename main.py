f = open("input.txt", "r")
fOut = open("output.txt", "w")
doc = f.read()
docSplit = doc.split("\n")

print(docSplit[len(docSplit) - 2])
filterIdentifier = True
dataOnly = "601"
getOnly = False # variable for running
for i in range(1, len(docSplit) - 1):
  #print(i)
  line = docSplit[i]
  lineSplit = line.split(',')
  #print(lineSplit)
  if lineSplit[1] == '"identifier_field"':
    #print(i)
    dat = lineSplit[4]
    index = 2
    find = False
    while index < len(dat):
      if dat[index] != '0':
        find = True
        break;
      index = index + 1
    if filterIdentifier:
      datTemp = dat[index:len(dat)]
      if datTemp == dataOnly:
        getOnly = True
        if find:
          fOut.write(dat[index:len(dat)])
        else:
          fOut.write("000")
        fOut.write(",")
      else:
        getOnly = False
    else:
      if find:
        fOut.write(dat[index:len(dat)])
      else:
        fOut.write("000")
      fOut.write(",")
  elif lineSplit[1] == '"control_field"' and ((filterIdentifier == False) or (getOnly == True)):
    dat = lineSplit[5]
    index = 2
    find = False
    while index < len(dat):
      if dat[index] != '0':
        find = True
        break;
      index = index + 1
    if find:
      fOut.write(dat[index:len(dat)])
    else:
      fOut.write("000")
    fOut.write(",")
  elif lineSplit[1] == '"data_field"' and ((filterIdentifier == False) or (getOnly == True)):
    dat = lineSplit[6]
    index = 2
    find = False
    while index < len(dat):
      if dat[index] != '0':
        find = True
        break;
      index = index + 1
    if find:
      fOut.write(dat[index:len(dat)])
    else:
      fOut.write("000")
    fOut.write(",")
  elif lineSplit[1] == '"crc_field"' and ((filterIdentifier == False) or (getOnly == True)):
    pass
  elif lineSplit[1] == '"can_error"' and ((filterIdentifier == False) or (getOnly == True)):
    fOut.write("Err,\n")
  elif lineSplit[1] == '"ack_field"' and ((filterIdentifier == False) or (getOnly == True)):
    if lineSplit[8] == "true":
      fOut.write("ACK,\n")
    else:
      fOut.write("NAK,\n")
    
fOut.close()