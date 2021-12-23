print("\\Clear");
run("Close All");
setOption("ExpandableArrays", true);

dir = getDirectory( "Where are your photos?" );
output = getDirectory( "Where do you want to store them?" );

dir = replace(dir, "\\", "/"); // Fixes the name of the directory in windows machines, inserting a '/'
output = replace(output, "\\", "/");

//I create a window where the user can indicate which values will be used in the processing


Dialog.create("Let's set the numebr of filters to process")
Dialog.addNumber("How many filters do you have?", 3);
Dialog.show();
var numFilters = Dialog.getNumber();

var filters = newArray();
var baseFilters = newArray("DAPI","DCX","BRDU","FILTER4","FILTER5","FILTER6","FILTER7","FILTER8")

for (i = 0; i < numFilters; i++){
  Dialog.create("Let's set the name of each filter")
  Dialog.addString("Name of filter "+(i+1)+"", baseFilters[i]);
  Dialog.show();
  filters[i] = Dialog.getString();
}
Array.deleteValue(filters, "undefined") //Remove valores undefined

Dialog.create("Let's set some options")
for (i = 0; i < numFilters; i++){
  Dialog.addCheckbox("Remove the background of the filter for "+filters[i]+"?", true);
}
Dialog.show();

for (i = 0; i < numFilters; i++){
  var remove_filter = Dialog.getCheckbox();
}

//TODO: Continue from here adding the features of a generic algorithm..


var list_file_names = getFileList(dir); //Gives a list with the filenames in the selected directory
list_file_names = Array.sort(list_file_names);

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

  //TODO: Modulate based on the control group's background (image histogram)

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
//Invisible Doors · Will Bates & Phil Mossman