run("Blobs");
scale = getNumber("Known distance (um/pixels):", 0.5123);
run("Set Scale...", "distance=1 known="+scale+" unit=um global");
close("*");