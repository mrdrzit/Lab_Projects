run("Show All");

list = getList("image.titles"); 

for (i=0; i<list.length; i++) {
	if (indexOf(list[i], "C=0") >= 0) {
	selectWindow(list[i]);
	run("Z Project...", "start=3 stop=10 projection=[Max Intensity]");
	selectWindow(list[i]);
	close();
	} else {
	selectWindow(list[i]);
	run("Z Project...", "start=3 stop=10 projection=[Average Intensity]");
	selectWindow(list[i]);
	close();
	}
}

run("Show All");
list = getList("image.titles");

for (i=0; i<list.length; i++) {
	if (indexOf(list[i], "C=0.tif") >= 0) {
		selectWindow(list[i]);
		run("Subtract Background...", "rolling=30");
		setOption("ScaleConversions", true);
		run("8-bit");
	}else if (indexOf(list[i], "C=1.tif") >= 0) {
		selectWindow(list[i]);
		run("Subtract Background...", "rolling=30");
		setOption("ScaleConversions", true);
		run("8-bit");
	}else if (indexOf(list[i], "C=2.tif") >= 0) {
		selectWindow(list[i]);
		run("Subtract Background...", "rolling=50");
		setOption("ScaleConversions", true);
		run("8-bit");
	}
}

Array.sort(list)
run("Merge Channels...", "c2=["+ list[2] + "] c3=[" + list[0] + "] c6=[" + list[1] + "] create keep");