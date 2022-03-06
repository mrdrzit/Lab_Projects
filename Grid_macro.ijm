// command to draw a line grid on an image in a non-destructive overlay.

requires("1.43j");
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
  xoff=tileWidth;
  lamp=1;
  while (true && xoff<width) { // draw vertical lines
    if (lamp == 1){
      makeLine(xoff/2, 0, xoff/2, height);
      run("Add Selection...", "stroke="+color);
        xoff += tileWidth/2;
        lamp +=1;
        continue
    }
    makeLine(xoff, 0, xoff, height);
      run("Add Selection...", "stroke="+color);
        xoff += tileWidth;
   }
  yoff=tileHeight;
  while (true && yoff<height) { // draw horizonal lines
    if (lamp == 1){
      makeLine(0, yoff/2, width, yoff/2);
      run("Add Selection...", "stroke="+color);
        yoff += tileHeight/2;
        lamp +=1;
        continue
    }
    makeLine(0, yoff, width, yoff);
    run("Add Selection...", "stroke="+color);
      yoff += tileHeight;
   }
  run("Select None");