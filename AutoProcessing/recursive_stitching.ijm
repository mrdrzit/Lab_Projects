rootDir = getDirectory("Where are your photos?");
rootDir = replace(rootDir, "\\", "/");
allList = getFileList(rootDir);

for (rooti = 0; rooti < allList.length; rooti++) {
    hemi_list = getFileList(rootDir + allList[rooti]);
    for (sidei = 0; sidei < hemi_list.length; sidei++) {
        slice_list = getFileList(rootDir + allList[rooti] + hemi_list[sidei]);
        for (slicei = 0; slicei < slice_list.length; slicei++) {
            side_list = getFileList(rootDir + allList[rooti] + hemi_list[sidei] + slice_list[slicei]);
            for (hemispheri = 0; hemispheri < side_list.length; hemispheri++) {
                current_pano = rootDir + allList[rooti] + hemi_list[sidei] + slice_list[slicei] + side_list[hemispheri];
                print("Arranging: " + current_pano);
                runMacro("auto_stitching_tiff.ijm", current_pano)
            }
        }
    }
}


// Listening to Hybrisma - Datura