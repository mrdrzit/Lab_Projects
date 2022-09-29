run("Blobs");
scale = getNumber("Known distance (um/pixels):", 0.2558);
run("Set Scale...", "distance=1 known="+scale+" unit=um global");
close("*");