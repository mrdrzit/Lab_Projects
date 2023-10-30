
function get_sum(start, end, histogram_count){
  sum = 0;
  for (i=start; i<end; i++){
    sum = sum + histogram_count[i];
  }
  return sum;
}

bins = 256;
getHistogram(values, counts, bins);

sum = 0;

for(i=0; i<counts.length; i++){
  sum = sum + counts[i];
}

for (j=counts.length; j>0; j--){
  if (get_sum(0, j, counts) <= 0.07 * sum){
    max_hist_cutoff = j;
    break;
  }
}
desired_threshold = 0.07 * sum;

dist_list = newArray;
J = 0;
L = 20;
for (k=-4; k<4; k++){
  current_histogram_sum_neighbors = get_sum(0, j+k, counts);
  current_percentage = (100 * current_histogram_sum_neighbors)/sum;

  dist = abs(7 - current_percentage);
  
  if (dist < L){
    L = dist;
    max_hist_cutoff = j + k-1;
  }
}

// Listening to pretend you're happy - Jay foreman