dir = getDirectory( "Where are your photos?" );
dir = replace(dir, "\\", "/");
  
folder_list = getFileList(dir);

// Open the first file of each folder in the list 
for (i=0; i<folder_list.length; i++) {
  pic_list = getFileList(dir + folder_list[i]);
  
  for (j=0; j<pic_list.length; j++){
    is_stitched = indexOf(pic_list[j], "stitched.tif");
    print(dir + folder_list[i] + pic_list[j]);
    if (is_stitched > 0){
      to_open = dir + folder_list[i] + pic_list[j];
      open(to_open);
      runMacro("005_all_processing.ijm");
      break;
    }
  }
}

