function get_sum(start, end, histogram_count){
  sum = 0;
  for (i=start; i<end; i++){
    sum = sum + histogram_count[i];
  }
  return sum;
}


print("\\Clear");
run("Close All");
setOption("ExpandableArrays", true);

dir = getDirectory("Where are your photos?");


dir = replace(dir, "\\", "/"); // Fixes the name of the directory in windows machines, inserting a '/'
output = replace(output, "\\", "/");

//I create a window where the user can indicate which values will be used in the processing

Dialog.create("Values to cut the z-stack and remove the background");

Dialog.addMessage("What will be the slices that you want to remove at the start and end of the z-stack?");
Dialog.addNumber("Number of slices", 2);
Dialog.addMessage("Rolling to be used:\nminimum = 0");
Dialog.addNumber("Value for Hoechst:", 50);
Dialog.addToSameRow();
Dialog.addNumber("Value for etidio:", 50);
Dialog.addToSameRow();

Dialog.show();

var number_slices = Dialog.getNumber();
var rolling_Hoechst = Dialog.getNumber();
var remove_Hoechst = Dialog.getCheckbox();
var rolling_etidio = Dialog.getNumber();
var remove_etidio = Dialog.getCheckbox();

list_file_names = getFileList(dir); //Gives a list with the filenames in the selected directory
var list_file_names = Array.sort(list_file_names);

for (i = 0; i < list_file_names.length; i++) { //Loop to select only .zvi images
  if (File.isDirectory(dir + File.separator + list_file_names[i])) {
    exit("You need to select inside of the folder containing the images");
  }
  if (!(endsWith(list_file_names[i], ".zvi"))) {
    print("The files need to be in the .zvi format");
  }
}

Array.sort(list_file_names);
qtd = list_file_names.length //The number of times that i'll iterate the loop

//Loop that actually processess the images
for (i = 0; i < qtd; i++) {
  showProgress(i, qtd);
  atual = i + 1;

  print("\nI'm processing the photo " + list_file_names[i] + " for you");
  current_image = dir + list_file_names[i];
  name_to_save = File.getNameWithoutExtension(list_file_names[i]);
  open(current_image);
  
  // ----------- Block of code to remove the first and last 3 images from the z-stack -----------------

  // get the number of slices in the stack
  stack_size = nSlices;

  // if the number of slices is 1, then the image is not a z-stack
  if (stack_size == 1){
    exit("This image is probably not a z-stack\nCan you check it and restart the analysis?");
  }
  // calculate the number of slices in the stack and the number of slices to remove
  n_inicial = number_slices + 1;
  n_final = stack_size - number_slices;
  // --------------------------------------------------------------------------------------------------

  run("Show All");
  list_open_filters = getList("image.titles"); //Creates an array containing the opened windows's names 

  //Runs a z-stack compression removing the selected range of photos at the start and end of the stack 
  for (j = 0; j < list_open_filters.length; j++) {
    selectWindow(list_open_filters[j]);
    stack_size = nSlices;
    if (stack_size == 1) {
      exit("Currently the program cannot process\nphotos that aren't a z-stack\nLike the photo " + current_image);
    }

    if (n_final < n_inicial) {
      exit("With the amount of slices to remove set, the z-stack will be empty\nPlease, check the values for this slice and try again\nThe name of the photo is " + current_image);
    }

    if (j == 0) {
      print("I'll start at the slice " + n_inicial + "\nand stop at the slice " + n_final + "\nand the photo has " + stack_size + " slices");
    }
    run("Z Project...", "start=" + n_inicial + " stop=" + n_final + " projection=[Max Intensity]");
    selectWindow(list_open_filters[j]);
    close();
  }

  run("Show All"); //This always has to come before to be sure that all the images are on the foreground to be able to be selected (a.k.a: Aren't minimized)
  list_open_filters = getList("image.titles"); //Re-create the array because the compression operation on the z-stack changes the imagename

  //Removes the background
  if (1) {
    filters_to_merge = newArray();
    for (k = 0; k < list_open_filters.length; k++) {
      name_atual = "";
      if ((indexOf(list_open_filters[k], "C=0") >= 0)) {
        selectWindow(list_open_filters[k]);
        run("Subtract Background...", "rolling=" + rolling_Hoechst);
        setOption("ScaleConversions", true);
        run("8-bit");
        selectWindow(list_open_filters[k]);
        name_atual = File.getNameWithoutExtension(list_open_filters[k]) + "_MAX_PROJECTION_Hoechst";
        saveAs("PNG", dir + File.separator + name_atual + ".png");
        filters_to_merge = Array.concat(filters_to_merge, dir + File.separator + name_atual + ".png");
        close();

      }
      else if ((indexOf(list_open_filters[k], "C=1") >= 0)) {
        selectWindow(list_open_filters[k]);
        run("Subtract Background...", "rolling=" + rolling_etidio);
        setOption("ScaleConversions", true);
        run("8-bit");
        selectWindow(list_open_filters[k]);
        name_atual = File.getNameWithoutExtension(list_open_filters[k]) + "_MAX_PROJECTION_etidio";
        saveAs("PNG", dir + File.separator + name_atual + ".png");
        filters_to_merge = Array.concat(filters_to_merge, dir + File.separator + name_atual + ".png");
        close();
      }
    }
  }

  //Create a composite of the available filters without background 
  for (l = 0; l < filters_to_merge.length; l++) {
    open(filters_to_merge[l]);
  }

  run("Show All"); //This always has to come before to be sure that all the images are on the foreground to be able to be selected (a.k.a: Aren't minimized)
  list_open_filters = getList("image.titles"); //Re-create the array because the compression operation on the z-stack changes the imagename
  Array.sort(list_open_filters);
  blur_hoechst = list_open_filters[1];
  blur_etidio = list_open_filters[0];

  selectImage(blur_hoechst);
  run("Duplicate...", "title=blur_hoechst");
  run("Gaussian Blur...", "sigma=15");

  selectImage(blur_etidio);
  run("Duplicate...", "title=blur_etidio");
  run("Gaussian Blur...", "sigma=15");

  imageCalculator("Subtract create", list_open_filters[1],"blur_hoechst");
  selectWindow("Result of " + list_open_filters[1]);
  saveAs("PNG", dir + File.separator + blur_hoechst);

  imageCalculator("Subtract create", list_open_filters[0],"blur_etidio");
  selectWindow("Result of " + list_open_filters[0]);
  saveAs("PNG", dir + File.separator + blur_etidio);

  run("Close All");
  for (l = 0; l < filters_to_merge.length; l++) {
    open(filters_to_merge[l]);
  }

  run("Show All"); //This always has to come before to be sure that all the images are on the foreground to be able to be selected (a.k.a: Aren't minimized)
  list_open_filters = getList("image.titles"); //Re-create the array because the compression operation on the z-stack changes the imagename
  Array.sort(list_open_filters);

  run("Merge Channels...", "c3=[" + list_open_filters[1] + "] c7=[" + list_open_filters[0] + "] create keep");

  //Selects all the images and saves the composite as a .PNG for further analysis
  name_atual = name_to_save + "_MERGE_etidio_hoechst";

  selectImage("Composite");
  saveAs("PNG", dir + File.separator + name_atual + ".png");

  run("Show All");
  list = getList("image.titles");
  Array.sort(list);

  for (p = 0; p < list.length; p++) {
    if (p == 0) {
      continue;
    } else {
      close(list[p]);
    }
  }
  run("Close All");
}
waitForUser("I've finished");


//Listening to:
//Never Forgive Me, Never Forget Me by Akira Yamaoka