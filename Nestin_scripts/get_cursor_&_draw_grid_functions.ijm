function draw_grid() { 
	color = "red";
	nLines = 20;
	if (nImages==0) waitForUser("There are no images opened");
	run("Remove Overlay");
	width = getWidth;
	height = getHeight;
	tileWidth = width/(nLines+1);
	tileHeight = tileWidth;
	xoff=tileWidth;
	while (true && xoff<width) { // draw vertical lines
	  makeLine(xoff, 0, xoff, height);
	  run("Add Selection...", "stroke="+color);
	  xoff += tileWidth;
	}
	yoff=tileHeight;
	while (true && yoff<height) { // draw horizonal lines
	  makeLine(0, yoff, width, yoff);
	  run("Add Selection...", "stroke="+color);
	  yoff += tileHeight;
	}
	run("Select None");
}

function get_cursor(){
	waitForUser("Now click where the grid should intersect the image");
	shift=1;
	ctrl=2; 
	rightButton=4;
	alt=8;
	leftButton=16;
	
	x2=-1; y2=-1; z2=-1; flags2=-1;
	logOpened = false;
	clicked = false;
	
	if (getVersion>="1.37r")
	    setOption("DisablePopupMenu", true);
	
	while (!clicked) {
	    getCursorLoc(x, y, z, flags);
	    if (x!=x2 || y!=y2 || z!=z2 || flags!=flags2) {
	        if (flags&leftButton!=0) {
	            clicked = true;
	            x_clicked = x;
	            y_clicked = y;
	            print("Cursor location saved: (" + x_clicked + ", " + y_clicked + ")");
	            return newArray(x_clicked, y_clicked);
	        }
	    }
	    x2=x; y2=y; z2=z; flags2=flags;
	    wait(10);
	}
	
	if (getVersion>="1.37r")
	    setOption("DisablePopupMenu", false);
}
