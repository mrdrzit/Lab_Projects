function copyImages(images, sourceDir, targetDir) {
    for (i = 0; i < images.length; i++) {
      File.copy(sourceDir + images[i], targetDir + "/" + images[i]);
    }
  }
  
  function stitchAndSaveImages(folder, nameToSave, regressionThreshold) {
    run("Grid/Collection stitching", "type=[Unknown position] order=[All files in directory] directory=[" + folder + "] output_textfile_name=TileConfiguration.txt fusion_method=[Linear Blending] regression_threshold=" + regressionThreshold + " max/avg_displacement_threshold=2 absolute_displacement_threshold=3.00 computation_parameters=[Save computation time (but use more RAM)] image_output=[Fuse and display]");
    selectWindow("Fused");
    fullFilePath = folder + File.separator + nameToSave + "_panorama.tif";
    saveAs("PNG", fullFilePath);
    close();
  }
  
print("\\Clear");
run("Close All");
setOption("ExpandableArrays", true);
run("Input/Output...", "jpeg=100 gif=-1 file=.csv use_file save_column");
run("Set Measurements...", "area centroid bounding limit redirect=None decimal=3");

  // See if the scale is set and if it is global
if(!(is("global scale"))){
    run("Blobs");
    waitForUser("The scale is probably not set\nOr at least is not global\n\nIn the next window, please enter the scaling factor.\nTip: The known distance for 20x magnification is 0.5123 um/pixel\nAfter this, check nonetheless! :)");
    scale = getNumber("Known distance (um/pixels):", 0.5123);
    run("Set Scale...", "distance=1 known="+scale+" unit=um global");
    close("*");
    exit("Don't forget to also set it as global if it was not set properly automatically!");
  }
  
dir = getDirectory("Where are your photos?");
dir = replace(dir, "\\", "/"); // Fixes the name of the directory in windows machines, inserting a '/'
output = dir;

Dialog.create("Values to cut the z-stack and remove the background");
Dialog.addMessage("Rolling to be used:\nminimum = 0");
Dialog.addNumber("Value for Green filter:", 30);

Dialog.show();

number_slices = 0;
rolling_green = Dialog.getNumber();

list_file_names = getFileList(dir); //Gives a list with the filenames in the selected directory
list_file_names = Array.sort(list_file_names);

// Check if all files in the folder are in the .zvi format
for (i = 0; i < list_file_names.length; i++) { //Loop to select only .zvi images
    if (File.isDirectory(dir + File.separator + list_file_names[i])) {
      exit("You need to select inside of the folder containing the images");
    }
    if (!(endsWith(list_file_names[i], ".zvi"))) {
      exit("All files need to be in the .zvi format");
    }
  }

Array.sort(list_file_names);
qtd = list_file_names.length; //The number of times that i'll iterate the loop

//Loop that actually processess the images
for (i = 0; i < qtd; i++) {
  showProgress(i, qtd);
  print("\nI'm processing the photo " + list_file_names[i] + " for you");
  current_image = dir + list_file_names[i];
  name_to_save = File.getNameWithoutExtension(list_file_names[i]);
  atual = i + 1;
  if (atual == 1) {
    open(current_image);
  }else{
    run("Bio-Formats Importer", "open=[" + current_image + "] autoscale color_mode=Default rois_import=[ROI manager] split_channels view=Hyperstack stack_order=XYCZT"); 
  }

  // ----------- Block of code to remove the first and last n images from the z-stack -----------------

  // get the number of slices in the stack
  stack_size = nSlices;

  // if the number of slices is 1, then the image is not a z-stack
  if (stack_size == 1){
    exit("This image is probably not a z-stack\nCan you check it and restart the analysis?");
  }
  // calculate the number of slices in the stack and the number of slices to remove
  n_inicial = number_slices + 1;
  n_final = stack_size - number_slices;
  // --------------------------------------------------------------------------------------------------

  run("Show All"); //This always has to come before to be sure that all the images are on the foreground to be able to be selected (a.k.a: Aren't minimized)
  list_open_filters = getList("image.titles"); //Re-create the array because the compression operation on the z-stack changes the imagename

  stack_size = nSlices;
  if (stack_size == 1) {
    exit("Currently the program cannot process\nphotos that aren't a z-stack\nLike the photo " + current_image);
  }

  run("Z Project...", "start=" + n_inicial + " stop=" + n_final + " projection=[Max Intensity]");

  // Background subtraction and image processing
  allExceptMax = getList("image.titles");
  for (k = 0; k < allExceptMax.length; k++) {
    if (!(startsWith(allExceptMax[k], "MAX"))) {
      close(allExceptMax[k]);
    } 
    else {
      run("Subtract Background...", "rolling=" + rolling_green);
      setOption("ScaleConversions", true);
      run("8-bit");
    }
  }
  
  run("Show All"); //This always has to come before to be sure that all the images are on the foreground to be able to be selected (a.k.a: Aren't minimized)
  list_open_filters = getList("image.titles"); //Re-create the array because the compression operation on the z-stack changes the imagename
  Array.sort(list_open_filters);
  blur_green = list_open_filters[0];

  selectImage(blur_green);
  run("Duplicate...", "title=blur");
  run("Gaussian Blur...", "sigma=15");

  imageCalculator("Subtract create", list_open_filters[0],"blur");
  selectWindow("Result of " + list_open_filters[0]);
  saveAs("PNG", output + name_to_save);
  waitForUser("Please, now create the ROI for the image selecting the areas to be analyzed and press OK");

  run("Threshold...");
  setAutoThreshold("Default dark no-reset");
  setOption("BlackBackground", true);
  setThreshold(20, 255);

  waitForUser("Check if the threshold was set\nIf so, click OK to continue");

  run("Convert to Mask");
  run("Fill Holes");
  run("Remove Outliers...", "radius=2 threshold=50 which=Bright");
  run("Watershed");

  continue_analysis = true;
  mask_number = 0;
  while (continue_analysis) {
    waitForUser("Please drag the pre-created mask for the area to be analyzed into the ImageJ window and press OK to continue.");
    roi_name = File.nameWithoutExtension;

    // Perform the analysis
    run("Measure");
    selectWindow("Results");
    Table.update;

    num_rows_in_table = Table.size;
    if (num_rows_in_table > 1){
        waitForUser("Please close the results table and press OK. There can be only one row in the table, that is, for the current ROI.");
        run("Measure");
        Table.rename("Summary", "Results");
        selectWindow("Results");
        Table.update;
    }else{
        roi_area = Table.get("Area", 0);
        String.copy(roi_area);
        waitForUser("The ROI area is on the clipboard, please paste it into excel, check to see if its the correct value as shown in the results/summary table and, if yes, press OK to continue.\nTip: Excel will have the decimals separated by a dot and the thousands separated by a comma if the language is set to Portuguese.\nSo to properly paste it, you need to change this configuration or convert it manually");
        if (isOpen("Results")){
            selectWindow("Results"); 
            close("Results");
        }
    }

    run("Analyze Particles...", "size=10-1500 circularity=0.00-1.00 show=Masks clear summarize");
    Table.rename("Summary", "Results");
    selectWindow("Results");
    Table.update;
    waitForUser("Please check if the mask is matches the ROI currently being analyzed and press OK to continue. if not, please re-run the analyze particles with the adjusted parameters before continuing.");
    selectWindow("Results");
    Table.update;

    num_rows_in_table = Table.size;
    if (num_rows_in_table > 1){
        waitForUser("Please close the results table and press OK. There can be only one row in the table, that is, for the current ROI.")
        run("Measure");
        Table.rename("Summary", "Results");
        selectWindow("Results");
        Table.update;
    }else{
        count = Table.get("Count", 0);
        String.copy(count);
        waitForUser("The number of cells counted is on the clipboard, please paste it into excel.\nCheck to see if its the correct value as shown in the results/summary table and, if yes,\npress OK to continue.");
        if (isOpen("Results")){
            selectWindow("Results"); 
            close("Results");
        }
    }

    selectImage("Mask of " + name_to_save + ".png");
    saveAs("PNG", output + name_to_save + "_mask" + mask_number + ".png");
    close(name_to_save + "_mask.png");

    // Close everything and go to the next image
    if (isOpen("Results")){
        selectWindow("Results"); 
        run("Close");
    }
    if (isOpen("Log")){
        selectWindow("Log");
        run("Close");
    }
    run("Select None");

    // Ask if the user wants to continue analyzing more areas 
    continue_analysis = getBoolean("Do you want to analyze more areas?");
    mask_number++;

    run("Show All");
    list = getList("image.titles");
    Array.sort(list);
  
    for (p = 0; p < list.length; p++) {
      if (indexOf(list[p], "blur") > -1) {
        close(list[p]);
      }
      else if (indexOf(list[p], "MAX") > -1) {
        close(list[p]);
      }
      else if (indexOf(list[p], "mask") > -1) {
        close(list[p]);
      }else{
        continue;
      }
    }
  }
}


// Close All Open Windows
run("Close All");

// Close Additional Windows if Open
if (isOpen("Results")) {
  selectWindow("Results");
  run("Close");
}
if (isOpen("Log")) {
  selectWindow("Log");
  run("Close");
}
if (isOpen("ROI Manager")) {
  selectWindow("ROI Manager");
  run("Close");
}

// Close Any Remaining Images
while (nImages() > 0) {
  selectImage(nImages());
  run("Close");
}

waitForUser("Finished\nLets go to the next one! :)");