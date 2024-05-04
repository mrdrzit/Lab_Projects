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
var rolling_nestin = 20; // Rolling nestin value for background subtraction

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
  
  // Background subtraction and image processing
  allExceptMax = getList("image.titles");
  for (k = 0; k < allExceptMax.length; k++) {
    if (endsWith(allExceptMax[k], "C=1")) {
        selectWindow(allExceptMax[k]);
        run("Subtract Background...", "rolling=" + rolling_nestin);
      }
      else {
        continue;
    }
  }
  // Merge channels 
  run("Merge Channels...", "c2=[" + list_open_filters[1] + "] c3=[" + list_open_filters[0] + "] create keep");
  actual_name = File.nameWithoutExtension;
  selectImage("Composite");
  saveAs("PNG", output + actual_name + ".png");
  // Close All Open Windows
  run("Close All");
}



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
