function listFiles(dir) {
  list = getFileList(dir);
  for (i=0; i<list.length; i++) {
    if (endsWith(list[i], "/")){
      listFiles(""+dir+list[i]);
      idx++;
    }
    else{
      to_process[idx] = dir + list[i];
      idx++;
    }
  }
}

run("Close All");

dir = getDirectory( "Where are your photos?" );
output = dir;

dir = replace(dir, "\\", "/"); // Fixes the name of the directory in windows machines, inserting a '/'
output = replace(output, "\\", "/");
var to_process = newArray(0);
idx = 0;
listFiles(dir);

Array.sort(to_process);
qtd = to_process.length //The number of times that i'll iterate the loop

//Loop that actually processess the images
for (i=0; i < qtd; i++ ) {
  atual = i + 1;

  current_image = to_process[i];
  run("Bio-Formats Importer", "open=["+current_image+"] autoscale color_mode=[Default]");
  run("Show All");
  list_open_windows = getList("image.titles"); //Creates an array with the names of the currently open windows
  Array.sort(list_open_windows);

  //Selects all the images and saves the composite as a .TIFF for further analysis
  run("Show All");
  list_open_windows = getList("image.titles");
  nome_atual = File.nameWithoutExtension;
  
  selectWindow(current_image);
  setOption("ScaleConversions", true);
  run("8-bit");

  //selectImage(current_image);
  dir_without_file = replace(current_image, File.getName(current_image), "");
  saveAs("Tiff", dir_without_file + nome_atual + ".tif");
  run("Close All");
}


waitForUser("I've finished processing all of your photos\n:)");


//Listening to:
//Death Note - Track 