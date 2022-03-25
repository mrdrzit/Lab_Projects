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
Dialog.addNumber("Valor para BDNF:", 50);
Dialog.addToSameRow();
Dialog.addCheckbox("Remover background do BDNF?", true);

Dialog.show();

var n_iniciali = Dialog.getNumber();
var n_finali = Dialog.getNumber();
var rolling_dapi = Dialog.getNumber();
var remove_dapi = Dialog.getCheckbox();
var rolling_bdnf = Dialog.getNumber();
var remove_bdnf = Dialog.getCheckbox();

var foto_atual = 1;
var list_file_names = getFileList(dir); //Me dá uma lista com o nome dos arquivos no diretório selecionado
list_file_names = Array.sort(list_file_names); //Mas não discrimina entre 10x e 40x

debug_file_list = newArray //Array com o path apenas das fotos de 40x
z = 0;
for (i = 0; i < list_file_names.length; i++) { //Loop para selecionar apenas imagens .zvi
  if(File.isDirectory(dir + File.separator + list_file_names[i])){
  exit("Você precisa selecionar dentro da pasta onde estão os arquivos");
  }
  if((endsWith(list_file_names[i], ".zvi")) && (indexOf(list_file_names[i], "40x") > 0)){
    path = dir + list_file_names[i];
    debug_file_list[z] = path;
  }else{
    continue;
  }
  z++;
}
Array.deleteValue(debug_file_list, "undefined") //Remove valores undefined

Array.sort(debug_file_list);
qtd = debug_file_list.length;

//Loop que faz o processamento das imagens
for ( i=0; i < qtd; i+=2) {
  showProgress(i, qtd);
  print("Estou processando a foto "+debug_file_list[i]);

  for (p=i; p<(i+2); p++){
    current_image = debug_file_list[p];
    open(current_image);
    tmp = getInfo("image.title");
    selectWindow(tmp);
    if(p == i){
      stack_size = nSlices;
      n_inicial = stack_size + 1 - (stack_size - n_iniciali);
      n_final = stack_size - n_finali;
      print("Vou começar na fatia "+n_inicial+"\ne terminar na fatia "+n_final+"\ne a foto tem "+stack_size +" fotos");
    }else if (stack_size == 1){
      exit("Atualmente o programa não consegue lidar\ncom fotos que não possuem uma série Z\nComo a foto "+current_image);
    }
  }


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
  for (k=0; k<list_open_filters.length; k++) {
    if ((indexOf(list_open_filters[k], "DAPI") >= 0) && remove_dapi) {
      selectWindow(list_open_filters[k]);
      run("Subtract Background...", "rolling="+rolling_dapi);
      setOption("ScaleConversions", true);
      run("8-bit");
    }else if ((indexOf(list_open_filters[k], "DAPI") >= 0) && !remove_dapi){
      selectWindow(list_open_filters[k]);
      setOption("ScaleConversions", true);
      run("8-bit");
      continue;
    }
    else if ((indexOf(list_open_filters[k], "BDNF") >= 0) && remove_bdnf) {
      selectWindow(list_open_filters[k]);
      run("Subtract Background...", "rolling="+rolling_bdnf);
      setOption("ScaleConversions", true);
      run("8-bit");
    }else if ((indexOf(list_open_filters[k], "BDNF") >= 0) && !remove_bdnf){
      selectWindow(list_open_filters[k]);
      setOption("ScaleConversions", true);
      run("8-bit");
      continue;
    }
  }

  //Faz o composite com as três imagens sem background
  Array.sort(list_open_filters);
  // Eplanation for the brackets:
  // If your file names (i.e. the ‘values’ of the parameters c1, c2, etc.) contain spaces,
  // you have to enclose them in square brackets []
  run("Merge Channels...", "c2=["+ list_open_filters[0] + "] c3=[" + list_open_filters[1] + "] create keep");

  //Seleciona todas as imagens e salva o composite como um .PNG para análise
  run("Show All");
  list_open_filters = getList("image.titles");

  nome_atual = File.nameWithoutExtension;

  selectImage("Composite");
  saveAs("PNG", output + nome_atual + "_composite" + ".png");
  foto_atual++;

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

waitForUser("All images/filters processed");
