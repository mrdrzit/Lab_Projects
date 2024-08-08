dir = getDir("Escolha o diretório das imagens a serem demarcadas")
dir_to_save = getDirectory("Where do you want to save your files?");
file_list = getFileList(dir)
for (i = 0; i < file_list.length; i++)	{
	open(dir + "/" + file_list[i]);
	waitForUser("Selecione a área do polígono a ser demarcada");
	setTool ("polygon");
	image_name = File.nameWithoutExtension;
	saveAs("XY Coordinates", dir_to_save + image_name + ".txt");
	close();
}
