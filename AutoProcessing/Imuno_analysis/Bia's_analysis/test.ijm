// Download the macro file from GitHub
url = "https://raw.githubusercontent.com/mrdrzit/Lab_Projects_as_IC/main/AutoProcessing/Imuno_analysis/Bia's_analysis/000_autoprocessing_bia.ijm";
file = File.openUrlAsString(url);

// Save the macro to a local file
temp_dir = getDir("temp")
File.saveString(file, temp_dir + "macro.ijm");

// Run the macro
runMacro(temp_dir + "macro.ijm");