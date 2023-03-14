import os

folder = r'C:/Users/b7079552/OneDrive - Newcastle University/PhD/Data/22-06-30-Cactus/Images/R_b24_3280x2464_CACT/'
i = 190

# iterate all files from a directory
for file_name in os.listdir(folder):
    
    # Construct old file name
    source = folder + file_name

    # Adding the count (distance) to the new file name and extension, remember to select the correct camera (R or L)
    destination = f"{folder}R_b24_d{str(i)}_m2.png"

    # Renaming the file
    os.rename(source, destination)
    
    # Increase the count (distance) by 10
    i += 10
    
print('All Files Renamed')

print('New Names are')
# Verify the result
res = os.listdir(folder)
print(res)
