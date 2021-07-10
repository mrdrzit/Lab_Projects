run("Show All");
list = getList("image.titles"); 

//Faz a compressão da série Z retirando as 2 primeiras e duas últimas imagens
for (i=0; i<list.length; i++) {
	selectWindow(list[i]);
	run("Z Project...", "start=3 stop=10 projection=[Max Intensity]");
	selectWindow(list[i]);
	close();
}

run("Show All");
list = getList("image.titles");

//Retira o background
//Aqui apenas o filtro do BRDU não é com um roling window de 30px

for (i=0; i<list.length; i++) {
	if (indexOf(list[i], "C=0") >= 0) {
		selectWindow(list[i]);
		run("Subtract Background...", "rolling=30");
		setOption("ScaleConversions", true);
		run("8-bit");
	}else if (indexOf(list[i], "C=1") >= 0) {
		selectWindow(list[i]);
		run("Subtract Background...", "rolling=30");
		setOption("ScaleConversions", true);
		run("8-bit");
	}else if (indexOf(list[i], "C=2") >= 0) {
		selectWindow(list[i]);
		run("Subtract Background...", "rolling=50");
		setOption("ScaleConversions", true);
		run("8-bit");
	}
}

//Faz o composite com as três imagens sem background
Array.sort(list)
run("Merge Channels...", "c2=["+ list[2] + "] c3=[" + list[0] + "] c6=[" + list[1] + "] create keep");

//Seleciona todas as imagaens e salva o composite como um .TIF para análise
run("Show All");
list = getList("image.titles");

nome_atual = File.nameWithoutExtension;
working_dir = File.directory;

selectImage("Composite");
saveAs("Tiff", working_dir + nome_atual + ".tif");

nome_da_foto_composite = nome_atual + ".tif";

run("Show All");
list = getList("image.titles");
Array.sort(list)

for (i=0; i<list.length; i++) {
	if (i == 0) {
		continue;
	}else {
		close(list[i]);
	}
}
