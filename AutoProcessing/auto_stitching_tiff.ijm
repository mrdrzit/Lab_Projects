function listdirs(dir) {
  list = getFileList(dir);
  for (i=0; i<list.length; i++) {
    if (startsWith(list[i], "hipocampo")){
      listdirs(""+dir+list[i]);
      idx++;
    }
    else if (endsWith(list[i], "/")){
      to_process[idx] = list[i];
      idx++;
    }
  }
}

function listFiles(dir) {
    list = getFileList(dir);
    for (i=0; i<list.length; i++) {
      if (endsWith(list[i], "/")){
          listFiles(""+dir+list[i]);
      }else{
          idj++;
          all_files[idj] = dir + list[i];
    }
  }
}

function directories(dir) {
  list = getFileList(dir);
  for (i=0; i<list.length; i++) {
    if (endsWith(list[i], "/")){
      current_directories[idx] = list[i];
      idx++;
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
var all_files = newArray(30000);
var current_directories = newArray(30000);
idj = 0;
idx = 0;
listFiles(dir);
listdirs(dir);
subdir_list = getFileList(dir);

all_files = Array.deleteValue(all_files, 0); //Remove undefined
to_process = Array.deleteValue(to_process, 0); //Remove undefined
subdir_list = Array.deleteValue(subdir_list, 0); //Remove undefined


if (subdir_list.length != 0) {
  print("\nThere are multiple subfolders in this folder.\nChecking them one by one...\n");
  for (i=0; i<subdir_list.length; i++) {
    current_dir = subdir_list[i];
    directories(dir + subdir_list[i]);
    current_directories = Array.deleteValue(current_directories, 0); //Remove undefined
    for(lindex=0; lindex<current_directories.length; lindex++){  
      print(current_directories.length);
      tmp_name_dir = dir + subdir_list[i] + current_directories[lindex];
      print("working on the folder: " + current_dir);
      run("Grid/Collection stitching", "type=[Sequential Images] order=[All files in directory] directory=["+ tmp_name_dir +"] output_textfile_name=TileConfiguration.txt fusion_method=[Linear Blending] regression_threshold=0.30 max/avg_displacement_threshold=2.50 absolute_displacement_threshold=3.50 frame=1 ignore_z_stage computation_parameters=[Save computation time (but use more RAM)] image_output=[Fuse and display]");
      tmp = getFileList(dir + current_dir + current_directories[lindex]);
      name_to_save = substring(tmp[0], 0, (tmp[0].length)-6);
      full_path_with_file = dir + current_dir + current_directories[lindex] + name_to_save;
      selectImage("Fused");
      saveAs("Tiff", full_path_with_file + "_stitched.tif");
      run("Close All");
    }
    current_directories = newArray(30000);
  }
}
else{
  print("\nThere are only images in this folder.\nWorking with all of them...\n");
  for (i=0; i<to_process.length; i++) {
    print("working on the folder: " + dir + to_process[i]);
    current_dir = dir + to_process[i];
    run("Grid/Collection stitching", "type=[Sequential Images] order=[All files in directory] directory=["+current_dir +"] output_textfile_name=TileConfiguration.txt fusion_method=[Linear Blending] regression_threshold=0.30 max/avg_displacement_threshold=2.50 absolute_displacement_threshold=3.50 frame=1 ignore_z_stage computation_parameters=[Save computation time (but use more RAM)] image_output=[Fuse and display]");    
    tmp = getFileList(current_dir);
    name_to_save = substring(tmp[0], 0, (tmp[0].length)-6);
    full_path_with_file = current_dir + name_to_save;
    selectImage("Fused");
    wait(200);
    saveAs("Tiff", full_path_with_file + "_stitched.tif");
    run("Close All");
  }
}

waitForUser("Done!\n =]");

// Listening to: Eyes Without a Face by Billy Idol