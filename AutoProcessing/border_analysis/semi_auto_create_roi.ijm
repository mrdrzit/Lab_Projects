function listFiles(dir) {
    list = getFileList(dir);
    for (i = 0; i < list.length; i++) {
        if (endsWith(list[i], "/")) {
            listFiles("" + dir + list[i]);
            idx++;
        }
        else {
            if (endsWith(list[i], ".jpg")) { // Only add jpg files to the list
                to_process[idx] = dir + list[i];
                idx++;
            }
        }
    }
}

run("Close All");

Dialog.createNonBlocking("Dialog to create a suffix for the ROIs");
Dialog.addMessage("Type a phrase to be the suffix of the saved ROIs. For example: '\_border\_roi'");
Dialog.addString("Suffix:", "_roi", 15)
Dialog.addMessage("Note:\nThis script only works for saving ONE roi.\nI.e.: It only works for social recognition\nor for cases when you only need one roi file only.", 12, "#ff0000");
Dialog.show();
suffix = Dialog.getString();

dir = getDirectory("Where are your photos?");
output = dir;

dir = replace(dir, "\\", "/"); // Fixes the name of the directory in windows machines, inserting a '/'
output = replace(output, "\\", "/");
var to_process = newArray(0);
idx = 0;
listFiles(dir);

// Replace the original array with the filtered array
to_process = Array.deleteValue(to_process, "undefined");
to_process = Array.deleteValue(to_process, "null");
to_process = Array.deleteValue(to_process, "");

to_process = Array.sort(to_process);
qtd = to_process.length; //The number of times that i'll iterate the loop

for (i = 0; i < qtd; i++) {
    atual = i + 1;
	
    current_image = to_process[i];
    nome_atual = File.getNameWithoutExtension(current_image);
	suffix_lower = toLowerCase(suffix);

	final_roi_name = dir + nome_atual + suffix + ".roi";
	final_txt_name = dir + nome_atual + suffix + ".txt";
	final_csv_name = dir + nome_atual + suffix + ".csv";

	if (File.exists(final_txt_name)){
		print("The rois for " + nome_atual + " already exist. Skipping to the next image.");
		continue;
	}
	if (File.exists(final_roi_name) && File.exists(final_csv_name)){
		print("The rois for " + nome_atual + " already exist. Skipping to the next image.");
		continue;
	}

	// waitForUser("Please select the region of interest and press OK when you're done.\nProgress = " + atual + "/" + qtd);
    open(current_image);
    run("Show All");
    list_open_windows = getList("image.titles"); //Creates an array with the names of the currently open windows
    Array.sort(list_open_windows);
    
    run("Show All");
    list_open_windows = getList("image.titles");

    selectWindow(list_open_windows[0]);
    run("Maximize");
    setTool("rectangle");
	if (isOpen("Results")){
        selectWindow("Results"); 
        run("Close");
    }
	Dialog.createNonBlocking("ROI creation");
	Dialog.addMessage("Please select the region of interest and press OK when you're done.\nProgress = " + atual + "/" + qtd);
	Dialog.addCheckbox("If this is an abritrary ROI, check this:", false);
	Dialog.show();

	is_arbitrary_roi = Dialog.getCheckbox();
	if (is_arbitrary_roi){
		saveAs("XY Coordinates", dir + nome_atual + suffix + ".txt");
		saveAs("Selection", dir + nome_atual + suffix + ".roi");
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
		setTool("polygon");
	}else{
		run("Measure");
		if (getValue("results.count") == 1){
			img_width = getWidth();
			img_height = getHeight();
			measured_width = getResult("Width", 0);
			measured_height = getResult("Height", 0);
		}else{
			selectWindow("Results"); 
			run("Close");
			img_width = getWidth();
			img_height = getHeight();
			measured_width = getResult("Width", 0);
			measured_height = getResult("Height", 0);
		}
		equal_dimensions = 0;
		if ((Math.ceil(measured_width) == Math.ceil(img_width)) && (Math.ceil(measured_height) == Math.ceil(img_height))){
			equal_dimensions = getBoolean("You did not create any ROI\nIf this was intended, just press Yes\nElse, press No and proceed with ROI creation");
		}
		if (equal_dimensions){
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
			continue
		}else{
			selectWindow(list_open_windows[0]);
			run("Maximize");
			setTool("rectangle");
			if (isOpen("Results")){
				selectWindow("Results"); 
				run("Close");
			}
			if ((Math.ceil(measured_width) == Math.ceil(img_width)) && (Math.ceil(measured_height) == Math.ceil(img_height))){
				waitForUser("Please select the region of interest and press OK when you're done.\nProgress = " + atual + "/" + qtd);
			}
			run("Measure");
			selectWindow("Results");	
			saveAs("Results", dir + nome_atual + suffix + ".csv");
			saveAs("Selection", dir + nome_atual + suffix + ".roi");
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
		}
	}
}

waitForUser("Done!\n =]");
// Listening to: Let Down - Pedro the lion
