print("\\Clear");
run("Close All");
setOption("ExpandableArrays", true);

run("Input/Output...", "jpeg=100 gif=-1 file=.csv use_file save_column");
run("Set Measurements...", "area perimeter bounding limit redirect=None decimal=3");

// See if the scale is set and if it is global
if (!(is("global scale"))) {
  run("Blobs");
  waitForUser("The scale is probably not set\nOr at least is not global\n\nIn the next window, please enter the scaling factor.\nTip: The known distance for 20x magnification is 0.5123 um/pixel\nAfter this, check nonetheless! :)");
  scale = getNumber("Known distance (um/pixels):", 0.5123);
  run("Set Scale...", "distance=1 known=" + scale + " unit=um global");
  close("*");
  exit("Don't forget to also set it as global if it was not set properly automatically!");
}

dir = getDirectory("Select the analysis folder where the panoramas are located");
dir = replace(dir, "\\", "/"); // Fixes the name of the directory in windows machines, inserting a '/'

panoramas = getFileList(dir);
triple_panorama = "";

for (i = 0; i < panoramas.length; i++) {
  if (endsWith(panoramas[i], "/")) {
    waitForUser("There are folders in the analysis folder. Please remove them and press OK to continue.\nLeave only the panoramas to be analyzed, that is, the NEUN, CFOS and triple marked panoramas")
  }
  if (indexOf(panoramas[i], "MERGE_dapi_neun_cfos") >= 0) {
    triple_panorama = panoramas[i];
  }
}

if (triple_panorama == "") {
  exit("You need the triple marked panorama to create the rois. Please check the folder and try again.");
}

open(dir + triple_panorama);
while (true) {
  waitForUser("Draw the ROI for the area to be analyzed on the image and click OK to continue.\nYou will need to create all of them individually.\nThat is, one for CA1, one for CA3, one for DG and so on.\n:)");
  roiName = getString("This roi is for what area? (without extension e.g.: ca1):", "");
  if (roiName == "") {
    exit("No name entered. Exiting.");
  }
  saveAs("Selection", dir + roiName + ".roi");

  isLast = getBoolean("Is this the last ROI?");
  if (isLast) {
    break;
  }
  run("Select None");
}

close("*");
waitForUser("Check that all ROIS are saved correctly.");