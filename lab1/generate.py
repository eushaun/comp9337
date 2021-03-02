size = [2,4,8,16,32,64,128,512,4096,32768,262144,2047152]
text = ''
i = 0
while i < 2047155:
    text += 'A'
    if len(text) in size:
        file = 'text' + str(len(text)) + '.txt'
        with open(file, 'w') as f:
            f.write(text)
    i += 1