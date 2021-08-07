print("\\Clear");
dir = getDirectory( "Onde estão as fotos?" );
output = getDirectory( "Onde você quer guardá-las?" );

dir = replace(dir, "\\", "/"); // Conserta o nome do diretório para windows, colocando '/'
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

//contents = getFileList( dir );
//list = split(contents, "\n");

	var list_file_names = getFileList(dir); //Me dá uma lista com o nome dos arquivos no diretório selecionado
	list_file_names = Array.sort(list_file_names);
	for (i = 0; i < list_file_names.length; i++) { //Loop para selecionar apenas imagens .zvi
		if(File.isDirectory(dir + File.separator + list_file_names[i]))
			exit("Você precisa selecionar dentro da pasta onde estão os arquivos");
		if(endsWith(list_file_names[i], ".zvi"))
			print(dir + list_file_names[i]);
	}

Array.sort(list_file_names);
print("list length is " + list_file_names.length)
qtd = list_file_names.length

//Loop que faz o processamento das imagens
Array.sort(list);
print("list length is " + list.length)
qtd = list.length
for ( i=0; i < qtd; i++ ) {
	showProgress(i, qtd);
	atual = i + 1;
	
	
	print("Estou processando a foto " + (i+1) + " para você");
    open("D:/Analise/tests/animal1cx35F11BO40x" + atual + ".zvi");

    run("Show All");
	list = getList("image.titles"); 
	
	//Faz a compressão da série Z retirando as 2 primeiras e duas últimas imagens
	for (j=0; j<list.length; j++) {
		selectWindow(list[j]);
		run("Z Project...", "start=2 stop=8 projection=[Max Intensity]");
		selectWindow(list[j]);
		close();
	}
	
	run("Show All");
	list = getList("image.titles");
	
	//Retira o background
	//Aqui apenas o filtro do BRDU não é com um rolling window de 30px
	
	for (k=0; k<list.length; k++) {
		if (indexOf(list[k], "C=0") >= 0) {
			selectWindow(list[k]);
			run("Subtract Background...", "rolling=30");
			setOption("ScaleConversions", true);
			run("8-bit");
		}else if (indexOf(list[k], "C=1") >= 0) {
			selectWindow(list[k]);
			run("Subtract Background...", "rolling=30");
			setOption("ScaleConversions", true);
			run("8-bit");
		}else if (indexOf(list[k], "C=2") >= 0) {
			selectWindow(list[k]);
			run("Subtract Background...", "rolling=50");
			setOption("ScaleConversions", true);
			run("8-bit");
		}
	}
	
	//Faz o composite com as três imagens sem background
	Array.sort(list);
	run("Merge Channels...", "c2=["+ list[2] + "] c3=[" + list[0] + "] c6=[" + list[1] + "] create keep");
	
	//Seleciona todas as imagaens e salva o composite como um .TIF para análise
	run("Show All");
	list = getList("image.titles");
	
	nome_atual = File.nameWithoutExtension;
//	working_dir = File.directory;
	
	selectImage("Composite");
	saveAs("Tiff", output + nome_atual + ".tif");
	
	nome_da_foto_composite = nome_atual + ".tif";
	
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
