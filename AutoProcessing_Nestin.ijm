print("\\Clear");
run("Close All");
setOption("ExpandableArrays", true);

dir = getDirectory( "Where are your photos?" );
output = getDirectory( "Where do you want to store them?" );

dir = replace(dir, "\\", "/"); // Fixes the name of the directory in windows machines, inserting a '/'
output = replace(output, "\\", "/");

//I create a window where the user can indicate which values will be used in the processing
//TODO: #1 Modulate to include all the available filters

Dialog.create("Values to cut the z-stack and remove the background");

Dialog.addMessage("What will be the slices that you want to remove at the start and end of the z-stack?");
Dialog.addNumber("Start:", 2);
Dialog.addNumber("End:", 2);
Dialog.addMessage("Rolling to be used:\nminimum = 0");
Dialog.addNumber("Value for Nestin:", 50);
Dialog.addToSameRow();
Dialog.addCheckbox("Remove the background of the filter for Nestin?", true);

Dialog.show();

var n_iniciali = Dialog.getNumber();
var n_finali = Dialog.getNumber();
var rolling_nestin = Dialog.getNumber();
var remove_nestin = Dialog.getCheckbox();

var list_file_names = getFileList(dir); //Gives a list with the filenames in the selected directory
for (i = 0; i < list_file_names.length; i++){
    if (endsWith(list_file_names[i], "/")){
    exit("Please remove all folders inside from wherever the photos are stored")
  }
}
list_file_names = Array.sort(list_file_names);

for (i = 0; i < list_file_names.length; i++) { //Loop to select only .zvi images
  if(File.isDirectory(dir + File.separator + list_file_names[i])){
    exit("You need to select inside of the folder containing the images");
  }
  if(!(endsWith(list_file_names[i], ".zvi"))){
    exit("The files need to be in the .zvi format");
  }
  if(!(endsWith(list_file_names[i], "/"))){
    exit("There can be only the images that you want to process inside the folder");
}

Array.sort(list_file_names);
qtd = list_file_names.length //The number of times that i'll iterate the loop