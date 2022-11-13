import os

folder = r'C:/Users/b7079552/OneDrive - Newcastle University/PhD/Data/22-06-30-Cactus/Images/R_b24_3280x2464_CACT/'
count = 40

# iterate all files from a directory
for file_name in os.listdir(folder):
    
    # Construct old file name
    source = folder + file_name

    # Adding the count to the new file name and extension
    destination = folder + "L_b24_d" + str(count) + "_m2.png"

    # Renaming the file
    os.rename(source, destination)
    
    # Increase the count by 10
    count += 10
    
print('All Files Renamed')

print('New Names are')
# Verify the result
res = os.listdir(folder)
print(res)
