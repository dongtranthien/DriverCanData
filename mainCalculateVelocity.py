f = open("input.txt", "r")
fOut = open("output.txt", "w")
doc = f.read()
docSplit = doc.split("\n")

filterIdentifier = True
dataOnly = "601"
getOnly = False # variable for running
strWrite = ""
dataFieldIndex = 0
identifier = ""
data0 = ""
data1 = ""
data2 = ""
data3 = ""
first1 = True
first2 = True
encoderPre1 = 0
encoderPre2 = 0
timePre1 = 0
timePre2 = 0
time = ""
writeTimeDebug = False
for i in range(1, len(docSplit) - 1):
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
        break
      index = index + 1
    datTemp = dat[index:len(dat)]
    if datTemp == "581" or datTemp == "582":
      getOnly = True
      if find:
        strWrite = strWrite + dat[index:len(dat)]
      else:
        strWrite = strWrite + "000"
      strWrite = strWrite + ","
      identifier = datTemp
      time = lineSplit[2]
    else:
      getOnly = False
      strWrite = ""
      print('2')
  elif lineSplit[1] == '"control_field"' and ((filterIdentifier == False) or (getOnly == True)):
    dat = lineSplit[5]
    index = 2
    find = False
    while index < len(dat):
      if dat[index] != '0':
        find = True
        break
      index = index + 1
    if dat[index:len(dat)] == "8":
      strWrite = strWrite + "8,"
      dataFieldIndex = 0
    else:
      print('2')
      getOnly = False
      strWrite = ""
  elif lineSplit[1] == '"data_field"' and ((filterIdentifier == False) or (getOnly == True)):
    dat = lineSplit[6]
    index = 2
    find = False
    while index < len(dat):
      if dat[index] != '0':
        find = True
        break
      index = index + 1
    if(dataFieldIndex == 0):
      if dat[index:len(dat)] == "43":
        strWrite = strWrite + "43,"
        dataFieldIndex = dataFieldIndex + 1
      else:
        print('3')
        getOnly = False
        strWrite = ""
    elif(dataFieldIndex == 1):
      if dat[index:len(dat)] == "64":
        strWrite = strWrite + "64,"
        dataFieldIndex = dataFieldIndex + 1
      else:
        print('4')
        getOnly = False
        strWrite = ""
    elif(dataFieldIndex == 2):
      if dat[index:len(dat)] == "60":
        strWrite = strWrite + "60,"
        dataFieldIndex = dataFieldIndex + 1
      else:
        print('5')
        getOnly = False
        strWrite = ""
    else:
      temp = ""
      if find:
        temp = dat[index:len(dat)]
        if len(temp) == 1:
          temp = "0" + temp
        strWrite = strWrite + dat[index:len(dat)]
      else:
        temp = "00"
        strWrite = strWrite + "00"

      if dataFieldIndex == 4:
        data0 = temp
      elif dataFieldIndex == 5:
        data1 = temp
      elif dataFieldIndex == 6:
        data2 = temp
      elif dataFieldIndex == 7:
        data3 = temp
      strWrite = strWrite + ","

      dataFieldIndex = dataFieldIndex + 1
  elif lineSplit[1] == '"crc_field"' and ((filterIdentifier == False) or (getOnly == True)):
    fOut.write(strWrite)
    strWrite = ""
  elif lineSplit[1] == '"can_error"' and ((filterIdentifier == False) or (getOnly == True)):
    fOut.write("Err,\n")
  elif lineSplit[1] == '"ack_field"' and ((filterIdentifier == False) or (getOnly == True)):
    if lineSplit[8] == "true":
      fOut.write("ACK,")
    else:
      fOut.write("NAK,")
    
    data32Bit = data3 + data2 + data1 + data0
    fOut.write(data32Bit)
    fOut.write(",")
    x = int(data32Bit, 16)
    fOut.write(str(x))
    fOut.write(",")

    timeTemp = float(time)

    if identifier == "581":
      if first1:
        encoderPre1 = x
        fOut.write("0")
        first1 = False
        fOut.write(",")
        fOut.write(time)
        timePre1 = timeTemp
        fOut.write(",")
        fOut.write("0")
      else:
        delta = x - encoderPre1
        fOut.write(str(delta))
        encoderPre1 = x
        if writeTimeDebug:
          fOut.write(",")
          fOut.write(time)

        delta1 = timeTemp - timePre1
        if writeTimeDebug:
          fOut.write(",")
          fOut.write(str(delta1))
        timePre1 = timeTemp

        velocityTemp = delta/delta1
        fOut.write(",")
        fOut.write(str(velocityTemp))
    else:
      if first2:
        encoderPre2 = x
        fOut.write("0")
        first2 = False
        fOut.write(",")
        fOut.write(time)
        timePre2 = timeTemp
        fOut.write(",")
        fOut.write("0")
      else:
        delta = x - encoderPre2
        fOut.write(str(delta))
        encoderPre2 = x
        if writeTimeDebug:
          fOut.write(",")
          fOut.write(time)
        delta1 = timeTemp - timePre2
        timePre2 = timeTemp
        if writeTimeDebug:
          fOut.write(",")
          fOut.write(str(delta1))

        velocityTemp = delta/delta1
        fOut.write(",")
        fOut.write(str(velocityTemp))
    
    fOut.write("\n")



    
fOut.close()