opened_images = getList("image.titles");
for (i = 0; i < opened_images.length; i++) {
    selectWindow(opened_images[i]);

    // Get the image bit depth
    image_bit_depth = bitDepth();

    // Imagej has a input/output settings that, when creating or importing some
    // files, it reads from and sets the configuration for that
    // This line is adjusting this to make the program output csv files with a
    // header and eliminates the compression on jpeg files
    run("Input/Output...", "jpeg=100 gif=-1 file=.csv use_file save_column");

    // This is just setting the name and directory for input/output
    name = File.getNameWithoutExtension(getTitle);
    directory = getDir("image");

    // we needed to have an image in 8-bit so here i check if the current image
    // is in this bit-depth. If not i try to convert it
    if (image_bit_depth != 8) {
        selectWindow(getTitle);
        setOption("ScaleConversions", true);
        run("8-bit");
        waitForUser("The image is probably not in 8bit\nI tried to convert it, but check nonetheless! :)");
    }
    selectWindow(opened_images[i]);
    run("Enhance Contrast", "saturated=0.8");

    waitForUser("Create the ROI and click OK to save it");
    // We were saving the ROIs created during the analysis as a form of backup
    save_path = directory + name + ".roi";
    saveAs("Selection", save_path);
    resetMinAndMax();
    close(opened_images[i]);
}