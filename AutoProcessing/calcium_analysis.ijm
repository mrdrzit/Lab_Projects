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

var rolling_nestin = 30; // Rolling nestin value for background subtraction
to_process = getFileList(dir); 
to_process = Array.sort(to_process); // Sort the file list

// Main Processing Loop
for (i = 0; i < to_process.length; i++) {
  
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
  filters = getList("image.titles");
  for (k = 0; k < filters.length; k++){
    selectWindow(filters[k]);
    run("Subtract Background...", "rolling=" + rolling_nestin);
  }
  run("Merge Channels...", "c2=[" + list_open_filters[1] + "] c3=[" + list_open_filters[0] + "] create keep");
  
  selectWindow("Composite");
  list_open_filters = getList("image.titles");
  name_atual = File.nameWithoutExtension;
  selectImage("Composite");
  saveAs("tiff", output + name_atual + ".tif");
  // Close all images in the stack
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
