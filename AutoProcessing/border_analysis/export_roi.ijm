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

Dialog.create("Dialog to create a suffix for the ROIs");
Dialog.addMessage("Type a phrase to be the suffix of the saved ROIs. For example: '\_border\_roi'");
Dialog.addString("Suffix:", "_roi", 15)
Dialog.addMessage("Note:\nThis script only works for saving ONE roi.\nI.e.: It only works for social recognition\nor for cases when you only need one roi file only.", 9, "#ff0000");
Dialog.show();
suffix = Dialog.getString();

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