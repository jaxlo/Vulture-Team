import glob

folderFilepath = 'C:\\Users\\reyno\\Downloads\\dataset\\CHANGE_THIS_TJ'#change this 
print('Use :'+folderFilepath+' as the folder location?')
x = input('  ENTER for yes\n  Enter an alternative filepath if not: ')

for filename in glob.iglob(folderFilepath+'/*.jpg'):
    ft = open('C:\\Users\\reyno\\Downloads\\dataset\\labels.txt', 'a+')
    ft.write('\nC:\\Users\\reyno\\Downloads\\dataset\\forward\\'+filename)
    print('written file: '+filename)
ft.close()
