image_bit_depth = bitDepth();
run("Input/Output...", "jpeg=100 gif=-1 file=.csv use_file save_column");

if(!(is("global scale"))){
  waitForUser("The scale is probably not set\nOr at least is not global");
  exit("Please, adjust the scale and also set it as global!");
}

name = File.getNameWithoutExtension(getTitle);
directory = getDir("image");

if(image_bit_depth != 8){
  selectWindow(getTitle);
  setOption("ScaleConversions", true);
  run("8-bit");
  waitForUser("The image is probably not in 8bit\nI tried to convert it, but check nonetheless! :)");
}

save_path = directory + name + ".roi";
saveAs("Selection", save_path);

run("Measure");
String.copy(d2s(getResult("Area"), 3));

run("Clear Outside");

run("Subtract Background...", "rolling=50 light");

run("Threshold...");
setThreshold(0, 207);

// Listening to: ??????? salyu × salyu GHOST IN THE SHELL ARISE

