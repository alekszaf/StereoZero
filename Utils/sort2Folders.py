import os
import shutil
""
#parent_dir = "C:/Users/b7079552/OneDrive - Newcastle University/PhD/Data/22-11-08-Branches/Images/"

#m2folder = "C:/Users/b7079552/OneDrive - Newcastle University/PhD/Data/22-11-08-Branches/Images/3280x2464"
#m4folder = "C:/Users/b7079552/OneDrive - Newcastle University/PhD/Data/22-11-08-Branches/Images/1640x1232"

#d = 10

def create_folders(d, df, parent_dir):
    for i in range(len(os.listdir(parent_dir))):
        folder = "d" + str(d)
        os.mkdir(os.path.join(parent_dir, folder))
        if d == df:
            break
        else:
            d += 1
            
create_folders(5, 15, "C:/Users/b7079552/OneDrive - Newcastle University/PhD/Data/22-11-25-ExhibitionPark/Images/Lime/")

def sort_files(parent_dir):
    for file in os.listdir(parent_dir):
        if 'm2' in file:
        #     if not os.path.exists("3280x2464"):
        #         m2folder = os.mkdir(os.path.join(parent_dir, m2folder))
        #         shutil.move(os.path.join(parent_dir, file), m2folder)
        #     else:
            shutil.move(os.path.join(parent_dir, file), m2folder)
        if 'm4' in file:
            # if not os.path.exists(os.path.join(parent_dir, m4folder)):
            #     m4folder = os.mkdir(os.path.join(parent_dir, m4folder))
            #     shutil.move(os.path.join(parent_dir, file), m4folder)
            # else:
            shutil.move(os.path.join(parent_dir, file), m4folder)
        
