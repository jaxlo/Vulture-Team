print('1 = forward\n2 = left\n3 = right\n4 = stop')
x = int(input('option number 1,2,3, or 4: '))


if x == 1:#forward
    forwardimg = 240
    countf = 0
    while countf != forwardimg:
        f = open('C:\\Users\\reyno\\Downloads\\dataset\\labels.txt', 'a+')
        f.write('\nC:\\Users\\reyno\\Downloads\\dataset\\forward\\blueroadforward' + str(countf) + '.jpg 1')
        countf += 1
        print('written file number: ' +str(countf))
    f.close()
        
       
elif x == 2:#left
    leftimg = 76
    countl = 0
    while countl != leftimg:
        f = open('C:\\Users\\reyno\\Downloads\\dataset\\labels.txt', 'a+')
        f.write('\nC:\\Users\\reyno\\Downloads\\dataset\\turnLeft\\blueroadleft' + str(countl) + '.jpg 2')
        countl += 1
        print('written file number: ' +str(countl))
    f.close()

        
elif x == 3:#right
    rightimg = 146
    countr = 0
    while countr != rightimg:
        f = open('C:\\Users\\reyno\\Downloads\\dataset\\labels.txt', 'a+')
        f.write('\nC:\\Users\\reyno\\Downloads\\dataset\\turnRight\\blueroadright' + str(countr) + '.jpg 3')
        countr += 1
        print('written file number: ' +str(countr))
    f.close()

elif x == 4:#stop
    stopimg = 0
    counts = 0
    while counts != stopimg:
        f = open('C:\\Users\\reyno\\Downloads\\dataset\\labels.txt', 'a+')
        f.write('\nC:\\Users\\reyno\\Downloads\\dataset\\stop\\blueroadstop' + str(counts) + '.jpg 4')
        countr += 1
        print('written file number: ' +str(counts))
    f.close()
    
elif x == 5:#filler
    f = open('C:\\Users\\reyno\\Downloads\\dataset\\labels.txt', 'a+')
    f.write('\nC:\\Users\\reyno\\Downloads\\dataset\\filler\\filler.jpg 0')
    print('filler written')
    f.close()
  
elif x == 6: #test
    testimg = 58
    countt = 0
    while countt != testimg:
        f = open('C:\\Users\\reyno\\Downloads\\dataset\\testlabels.txt', 'a+')
        f.write('\nC:\\Users\\reyno\\Downloads\\dataset\\testRandom\\bluetestrandom' + str(countt) + '.jpg')
        countt += 1
        print('written test file number: ' +str(countt))
    f.close()


