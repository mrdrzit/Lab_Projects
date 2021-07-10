run("Show All");
list = getList("image.titles");

nome_atual = File.nameWithoutExtension;
working_dir = File.directory;

selectImage("Composite");
saveAs("Tiff", working_dir + nome_atual + ".tif");

run("Show All");
list = getList("image.titles");

for (i=0; i<list.length; i++) {
	close();
}
