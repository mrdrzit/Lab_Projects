// This function is used for calculating the sum of values of the
// histogram_count array.
function get_sum(start, end, histogram_count){
    sum = 0;
    for (i=start; i<end; i++){
      sum = sum + histogram_count[i];
    }
    return sum;
  }
  
  // ------------- This bit of code is to get a threshold value closest to 7% --------------- //
  // To achieve this i first get the whole histogram and calculate sum of every value and do a 
  // simple calculation to find in which value i should set the cutoff at. Then i get the range
  // in which i need to set the threshold that grants the 7%.
  
  // This is the number of bins for pixel intensity
  bins = 256;
  getHistogram(values, counts, bins);
  
  sum = 0;
  
  // Here i just sum all the values to get the 7% value
  for(i=0; i<counts.length; i++){
    sum = sum + counts[i];
  }
  
  // Because imagej needs a range in which we set the threshold, i need to find which bins i need to
  // select that will give me the 7% that i need. So i loop through all combinations of 
  // "binZero - endBin" and check if this range is close to the 7% that i want. That's why i go 
  // backwards from the ending index to the start with a "j--"
  for (j=0; j<counts.length; j++){
    if (get_sum(j, 255, counts) <= 0.07 * sum){
      max_hist_cutoff = j;
      break;
    }
  }
  
  // this code calculates the maximum histogram cutoff value (max_hist_cutoff) which is the
  // point where the histogram is cut-off (i.e. where the histogram is no longer in the 
  // top 7% of the histogram) and the point where the histogram is no longer in the bottom
  // 7% of the histogram. The code does this by calculating the sum of the histogram values
  // to the left of the current histogram value and to the right of the current histogram
  // value. Then, it calculates the percentage of the sum of the histogram values to the
  // left of the current histogram value and to the right of the current histogram value
  // relative to the sum of all histogram values. The point where the percentage is closest
  // to 7% is the maximum histogram cutoff value.
  
  desired_threshold = 0.0153 * sum;
  
  dist_list = newArray;
  J = 0;
  L = 20;
  for (k=-4; k<4; k++){
    current_histogram_sum_neighbors = get_sum(0, j+k, counts);
    current_percentage = (100 * current_histogram_sum_neighbors)/sum;
  
    dist = abs(98.47 - current_percentage);
    
    if (dist < L){
      L = dist;
      max_hist_cutoff = j + k-1;
    }
  }
  
  // ------------- This bit of code is to get a threshold value closest to 7% --------------- //
  
  // Now that we have the index to input at the threshold, use it to process the image 
  run("Threshold...");
  setThreshold(0, max_hist_cutoff, "red dark no-reset");
  
  waitForUser("Check if the threshold was set\nIf so, click OK to continue to outlier removal.");