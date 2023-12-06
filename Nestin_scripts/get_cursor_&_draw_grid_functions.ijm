// Function to draw a grid on the image
function draw_grid() {
	// Set the color and number of lines for the grid
	color = "red";
	nLines = 20;
  
	// Check if there are any open images
	if (nImages == 0)
	  waitForUser("There are no images opened");
  
	// Remove any existing overlay
	run("Remove Overlay");
  
	// Get the width and height of the current image
	width = getWidth;
	height = getHeight;
  
	// Calculate the tile dimensions for the grid
	tileWidth = width / (nLines + 1);
	tileHeight = tileWidth;
  
	// Initialize offsets for drawing lines
	xoff = tileWidth;
  
	// Draw vertical lines
	while (true && xoff < width) {
	  makeLine(xoff, 0, xoff, height);
	  run("Add Selection...", "stroke=" + color);
	  xoff += tileWidth;
	}
  
	// Reset offset for drawing horizontal lines
	yoff = tileHeight;
  
	// Draw horizontal lines
	while (true && yoff < height) {
	  makeLine(0, yoff, width, yoff);
	  run("Add Selection...", "stroke=" + color);
	  yoff += tileHeight;
	}
  
	// Clear the selection
	run("Select None");
  }
  
  // Function to get cursor location from user input
  function get_cursor() {
	waitForUser("Now click where the grid should intersect the image");
  
	// Define constants for mouse buttons
	shift = 1;
	ctrl = 2;
	rightButton = 4;
	alt = 8;
	leftButton = 16;
  
	// Initialize variables to track cursor location and flags
	x2 = -1;
	y2 = -1;
	z2 = -1;
	flags2 = -1;
	logOpened = false;
	clicked = false;
  
	// Disable pop-up menu if using version 1.37r or later
	if (getVersion >= "1.37r")
	  setOption("DisablePopupMenu", true);
  
	// Loop until the user clicks with the left mouse button
	while (!clicked) {
	  getCursorLoc(x, y, z, flags);
  
	  // Check for a left mouse button click
	  if (x != x2 || y != y2 || z != z2 || flags != flags2) {
		if (flags & leftButton != 0) {
		  clicked = true;
		  x_clicked = x;
		  y_clicked = y;
		  print("Cursor location saved: (" + x_clicked + ", " + y_clicked + ")");
		  return newArray(x_clicked, y_clicked);
		}
	  }
  
	  // Update variables and wait for 10 milliseconds
	  x2 = x;
	  y2 = y;
	  z2 = z;
	  flags2 = flags;
	  wait(10);
	}
  
	// Enable pop-up menu if disabled
	if (getVersion >= "1.37r")
	  setOption("DisablePopupMenu", false);
  }
  