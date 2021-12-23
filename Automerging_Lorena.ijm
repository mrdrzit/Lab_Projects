print("\\Clear");
run("Close All");
setOption("ExpandableArrays", true);
run("Bio-Formats Macro Extensions");

dir = getDirectory( "Where are your photos?" );
output = getDirectory( "Where do you want to store them?" );

dir = replace(dir, "\\", "/"); // Fixes the name of the directory in windows machines, inserting a '/'
output = replace(output, "\\", "/");
run("Fix Funny Filenames", "which="+dir);
print("\\Clear");

Dialog.create("Let's set the numebr of filters to process")
Dialog.addNumber("How many filters do you have?", 3);
Dialog.show();

var list_file_names = getFileList(dir); //Gives a list with the filenames in the selected directory
list_file_names = Array.sort(list_file_names);

for (i = 0; i < list_file_names.length; i++) { //Loop to select only .zvi images
  if(File.isDirectory(dir + File.separator + list_file_names[i])){
    exit("You need to select inside of the folder containing the images");
  }
  if(!(endsWith(list_file_names[i], ".zvi"))){
    exit("The files need to be in the .zvi format\nPlease check for different files in the selected folder and remove them");
  }
}

Array.sort(list_file_names);
qtd = list_file_names.length //The number of times that i'll iterate the loop

//Loop that actually processess the images
for (i=0; i < qtd; i++ ) {
  showProgress(i, qtd);
  atual = i + 1;

  print("\nI'm processing the photo " + list_file_names[i] + " for you");
  current_image = dir+list_file_names[i];
  run("Bio-Formats Importer", "open="+current_image+" autoscale color_mode=Default rois_import=[ROI manager] split_channels view=Hyperstack stack_order=XYCZT");
  run("Show All");
  list_open_filters = getList("image.titles"); //Creates an array with the names of the currently open windows

  //Create a composite of the available filters
  Array.sort(list_open_filters);

  //Creates a building block to run the complete statement later (with the selected filters)
  run("Merge Channels...", "c2=["+ list_open_filters[1] + "] c3=[" + list_open_filters[2] + "] c7=[" + list_open_filters[0] + "] create keep");

  //Selects all the images and saves the composite as a .TIFF for further analysis
  run("Show All");
  list_open_filters = getList("image.titles");

  name_atual = File.nameWithoutExtension;

  selectImage("Composite");
  saveAs("TIFF", output + name_atual + ".tiff");

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

waitForUser("I've finished processing all of your photos\n:)");


//Listening to:
//(Ocean) Bloom ft. Radiohead