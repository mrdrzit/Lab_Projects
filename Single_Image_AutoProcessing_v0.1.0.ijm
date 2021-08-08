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