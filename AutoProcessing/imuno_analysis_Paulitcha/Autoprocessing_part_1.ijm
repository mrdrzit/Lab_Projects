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

//I create a window where the user can indicate which values will be used in the processing

Dialog.create("Values to cut the z-stack and remove the background");
Dialog.addMessage("Rolling to be used:\nminimum = 0");
Dialog.addNumber("Value for dapi:", 35);
Dialog.addToSameRow();
Dialog.addNumber("Value for cfos:", 100);
Dialog.addToSameRow();
Dialog.addNumber("Value for neun:", 35);
Dialog.addMessage("Photos from which hemispheres are in this folder?");
Dialog.addCheckbox("Left hemisphere", true);
Dialog.addToSameRow();
Dialog.addCheckbox("Right hemisphere", true);

Dialog.show();

number_slices = 0;
rolling_Dapi = Dialog.getNumber();
rolling_cfos = Dialog.getNumber();
rolling_neun = Dialog.getNumber();
left_hemisphere_analysis = Dialog.getCheckbox();
right_hemisphere_analysis = Dialog.getCheckbox();

list_file_names = getFileList(dir); //Gives a list with the filenames in the selected directory
list_file_names = Array.sort(list_file_names);

// Get a list of all neun and cfos images in the folder
if (left_hemisphere_analysis){
  left_neun_images = newArray();
  left_cfos_images = newArray();
  left_dapi_images = newArray();
  left_triple_images = newArray();
}else if (right_hemisphere_analysis){
  right_neun_images = newArray();
  right_cfos_images = newArray();
  right_dapi_images = newArray();
  right_triple_images = newArray();
}else{
  exit("Please, select at least one hemisphere to analyze");
}

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

  run("Show All");
  list_open_filters = getList("image.titles"); //Creates an array containing the opened windows's names 

  //Runs a z-stack compression removing the selected range of photos at the start and end of the stack 
  for (j = 0; j < list_open_filters.length; j++) {
    selectWindow(list_open_filters[j]);
    stack_size = nSlices;
    if (stack_size == 1) {
      exit("Currently the program cannot process\nphotos that aren't a z-stack\nLike the photo " + current_image);
    }

    if (n_final < n_inicial) {
      exit("With the amount of slices to remove set, the z-stack will be empty\nPlease, check the values for this slice and try again\nThe name of the photo is " + current_image);
    }

    if (j == 0) {
      print("I'll start at the slice " + n_inicial + "\nand stop at the slice " + n_final + "\nand the photo has " + stack_size + " slices");
    }
    run("Z Project...", "start=" + n_inicial + " stop=" + n_final + " projection=[Max Intensity]");
    selectWindow(list_open_filters[j]);
    close();
  }

  run("Show All"); //This always has to come before to be sure that all the images are on the foreground to be able to be selected (a.k.a: Aren't minimized)
  list_open_filters = getList("image.titles"); //Re-create the array because the compression operation on the z-stack changes the imagename

  //Removes the background
  if (1) {
    filters_to_merge = newArray();
    for (k = 0; k < list_open_filters.length; k++) {
      name_atual = "";
      if ((indexOf(list_open_filters[k], "C=0") >= 0)) {
        selectWindow(list_open_filters[k]);
        run("Subtract Background...", "rolling=" + rolling_Dapi);
        setOption("ScaleConversions", true);
        run("8-bit");
        selectWindow(list_open_filters[k]);
        name_atual = File.getNameWithoutExtension(list_open_filters[k]) + "_MAX_PROJECTION_dapi";
        saveAs("PNG", dir + File.separator + name_atual + ".png");
        filters_to_merge = Array.concat(filters_to_merge, dir + File.separator + name_atual + ".png");
        close();
      }
      else if ((indexOf(list_open_filters[k], "C=1") >= 0)) {
        selectWindow(list_open_filters[k]);
        run("Enhance Contrast", "saturated=0.30");
        run("Apply LUT");
        run("Subtract Background...", "rolling=" + rolling_cfos);

        selectWindow(list_open_filters[k]);
        run("Duplicate...", "title=blur_cfos");
        run("Gaussian Blur...", "sigma=35");

        imageCalculator("Subtract create", list_open_filters[k], "blur_cfos");
        setOption("ScaleConversions", true);
        run("8-bit");

        selectWindow("Result of " + list_open_filters[k]);
        name_atual = File.getNameWithoutExtension(list_open_filters[k]) + "_MAX_PROJECTION_cfos.png";
        close(list_open_filters[k]);
        saveAs("PNG", dir + File.separator + name_atual);
        close();
        filters_to_merge = Array.concat(filters_to_merge, dir + File.separator + name_atual);
        close("blur_cfos");
      }
      else if ((indexOf(list_open_filters[k], "C=2") >= 0)) {
        selectWindow(list_open_filters[k]);
        run("Subtract Background...", "rolling=" + rolling_neun);
        setOption("ScaleConversions", true);
        run("8-bit");
        selectWindow(list_open_filters[k]);
        name_atual = File.getNameWithoutExtension(list_open_filters[k]) + "_MAX_PROJECTION_neun";
        saveAs("PNG", dir + File.separator + name_atual + ".png");
        filters_to_merge = Array.concat(filters_to_merge, dir + File.separator + name_atual + ".png");
        close();
      }
    }
  }

  //Create a composite of the available filters without background 
  for (l = 0; l < filters_to_merge.length; l++) {
    open(filters_to_merge[l]);
  }

  run("Show All"); //This always has to come before to be sure that all the images are on the foreground to be able to be selected (a.k.a: Aren't minimized)
  list_open_filters = getList("image.titles"); //Re-create the array because the compression operation on the z-stack changes the imagename
  Array.sort(list_open_filters);

  run("Merge Channels...", "c1=[" + list_open_filters[2] + "] c2=[" + list_open_filters[1] + "] c3=[" + list_open_filters[0] + "] create keep");

  //Selects all the images and saves the composite as a .PNG for further analysis
  name_atual = name_to_save + "_MERGE_dapi_neun_cfos";

  selectImage("Composite");
  saveAs("PNG", dir + File.separator + name_atual + ".png");

  run("Show All");
  list = getList("image.titles");
  Array.sort(list);

  for (p = 0; p < list.length; p++) {
    if (p == 0) {
      continue;
    } else {
      close(list[p]);
    }
  }
  run("Close All");
}

// -------- Now copy the images to separate folders and stitch them together --------

// Copy the left hemisphere images to the respective directories
list_files = getFileList(dir);

if (left_hemisphere_analysis){
  for(i = 0; i < list_files.length; i++){
    if (endsWith(list_files[i], "/")){
      continue;
    }else if (indexOf(list_files[i], "MAX_PROJECTION_neun.png") >= 0 && list_files[i].endsWith(".png") && indexOf(list_files[i], "E_20") >= 0){
        left_neun_images = Array.concat(left_neun_images, list_files[i]);
    }else if (indexOf(list_files[i], "MAX_PROJECTION_cfos.png") >= 0 && list_files[i].endsWith(".png") && indexOf(list_files[i], "E_20") >= 0){
        left_cfos_images = Array.concat(left_cfos_images, list_files[i]);
    }else if (indexOf(list_files[i], "MAX_PROJECTION_dapi.png") >= 0 && list_files[i].endsWith(".png") && indexOf(list_files[i], "E_20") >= 0){
        left_dapi_images = Array.concat(left_dapi_images, list_files[i]);
    }else if (indexOf(list_files[i], "MERGE_dapi_neun_cfos.png") >= 0 && list_files[i].endsWith(".png") && indexOf(list_files[i], "E_20") >= 0){
        left_triple_images = Array.concat(left_triple_images, list_files[i]);
    }
  }
  left_neun_images = Array.deleteValue(left_neun_images, 0);
  left_cfos_images = Array.deleteValue(left_cfos_images, 0);
  left_dapi_images = Array.deleteValue(left_dapi_images, 0);
  left_triple_images = Array.deleteValue(left_triple_images, 0);
}


if (right_hemisphere_analysis){
  // Copy the right hemisphere images to the respective directories
  for(i = 0; i < list_files.length; i++){
    if (endsWith(list_files[i], "/")){
      continue;
    }else if (indexOf(list_files[i], "MAX_PROJECTION_neun.png") >= 0 && list_files[i].endsWith(".png") && indexOf(list_files[i], "D_20") >= 0){
        right_neun_images = Array.concat(right_neun_images, list_files[i]);
    }else if (indexOf(list_files[i], "MAX_PROJECTION_cfos.png") >= 0 && list_files[i].endsWith(".png") && indexOf(list_files[i], "D_20") >= 0){
        right_cfos_images = Array.concat(right_cfos_images, list_files[i]);
    }else if (indexOf(list_files[i], "MAX_PROJECTION_dapi.png") >= 0 && list_files[i].endsWith(".png") && indexOf(list_files[i], "D_20") >= 0){
        right_dapi_images = Array.concat(right_dapi_images, list_files[i]);
    }else if (indexOf(list_files[i], "MERGE_dapi_neun_cfos.png") >= 0 && list_files[i].endsWith(".png") && indexOf(list_files[i], "D_20") >= 0){
        right_triple_images = Array.concat(right_triple_images, list_files[i]);
    }
  }
  right_neun_images = Array.deleteValue(right_neun_images, 0);
  right_cfos_images = Array.deleteValue(right_cfos_images, 0);
  right_dapi_images = Array.deleteValue(right_dapi_images, 0);
  right_triple_images = Array.deleteValue(right_triple_images, 0);
}


if (left_hemisphere_analysis){
  // Check if there is a directory for each type of image
  name_to_save_left_neun = substring(left_neun_images[0], 0, (left_neun_images[0].length) - 4);
  name_to_save_left_cfos = substring(left_cfos_images[0], 0, (left_cfos_images[0].length) - 4);
  name_to_save_left_dapi = substring(left_dapi_images[0], 0, (left_dapi_images[0].length) - 4);
  name_to_save_left_triple = substring(left_triple_images[0], 0, (left_triple_images[0].length) - 4);
}
if (right_hemisphere_analysis){
  name_to_save_right_neun = substring(right_neun_images[0], 0, (right_neun_images[0].length) - 4);
  name_to_save_right_cfos = substring(right_cfos_images[0], 0, (right_cfos_images[0].length) - 4);
  name_to_save_right_dapi = substring(right_dapi_images[0], 0, (right_dapi_images[0].length) - 4);
  name_to_save_right_triple = substring(right_triple_images[0], 0, (right_triple_images[0].length) - 4);
}

// Check if the directories exist, if not, create them
left_hemisphere_folder = false;
right_hemisphere_folder = false;

// Use the folder boolean to check if the folder already exists and exit if any of them does, informing which ones
if (left_hemisphere_folder || right_hemisphere_folder){
  message = "The following folders already exist:\n";
  if (left_hemisphere_folder){
    message = message + "left_hemisphere\n";
  }
  if (right_hemisphere_folder){
    message = message + "right_hemisphere\n";
  }
  exit(message + "\nPlease, delete them, and run the script again\nTo avoid errors, leave only .zvi files in the folder");
}


if (left_hemisphere_analysis){
  // Create the directories
  left_hemisphere_folder = dir + "left_hemisphere";
  left_hemisphere_folder_neun = left_hemisphere_folder + "/neun";
  left_hemisphere_folder_cfos = left_hemisphere_folder + "/cfos";
  left_hemisphere_folder_dapi = left_hemisphere_folder + "/dapi";
  left_hemisphere_folder_triple = left_hemisphere_folder + "/triple";
  // Define the directories for the left hemisphere
  leftDirectories = newArray(
    left_hemisphere_folder,
    left_hemisphere_folder_neun,
    left_hemisphere_folder_cfos,
    left_hemisphere_folder_dapi,
    left_hemisphere_folder_triple
  );
}

if (right_hemisphere_analysis){
  // Define the directories for the right hemisphere
  right_hemisphere_folder = dir + "right_hemisphere";
  right_hemisphere_folder_neun = right_hemisphere_folder + "/neun";
  right_hemisphere_folder_cfos = right_hemisphere_folder + "/cfos";
  right_hemisphere_folder_dapi = right_hemisphere_folder + "/dapi";
  right_hemisphere_folder_triple = right_hemisphere_folder + "/triple";
  rightDirectories = newArray(
    right_hemisphere_folder,
    right_hemisphere_folder_neun,
    right_hemisphere_folder_cfos,
    right_hemisphere_folder_dapi,
    right_hemisphere_folder_triple
  );
}

if (left_hemisphere_analysis){
  // Create the directories for the left hemisphere
  for (i = 0; i < leftDirectories.length; i++) {
    File.makeDirectory(leftDirectories[i]);
    wait(50);
  }
}

if (right_hemisphere_analysis){
  // Create the directories for the right hemisphere
  for (i = 0; i < rightDirectories.length; i++) {
    File.makeDirectory(rightDirectories[i]);
    wait(50);
  }
}

if (left_hemisphere_analysis){
  // Copy left images
  copyImages(left_dapi_images, dir, left_hemisphere_folder_dapi);
  copyImages(left_cfos_images, dir, left_hemisphere_folder_cfos);
  copyImages(left_neun_images, dir, left_hemisphere_folder_neun);
  copyImages(left_triple_images, dir, left_hemisphere_folder_triple);
}

if (right_hemisphere_analysis){
  // Copy right images
  copyImages(right_dapi_images, dir, right_hemisphere_folder_dapi);
  copyImages(right_cfos_images, dir, right_hemisphere_folder_cfos);
  copyImages(right_neun_images, dir, right_hemisphere_folder_neun);
  copyImages(right_triple_images, dir, right_hemisphere_folder_triple);
}

if (left_hemisphere_analysis){
  // Stitch and save left hemisphere images
  stitchAndSaveImages(left_hemisphere_folder_neun, name_to_save_left_neun, 0.80);
  stitchAndSaveImages(left_hemisphere_folder_cfos, name_to_save_left_cfos, 0.80);
  stitchAndSaveImages(left_hemisphere_folder_dapi, name_to_save_left_dapi, 0.80);
  stitchAndSaveImages(left_hemisphere_folder_triple, name_to_save_left_triple, 0.80);
}

if (right_hemisphere_analysis){
  // Stitch and save right hemisphere images
  stitchAndSaveImages(right_hemisphere_folder_neun, name_to_save_right_neun, 0.80);
  stitchAndSaveImages(right_hemisphere_folder_cfos, name_to_save_right_cfos, 0.80);
  stitchAndSaveImages(right_hemisphere_folder_dapi, name_to_save_right_dapi, 0.80);
  stitchAndSaveImages(right_hemisphere_folder_triple, name_to_save_right_triple, 0.80);
}

waitForUser("All done! :)\nNow check if the panoramas are correct, when you're done, click ok to continue with the analysis");

// Create analysis directory
left_hemisphere_analysis_dir = dir + "left_hemisphere_analysis";
right_hemisphere_analysis_dir = dir + "right_hemisphere_analysis";

if (left_hemisphere_analysis){
  // Check if the directory exists, if yes, delete everything inside
  if (File.isDirectory(left_hemisphere_analysis_dir)){
    list_files = getFileList(left_hemisphere_analysis_dir);
    file_list_length = list_files.length;

    while (file_list_length > 0){
      deleted_successfully = File.delete(left_hemisphere_analysis_dir + "/" + list_files[file_list_length - 1]);
      if (!deleted_successfully){
        waitForUser("The file " + list_files[file_list_length - 1] + " could not be deleted\nPlease, delete it manually and press OK");
      }else{
        file_list_length = file_list_length - 1;
      }
    }
  }
}

if (right_hemisphere_analysis){
  // Check if the directory exists, if yes, delete everything inside
  if (File.isDirectory(right_hemisphere_analysis_dir)){
    list_files = getFileList(right_hemisphere_analysis_dir);
    file_list_length = list_files.length;

    while (file_list_length > 0){
      deleted_successfully = File.delete(right_hemisphere_analysis_dir + "/" + list_files[file_list_length - 1]);
      if (!deleted_successfully){
        waitForUser("The file " + list_files[file_list_length - 1] + " could not be deleted\nPlease, delete it manually and press OK");
      }else{
        file_list_length = file_list_length - 1;
      }
    }
  }
}

if (left_hemisphere_analysis){
  if (File.isDirectory(left_hemisphere_analysis_dir)){
    exit("The script ran into an issue when deleting the files in the analysis directory\nPlease, restart");
  }else{
    File.makeDirectory(left_hemisphere_analysis_dir);
  }
}

if (right_hemisphere_analysis){
  if (File.isDirectory(right_hemisphere_analysis_dir)){
    exit("The script ran into an issue when deleting the files in the analysis directory\nPlease, restart");
  }else{
    File.makeDirectory(right_hemisphere_analysis_dir);
  }
}

if (left_hemisphere_analysis){
  // Copy the left hemisphere panorama to the analysis directory
  left_hemisphere_panorama = left_hemisphere_folder_neun + "/" + name_to_save_left_neun + "_panorama.png";
  if (!File.exists(left_hemisphere_panorama)){
    waitForUser("The left hemisphere panorama for NEUN could not be found\nPlease, create them manually before continuing\nPress OK to continue");
  }else{
    File.copy(left_hemisphere_panorama, left_hemisphere_analysis_dir + "/" + name_to_save_left_neun + "_panorama.png");
  }

  if (!File.exists(left_hemisphere_folder_cfos + "/" + name_to_save_left_cfos + "_panorama.png")){
    waitForUser("The left hemisphere panorama for CFOS could not be found\nPlease, create them manually before continuing\nPress OK to continue");
  }else{
    File.copy(left_hemisphere_folder_cfos + "/" + name_to_save_left_cfos + "_panorama.png", left_hemisphere_analysis_dir + "/" + name_to_save_left_cfos + "_panorama.png");
  }

  if (!File.exists(left_hemisphere_folder_triple + "/" + name_to_save_left_triple + "_panorama.png")){
    waitForUser("The left hemisphere panorama for the triple could not be found\nPlease, create them manually before continuing\nPress OK to continue");
  }else{
    File.copy(left_hemisphere_folder_triple + "/" + name_to_save_left_triple + "_panorama.png", left_hemisphere_analysis_dir + "/" + name_to_save_left_triple + "_panorama.png");
  }
}

if (right_hemisphere_analysis){
  // Copy the right hemisphere panorama to the analysis directory
  right_hemisphere_panorama = right_hemisphere_folder_neun + "/" + name_to_save_right_neun + "_panorama.png";
  if (!File.exists(right_hemisphere_panorama)){
    waitForUser("The right hemisphere panorama for NEUN could not be found\nPlease, create them manually before continuing\nPress OK to continue");
  }else{
    File.copy(right_hemisphere_panorama, right_hemisphere_analysis_dir + "/" + name_to_save_right_neun + "_panorama.png");
  }  

  if (!File.exists(right_hemisphere_folder_cfos + "/" + name_to_save_right_cfos + "_panorama.png")){
    waitForUser("The right hemisphere panorama for CFOS could not be found\nPlease, create them manually before continuing\nPress OK to continue");
  }else{
    File.copy(right_hemisphere_folder_cfos + "/" + name_to_save_right_cfos + "_panorama.png", right_hemisphere_analysis_dir + "/" + name_to_save_right_cfos + "_panorama.png");
  }

  if (!File.exists(right_hemisphere_folder_triple + "/" + name_to_save_right_triple + "_panorama.png")){
    waitForUser("The right hemisphere panorama for the triple could not be found\nPlease, create them manually before continuing\nPress OK to continue");
  }else{
    File.copy(right_hemisphere_folder_triple + "/" + name_to_save_right_triple + "_panorama.png", right_hemisphere_analysis_dir + "/" + name_to_save_right_triple + "_panorama.png");
  }
}

waitForUser("All done! :)\n Now you can analyze each hemisphere separately using the second part of the script\nMake sure that the cfos and neun's panoramas are in each respective analysis directory\nPress OK to finish the script");

//Listening to:
//Silver Soul - Beach House