function extract_digits(a) {
	arr2 = newArray; //return array containing digits
	for (i = 0; i < a.length; i++) {
		str = a[i];
		digits = "";
		for (j = 0; j < str.length; j++) {
			ch = str.substring(j, j+1);
			if(!isNaN(parseInt(ch)))
				digits += ch;
		}
		arr2[i] = parseInt(digits);
	}
	return arr2;
}

dir = getDirectory( "Where are your photos?" );
dir = replace(dir, "\\", "/");
  
folder_list = getFileList(dir);

arr_num = extract_digits(folder_list);
Array.sort(arr_num, folder_list);

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

