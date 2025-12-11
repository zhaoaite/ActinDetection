This Code is for the paper titled 'Selective vulnerability of cerebral vasculature to NOTCH3 variants in small vessel disease and rescue by phosphodiesterase-5 inhibito'. It is permanently open and free to read/download for the entire research community (no access code is needed).


1.Modify the directory in the BlueAreaCenter2dis_2.py file.

image = cv2.imread("./R153C/R153C_SNAP(Treatment 2)/0" + str(p) + "_R153C_SNAP.png")                      
output_path = "./R153C/result/R153C_SNAP(Treatment 2)/image/0" + str(p) + "_R153C_SNAP.png"         //output the file path and filename of stress fiber edge and blue area
lunkuo_path = "./R153C/result/R153C_SNAP(Treatment 2)/image/outline/0" + str(p) + "_R153C_SNAP.png"      //Output the file path and filename of the binary image for the edge contour:  
dis_csv = "./R153C/result/R153C_SNAP(Treatment 2)/distance/0" + str(p) + "_R153C_SNAP.csv"  // File path and filename of the calculated distances saved to the CSV file  
angle_csv = "./R153C/result/R153C_SNAP(Treatment 2)/angle/0" + str(p) + "_R153C_SNAP.csv"  // File path and filename of the calculated angles saved to the CSV file  
After making the modifications, you can run the script directly.  

2. dis_mean.py 

# set the path  
dis_folder_path = './R153C/result/R153C_SNAP(Treatment 2)/distance'  // Path to the folder where the distance CSV files from BlueAreaCenter2dis_2.py are saved (only the path, not the filename)  
angle_folder_path = './R153C/result/R153C_SNAP(Treatment 2)/angle'   // Path to the folder where the angle CSV files from BlueAreaCenter2dis_2.py are saved (only the path, not the filename)  
output_path = './R153C/result/R153C_SNAP(Treatment 2)/dis_angle'      // Path to save the average distance and angle values (only the path, not the filename)  

3. Spatial_dispersion.py  
Modify:  
```python  
dsp_csv = "./R153C/result/R153C_SNAP(Treatment 2)/Spatial_dispersion.csv"  // Output path for the spatial dispersion results  
```  
Modify:  
```python  
data = pd.read_csv("./R153C/result/R153C_SNAP(Treatment 2)/dis_angle/0" + str(p) + "_R153C_SNAP_averages.csv", header=None)  
```  
to the `output_path` from **dis_mean.py**, including the filename.  

Execution Order:  
First, run **BlueAreaCenter2dis_2.py**, then execute **dis_mean.py**, and finally run **Spatial_dispersion.py**.
