// "StartupMacros"
// The macros and macro tools in this file ("StartupMacros.txt") are
// automatically installed in the Plugins>Macros submenu and
//  in the tool bar when ImageJ starts up.

//  About the drawing tools.
//
//  This is a set of drawing tools similar to the pencil, paintbrush,
//  eraser and flood fill (paint bucket) tools in NIH Image. The
//  pencil and paintbrush draw in the current foreground color
//  and the eraser draws in the current background color. The
//  flood fill tool fills the selected area using the foreground color.
//  Hold down the alt key to have the pencil and paintbrush draw
//  using the background color or to have the flood fill tool fill
//  using the background color. Set the foreground and background
//  colors by double-clicking on the flood fill tool or on the eye
//  dropper tool.  Double-click on the pencil, paintbrush or eraser
//  tool  to set the drawing width for that tool.
//
// Icons contributed by Tony Collins.

// Global variables
var pencilWidth=1,  eraserWidth=10, leftClick=16, alt=8;
var brushWidth = 10; //call("ij.Prefs.get", "startup.brush", "10");
var floodType =  "8-connected"; //call("ij.Prefs.get", "startup.flood", "8-connected");

// The macro named "AutoRunAndHide" runs when ImageJ starts
// and the file containing it is not displayed when ImageJ opens it.

// macro "AutoRunAndHide" {}

function UseHEFT {
  requires("1.38f");
  state = call("ij.io.Opener.getOpenUsingPlugins");
  if (state=="false") {
    setOption("OpenUsingPlugins", true);
    showStatus("TRUE (images opened by HandleExtraFileTypes)");
  } else {
    setOption("OpenUsingPlugins", false);
    showStatus("FALSE (images opened by ImageJ)");
  }
}

UseHEFT();

// The macro named "AutoRun" runs when ImageJ starts.

macro "AutoRun" {
  // run all the .ijm scripts provided in macros/AutoRun/
  autoRunDirectory = getDirectory("imagej") + "/macros/AutoRun/";
  if (File.isDirectory(autoRunDirectory)) {
    list = getFileList(autoRunDirectory);
    // make sure startup order is consistent
    Array.sort(list);
    for (i = 0; i < list.length; i++) {
      if (endsWith(list[i], ".ijm")) {
        runMacro(autoRunDirectory + list[i]);
      }
    }
  }
}

var pmCmds = newMenu("Popup Menu",
  newArray("Help...", "Rename...", "Duplicate...", "Original Scale",
  "Paste Control...", "-", "Record...", "Capture Screen ", "Monitor Memory...",
  "Find Commands...", "Control Panel...", "Startup Macros...", "Search..."));

macro "Popup Menu" {
  cmd = getArgument();
  if (cmd=="Help...")
    showMessage("About Popup Menu",
      "To customize this menu, edit the line that starts with\n\"var pmCmds\" in ImageJ/macros/StartupMacros.txt.");
  else
    run(cmd);
}

macro "Abort Macro or Plugin (or press Esc key) Action Tool - CbooP51b1f5fbbf5f1b15510T5c10X" {
  setKeyDown("Esc");
}

var xx = requires138b(); // check version at install
function requires138b() {requires("1.38b"); return 0; }

var dCmds = newMenu("Developer Menu Tool",
newArray("ImageJ Website","News", "Documentation", "ImageJ Wiki", "Resources", "Macro Language", "Macros",
  "Macro Functions", "Startup Macros...", "Plugins", "Source Code", "Mailing List Archives", "-", "Record...",
  "Capture Screen ", "Monitor Memory...", "List Commands...", "Control Panel...", "Search...", "Debug Mode"));

macro "Developer Menu Tool - C037T0b11DT7b09eTcb09v" {
  cmd = getArgument();
  if (cmd=="ImageJ Website")
    run("URL...", "url=http://rsbweb.nih.gov/ij/");
  else if (cmd=="News")
    run("URL...", "url=http://rsbweb.nih.gov/ij/notes.html");
  else if (cmd=="Documentation")
    run("URL...", "url=http://rsbweb.nih.gov/ij/docs/");
  else if (cmd=="ImageJ Wiki")
    run("URL...", "url=http://imagejdocu.tudor.lu/imagej-documentation-wiki/");
  else if (cmd=="Resources")
    run("URL...", "url=http://rsbweb.nih.gov/ij/developer/");
  else if (cmd=="Macro Language")
    run("URL...", "url=http://rsbweb.nih.gov/ij/developer/macro/macros.html");
  else if (cmd=="Macros")
    run("URL...", "url=http://rsbweb.nih.gov/ij/macros/");
  else if (cmd=="Macro Functions")
    run("URL...", "url=http://rsbweb.nih.gov/ij/developer/macro/functions.html");
  else if (cmd=="Plugins")
    run("URL...", "url=http://rsbweb.nih.gov/ij/plugins/");
  else if (cmd=="Source Code")
    run("URL...", "url=http://rsbweb.nih.gov/ij/developer/source/");
  else if (cmd=="Mailing List Archives")
    run("URL...", "url=https://list.nih.gov/archives/imagej.html");
  else if (cmd=="Debug Mode")
    setOption("DebugMode", true);
  else if (cmd!="-")
    run(cmd);
}

var sCmds = newMenu("Stacks Menu Tool",
  newArray("Add Slice", "Delete Slice", "Next Slice [>]", "Previous Slice [<]", "Set Slice...", "-",
    "Convert Images to Stack", "Convert Stack to Images", "Make Montage...", "Reslice [/]...", "Z Project...",
    "3D Project...", "Plot Z-axis Profile", "-", "Start Animation", "Stop Animation", "Animation Options...",
    "-", "MRI Stack (528K)"));
macro "Stacks Menu Tool - C037T0b11ST8b09tTcb09k" {
  cmd = getArgument();
  if (cmd!="-") run(cmd);
}

var luts = getLutMenu();
var lCmds = newMenu("LUT Menu Tool", luts);
macro "LUT Menu Tool - C037T0b11LT6b09UTcb09T" {
  cmd = getArgument();
  if (cmd!="-") run(cmd);
}
function getLutMenu() {
  list = getLutList();
  menu = newArray(16+list.length);
  menu[0] = "Invert LUT"; menu[1] = "Apply LUT"; menu[2] = "-";
  menu[3] = "Fire"; menu[4] = "Grays"; menu[5] = "Ice";
  menu[6] = "Spectrum"; menu[7] = "3-3-2 RGB"; menu[8] = "Red";
  menu[9] = "Green"; menu[10] = "Blue"; menu[11] = "Cyan";
  menu[12] = "Magenta"; menu[13] = "Yellow"; menu[14] = "Red/Green";
  menu[15] = "-";
  for (i=0; i<list.length; i++)
    menu[i+16] = list[i];
  return menu;
}

function getLutList() {
  lutdir = getDirectory("luts");
  list = newArray("No LUTs in /ImageJ/luts");
  if (!File.exists(lutdir))
    return list;
  rawlist = getFileList(lutdir);
  if (rawlist.length==0)
    return list;
  count = 0;
  for (i=0; i< rawlist.length; i++)
    if (endsWith(rawlist[i], ".lut")) count++;
  if (count==0)
    return list;
  list = newArray(count);
  index = 0;
  for (i=0; i< rawlist.length; i++) {
    if (endsWith(rawlist[i], ".lut"))
      list[index++] = substring(rawlist[i], 0, lengthOf(rawlist[i])-4);
  }
  return list;
}

macro "Pencil Tool - C037L494fL4990L90b0Lc1c3L82a4Lb58bL7c4fDb4L5a5dL6b6cD7b" {
  getCursorLoc(x, y, z, flags);
  if (flags&alt!=0)
    setColorToBackgound();
  draw(pencilWidth);
}

macro "Paintbrush Tool - C037La077Ld098L6859L4a2fL2f4fL3f99L5e9bL9b98L6888L5e8dL888c" {
  getCursorLoc(x, y, z, flags);
  if (flags&alt!=0)
    setColorToBackgound();
  draw(brushWidth);
}

macro "Flood Fill Tool -C037B21P085373b75d0L4d1aL3135L4050L6166D57D77D68La5adLb6bcD09D94" {
  requires("1.34j");
  setupUndo();
  getCursorLoc(x, y, z, flags);
  if (flags&alt!=0) setColorToBackgound();
  floodFill(x, y, floodType);
}

function draw(width) {
  requires("1.32g");
  setupUndo();
  getCursorLoc(x, y, z, flags);
  setLineWidth(width);
  moveTo(x,y);
  x2=-1; y2=-1;
  while (true) {
    getCursorLoc(x, y, z, flags);
    if (flags&leftClick==0) exit();
    if (x!=x2 || y!=y2)
      lineTo(x,y);
    x2=x; y2 =y;
    wait(10);
  }
}

function setColorToBackgound() {
  savep = getPixel(0, 0);
  makeRectangle(0, 0, 1, 1);
  run("Clear");
  background = getPixel(0, 0);
  run("Select None");
  setPixel(0, 0, savep);
  setColor(background);
}

// Runs when the user double-clicks on the pencil tool icon
macro 'Pencil Tool Options...' {
  pencilWidth = getNumber("Pencil Width (pixels):", pencilWidth);
}

// Runs when the user double-clicks on the paint brush tool icon
macro 'Paintbrush Tool Options...' {
  brushWidth = getNumber("Brush Width (pixels):", brushWidth);
  call("ij.Prefs.set", "startup.brush", brushWidth);
}

// Runs when the user double-clicks on the flood fill tool icon
macro 'Flood Fill Tool Options...' {
  Dialog.create("Flood Fill Tool");
  Dialog.addChoice("Flood Type:", newArray("4-connected", "8-connected"), floodType);
  Dialog.show();
  floodType = Dialog.getChoice();
  call("ij.Prefs.set", "startup.flood", floodType);
}

macro "Set Drawing Color..."{
  run("Color Picker...");
}

macro "-" {} //menu divider

macro "About Startup Macros..." {
  title = "About Startup Macros";
  text = "Macros, such as this one, contained in a file named\n"
    + "'StartupMacros.txt', located in the 'macros' folder inside the\n"
    + "Fiji folder, are automatically installed in the Plugins>Macros\n"
    + "menu when Fiji starts.\n"
    + "\n"
    + "More information is available at:\n"
    + "<http://imagej.nih.gov/ij/developer/macro/macros.html>";
  dummy = call("fiji.FijiTools.openEditor", title, text);
}

macro "Save As JPEG... [j]" {
  quality = call("ij.plugin.JpegWriter.getQuality");
  quality = getNumber("JPEG quality (0-100):", quality);
  run("Input/Output...", "jpeg="+quality);
  saveAs("Jpeg");
}

macro "Save Inverted FITS" {
  run("Flip Vertically");
  run("FITS...", "");
  run("Flip Vertically");
}

macro "AutoProcessing [Y]" {
print("\\Clear");
run("Close All");
setOption("ExpandableArrays", true);

dir = getDirectory( "Onde estão as fotos?" );
output = getDirectory( "Onde você quer guardá-las?" );

dir = replace(dir, "\\", "/"); // Conserta o nome do diretório para windows, colocando '/'
output = replace(output, "\\", "/");

//Crio uma janela para o usuário indicar quais valores serão usados no processamento
//TODO: Modular com base nos filtros possíveis
Dialog.create("Valores para cortar série Z e remover background");

Dialog.addMessage("Quais serão as fatias você quer remover do início e fim da série Z?");
Dialog.addNumber("Início:", 2);
Dialog.addNumber("Final:", 2);
Dialog.addMessage("Rolling window a ser usada:\nMínimo = 0");
Dialog.addNumber("Valor para DAPI:", 50);
Dialog.addToSameRow();
Dialog.addCheckbox("Remover background do DAPI?", true);
Dialog.addNumber("Valor para BRDU:", 50);
Dialog.addToSameRow();
Dialog.addCheckbox("Remover background do BRDU?", true);
Dialog.addNumber("Valor para DCX:", 50);
Dialog.addToSameRow();
Dialog.addCheckbox("Remover background do DCX?", true);

Dialog.show();

var n_iniciali = Dialog.getNumber();
var n_finali = Dialog.getNumber();
var rolling_dapi = Dialog.getNumber();
var remove_dapi = Dialog.getCheckbox();
var rolling_brdu = Dialog.getNumber();
var remove_brdu = Dialog.getCheckbox();
var rolling_dcx = Dialog.getNumber();
var remove_dcx = Dialog.getCheckbox();

list_file_names = getFileList(dir); //Me dá uma lista com o nome dos arquivos no diretório selecionado
var list_file_names = Array.sort(list_file_names);

for (i = 0; i < list_file_names.length; i++) { //Loop para selecionar apenas imagens .zvi
  if(File.isDirectory(dir + File.separator + list_file_names[i])){
    exit("Você precisa selecionar dentro da pasta onde estão os arquivos");
  }
  if(!(endsWith(list_file_names[i], ".zvi"))){
    print("Os arquivos precisam estar em formato .zvi");
  }
}

Array.sort(list_file_names);
qtd = list_file_names.length

//Loop que faz o processamento das imagens
for ( i=0; i < qtd; i++ ) {
  showProgress(i, qtd);
  atual = i + 1;

  print("Estou processando a foto " + list_file_names[i] + " para você");
  current_image = dir+list_file_names[i];
  open(current_image);
  run("Show All");
  list_open_filters = getList("image.titles"); //Faz um array com o nome das janelas abertas

  //Faz a compressão da série Z retirando as primeiras e últimas imagens pedidas pelo usuário
  for (j=0; j<list_open_filters.length; j++) {
    selectWindow(list_open_filters[j]);
    stack_size = nSlices;
    if (stack_size == 1){
      exit("Atualmente o programa não consegue lidar\ncom fotos que não possuem uma série Z\nComo a foto "+current_image);
    }
    n_inicial = stack_size + 1 - (stack_size - n_iniciali);
    n_final = stack_size - n_finali;
    print("Vou começar na fatia "+n_inicial+"\ne terminar na fatia "+n_final+"\ne a foto tem "+stack_size +" fotos");
    
    run("Z Project...",  "start=" + n_inicial + " stop="+n_final + " projection=[Max Intensity]");
    selectWindow(list_open_filters[j]);
    close();
  }

  run("Show All"); //Isso sempre vem antes pra ter certeza que todas as imagens que foram abertas podem ser selecionadas (a.k.a.: não estão minimizadas)
  list_open_filters = getList("image.titles"); //Refaz o array porque a operação de comprimir a série Z muda o nome da imagem

  //Retira o background
  for (k=0; k<list_open_filters.length; k++) {
    if ((indexOf(list_open_filters[k], "C=0") >= 0) && remove_dcx) {
      selectWindow(list_open_filters[k]);
      run("Subtract Background...", "rolling="+rolling_dcx);
      setOption("ScaleConversions", true);
      run("8-bit");
    }else if ((indexOf(list_open_filters[k], "C=0") >= 0) && !remove_dcx){
      selectWindow(list_open_filters[k]);
      setOption("ScaleConversions", true);
      run("8-bit");
      continue;
    }
    else if ((indexOf(list_open_filters[k], "C=1") >= 0) && remove_dapi) {
      selectWindow(list_open_filters[k]);
      run("Subtract Background...", "rolling="+rolling_dapi);
      setOption("ScaleConversions", true);
      run("8-bit");
    }else if ((indexOf(list_open_filters[k], "C=1") >= 0) && !remove_dapi){
      selectWindow(list_open_filters[k]);
      setOption("ScaleConversions", true);
      run("8-bit");
      continue;
    }
    else if ((indexOf(list_open_filters[k], "C=2") >= 0) && remove_brdu) {
      selectWindow(list_open_filters[k]);
      run("Subtract Background...", "rolling="+rolling_brdu);
      setOption("ScaleConversions", true);
      run("8-bit");
    }else if ((indexOf(list_open_filters[k], "C=2") >= 0) && !remove_brdu){
      selectWindow(list_open_filters[k]);
      setOption("ScaleConversions", true);
      run("8-bit");
      continue;
    }
  }

  //Faz o composite com as três imagens sem background
  Array.sort(list_open_filters);
  run("Merge Channels...", "c2=["+ list_open_filters[2] + "] c3=[" + list_open_filters[0] + "] c6=[" + list_open_filters[1] + "] create keep");

  //Seleciona todas as imagaens e salva o composite como um .PNG para análise
  run("Show All");
  list_open_filters = getList("image.titles");

  nome_atual = File.nameWithoutExtension;

  selectImage("Composite");
  saveAs("PNG", output + nome_atual + ".png");

  run("Show All");
  list = getList("image.titles");
  Array.sort(list);

  for (p=0; p<list.length; p++) {
    if (p==0){
      continue;
    }else{
      close(list[p]);
    }
  }
  run("Close All");
}

waitForUser("I've finished");

}

macro "AutoProcessing - Single Image [U]" {
  print("\\Clear");
  output = getDirectory( "Onde você quer guardá-las?" );

  // Conserta o nome do diretório para windows, colocando '/'
  output = replace(output, "\\", "/");

  //Crio uma janela para o usuário indicar quais valores serão usados no processamento
  //TODO: Modular com base nos filtros possíveis
  Dialog.create("Valores para cortar série Z e remover background");

  Dialog.addMessage("Quais serão as fatias que serão usadas na série Z final?");
  Dialog.addNumber("Primeira fatia:", 1);
  Dialog.addNumber("última fatia:", 12);
  Dialog.addMessage("Rolling window a ser usada:");
  Dialog.addNumber("Valor para DAPI:", 30);
  Dialog.addNumber("Valor para BRDU:", 50);
  Dialog.addNumber("Valor para DCX:", 30);

  Dialog.show();

  n_inicial = Dialog.getNumber();
  n_final = Dialog.getNumber();
  rolling_dapi = Dialog.getNumber();
  rolling_brdu = Dialog.getNumber();
  rolling_dcx = Dialog.getNumber();

  var list_file_names = getList("image.titles"); //Me dá uma lista com o nome dos arquivos no diretório selecionado
    list_file_names = Array.sort(list_file_names);

  print("Vou processar " + list_file_names.length + " fotos/filtros")
  qtd = list_file_names.length;

  //Faz o processamento das imagens
  current_dir = File.directory;
  current_dir = replace(current_dir, "\\", "/"); //Arrumar nome do diretório com /

  print("Estou processando a sua foto");
  run("Show All");
  list_open_filters = getList("image.titles"); //Faz um array com o nome das janelas abertas

  //Faz a compressão da série Z retirando as primeiras e últimas imagens pedidas pelo usuário
  for (j=0; j<list_open_filters.length; j++) {
    selectWindow(list_open_filters[j]);
    run("Z Project...",  "start=" + n_inicial + " stop="+n_final + " projection=[Max Intensity]");
    selectWindow(list_open_filters[j]);
    close();
  }

  run("Show All"); //Isso sempre vem antes pra ter certeza que todas as imagens que foram abertas podem ser selecionadas (a.k.a.: não estão minimizadas)
  list_open_filters = getList("image.titles"); //Refaz o array porque a operação de comprimir a série Z muda o nome da imagem

  //Retira o background
  //Aqui apenas o filtro do BRDU não é com um rolling window de 30px

  for (k=0; k<list_open_filters.length; k++) {
    if (indexOf(list_open_filters[k], "C=0") >= 0) {
      selectWindow(list_open_filters[k]);
      run("Subtract Background...", "rolling="+rolling_dcx);
      setOption("ScaleConversions", true);
      run("8-bit");
    }else if (indexOf(list_open_filters[k], "C=1") >= 0) {
      selectWindow(list_open_filters[k]);
      run("Subtract Background...", "rolling="+rolling_dapi);
      setOption("ScaleConversions", true);
      run("8-bit");
    }else if (indexOf(list_open_filters[k], "C=2") >= 0) {
      selectWindow(list_open_filters[k]);
      run("Subtract Background...", "rolling="+rolling_brdu);
      setOption("ScaleConversions", true);
      run("8-bit");
    }
  }

  //Faz o composite com as três imagens sem background
  Array.sort(list_open_filters);
  run("Merge Channels...", "c2=["+ list_open_filters[2] + "] c3=[" + list_open_filters[0] + "] c6=[" + list_open_filters[1] + "] create keep");

  //Seleciona todas as imagaens e salva o composite como um .PNG para análise
  run("Show All");
  list_open_filters = getList("image.titles");

  nome_atual = File.nameWithoutExtension;

  selectImage("Composite");
  saveAs("PNG", output + nome_atual + ".png");

  run("Show All");
  list = getList("image.titles");
  Array.sort(list);

  for (p=0; p<list.length; p++) {
    if (p==0){
      continue;
    }else{
      close(list[p]);
    }
  }
  run("Close All");

  waitForUser("All images/filters processed");
}