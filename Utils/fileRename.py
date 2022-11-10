import os

folder = r'C:/Users/b7079552/OneDrive - Newcastle University/PhD/Camera calibration/2022/Aug22/R_b10_6-08-22/'
count = 1
# count increase by 1 in each iteration
# iterate all files from a directory
for file_name in os.listdir(folder):
    # Construct old file name
    source = folder + file_name

    # Adding the count to the new file name and extension
    destination = folder + "frame_" + str(count) + ".png"

    # Renaming the file
    os.rename(source, destination)
    count += 1
print('All Files Renamed')

print('New Names are')
# verify the result
res = os.listdir(folder)
print(res)