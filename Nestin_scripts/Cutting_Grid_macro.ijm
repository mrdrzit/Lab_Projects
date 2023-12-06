// Command to draw a line grid on an image in a non-destructive overlay and then cut the image into pieces.
// getSelectionBounds(x, y, width, height);

requires("1.53d");

// Prompt the user to select the directory for storing chopped-up photos
dir = getDirectory("Where do you want to store your chopped-up photo?");

// Fix the directory name by replacing backslashes with forward slashes (Windows-specific adjustment)
dir = replace(dir, "\\", "/");

// Set the color for drawing the grid lines
color = "red";

// Define the number of lines for the grid
nLines = 4;

// Check if there are any open images
if (nImages == 0) {
  waitForUser("No images opened");
  exit();
}

// Remove any existing overlay
run("Remove Overlay");

// Get the width and height of the current image
width = getWidth;
height = getHeight;

// Calculate the tile dimensions for the grid
tileWidth = width / (nLines + 1);
tileHeight = tileWidth;

// Initialize offsets for the grid
xoff = yoff = tileWidth;

// Create the initial rectangle for the first grid cell
makeRectangle(0, 0, tileWidth, tileHeight);
Overlay.addSelection;
currentX = currentY = 0;

// Loop to chop the images into pieces
while (true) {
  // Crop the image based on the overlay and save it to the specified directory in TIFF format
  Overlay.cropAndSave(dir, "tif");

  // Get the bounds of the overlay for the current grid cell
  Overlay.getBounds(0, currentX, currentY, currentWidth, currentHeight);

  // Remove the overlay
  Overlay.remove;

  // Create a new rectangle for the next grid cell
  makeRectangle(currentX + xoff, currentY, tileWidth, tileHeight);
  Overlay.addSelection;

  // Check if the end of the row is reached, move to the next row if necessary
  if (currentX + xoff >= width) {
    if ((currentX + xoff + 30) > width && (currentY + yoff + 30) > height) {
      break; // Exit the loop if the entire image is covered
    }

    // Remove the overlay and reset coordinates for the new row
    Overlay.remove;
    currentX = 0;
    currentY += yoff;
    makeRectangle(currentX, currentY, tileWidth, tileHeight);
    Overlay.addSelection;
  }
}

// Clear the selection and notify the user that the process is complete
run("Select None");
waitForUser("I've finished");

// Listening to "there is light in us" - Mathbonus
