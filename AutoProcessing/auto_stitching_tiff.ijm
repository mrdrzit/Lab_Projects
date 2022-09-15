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

function directories(dir) {
  list = getFileList(dir);
  for (i=0; i<list.length; i++) {
    if (endsWith(list[i], "/")){
      directory_list[idx] = list[i];
      idx++;
    }else{
      continue;
    }
  }
}

setOption("ExpandableArrays", true);
run("Close All");

dir = getDirectory( "Where are your photos?" );
output = dir;

dir = replace(dir, "\\", "/"); // Fixes the name of the directory in windows machines, inserting a '/'
output = replace(output, "\\", "/");
var to_process = newArray(30000);
var directory_list = newArray(30000);
var current_file_list = newArray(30000);
idj = 0;
idx = 0;

directories(dir);
directory_list = Array.deleteValue(directory_list, 0); //Remove undefined

if (directory_list.length != 0) {
  print("\nThere are multiple subfolders in this folder.\nChecking them one by one...\n");
  for (i=0; i<directory_list.length; i++) {
    current_dir = dir + directory_list[i];
    print("working on the folder: " + current_dir);
    run("Grid/Collection stitching", "type=[Unknown position] order=[All files in directory] directory=["+ current_dir +"] output_textfile_name=TileConfiguration.txt fusion_method=[Linear Blending] regression_threshold=0.30 max/avg_displacement_threshold=2.50 absolute_displacement_threshold=3.50 frame=1 ignore_z_stage computation_parameters=[Save computation time (but use more RAM)] image_output=[Fuse and display]");
    tmp = getFileList(current_dir);
    name_to_save = substring(tmp[0], 0, (tmp[0].length)-6);
    full_path_with_file = current_dir + name_to_save;
    selectImage("Fused");
    saveAs("Tiff", full_path_with_file + "_stitched.tif");
    run("Close All");
  }
}
else{
  print("\nThere are only images in this folder.\nWorking with all of them...\n");
  current_dir = dir;
  run("Grid/Collection stitching", "type=[Unknown position] order=[All files in directory] directory=["+current_dir +"] output_textfile_name=TileConfiguration.txt fusion_method=[Linear Blending] regression_threshold=0.30 max/avg_displacement_threshold=2.50 absolute_displacement_threshold=3.50 frame=1 ignore_z_stage computation_parameters=[Save computation time (but use more RAM)] image_output=[Fuse and display]");    
  tmp = getFileList(current_dir);
  name_to_save = substring(tmp[0], 0, (tmp[0].length)-6);
  full_path_with_file = current_dir + name_to_save;
  selectImage("Fused");
  wait(200);
  saveAs("Tiff", full_path_with_file + "_stitched.tif");
  run("Close All");
}

waitForUser("Done!\n =]");

// Listening to: Eyes Without a Face by Billy Idol