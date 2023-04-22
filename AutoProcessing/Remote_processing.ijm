// Download the macro file from GitHub
url = "https://raw.githubusercontent.com/mrdrzit/Lab_Projects_as_IC/main/AutoProcessing/Whatever file that you want.ijm";
file = File.openUrlAsString(url);

// Save the macro to a local file
temp_dir = getDir("temp")
File.saveString(file, temp_dir + "macro.ijm");

// Run the macro
runMacro(temp_dir + "macro.ijm");