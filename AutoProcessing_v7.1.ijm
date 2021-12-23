print("\\Clear");
run("Close All");
setOption("ExpandableArrays", true);

dir = getDirectory( "Where are your photos?" );
output = getDirectory( "Where do you want to store them?" );

dir = replace(dir, "\\", "/"); // Fixes the name of the directory in windows machines, inserting a '/'
output = replace(output, "\\", "/");

//I create a window where the user can indicate which values will be used in the processing
//TODO: Modulate to include all the available filters

Dialog.create("Values to cut the z-stack and remove the background");

Dialog.addMessage("What will be the slices that you want to remove at the start and end of the z-stack?");
Dialog.addNumber("Start:", 2);
Dialog.addNumber("End:", 2);
Dialog.addMessage("Rolling to be used:\nminimum = 0");
Dialog.addNumber("Value for DAPI:", 50);
Dialog.addToSameRow();
Dialog.addCheckbox("Remove the background of the filter for DAPI?", true);
Dialog.addNumber("Value for BRDU:", 50);
Dialog.addToSameRow();
Dialog.addCheckbox("Remove the background of the filter for BRDU?", true);
Dialog.addNumber("Value for DCX:", 50);
Dialog.addToSameRow();
Dialog.addCheckbox("Remove the background of the filter for DCX?", true);

Dialog.show();

var n_iniciali = Dialog.getNumber();
var n_finali = Dialog.getNumber();
var rolling_dapi = Dialog.getNumber();
var remove_dapi = Dialog.getCheckbox();
var rolling_brdu = Dialog.getNumber();
var remove_brdu = Dialog.getCheckbox();
var rolling_dcx = Dialog.getNumber();
var remove_dcx = Dialog.getCheckbox();

list_file_names = getFileList(dir); //Gives a list with the filenames in the selected directory
var list_file_names = Array.sort(list_file_names);

for (i = 0; i < list_file_names.length; i++) { //Loop to select only .zvi images
  if(File.isDirectory(dir + File.separator + list_file_names[i])){
    exit("You need to select inside of the folder containing the images");
  }
  if(!(endsWith(list_file_names[i], ".zvi"))){
    print("The files need to be in the .zvi format");
  }
}

Array.sort(list_file_names);
qtd = list_file_names.length //The number of times that i'll iterate the loop

//Loop that actually processess the images
for ( i=0; i < qtd; i++ ) {
  showProgress(i, qtd);
  atual = i + 1;

  print("\nI'm processing the photo " + list_file_names[i] + " for you");
  current_image = dir+list_file_names[i];
  open(current_image);
  run("Show All");
  list_open_filters = getList("image.titles"); //Faz um array com o name das janelas abertas Creates an array with the names of the currently open windows

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
    close();
  }

  run("Show All"); //This always has to come before to be sure that all the images are on the foreground to be able to be selected (a.k.a: Aren't minimized)
  list_open_filters = getList("image.titles"); //Re-create the array because the compression operation on the z-stack changes the imagename

  //Removes the background
  //TODO: Modulate based on the control group's background (image histogram)
  if(removebackground){
  for (k=0; k<list_open_filters.length; k++) {
    if ((indexOf(list_open_filters[k], "C=0") >= 0) && remove_dcx) {
      selectWindow(list_open_filters[k]);
      run("Subtract Background...", "rolling="+rolling_dcx);
      setOption("ScaleConversions", true);
      run("8-bit");
    }else if ((indexOf(list_open_filters[k], "C=0") >= 0) && !remove_dcx){
      selectWindow(list_open_filters[k]);
      setOption("ScaleConversions", true);
      run("8-bit");
      continue;
    }
    else if ((indexOf(list_open_filters[k], "C=1") >= 0) && remove_dapi) {
      selectWindow(list_open_filters[k]);
      run("Subtract Background...", "rolling="+rolling_dapi);
      setOption("ScaleConversions", true);
      run("8-bit");
    }else if ((indexOf(list_open_filters[k], "C=1") >= 0) && !remove_dapi){
      selectWindow(list_open_filters[k]);
      setOption("ScaleConversions", true);
      run("8-bit");
      continue;
    }
    else if ((indexOf(list_open_filters[k], "C=2") >= 0) && remove_brdu) {
      selectWindow(list_open_filters[k]);
      run("Subtract Background...", "rolling="+rolling_brdu);
      setOption("ScaleConversions", true);
      run("8-bit");
    }else if ((indexOf(list_open_filters[k], "C=2") >= 0) && !remove_brdu){
      selectWindow(list_open_filters[k]);
      setOption("ScaleConversions", true);
      run("8-bit");
      continue;
    }
  }

  //Create a composite of the available filters without background 
  Array.sort(list_open_filters);
  run("Merge Channels...", "c2=["+ list_open_filters[2] + "] c3=[" + list_open_filters[0] + "] c6=[" + list_open_filters[1] + "] create keep");

  //Selects all the images and saves the composite as a .PNG for further analysis
  run("Show All");
  list_open_filters = getList("image.titles");

  name_atual = File.nameWithoutExtension;

  selectImage("Composite");
  saveAs("PNG", output + name_atual + ".png");

  run("Show All");
  list = getList("image.titles");
  Array.sort(list);

  for (p=0; p<list.length; p++) {
    if (p==0){
      continue;
    }else{
      close(list[p]);
    }
  }
  run("Close All");
}

waitForUser("I've finished");


//Listening to:
//Never Forgive Me, Never Forget Me by Akira Yamaoka