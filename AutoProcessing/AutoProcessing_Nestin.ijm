// Initialization and Setup
print("\\Clear"); // Clear console
run("Close All"); // Close all open windows
setOption("ExpandableArrays", true); // Enable expandable arrays

// User Input for Directories
dir = getDirectory("Where are your photos?"); // Select source directory for photos
output = getDirectory("Where do you want to store them?"); // Select output directory for processed photos

// Directory Path Formatting
dir = replace(dir, "\\", "/"); // Replace backslashes with forward slashes in the source directory path
output = replace(output, "\\", "/"); // Replace backslashes with forward slashes in the output directory path

// Variables Initialization
var n_iniciali = 0; // Initial slice number to start processing
var n_finali = 0; // Final slice number to stop processing
var rolling_nestin = 30; // Rolling nestin value for background subtraction

// File List Validation
var to_process = getFileList(dir); // Get a list of filenames in the selected directory
for (i = 0; i < to_process.length; i++) { // Loop to check file formats and presence of folders
  if (endsWith(to_process[i], "/")) {
    exit("Please remove all folders inside from wherever the photos are stored");
  } 
  if (!(endsWith(to_process[i], ".zvi"))) {
    exit("The files need to be in the .zvi format");
  }
}
to_process = Array.sort(to_process); // Sort the file list

// Main Processing Loop
for (i = 0; i < to_process.length; i++) {
  // File format validation
  if (!(endsWith(to_process[i], ".zvi"))) {
    exit("The files need to be in the .zvi format");
  }
  
  // Processing progress indication
  showProgress(i, to_process.length);
  print("\nI'm processing the photo " + to_process[i] + " for you");
  
  // Current image path
  current_image = dir + to_process[i];
  
  // Open the current image and display
  open(current_image);
  run("Show All");
  list_open_filters = getList("image.titles"); // Create an array containing the opened windows' names
  
  // Z-stack compression loop
  for (j = 0; j < list_open_filters.length; j++) {
    // Select the current window
    selectWindow(list_open_filters[j]);
    stack_size = nSlices; // Get the number of slices in the current stack
    t = indexOf(current_image, "x00");
    
    // Check if it's the first image in the stack
    if (stack_size == 1 && t != -1) {
      print("The photo " + current_image + " is the first image taken, in the 5x objective\n I'll skip it");
      run("Close All");
      continue;
    } else if (stack_size == 1) {
      exit("Currently, the program cannot process\nphotos that aren't a z-stack\nLike the photo " + current_image);
    }
    
    // Define the initial and final slices for processing
    n_inicial = stack_size + 1 - (stack_size - n_iniciali);
    n_final = stack_size - n_finali;
    
    // Display processing information
    if (j == 0) {
      print("I'll start at slice " + n_inicial + "\nand stop at slice " + n_final + "\nand the photo has " + stack_size + " slices");
    }
    
    // Z-stack projection
    run("Z Project...", "start=" + n_inicial + " stop=" + n_final + " projection=[Max Intensity]");
    selectWindow(list_open_filters[j]);

    // Background subtraction and image processing
    allExceptMax = getList("image.titles");
    for (k = 0; k < allExceptMax.length; k++) {
      if (!(startsWith(allExceptMax[k], "MAX"))) {
        close(allExceptMax[k]);
      } 
      else {
        run("Subtract Background...", "rolling=" + rolling_nestin);
        setOption("ScaleConversions", true);
        run("8-bit");
        saveAs("Tiff", output + File.nameWithoutExtension + ".tif");
        
        // Close all images in the stack
        while (nImages() > 0) {
          selectImage(nImages());
          run("Close");
        }
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
