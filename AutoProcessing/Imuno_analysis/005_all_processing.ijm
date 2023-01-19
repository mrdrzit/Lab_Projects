// This function is used for calculating the sum of values of the
// histogram_count array.
function get_sum(start, end, histogram_count){
  sum = 0;
  for (i=start; i<end; i++){
    sum = sum + histogram_count[i];
  }
  return sum;
}

// Get the image bit depth
image_bit_depth = bitDepth();

// Imagej has a input/output settings that, when creating or importing some
// files, it reads from and sets the configuration for that
// This line is adjusting this to make the program output csv files with a
// header and eliminates the compression on jpeg files
run("Input/Output...", "jpeg=100 gif=-1 file=.csv use_file save_column");

// See if the scale is set and if it is global
if(!(is("global scale"))){
  waitForUser("The scale is probably not set\nOr at least is not global");
  exit("Please, adjust the scale and also set it as global!");
}

// This is just setting the name and directory for input/output
name = File.getNameWithoutExtension(getTitle);
directory = getDir("image");

// we needed to have an image in 8-bit so here i check if the current image
// is in this bit-depth. If not i try to convert it
if(image_bit_depth != 8){
  selectWindow(getTitle);
  setOption("ScaleConversions", true);
  run("8-bit");
  waitForUser("The image is probably not in 8bit\nI tried to convert it, but check nonetheless! :)");
}

// We were saving the ROIs created during the analysis as a form of backup
save_path = directory + name + ".roi";
saveAs("Selection", save_path);

// After creating the backup we analyzed the area of the ROI to begin the analysis
// and then saved the results in the clipboard to paste in an excel window kept opened
run("Measure");
String.copy(d2s(getResult("Area"), 3));

run("Clear Outside");

waitForUser("Check if the region outside of the selection was cleared\nIf so, click OK to continue to background subtraction.");

run("Subtract Background...", "rolling=50 light");

waitForUser("Check if the backgound was substracted\nIf so, click OK to continue to thresholding.");

// ------------- This bit of code is to get a threshold value closest to 7% --------------- //
// To achieve this i first get the whole histogram and calculate sum of every value and do a 
// simple calculation to find in which value i should set the cutoff at. Then i get the range
// in which i need to set the threshold that grants the 7%.

// This is the number of bins for pixel intensity
bins = 256;
getHistogram(values, counts, bins);

sum = 0;

// Here i just sum all the values to get the 7% value
for(i=0; i<counts.length; i++){
  sum = sum + counts[i];
}

// Because imagej needs a range in which we set the threshold, i need to find which bins i need to
// select that will give me the 7% that i need. So i loop through all combinations of 
// "binZero - endBin" and check if this range is close to the 7% that i want. That's why i go 
// backwards from the ending index to the start with a "j--"
for (j=counts.length; j>0; j--){
  if (get_sum(0, j, counts) <= 0.07 * sum){
    max_hist_cutoff = j;
    break;
  }
}

// this code calculates the maximum histogram cutoff value (max_hist_cutoff) which is the
// point where the histogram is cut-off (i.e. where the histogram is no longer in the 
// top 7% of the histogram) and the point where the histogram is no longer in the bottom
// 7% of the histogram. The code does this by calculating the sum of the histogram values
// to the left of the current histogram value and to the right of the current histogram
// value. Then, it calculates the percentage of the sum of the histogram values to the
// left of the current histogram value and to the right of the current histogram value
// relative to the sum of all histogram values. The point where the percentage is closest
// to 7% is the maximum histogram cutoff value.

desired_threshold = 0.07 * sum;

dist_list = newArray;
J = 0;
L = 20;
for (k=-4; k<4; k++){
  current_histogram_sum_neighbors = get_sum(0, j+k, counts);
  current_percentage = (100 * current_histogram_sum_neighbors)/sum;

  dist = abs(7 - current_percentage);
  
  if (dist < L){
    L = dist;
    max_hist_cutoff = j + k-1;
  }
}

// ------------- This bit of code is to get a threshold value closest to 7% --------------- //

// Now that we have the index to input at the threshold, use it to process the image 
run("Threshold...");
setThreshold(0, max_hist_cutoff);

waitForUser("Check if the threshold was set\nIf so, click OK to continue to outlier removal.");

run("Remove Outliers...", "radius=10 threshold=50 which=Dark");

waitForUser("Check if the outliers were removed\nIf so, click OK to continue to particle analysis.");

if (isOpen("Results")){
  selectWindow("Results"); 
  run("Close");
}
run("Analyze Particles...", "size=10-Infinity show=Masks display summarize add");

// Get the current image ID
id = getImageID();

// Select the current image using the ID that we got
selectImage(id);

// Get the directory where the image is going to be saved
directory = File.directory;

// Get the name of the image
name = File.getNameWithoutExtension(getTitle);

// Create a path with the file name to be saved
save_directory = directory + name + ".tif";

// Save the image
saveAs("Tiff", save_directory);

close("Results");

Table.rename("Summary", "Results");

selectWindow("Results");

//Table.deleteColumn("Slice");

Table.update;

String.copyResults;

waitForUser("Please, check:\n- If the mask was saved\n- If you pasted the results into the excel table\n- If everything's in order, then press OK to continue!");

// Close everything and sets the polygon tool to go to the next image
if (isOpen("Results")){
  selectWindow("Results"); 
  run("Close");
}
if (isOpen("Log")){
  selectWindow("Log");
  run("Close");
}
if (isOpen("ROI Manager")){
  selectWindow("ROI Manager");
  run("Close");
}
while (nImages()>0){
  selectImage(nImages());  
  run("Close");
}

setTool("polygon");
waitForUser("Finished\nLets go to the next one! :)");

// Listening to: ??????? salyu × salyu GHOST IN THE SHELL ARISE