// Sets up the working space for the analysis by closing all the open images
print("\\Clear");
run("Close All");
setOption("ExpandableArrays", true);

dir = getDirectory("Where are your photos?");
dir = replace(dir, "\\", "/"); // Fixes the name of the directory in windows machines, inserting a '/'
output = replace(output, "\\", "/");

list_file_names = getFileList(dir); //Gives a list with the filenames in the selected directory
var list_file_names = Array.sort(list_file_names);

for (i = 0; i < list_file_names.length; i++) { //Loop to select only .zvi images
  if (File.isDirectory(dir + File.separator + list_file_names[i])) {
    exit("Remove everything from the folde containing the images to be analyzed, inclunding subfolders");
  }
}

Array.sort(list_file_names);
qtd = list_file_names.length //The number of times that i'll iterate the loop

// This line sets these options in the set measurements window
// - bounding rectangle
// - Area
// - Mix and max gray value
// - Area fraction 
// - Limit to threshold 
run("Set Measurements...", "area min bounding area_fraction limit redirect=None decimal=3");
run("Input/Output...", "jpeg=100 gif=-1 file=.csv use_file save_column");

for (i = 0; i < qtd; i++) {
    showProgress(i, qtd);
    atual = i + 1;
  
    print("\nI'm processing the photo " + list_file_names[i] + " for you");
    current_image = dir + list_file_names[i];
    name_to_save = File.getNameWithoutExtension(list_file_names[i]);
    open(current_image);

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

    // we need an image in 8-bit so here i check if the current image
    // is in this bit-depth. If not i try to convert it
    if(image_bit_depth != 8){
    selectWindow(getTitle);
    setOption("ScaleConversions", true);
    run("8-bit");
    waitForUser("The image is probably not in 8bit\nI tried to convert it, but check nonetheless! :)");
    }

    // Now that we have the index to input at the threshold, use it to process the image 
    run("Threshold...");
    setThreshold(28, 255, "red dark");
    waitForUser("Check if the threshold was set\nIf so, click OK to continue.");
    close("Threshold");

    run("Analyze Particles...", "size=2-Infinity show=Masks display summarize");
    Table.rename("Summary", "Results");
    selectWindow("Results");
    String.copyResults();
    waitForUser("Make sure that the analyze particles results are pasted into excel\nIf so, click OK to continue");
    close("Results");

    open_windows = getList("image.titles");
    for (j = 0; j < open_windows.length; j++){
      if (startsWith(open_windows[j], "Mask")){
        selectWindow(open_windows[j]);
        saveAs("Tiff", dir + name_to_save + "_Mask_" + (i+1) +".tif");
        open_windows = getList("image.titles");
        close(open_windows[j]);
      }
    }
}
