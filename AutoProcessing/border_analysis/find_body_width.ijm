function listFiles(dir, extension) {
    list = getFileList(dir);
    for (i = 0; i < list.length; i++) {
        if (endsWith(list[i], "/")) {
            listFiles("" + dir + list[i]);
            idx++;
        }
        else {
            if (endsWith(list[i], extension)) { // Only add jpg files to the list
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

extension = ".jpg";
var to_process = newArray(0);
idx = 0;
listFiles(dir, extension);
to_process = Array.deleteValue(to_process, "undefined");
to_process = Array.deleteValue(to_process, "null");
to_process = Array.deleteValue(to_process, "");

MIN_WIDTH = 20000;
width_sum = 0;

qtd = to_process.length; //The number of times that i'll iterate the loop
for (i = 0; i < qtd; i++) {
    atual = i + 1;
    current_image = to_process[i];
    nome_atual = File.getNameWithoutExtension(current_image);
    open(current_image);

    run("Show All");
    list_open_windows = getList("image.titles"); //Creates an array with the names of the currently open windows
    Array.sort(list_open_windows);

    run("Show All");
    list_open_windows = getList("image.titles");
    selectWindow(list_open_windows[0]);

    run("8-bit");
    run("Subtract Background...", "rolling=50 light");
    setAutoThreshold("Default no-reset");
    run("Threshold...");
    setThreshold(0, 200);
    setOption("BlackBackground", true);
    run("Convert to Mask");
    run("Fill Holes");
    run("Remove Outliers...", "radius=10 threshold=50 which=Bright");
    run("Analyze Particles...", "  show=Masks display summarize overlay");
    n = Table.size - 1;
    Table.setColumn("Index", Array.getSequence(n));
    Table.sort("MinFeret");
    current_min_width = getResult("MinFeret", n);
    BX = getResult("BX", n);
    BY = getResult("BY", n);
    width = getResult("Width", n);
    height = getResult("Height", n);
    makeRectangle(BX, BY, width, height);
    run("Duplicate...", "title=biggest_selection");
    saveAs("Tiff", dir + nome_atual + "_biggest_selection" + ".tif");
    close("biggest_selection");

    width_sum += current_min_width;
    if (current_min_width < MIN_WIDTH) {
        MIN_WIDTH = current_min_width;
    }

    open_windows = getList("image.titles");
    for (k = 0; k < open_windows.length; k++) {
        if (startsWith(open_windows[k], "Mask")) {
            selectWindow(open_windows[k]);
            saveAs("Tiff", dir + nome_atual + "_Mask_" + ".tif");
            open_windows = getList("image.titles");
            close(open_windows[k]);
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
            while (nImages() > 0) {
                selectImage(nImages());
                run("Close");
            }
        }
    }
}
average_width_found = width_sum / qtd;
print("Average width found: " + average_width_found);
saveAs("Text", output + "average_width_found.txt");
waitForUser("Done.");