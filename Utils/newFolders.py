import os

d = 5
parent_dir = "C:\\Users\\b7079552\\OneDrive - Newcastle University\\PhD\\Data\\22-11-25-ExhibitionPark\\Images\\Lime\\"

for i in range(len(os.listdir(parent_dir))):
    folder = "d" + str(d)
    print(folder)
    os.mkdir(os.path.join(parent_dir, folder))
    print("Folder created")
    if d == df:
        break
    else:
        d += 1