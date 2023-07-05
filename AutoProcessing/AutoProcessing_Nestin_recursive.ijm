function listFiles(dir) {
  list = getFileList(dir);
  for (i = 0; i < list.length; i++) {
    if (endsWith(list[i], "/")) {
      listFiles("" + dir + list[i]);
      idx++;
    }
    else {
      to_process[idx] = dir + list[i];
      idx++;
    }
  }
}

print("\\Clear");
setOption("ExpandableArrays", true);
run("Close All");

dir = getDirectory("Where are your photos?");
var to_process = newArray(0);
idx = 0;
listFiles(dir);
to_process = Array.deleteValue(to_process, "undefined")
to_process = Array.sort(to_process);

var n_iniciali = 2;
var n_finali = 2;
var rolling_nestin = 30;

for (i = 0; i < to_process.length; i++) { //Loop to select only .zvi images and check for directories inside of the folder
  if (endsWith(to_process[i], "/")) {
    exit("Please remove all folders inside from wherever the photos are stored")
  } if (!(endsWith(to_process[i], ".zvi"))) {
    exit("The files need to be in the .zvi format");
  }
}

for (i = 0; i < to_process.length; i++) {
  if (!(endsWith(to_process[i], ".zvi"))) {
    exit("The files need to be in the .zvi format");
  }
}

Array.sort(to_process);
qtd = to_process.length //The number of times that it'll iterate the loop

for (i = 0; i < qtd; i++) {
  showProgress(i, qtd);
  print("\nI'm processing the photo " + to_process[i] + " for you");
  current_image = to_process[i];
  open(current_image);
  run("Show All");
  list_open_filters = getList("image.titles"); //Creates an array containing the opened windows's names

  //Runs a z-stack compression removing the selected range of photos at the start and end of the stack 
  for (j = 0; j < list_open_filters.length; j++) {
    selectWindow(list_open_filters[j]);
    stack_size = nSlices;
    t = indexOf(current_image, "x00");
    u = indexOf(current_image, "x01");
    v = indexOf(current_image, "x1");
    x = indexOf(current_image, "x0");
    if (stack_size == 1 && (t != -1 || u != -1 || v != -1 || x != -1)) {
      print("The photo " + current_image + " is the first image taken, in the 5x objective\n I'll skip it");
      run("Close All");
      continue;
    } else if (stack_size == 1) {
      exit("Currently the program cannot process\nphotos that aren't a z-stack\nLike the photo " + current_image);
    }
    n_inicial = stack_size + 1 - (stack_size - n_iniciali);
    n_final = stack_size - n_finali;
    if (j == 0) {
      print("I'll start at the slice " + n_inicial + "\nand stop at the slice " + n_final + "\nand the photo have " + stack_size + " slices");
    }
    run("Z Project...", "start=" + n_inicial + " stop=" + n_final + " projection=[Max Intensity]");
    selectWindow(list_open_filters[j]);

    allExceptMax = getList("image.titles");
    for (k = 0; k < allExceptMax.length; k++) {
      if (!(startsWith(allExceptMax[k], "MAX"))) {
        close(allExceptMax[k]);
      } else {
        dir_without_file = replace(current_image, File.getName(current_image), "");
        saveAs("Tiff", dir_without_file + File.nameWithoutExtension + "_background.tif");
        run("Subtract Background...", "rolling=" + rolling_nestin);
        setOption("ScaleConversions", true);
        run("8-bit");
        saveAs("Tiff", dir_without_file + File.nameWithoutExtension + ".tif");
        while (nImages() > 0) {
          selectImage(nImages());
          run("Close");
        }
      }
    }
  }
}

run("Close All");
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