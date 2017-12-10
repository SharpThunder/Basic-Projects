import string,random,os
base = open("base.txt").read()
files = []
i=0
ws = ["data","science","computer","games","software","blender","python","student","teacher","sehir"]
folders = []
for f in range(5):
    path = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(5))
    folders.append(path+"/")
for x in range(25):
    folders.append(folders[random.randint(0,len(folders)-1)]+ ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(5))+"/")
for folder in folders:
    os.makedirs(folder)
while i < len(base):
    newFilename = str(folders[random.randint(0,len(folders)-1)])+''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))
    newFilename += ".txt"
    nf = open(newFilename,'w')
    e1 = random.randint(i, i+60)
    e2 = random.randint(i+60, min(i+100,len(base)))
    for a in range(random.randint(0,len(ws)-1)):
        nf.write(base[i:e1]+" "+ws[a]+" "+base[e1:e2]+" "+ws[a]+" ")
    i = e2 + 200
