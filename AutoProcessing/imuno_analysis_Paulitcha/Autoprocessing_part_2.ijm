print("\\Clear");
run("Close All");
setOption("ExpandableArrays", true);

run("Input/Output...", "jpeg=100 gif=-1 file=.csv use_file save_column");
run("Set Measurements...", "area perimeter bounding limit redirect=None decimal=3");

// See if the scale is set and if it is global
if(!(is("global scale"))){
  run("Blobs");
  waitForUser("The scale is probably not set\nOr at least is not global\n\nIn the next window, please enter the scaling factor.\nTip: The known distance for 20x magnification is 0.5123 um/pixel\nAfter this, check nonetheless! :)");
  scale = getNumber("Known distance (um/pixels):", 0.5123);
  run("Set Scale...", "distance=1 known="+scale+" unit=um global");
  close("*");
  exit("Don't forget to also set it as global if it was not set properly automatically!");
}

dir = getDirectory("Select the analysis folder where the panoramas are located");
dir = replace(dir, "\\", "/"); // Fixes the name of the directory in windows machines, inserting a '/'
output = replace(output, "\\", "/");

panoramas = getFileList(dir);
cfos_panorama = "";
neun_panorama = "";

for(i=0; i<panoramas.length; i++){
  if (endsWith(panoramas[i], "/")){
    waitForUser("There are folders in the analysis folder. Please remove them and press OK to continue.\nLeave only the panoramas to be analyzed, that is, the NEUN and CFOS panoramas")
  }
  if (indexOf(panoramas[i], "cfos") >= 0){
    cfos_panorama = panoramas[i];
  }
  if (indexOf(panoramas[i], "neun") >= 0){
    neun_panorama = panoramas[i];
  }
}

if (cfos_panorama == "" || neun_panorama == ""){
  exit("Some panoramas are missing from the folder. Please check the folder and try again.");
}
for (i=0; i<panoramas.length; i++){
  open(dir + panoramas[i]);
  run("8-bit");
}

run("Colocalization Threshold", "channel_1=[" + neun_panorama + "] channel_2=[" + cfos_panorama + "] use=None channel=[Red : Green] show use_0 include");
selectWindow("Results");
close("Results");
waitForUser("Check the colocalization and make sure that this is sensible, that is, that the colocalization is not too high or too low.\nIf it is not, take note of this hemisphere and continue to the next one pressing CANCEL and selecting the next hemisphere (OTHER FOLDER).\nYou will need to do the wrong ones manually later.\nALSO, please close the RESULTS table if it's opened still, please :)");

selectWindow("Colocalized Pixel Map RGB Image");
run("8-bit");
run("Threshold...");
setThreshold(250, 255);

waitForUser("Check the threshold values to see if it matches the colocalization map.\nIf it does, press OK to continue.\nIf it doesn't, adjust the threshold values to match the colocalization and only then press OK to continue.");

selectWindow("Colocalized Pixel Map RGB Image");
run("Convert to Mask");
run("Fill Holes");

run("Remove Outliers...", "radius=2 threshold=50 which=Bright");
run("Watershed");

selectWindow("Threshold");
close("Threshold");
continue_analysis = true;

while (continue_analysis) {
    waitForUser("Please drag the pre-created mask for the area to be analyzed into the ImageJ window and press OK to continue.");
    roi_name = File.nameWithoutExtension;

    // Perform the analysis
    run("Measure");
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
        roi_area = Table.get("Area", 0);
        String.copy(roi_area);
        waitForUser("The ROI area is on the clipboard, please paste it into excel, check to see if its the correct value as shown in the results/summary table and, if yes, press OK to continue.\nTip: Excel will have the decimals separated by a dot and the thousands separated by a comma if the language is set to Portuguese.\nSo to properly paste it, you need to change this configuration or convert it manually");
        if (isOpen("Results")){
            selectWindow("Results"); 
            close("Results");
        }
    }

    run("Analyze Particles...", "size=30-100 circularity=0.00-1.00 show=Masks clear summarize");
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
        waitForUser("The number of cells counted is on the clipboard, please paste it into excel, check to see if its the correct value as shown in the results/summary table and, if yes, press OK to continue.");
        if (isOpen("Results")){
            selectWindow("Results"); 
            close("Results");
        }
    }

    selectImage("Mask of Colocalized Pixel Map RGB Image");
    mask_save_name = substring(neun_panorama, 0, (neun_panorama.length) - 18);
    saveAs("PNG", dir + mask_save_name + "_" + roi_name + "_mask.png");
    close(mask_save_name + "_" + roi_name + "_mask.png");

    // Close everything and go to the next image
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
    run("Select None");

    // Ask if the user wants to continue analyzing more areas
    Dialog.create("Continue the analysis?");
    Dialog.addMessage("Do you want to analyze more areas? Check this box if yes, to stop the analysis leave it unchecked.");
    Dialog.addCheckbox("Yes", true);
    Dialog.show();

    continue_analysis = Dialog.getCheckbox();
}

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

  // Listening to: Magdalene - Akira Yamaoka