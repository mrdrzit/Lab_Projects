print("\\Clear");
run("Close All");
setOption("ExpandableArrays", true);

run("Input/Output...", "jpeg=100 gif=-1 file=.csv use_file save_column");

// See if the scale is set and if it is global
if(!(is("global scale"))){
  run("Blobs");
  waitForUser("The scale is probably not set\nOr at least is not global\n\nIn the next window, please enter the scaling factor.\nTip: The known distance for 20x magnification is 0.5123 um/pixel\nAfter this, check nonetheless! :)");
  scale = getNumber("Known distance (um/pixels):", 0.5123);
  run("Set Scale...", "distance=1 known=" + scale + " unit=um global");
  close("*");
  exit("Don't forget to also set it as global if it was not set properly automatically!");
}

dir = getDirectory("Where are your photos?");
dir = replace(dir, "\\", "/"); // Fixes the name of the directory in windows machines, inserting a '/'


// Get a list of all neun and cfos images in the folder
list_files = getFileList(dir);
neun_images = newArray();
cfos_images = newArray();
dapi_images = newArray();
triple_images = newArray();

for(i = 0; i < list_files.length; i++){
  if (endsWith(list_files[i], "/")){
    continue;
  }else if (indexOf(list_files[i], "MAX_PROJECTION_neun.png") >= 0 && list_files[i].endsWith(".png")){
      neun_images = Array.concat(neun_images, list_files[i]);
  }else if (indexOf(list_files[i], "MAX_PROJECTION_cfos.png") >= 0 && list_files[i].endsWith(".png")){
      cfos_images = Array.concat(cfos_images, list_files[i]);
  }else if (indexOf(list_files[i], "MAX_PROJECTION_dapi.png") >= 0 && list_files[i].endsWith(".png")){
      dapi_images = Array.concat(dapi_images, list_files[i]);
  }else if (indexOf(list_files[i], "MERGE_dapi_neun_cfos.png") >= 0 && list_files[i].endsWith(".png")){
      triple_images = Array.concat(triple_images, list_files[i]);
  }
}

// Check if there is a directory for each type of image
neun_temp_path = dir + File.separator + "neun";
cfos_temp_path = dir + File.separator + "cfos";
dapi_temp_path = dir + File.separator + "dapi";
triple_temp_path = dir + File.separator + "triple";

name_to_save_neun = substring(neun_images[0], 0, (neun_images[0].length) - 4);
name_to_save_cfos = substring(cfos_images[0], 0, (cfos_images[0].length) - 4);
name_to_save_dapi = substring(dapi_images[0], 0, (dapi_images[0].length) - 4);
name_to_save_triple = substring(triple_images[0], 0, (triple_images[0].length) - 4);

if (!File.isDirectory(neun_temp_path)){
    File.makeDirectory(neun_temp_path)
}
if (!File.isDirectory(cfos_temp_path)){
    File.makeDirectory(cfos_temp_path)
}
if (!File.isDirectory(dapi_temp_path)){
    File.makeDirectory(dapi_temp_path)
}
if (!File.isDirectory(triple_temp_path)){
    File.makeDirectory(triple_temp_path)
}

// Copy the images to the respective directories
for (i = 0; i < neun_images.length; i++){
    File.copy(dir + File.separator + neun_images[i], neun_temp_path + File.separator + neun_images[i]);
}

for (i = 0; i < cfos_images.length; i++){
    File.copy(dir + File.separator + cfos_images[i], cfos_temp_path + File.separator + cfos_images[i]);
}

for (i = 0; i < dapi_images.length; i++){
    File.copy(dir + File.separator + dapi_images[i], dapi_temp_path + File.separator + dapi_images[i]);
}

for (i = 0; i < triple_images.length; i++){
    File.copy(dir + File.separator + triple_images[i], triple_temp_path + File.separator + triple_images[i]);
}

// Stitch the neun images
run("Grid/Collection stitching", "type=[Unknown position] order=[All files in directory] directory=[" + neun_temp_path + "] output_textfile_name=TileConfiguration.txt fusion_method=[Linear Blending] regression_threshold=0.50 max/avg_displacement_threshold=2 absolute_displacement_threshold=3.00 computation_parameters=[Save computation time (but use more RAM)] image_output=[Fuse and display]");
selectWindow("Fused");
full_file_path_to_save_neun = neun_temp_path + File.separator + name_to_save_neun + "_panorama.tif";
saveAs("PNG", full_file_path_to_save_neun);
close();

// Stitch the cfos images
run("Grid/Collection stitching", "type=[Unknown position] order=[All files in directory] directory=[" + cfos_temp_path + "] output_textfile_name=TileConfiguration.txt fusion_method=[Linear Blending] regression_threshold=0.80 max/avg_displacement_threshold=2 absolute_displacement_threshold=3.00 computation_parameters=[Save computation time (but use more RAM)] image_output=[Fuse and display]");
selectWindow("Fused");
full_file_path_to_save_cfos = cfos_temp_path + File.separator + name_to_save_cfos + "_panorama.tif";
saveAs("PNG", full_file_path_to_save_cfos);
close();

// Stitch the dapi images
run("Grid/Collection stitching", "type=[Unknown position] order=[All files in directory] directory=[" + dapi_temp_path + "] output_textfile_name=TileConfiguration.txt fusion_method=[Linear Blending] regression_threshold=0.80 max/avg_displacement_threshold=2 absolute_displacement_threshold=3.00 computation_parameters=[Save computation time (but use more RAM)] image_output=[Fuse and display]");
selectWindow("Fused");
full_file_path_to_save_dapi = dapi_temp_path + File.separator + name_to_save_dapi + "_panorama.tif";
saveAs("PNG", full_file_path_to_save_dapi);
close();

// Stitch the triple images
run("Grid/Collection stitching", "type=[Unknown position] order=[All files in directory] directory=[" + triple_temp_path + "] output_textfile_name=TileConfiguration.txt fusion_method=[Linear Blending] regression_threshold=0.80 max/avg_displacement_threshold=2 absolute_displacement_threshold=3.00 computation_parameters=[Save computation time (but use more RAM)] image_output=[Fuse and display]");
selectWindow("Fused");
full_file_path_to_save_triple = triple_temp_path + File.separator + name_to_save_triple + "_panorama.tif";
saveAs("PNG", full_file_path_to_save_triple);
close();