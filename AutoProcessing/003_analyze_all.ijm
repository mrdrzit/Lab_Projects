// This function is used for calculating the sum of values of the
// histogram_count array.
function get_sum(start, end, histogram_count) {
    sum = 0;
    for (i = start; i < end; i++) {
        sum = sum + histogram_count[i];
    }
    return sum;
}

opened_images = getList("image.titles");
for (i = 0; i < opened_images.length; i++) {

    selectWindow(opened_images[i]);

    name = File.getNameWithoutExtension(getTitle);
    directory = getDir("image");
    roi = directory + name + ".roi";
    open(roi);


    run("Measure");
    String.copy(d2s(getResult("Area"), 0));

    run("Clear Outside");

    waitForUser("Check if the region outside of the selection was cleared\nIf so, click OK to continue");

    run("Threshold...");
    setAutoThreshold("Moments dark ");
    setOption("BlackBackground", true);
    setThreshold(24, 255);

    waitForUser("Check if the threshold was set\nIf so, click OK to continue");

    if (isOpen("Results")) {
        selectWindow("Results");
        close("Results");
    }

    run("Analyze Particles...", "size=100-1500 circularity=0.10-1.00 show=[Overlay Masks] display clear summarize add");
    roiManager("Save", directory + name + "_roi_set.zip");

    Table.rename("Summary", "Results");
    selectWindow("Results");
    Table.update;
    String.copyResults;
    waitForUser("Please, check:\n- If the mask was saved\n- If you pasted the results into the excel table\n- If everything's in order, then press OK to continue!");

    if (isOpen("Results")) {
        selectWindow("Results");
        run("Close");
    }
    if (isOpen("Log")) {
        selectWindow("Log");
        run("Close");
    }
    if (isOpen("ROI Manager")) {
        selectWindow("ROI Manager");
        run("Close");
    }

    selectWindow(opened_images[i]);
    close(opened_images[i]);
}

