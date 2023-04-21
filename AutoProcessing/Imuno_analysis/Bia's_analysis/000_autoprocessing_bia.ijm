// Set these in the set measurements window
// - bounding rectangle
// - Area
// - Mix and max gray value
// - Area fraction 
// - Limit to threshold 
dir = File.openDialog("Where is the photo to analyze?");
dir = replace(dir, "\\", "/"); // Fixes the name of the directory in windows machines, inserting a '/'
run("Bio-Formats Importer", "open=[" + dir + "] autoscale color_mode=Default rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT");
run("Set Measurements...", "area min bounding area_fraction limit redirect=None decimal=3");

// Get the image bit depth
image_bit_depth = bitDepth();

// This is the command to open a sample image to set the scale
// Because the scale is global, it will be set for all images
// And the program doesn't set scales without images opened
//run("Blobs");
scale = getNumber("Known distance (um/pixels):", 0.5123);
run("Set Scale...", "distance=1 known="+scale+" unit=um global");

// Imagej has a input/output settings that, when creating or importing some
// files, it reads from and sets the configuration for that
// This line is adjusting this to make the program output csv files with a
// header and eliminates the compression on jpeg files

// See if the scale is set and if it is global
if(!(is("global scale"))){
  waitForUser("The scale is probably not set\nOr at least is not global");
  exit("Please, adjust the scale and also set it as global!");
}

// What is this for?
// run("Input/Output...", "jpeg=100 gif=-1 file=.csv use_file save_column");

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

// ----------- Block of code to remove the first and last 3 images from the z-stack -----------------

// if the number of slices is 1, then the image is not a z-stack
stack_size = nSlices;

// calculate the number of slices in the stack
n_inicial = 4;
n_final = stack_size - 3;

if (stack_size == 1){
  exit("Currently the program cannot process\nphotos that aren't a z-stack\nLike the photo "+current_image);
}
selectWindow(getTitle);
run("Z Project...",  "start=" + n_inicial + " stop="+n_final + " projection=[Max Intensity]");
selectWindow(getTitle);
// --------------------------------------------------------------------------------------------------

// Subtract the background from the image
run("Subtract Background...", "rolling=10");
waitForUser("Check if the backgound was substracted\nIf so, click OK to continue to thresholding.");

// Now that we have the index to input at the threshold, use it to process the image 
run("Threshold...");
setAutoThreshold("Default dark no-reset");
waitForUser("Check if the threshold was set\nIf so, click OK to continue.");

//Check back later to see if this is necessary and will not remove unncecessary data
//run("Remove Outliers...", "radius=10 threshold=50 which=Dark");
// waitForUser("Check if the outliers were removed\nIf so, click OK to continue to particle analysis.");

//Open the ROIs that Bia created before
dir = File.openDialog("Where is the roi file?");
roiManager("Open", dir);
roiManager("Show All with labels");
run("ROI Manager...", "select all");
waitForUser("Check if the ROIs are at the desired location\n Also if they are all showing\nIf so, click OK to continue to particle analysis.");

// We were saving the ROIs created during the analysis as a form of backup
directory = File.directory();
name = File.nameWithoutExtension;
save_path = directory + name + ".zip";
roiManager("save", save_path)
//saveAs("Selection", save_path);

// After creating the backup we analyzed the area of the ROI to begin the analysis
// and then saved the results in the clipboard to paste in an excel window kept opened
number_of_ROIs =  RoiManager.size();
for(i = 0; i < number_of_ROIs; i++){
  roiManager("Select", i);
  run("Measure");
  String.copyResults();
  waitForUser("Make sure that the results are pasted into excel\nIf so, click OK to continue to the next ROI.");
  selectWindow("Results");
  close("Results");
  run("Analyze Particles...", "size=2,23-Infinity show=Masks display summarize");
  Table.rename("Summary", "Results");
  selectWindow("Results");
  String.copyResults();
  close("Results");
  waitForUser("Make sure that the results are pasted into excel\nIf so, click OK to continue to the next ROI.\nAnd, Tecedor Senpai, onegaishimasu, close the mask window");
  if (i == 2){
    waitForUser("Let's save this!");
  }
}

// Get the current iamage ID
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

// Listening to: Sorriso contagiante - Versão 

