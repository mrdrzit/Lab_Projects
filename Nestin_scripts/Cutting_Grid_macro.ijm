// command to draw a line grid on an image in a non-destructive overlay and the cut the image into pieces.
//getSelectionBounds(x, y, width, height);

requires("1.53d");
dir = getDirectory( "Where do you want to store your chopped up photo?" );

dir = replace(dir, "\\", "/"); // Fixes the name of the directory in windows machines, inserting a '/'

  color = "red";
  nLines = 4;
  if (nImages==0) {
    waitForUser("No images opened");
    exit();
  }
  run("Remove Overlay");
  width = getWidth;
  height = getHeight;
  tileWidth = width/(nLines+1);
  tileHeight = tileWidth;
  xoff = yoff = tileWidth;
  makeRectangle(0, 0, tileWidth, tileHeight);
  Overlay.addSelection;
  currentX = currentY = 0;

  while (true) { // Chop the images into pieces
    Overlay.cropAndSave(dir, "tif");
    Overlay.getBounds(0, currentX, currentY, currentWidth, currentHeight);
    Overlay.remove;
    makeRectangle(currentX + xoff, currentY, tileWidth, tileHeight);
    Overlay.addSelection;
    if (currentX + xoff >= width){
      if((currentX + xoff + 30) > width && (currentY + yoff + 30) > height){
        break
      }
      Overlay.remove;
      currentX = 0;
      currentY += yoff;
      makeRectangle(currentX, currentY, tileWidth, tileHeight);
      Overlay.addSelection;
    }
  }
  run("Select None");
  waitForUser("I've finished");


  //Listening to "there is light in us" - Mathbonus