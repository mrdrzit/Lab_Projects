opened_images = getList("image.titles");
for (i = 0; i < opened_images.length; i++) {
    selectWindow(opened_images[i]);

    name = File.getNameWithoutExtension(getTitle);
    directory = getDir("image");
    roi = directory + name + ".roi";

    open(roi);
    roi_load = isOpen(name + ".roi");
    if (roi_load) {
        // Create a dialog
        Dialog.create("Rotate Image");
        Dialog.addRadioButtonGroup("Rotation Direction:", newArray("Left", "Right"), 1, 2, "Left");
        Dialog.show();
        // Get the user's choice
        rotationDirection = Dialog.getRadioButton();

        if (rotationDirection == "Left") {
            selectWindow(opened_images[i]);
            run("Rotate 90 Degrees Left");
        } else if (rotationDirection == "Right") {
            selectWindow(opened_images[i]);
            run("Rotate 90 Degrees Right");
        }

        selectWindow(opened_images[i]);
        // waitForUser("If the image needs to be rotated, do it now\nIf not, click OK to continue");
        resetMinAndMax();
        run("Save");
        close(name + ".roi");
        open(roi);
    }

    run("Enhance Contrast", "saturated=0.8");
    waitForUser("Check if the roi is correct\nIf so, click OK to continue");
    resetMinAndMax();
    close(opened_images[i]);
}