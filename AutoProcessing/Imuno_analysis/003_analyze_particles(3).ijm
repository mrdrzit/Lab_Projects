if (isOpen("Results")){
  selectWindow("Results"); 
  run("Close");
}

run("Analyze Particles...", "size=10-Infinity show=Masks display summarize add");

id = getImageID();
selectImage(id);
directory = File.directory;

name = File.getNameWithoutExtension(getTitle);
save_directory = directory + name + ".tif";
saveAs("Tiff", save_directory);

close("Results");

Table.rename("Summary", "Results");

selectWindow("Results");

//Table.deleteColumn("Slice");

Table.update;

String.copyResults;

waitForUser("Please, check:\n- If the mask was saved\n- If you pasted the results into the excel table\n- If everything's in order, then press OK to continue!");

if (isOpen("Results")){
  selectWindow("Results"); 
  run("Close");
}
if (isOpen("Log")){
  selectWindow("Log");
  run("Close");
}
if (isOpen("ROI Manager")){
  selectWindow("ROI Manager"); 
  run("Close");
}
while (nImages()>0){
  selectImage(nImages());  
  run("Close");
}

waitForUser("Finished\nLets go to the next one! :)");

// Listening to: salyu × salyu GHOST IN THE SHELL ARISE