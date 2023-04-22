// Sets up the working space for the analysis by closing all the open images
print("\\Clear");
run("Close All");
setOption("ExpandableArrays", true);

dir = File.openDialog("Where is the photo to analyze?");
dir = replace(dir, "\\", "/"); // Fixes the name of the directory in windows machines, inserting a '/'
run("Bio-Formats Importer", "open=[" + dir + "] autoscale color_mode=Default rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT");

// This line sets these options in the set measurements window
// - bounding rectangle
// - Area
// - Mix and max gray value
// - Area fraction 
// - Limit to threshold 
run("Set Measurements...", "area min bounding area_fraction limit redirect=None decimal=3");

// Get the image bit depth
image_bit_depth = bitDepth();

// ------ Little loop to check if the scale is correctly set to 1.9520 um/pixel ------
Image_info = split(getImageInfo(), '\n');
Resolution_info = 0;
for (i = 0; i < Image_info.length; i++) {
    if (startsWith(Image_info[i], "Resolution")) {
        Resolution_info = Image_info[i];
        break;
    }
}
if (Resolution_info == 0) {
  waitForUser("Are you sure that this is a .zvi file with a z-stack?");
  exit("Could not process this image, you'll have to do it manually :(")
}
// -----------------------------------------------------------------------------------

// See if the scale is set and if it is global
if((!(is("global scale"))) || (indexOf(Resolution_info, "1.9520") == -1)){
  tmp = getList("image.titles");
  if (tmp.length == 0){
    run("Blobs");
  }
  waitForUser("The scale is probably not set\nOr at least is not global\nLet's try to set it, but check it and restart this image anyway!");
  scale = getNumber("Known distance (um/pixels):", 0.5123);
  run("Set Scale...", "distance=1 known="+scale+" unit=um global");
  exit("Now, check that the scale is correctly set to 1.9520 pixels/microns after this window closes and restart the analysis on this image!");
}

// // This is just setting the name and directory for input/output
// name = File.getNameWithoutExtension(getTitle);
// directory = getDir("image");

// we need an image in 8-bit so here i check if the current image
// is in this bit-depth. If not i try to convert it
if(image_bit_depth != 8){
  selectWindow(getTitle);
  setOption("ScaleConversions", true);
  run("8-bit");
  waitForUser("The image is probably not in 8bit\nI tried to convert it, but check nonetheless! :)");
}

// ----------- Block of code to remove the first and last 3 images from the z-stack -----------------

// get the number of slices in the stack
stack_size = nSlices;

// if the number of slices is 1, then the image is not a z-stack
if (stack_size == 1){
  exit("This image is probably not a z-stack\nCan you check it and restart the analysis?");
}

// calculate the number of slices in the stack and the number of slices to remove
n_inicial = 4;
n_final = stack_size - 3;
// --------------------------------------------------------------------------------------------------

// Selects the window and runs the Z-project removing the first and last 3 slices and creating the max intensity projection
selectWindow(getTitle);
Original_image_title = getTitle;
Original_image_dir = File.getDirectory(Original_image_title);
if (stack_size > 4){
  run("Z Project...",  "start=" + n_inicial + " stop="+n_final + " projection=[Max Intensity]");
}else{
  run("Z Project...",  "start=0 "+ " stop=" + stack_size + " projection=[Max Intensity]");
}
close(Original_image_title);
selectWindow(getTitle);

// Subtract the background from the image
run("Subtract Background...", "rolling=10");
waitForUser("Check if the backgound was substracted correctly\nIf so, click OK to continue to thresholding.");

// Now that we have the index to input at the threshold, use it to process the image 
run("Threshold...");
setAutoThreshold("Default dark no-reset");
waitForUser("Check if the threshold was set\nIf so, click OK to continue.");
close("Threshold");

//Check back later to see if this is necessary and will not remove unncecessary data
//run("Remove Outliers...", "radius=10 threshold=50 which=Dark");
// waitForUser("Check if the outliers were removed\nIf so, click OK to continue to particle analysis.");

//Open the ROIs that Bia created before
dir = File.openDialog("Where is the roi file?");
roiManager("Open", dir);
roiManager("Show All with labels");
run("ROI Manager...", "select all");
waitForUser("Check if the ROIs are at the desired location\nYou can click the number to select drag them around withtout using the ROI manager\nAlso check if they are all showing\nWhen everything is in order, click OK to continue to particle analysis.");

// Here we are saving the ROIs created during the analysis as a form of backup
file_name = File.getNameWithoutExtension(Original_image_title);
save_path = Original_image_dir + file_name + "_rois.zip";
roiManager("save", save_path)

// After creating the backup we analyzed the area of the ROI to begin the analysis
// and then saved the results in the clipboard to paste in an excel window kept opened
number_of_ROIs =  RoiManager.size();
for(i = 0; i < number_of_ROIs; i++){
  roiManager("Select", i);
  run("Measure");
  String.copyResults();
  waitForUser("Make sure that the ROI measure results are pasted into excel\nIf so, click OK to continue");
  selectWindow("Results");
  close("Results");
  run("Analyze Particles...", "size=2,23-Infinity show=Masks display summarize");
  Table.rename("Summary", "Results");
  selectWindow("Results");
  String.copyResults();
  waitForUser("Make sure that the analyze particles results are pasted into excel\nIf so, click OK to continue");
  close("Results");
  open_windows = getList("image.titles");
  for (j = 0; j < open_windows.length; j++){
    if (startsWith(open_windows[j], "Mask")){
      selectWindow(open_windows[j]);
      saveAs("Tiff", Original_image_dir + file_name + "_Mask_" + (i+1)+".tif");
      open_windows = getList("image.titles");
      close(open_windows[j]);
    }
  }
  waitForUser("Double check that the results are pasted into excel\nIf so, click OK to continue to the next ROI.\nAnd, Tecedor Senpai, onegaishimasu, close the mask window if it's not closed yet.");
}

waitForUser("Please, check:\n- If the masks were saved\n- If you pasted the results into the excel table\n- If everything's in order, then press OK to continue!");

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

waitForUser("Finished\nLets go to the next one! :)");

// Listening to: Sorriso contagiante - Yuyu Hakusho 

