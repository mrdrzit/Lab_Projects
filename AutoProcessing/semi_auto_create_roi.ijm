function listFiles(dir) {
    list = getFileList(dir);
    for (i = 0; i < list.length; i++) {
        if (endsWith(list[i], "/")) {
            listFiles("" + dir + list[i]);
            idx++;
        }
        else {
            if (endsWith(list[i], ".jpg")) { // Only add png files to the list
                to_process[idx] = dir + list[i];
                idx++;
            }
        }
    }
}

run("Close All");

dir = getDirectory("Where are your photos?");
output = dir;

dir = replace(dir, "\\", "/"); // Fixes the name of the directory in windows machines, inserting a '/'
output = replace(output, "\\", "/");
var to_process = newArray(0);
idx = 0;
listFiles(dir);
to_process = Array.deleteValue(to_process, "undefined")
to_process = Array.sort(to_process);
qtd = to_process.length //The number of times that i'll iterate the loop

for (i = 0; i < qtd; i++) {
    atual = i + 1;
  
    current_image = to_process[i];
    open(current_image);
    run("Show All");
    list_open_windows = getList("image.titles"); //Creates an array with the names of the currently open windows
    Array.sort(list_open_windows);
    
    //Selects all the images and saves the composite as a .TIFF for further analysis
    run("Show All");
    list_open_windows = getList("image.titles");
    nome_atual = File.nameWithoutExtension;

    selectWindow(list_open_windows[0]);
    run("Maximize");
    setTool("multipoint");
    waitForUser("Please selec the region of interest and press OK when you're done");
    run("Measure");
    selectWindow("Results");
    saveAs("Results", dir + nome_atual + "_coordinates.csv");
    saveAs("Selection", dir + nome_atual + "_coordinates.roi");
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

// Listening to: Let Down - Pedro the lion
