print("\\Clear");
dir = getDirectory( "Onde est�o as fotos?" );
output = getDirectory( "Onde voc� quer guard�-las?" );

dir = replace(dir, "\\", "/"); // Conserta o nome do diret�rio para windows, colocando '/'
output = replace(output, "\\", "/");

//Crio uma janela para o usu�rio indicar quais valores ser�o usados no processamento
//TODO: Modular com base nos filtros poss�veis
Dialog.create("Valores para cortar s�rie Z e remover background");

Dialog.addMessage("Quais ser�o as fatias voc� quer remover do in�cio e fim da s�rie Z?");
Dialog.addNumber("In�cio:", 2);
Dialog.addNumber("Final:", 2);

Dialog.show();

n_iniciali = Dialog.getNumber();
n_finali = Dialog.getNumber();

var foto_atual = 1;
var list_file_names = getFileList(dir); //Me d� uma lista com o nome dos arquivos no diret�rio selecionado
  list_file_names = Array.sort(list_file_names);

Array.sort(list_file_names);
qtd = list_file_names.length;

//Loop que faz o processamento das imagens
for ( i=0; i < qtd; i++) {
  if (indexOf(list_file_names[i], "DAPI") >= 0){
    continue;
  }else if (indexOf(list_file_names[i], "10x") >= 0){
    continue;
  }

  current_image = dir+list_file_names[i];
  open(current_image);
  imageid = getImageID();
  selectImage(imageid);
  if (nSlices() > 1) {
    stack_size = nSlices();
  }else {
  exit("Atualmente o programa n�o consegue lidar\ncom fotos que n�o possuem uma s�rie Z\nComo a foto "+current_image)
  }

  showProgress(i, qtd);
  print("Estou processando a foto "+list_file_names[i]);

  run("Show All");
  list_open_filters = getList("image.titles"); //Faz um array com o nome das janelas abertas

  //Faz a compress�o da s�rie Z retirando as primeiras e �ltimas imagens pedidas pelo usu�rio
  for (j=0; j<list_open_filters.length; j++) {
    selectWindow(list_open_filters[j]);
    n_inicial = stack_size + 1 - (stack_size - n_iniciali);
    n_final = (stack_size + 1) - n_finali;
    run("Z Project...",  "start=" + n_inicial + " stop="+n_final + " projection=[Max Intensity]");
    selectWindow(list_open_filters[j]);
    close();
  }

  run("Show All"); //Isso sempre vem antes pra ter certeza que todas as imagens que foram abertas podem ser selecionadas (a.k.a.: n�o est�o minimizadas)
  list_open_filters = getList("image.titles"); //Refaz o array porque a opera��o de comprimir a s�rie Z muda o nome da imagem

  //Seleciona todas as imagaens e salva o composite como um .PNG para an�lise
  run("Show All");
  list_open_filters = getList("image.titles");

  nome_atual = File.nameWithoutExtension;

  imageid = getImageID();
  selectImage(imageid);
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
