print("\\Clear");
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

Dialog.show();

n_iniciali = Dialog.getNumber();
n_finali = Dialog.getNumber();

var foto_atual = 1;
var list_file_names = getFileList(dir); //Me dá uma lista com o nome dos arquivos no diretório selecionado
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
  exit("Atualmente o programa não consegue lidar\ncom fotos que não possuem uma série Z\nComo a foto "+current_image)
  }

  showProgress(i, qtd);
  print("Estou processando a foto "+list_file_names[i]);

  run("Show All");
  list_open_filters = getList("image.titles"); //Faz um array com o nome das janelas abertas

  //Faz a compressão da série Z retirando as primeiras e últimas imagens pedidas pelo usuário
  for (j=0; j<list_open_filters.length; j++) {
    selectWindow(list_open_filters[j]);
    n_inicial = stack_size + 1 - (stack_size - n_iniciali);
    n_final = (stack_size + 1) - n_finali;
    run("Z Project...",  "start=" + n_inicial + " stop="+n_final + " projection=[Max Intensity]");
    selectWindow(list_open_filters[j]);
    close();
  }

  run("Show All"); //Isso sempre vem antes pra ter certeza que todas as imagens que foram abertas podem ser selecionadas (a.k.a.: não estão minimizadas)
  list_open_filters = getList("image.titles"); //Refaz o array porque a operação de comprimir a série Z muda o nome da imagem

  //Seleciona todas as imagaens e salva o composite como um .PNG para análise
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
