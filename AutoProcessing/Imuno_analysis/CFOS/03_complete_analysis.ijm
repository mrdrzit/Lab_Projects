image_bit_depth = bitDepth();
run("Input/Output...", "jpeg=100 gif=-1 file=.csv use_file save_column");

if(!(is("global scale"))){
  waitForUser("The scale is probably not set\nOr at least is not global");
  exit("Please, adjust the scale and also set it as global!");
}

name = File.getNameWithoutExtension(getTitle);
directory = getDir("image");

if(image_bit_depth != 8){
  selectWindow(getTitle);
  setOption("ScaleConversions", true);
  run("8-bit");
  waitForUser("The image is probably not in 8bit\nI tried to convert it, but check nonetheless! :)");
}

save_path = directory + name + ".roi";
saveAs("Selection", save_path);

run("Measure");
String.copy(d2s(getResult("Area"), 3));

run("Clear Outside");

waitForUser("Check if the region outside of the selection was cleared\nIf so, click OK to continue to background subtraction.");

run("Subtract Background...", "rolling=50 light");

waitForUser("Check if the backgound was substracted\nIf so, click OK to continue to thresholding.");

run("Threshold...");
setThreshold(0, 207);

waitForUser("Check the threshold, apply it, paste results in excel\nAnd if everything is ok, press OK");

if (isOpen("Results")){
  selectWindow("Results"); 
  run("Close");
}

run("Analyze Particles...", "size=25-100 circularity=0.40-1.00 show=Masks display summarize add");

id = getImageID();
selectImage(id);
directory = File.directory;

name = File.getNameWithoutExtension(getTitle);
save_directory = directory + name + ".tif";
saveAs("Tiff", save_directory);

close("Results");

Table.rename("Summary", "Results");

selectWindow("Results");

//Table.deleteColumn("Slice");

Table.update;

String.copyResults;

waitForUser("Please, check:\n- If the mask was saved\n- If you pasted the results into the excel table\n- If everything's in order, then press OK to continue!");

if (isOpen("Results")){
  selectWindow("Results"); 
  run("Close");
}
if (isOpen("Log")){
  selectWindow("Log");
  run("Close");
}
while (nImages()>0){
  selectImage(nImages());  
  run("Close");
}

if (isOpen("ROI Manager")) {
  close("ROI Manager");
}

waitForUser("Finished\nLets go to the next one! :)");

// Listening to: ??????? salyu × salyu GHOST IN THE SHELL ARISE

