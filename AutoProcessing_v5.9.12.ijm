print("\\Clear");
dir = getDirectory( "Choose the Directory" );
output = getDirectory( "Choose destination" );

//contents = getFileList( dir );
//list = split(contents, "\n");

	list = getFileList(dir);
	list = Array.sort(list);
	for (i = 0; i < list.length; i++) {
		if(File.isDirectory(dir + File.separator + list[i]))
			processFolder(dir + File.separator + list[i]);
		if(endsWith(list[i], ".zvi"))
		current_dir = dir;
			print(dir + list[i]);
	}

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