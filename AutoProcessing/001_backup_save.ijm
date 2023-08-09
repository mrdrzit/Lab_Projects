opened_image = getInfo("image.title")
selectWindow(opened_image);
run("Input/Output...", "jpeg=100 gif=-1 file=.csv use_file save_column");
name = File.getNameWithoutExtension(getTitle);
directory = getDir("image");

// We were saving the ROIs created during the analysis as a form of backup
save_path = directory + name + ".roi";
saveAs("Selection", save_path);
waitForUser("Check if the roi was saved\nIf so, click OK to continue");
close(opened_image);