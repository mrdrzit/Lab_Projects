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
Dialog.addMessage("Rolling window to be used:\nminimum = 0");
Dialog.addNumber("Value for Nestin:", 30);
Dialog.addToSameRow();
Dialog.addCheckbox("Remove the background of the filter for Nestin?", true);

Dialog.show();

var n_iniciali = Dialog.getNumber();
var n_finali = Dialog.getNumber();
var rolling_nestin = Dialog.getNumber();
var remove_nestin = Dialog.getCheckbox();

var list_file_names = getFileList(dir); //Gives a list with the filenames in the selected directory
for (i = 0; i < list_file_names.length; i++){ //Loop to select only .zvi images and check for directories inside of the folder
  if (endsWith(list_file_names[i], "/")){
    exit("Please remove all folders inside from wherever the photos are stored")
  }if(!(endsWith(list_file_names[i], ".zvi"))){
    exit("The files need to be in the .zvi format");
  }
}
list_file_names = Array.sort(list_file_names);

for (i = 0; i < list_file_names.length; i++) { 
  if(!(endsWith(list_file_names[i], ".zvi"))){
    exit("The files need to be in the .zvi format");
  }
}

Array.sort(list_file_names);
qtd = list_file_names.length //The number of times that i'll iterate the loop

for (i = 0; i < qtd; i++){
  showProgress(i, qtd);
  atual = i + 1;
  print("\nI'm processing the photo " + list_file_names[i] + " for you");
  current_image = dir+list_file_names[i];
  open(current_image);
  run("Show All");
  list_open_filters = getList("image.titles"); //Creates an array containing the opened windows's names

  //Runs a z-stack compression removing the selected range of photos at the start and end of the stack 
  for (j=0; j<list_open_filters.length; j++) {
    selectWindow(list_open_filters[j]);
    stack_size = nSlices;
    if (stack_size == 1){
      exit("Currently the program cannot process\nphotos that aren't a z-stack\nLike the photo "+current_image);
    }
    n_inicial = stack_size + 1 - (stack_size - n_iniciali);
    n_final = stack_size - n_finali;
    if (j==0){
      print("I'll start at the slice "+n_inicial+"\nand stop at the slice "+n_final+"\nand the photo have "+stack_size +" slices");
    }
    run("Z Project...",  "start=" + n_inicial + " stop="+n_final + " projection=[Max Intensity]");
    selectWindow(list_open_filters[j]);

    //Entraria o corte

    allExceptMax = getList("image.titles");
    for (i = 0; i < allExceptMax.length; i++){
      if (!(startsWith(allExceptMax[i], "MAX"))){
        close(allExceptMax[i]);
      }else {
        setOption("ScaleConversions", true);
        run("8-bit");
        close(allExceptMax[i]);
      }
    }

    
  }
}