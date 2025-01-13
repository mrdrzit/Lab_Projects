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
  output = replace(output, "\\", "/");

Dialog.create("Values to cut the z-stack and remove the background");
Dialog.addMessage("Rolling to be used:\nminimum = 0");
Dialog.addNumber("Value for NeuN:", 100);

Dialog.show();

number_slices = 0;
rolling_neun = Dialog.getNumber();

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
    atual = i + 1;
 
    print("\nI'm processing the photo " + list_file_names[i] + " for you");
    current_image = dir + list_file_names[i];
    name_to_save = File.getNameWithoutExtension(list_file_names[i]);
    open(current_image);
    opened_incorrectly = is("composite");
    if (opened_incorrectly) {
        waitForUser("The image " + current_image + " was not opened correctly\nProbably the stack wasn't divided into separate filters. Please, check the bio-formats configuration and re-run the script");
        run("Close All");
        exit();
    }
}