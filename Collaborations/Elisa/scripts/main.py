import pickle
import os
import numpy as np
import matplotlib.pyplot as plt
import math
import seaborn as sns
import scipy.stats as stats
from helper_functions import *
from matplotlib.ticker import MultipleLocator
from scipy.interpolate import make_interp_spline

save_figures = False
show_figures = False

# Set the path to the data folder and the pre-processed data file
data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
figures_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'figures'))
pre_processed_data = os.path.join(data_folder, 'animals_data_elisa.pkl')

# Load the animals data from the pickle file
with open(pre_processed_data, 'rb') as file:
    animals_data = pickle.load(file)
print("Data loaded successfully!")

# Get the maximum exploration bout duration overall
max_duration = 0
for session in animals_data.keys():
    for animal in animals_data[session].keys():
        max_duration = max(max_duration, max(animals_data[session][animal]) if len(animals_data[session][animal]) > max_duration else max_duration)

# Set the bin size for the histograms
bins = np.arange(0, math.ceil(max_duration), 0.5)

paired_data = []
paired_cdf = []
paired_bins = []

treino, reativacao, teste = list(animals_data.keys())

for animal_tr, animal_re, animal_tt in zip(animals_data[treino], animals_data[reativacao], animals_data[teste]):
    paired_data.append([animals_data[treino][animal_tr], animals_data[reativacao][animal_re], animals_data[teste][animal_tt]])
    paired_cdf.append([cumulative_distribution(animals_data[treino][animal_tr]), cumulative_distribution(animals_data[reativacao][animal_re]), cumulative_distribution(animals_data[teste][animal_tt])])
    paired_bins.append([np.histogram(animals_data[treino][animal_tr], bins=bins)[0], np.histogram(animals_data[reativacao][animal_re], bins=bins)[0], np.histogram(animals_data[teste][animal_tt], bins=bins)[0]])

# Set the colors for each experiment day
TR_color = '#b57ecb'
RE_color = '#5b9999'
TT_color = '#E45C5C'

TR_durations = []
RE_durations = []
TT_durations = []

for array in animals_data["treino"].values():
    TR_durations.extend(array)

for array in animals_data["reativacao"].values():
    RE_durations.extend(array)

for array in animals_data["teste"].values():
    TT_durations.extend(array)

# # Cumulative distribution using seaborn
# sns.kdeplot(TR_durations, color=TR_color, cumulative=True, alpha=0.8, linewidth=2, bw_adjust=1.6, clip=(0, 20))
# sns.kdeplot(RE_durations, color=RE_color, cumulative=True, alpha=0.8, linewidth=2, bw_adjust=1.6, clip=(0, 20))
# sns.kdeplot(TT_durations, color=TT_color, cumulative=True, alpha=0.8, linewidth=2, bw_adjust=1.6, clip=(0, 20))

# Calculate the cumulative distribution function for each session
values_TR, cdf_TR = cumulative_distribution(TR_durations)
values_RE, cdf_RE = cumulative_distribution(RE_durations)
values_TT, cdf_TT = cumulative_distribution(TT_durations)

# Find the maximum length
max_len = max(len(TR_durations), len(RE_durations), len(TT_durations))

# Pad the arrays with zeros
TR_durations_homogenous = np.pad(TR_durations, (0, max_len - len(TR_durations)), 'constant')
RE_durations_homogenous = np.pad(RE_durations, (0, max_len - len(RE_durations)), 'constant')
TT_durations_homogenous = np.pad(TT_durations, (0, max_len - len(TT_durations)), 'constant')

data = np.array((TR_durations_homogenous, RE_durations_homogenous, TT_durations_homogenous))
data_dataframe = pd.DataFrame(data.T, columns=["TR", "RE", "TT"])
data_dataframe["TR"] = data_dataframe["TR"]
data_dataframe["RE"] = data_dataframe["RE"]
data_dataframe["TT"] = data_dataframe["TT"]

# Run the kolmogorov-smirnov tests for each session ---------------------------------------------------------------------
training_session_values_all = np.array(TR_durations)
reactivation_session_values_all = np.array(RE_durations)
testing_session_values_all = np.array(TT_durations)

# Kolmogorov-Smirnov test for TR and RE
ks_stat_tr_vs_re, ks_p_value_tr_vs_re = stats.ks_2samp(training_session_values_all, reactivation_session_values_all)
ks_stat_tr_vs_tt, ks_p_value_tr_vs_tt = stats.ks_2samp(training_session_values_all, testing_session_values_all)
ks_stat_re_vs_tt, ks_p_value_re_vs_tt = stats.ks_2samp(testing_session_values_all, reactivation_session_values_all)

pairwise_dataframe_tr_vs_re = pd.DataFrame(columns=["Animal", "Comparison", "KS Statistic", "P-Value", "Reject Null Hypothesis"])
pairwise_dataframe_tr_vs_tt = pd.DataFrame(columns=["Animal", "Comparison", "KS Statistic", "P-Value", "Reject Null Hypothesis"])
pairwise_dataframe_re_vs_tt = pd.DataFrame(columns=["Animal", "Comparison", "KS Statistic", "P-Value", "Reject Null Hypothesis"])

for i, animal in enumerate(paired_data):
    animal_name = list(animals_data['treino'].keys())[i].replace('TR', '')
    training_session_values = np.array(animal[0])
    reactivation_session_values = np.array(animal[1])
    testing_session_values = np.array(animal[2])

    paired_ks_stat_tr_vs_re, paired_ks_p_value_tr_vs_re = stats.ks_2samp(training_session_values, reactivation_session_values)
    paired_ks_stat_tr_vs_tt, paired_ks_p_value_tr_vs_tt = stats.ks_2samp(training_session_values, testing_session_values)
    paired_ks_stat_re_vs_tt, paired_ks_p_value_re_vs_tt = stats.ks_2samp(testing_session_values, reactivation_session_values)

    formatted_p_value_tr_vs_re = f"{paired_ks_p_value_tr_vs_re:.6f}" if paired_ks_p_value_tr_vs_re >= 0.000001 else f"{paired_ks_p_value_tr_vs_re:.1e}"
    formatted_p_value_tr_vs_tt = f"{paired_ks_p_value_tr_vs_tt:.6f}" if paired_ks_p_value_tr_vs_tt >= 0.000001 else f"{paired_ks_p_value_tr_vs_tt:.1e}"
    formatted_p_value_re_vs_tt = f"{paired_ks_p_value_re_vs_tt:.6f}" if paired_ks_p_value_re_vs_tt >= 0.000001 else f"{paired_ks_p_value_re_vs_tt:.1e}"

    pairwise_dataframe_tr_vs_re = pd.concat([pairwise_dataframe_tr_vs_re, pd.DataFrame({
        "Animal": [animal_name],
        "Comparison": ["TR vs RE"],
        "KS Statistic": [paired_ks_stat_tr_vs_re],
        "P-Value": [formatted_p_value_tr_vs_re],
        "Reject Null Hypothesis": [paired_ks_p_value_tr_vs_re < 0.05]
    })], ignore_index=True)

    pairwise_dataframe_tr_vs_tt = pd.concat([pairwise_dataframe_tr_vs_tt, pd.DataFrame({
        "Animal": [animal_name],
        "Comparison": ["TR vs TT"],
        "KS Statistic": [paired_ks_stat_tr_vs_tt],
        "P-Value": [formatted_p_value_tr_vs_tt],
        "Reject Null Hypothesis": [paired_ks_p_value_tr_vs_tt < 0.05]
    })], ignore_index=True)

    pairwise_dataframe_re_vs_tt = pd.concat([pairwise_dataframe_re_vs_tt, pd.DataFrame({
        "Animal": [animal_name],
        "Comparison": ["RE vs TT"],
        "KS Statistic": [paired_ks_stat_re_vs_tt],
        "P-Value": [formatted_p_value_re_vs_tt],
        "Reject Null Hypothesis": [paired_ks_p_value_re_vs_tt < 0.05]
    })], ignore_index=True)

tr_vs_re_row = pd.DataFrame({
    "Comparison": ["TR vs RE"],
    "KS Statistic": [ks_stat_tr_vs_re],
    "P-Value": [ks_p_value_tr_vs_re],
    "Reject Null Hypothesis": [ks_p_value_tr_vs_re < 0.05]
})

tr_vs_tt_row = pd.DataFrame({
    "Comparison": ["TR vs TT"],
    "KS Statistic": [ks_stat_tr_vs_tt],
    "P-Value": [ks_p_value_tr_vs_tt],
    "Reject Null Hypothesis": [ks_p_value_tr_vs_tt < 0.05]
})

re_vs_tt_row = pd.DataFrame({
    "Comparison": ["RE vs TT"],
    "KS Statistic": [ks_stat_re_vs_tt],
    "P-Value": [ks_p_value_re_vs_tt],
    "Reject Null Hypothesis": [ks_p_value_re_vs_tt < 0.05]
})

statistics_dataframe = pd.DataFrame(columns=["Comparison", "KS Statistic", "P-Value", "Reject Null Hypothesis"])
statistics_dataframe = pd.concat([statistics_dataframe, tr_vs_re_row], ignore_index=True)
statistics_dataframe = pd.concat([statistics_dataframe, tr_vs_tt_row], ignore_index=True)
statistics_dataframe = pd.concat([statistics_dataframe, re_vs_tt_row], ignore_index=True)

# Save both dataframes to xlsx files
statistics_dataframe.to_excel(os.path.join(figures_folder, 'KS_Statistics_All_Animals.xlsx'), index=False)
pairwise_dataframe_tr_vs_re.to_excel(os.path.join(figures_folder, 'KS_Statistics_TR_vs_RE.xlsx'), index=False)
pairwise_dataframe_tr_vs_tt.to_excel(os.path.join(figures_folder, 'KS_Statistics_TR_vs_TT.xlsx'), index=False)
pairwise_dataframe_re_vs_tt.to_excel(os.path.join(figures_folder, 'KS_Statistics_RE_vs_TT.xlsx'), index=False)
print("KS statistics saved successfully!")

# Run a kruskal wallis test for each session ------------------------------------------------------------------------------
training_session_values_all = np.array(TR_durations)
reactivation_session_values_all = np.array(RE_durations)
testing_session_values_all = np.array(TT_durations)

# Kolmogorov-Smirnov test for TR and RE
ks_stat_tr_vs_re, ks_p_value_tr_vs_re = stats.kruskal(training_session_values_all, reactivation_session_values_all)
ks_stat_tr_vs_tt, ks_p_value_tr_vs_tt = stats.kruskal(training_session_values_all, testing_session_values_all)
ks_stat_re_vs_tt, ks_p_value_re_vs_tt = stats.kruskal(testing_session_values_all, reactivation_session_values_all)

pairwise_kruskal_tr_vs_re_dataframe = pd.DataFrame(columns=["Animal", "Comparison", "H-Statistic", "P-Value", "Reject Null Hypothesis"])
pairwise_kruskal_tr_vs_tt_dataframe = pd.DataFrame(columns=["Animal", "Comparison", "H-Statistic", "P-Value", "Reject Null Hypothesis"])
pairwise_kruskal_re_vs_tt_dataframe = pd.DataFrame(columns=["Animal", "Comparison", "H-Statistic", "P-Value", "Reject Null Hypothesis"])

kruskal_dataframe = pd.DataFrame(columns=["Comparison", "H-Statistic", "P-Value", "Reject Null Hypothesis"])

for i, animal in enumerate(paired_data):
    animal_name = list(animals_data['treino'].keys())[i].replace('TR', '')
    training_session_values = np.array(animal[0])
    reactivation_session_values = np.array(animal[1])
    testing_session_values = np.array(animal[2])

    paired_ks_stat_tr_vs_re, paired_ks_p_value_tr_vs_re = stats.kruskal(training_session_values, reactivation_session_values)
    paired_ks_stat_tr_vs_tt, paired_ks_p_value_tr_vs_tt = stats.kruskal(training_session_values, testing_session_values)
    paired_ks_stat_re_vs_tt, paired_ks_p_value_re_vs_tt = stats.kruskal(testing_session_values, reactivation_session_values)

    formatted_p_value_tr_vs_re = f"{paired_ks_p_value_tr_vs_re:.6f}" if paired_ks_p_value_tr_vs_re >= 0.000001 else f"{paired_ks_p_value_tr_vs_re:.1e}"
    formatted_p_value_tr_vs_tt = f"{paired_ks_p_value_tr_vs_tt:.6f}" if paired_ks_p_value_tr_vs_tt >= 0.000001 else f"{paired_ks_p_value_tr_vs_tt:.1e}"
    formatted_p_value_re_vs_tt = f"{paired_ks_p_value_re_vs_tt:.6f}" if paired_ks_p_value_re_vs_tt >= 0.000001 else f"{paired_ks_p_value_re_vs_tt:.1e}"

    pairwise_kruskal_tr_vs_re_dataframe = pd.concat([pairwise_kruskal_tr_vs_re_dataframe, pd.DataFrame({
        "Animal": [animal_name],
        "Comparison": ["TR vs RE"],
        "H-Statistic": [paired_ks_stat_tr_vs_re],
        "P-Value": [formatted_p_value_tr_vs_re],
        "Reject Null Hypothesis": [paired_ks_p_value_tr_vs_re < 0.05]
    })], ignore_index=True)

    pairwise_kruskal_tr_vs_tt_dataframe = pd.concat([pairwise_kruskal_tr_vs_tt_dataframe, pd.DataFrame({
        "Animal": [animal_name],
        "Comparison": ["TR vs TT"],
        "H-Statistic": [paired_ks_stat_tr_vs_tt],
        "P-Value": [formatted_p_value_tr_vs_tt],
        "Reject Null Hypothesis": [paired_ks_p_value_tr_vs_tt < 0.05]
    })], ignore_index=True)

    pairwise_kruskal_re_vs_tt_dataframe = pd.concat([pairwise_kruskal_re_vs_tt_dataframe, pd.DataFrame({
        "Animal": [animal_name],
        "Comparison": ["RE vs TT"],
        "H-Statistic": [paired_ks_stat_re_vs_tt],
        "P-Value": [formatted_p_value_re_vs_tt],
        "Reject Null Hypothesis": [paired_ks_p_value_re_vs_tt < 0.05]
    })], ignore_index=True)

kruskal_tr_vs_re_row = pd.DataFrame({
    "Comparison": ["TR vs RE"],
    "H-Statistic": [ks_stat_tr_vs_re],
    "P-Value": [ks_p_value_tr_vs_re],
    "Reject Null Hypothesis": [ks_p_value_tr_vs_re < 0.05]
})

kruskal_tr_vs_tt_row = pd.DataFrame({
    "Comparison": ["TR vs TT"],
    "H-Statistic": [ks_stat_tr_vs_tt],
    "P-Value": [ks_p_value_tr_vs_tt],
    "Reject Null Hypothesis": [ks_p_value_tr_vs_tt < 0.05]
})

kruskal_re_vs_tt_row = pd.DataFrame({
    "Comparison": ["RE vs TT"],
    "H-Statistic": [ks_stat_re_vs_tt],
    "P-Value": [ks_p_value_re_vs_tt],
    "Reject Null Hypothesis": [ks_p_value_re_vs_tt < 0.05]
})

kruskal_dataframe = pd.concat([kruskal_dataframe, kruskal_tr_vs_re_row], ignore_index=True)
kruskal_dataframe = pd.concat([kruskal_dataframe, kruskal_tr_vs_tt_row], ignore_index=True)
kruskal_dataframe = pd.concat([kruskal_dataframe, kruskal_re_vs_tt_row], ignore_index=True)

print(kruskal_dataframe)
print(statistics_dataframe)
print(pairwise_kruskal_tr_vs_tt_dataframe)
print(pairwise_kruskal_tr_vs_re_dataframe)
print(pairwise_kruskal_re_vs_tt_dataframe)
print(pairwise_dataframe_tr_vs_re)
print(pairwise_dataframe_tr_vs_tt)
print(pairwise_dataframe_re_vs_tt)

# Save both dataframes to xlsx files
kruskal_dataframe.to_excel(os.path.join(figures_folder, 'Kruskal_Wallis_Statistics_All_Animals.xlsx'), index=False)
pairwise_kruskal_tr_vs_re_dataframe.to_excel(os.path.join(figures_folder, 'Kruskal_Wallis_Statistics_TR_vs_RE.xlsx'), index=False)
pairwise_kruskal_tr_vs_tt_dataframe.to_excel(os.path.join(figures_folder, 'Kruskal_Wallis_Statistics_TR_vs_TT.xlsx'), index=False)
pairwise_kruskal_re_vs_tt_dataframe.to_excel(os.path.join(figures_folder, 'Kruskal_Wallis_Statistics_RE_vs_TT.xlsx'), index=False)
print("Kruskal Wallis statistics saved successfully!")


# Plot the cdfs for each session ---------------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(15, 8))
plt.plot(values_TR, cdf_TR, label="TR", color=TR_color, drawstyle='steps-post')
plt.plot(values_RE, cdf_RE, label="RE", color=RE_color, drawstyle='steps-post')
plt.plot(values_TT, cdf_TT, label="TT", color=TT_color, drawstyle='steps-post')
plt.legend()
plt.xlabel('Duration (s)', fontsize=12)
plt.ylabel('Cumulative Probability', fontsize=12)
plt.grid()
plt.title('Cumulative distribution function for every animal in each session (TR, RE, TT)')
plt.tight_layout()

if save_figures:
    plt.savefig(os.path.join(figures_folder, 'Cumulative distribution function for every animal in each session (TR, RE, TT).png'))
    plt.close("all")
    print("CDFs plotted successfully!")
elif show_figures:
    plt.show()
    plt.close("all")
plt.close("all")

# Plot the cdfs for each animal through the experiment days -------------------------------------------------------------
for animal in range(len(paired_data)):
    fig, ax = plt.subplots(figsize=(15, 8))
    plot_name = f'Cumulative Distribution Function for Animal {list(animals_data["treino"].keys())[animal].replace("TR", "")} in each session'
    plt.plot(paired_cdf[animal][0][0], paired_cdf[animal][0][1], label="TR", color=TR_color, drawstyle='steps-post')
    plt.plot(paired_cdf[animal][1][0], paired_cdf[animal][1][1], label="RE", color=RE_color, drawstyle='steps-post')
    plt.plot(paired_cdf[animal][2][0], paired_cdf[animal][2][1], label="TT", color=TT_color, drawstyle='steps-post')
    plt.legend()
    plt.xlabel('Duration (s)', fontsize=12)
    plt.ylabel('Cumulative Probability', fontsize=12)
    plt.grid()
    plt.title(plot_name)
    plt.tight_layout()
    if save_figures:
        plt.savefig(os.path.join(figures_folder, plot_name))
        plt.close("all")
plt.close("all")
print("Animal CDFs plotted successfully!")

# Plot the histograms, kdes and superimposed cdfs for each session ------------------------------------------------------
fig, axes = plt.subplots(3, 3, sharex=True, sharey=True, figsize=(15, 8))

# PLot histograms on the first row
axes[0][0].hist(TR_durations, bins=bins, density=True, color=TR_color, alpha=0.7, label='TR')
axes[0][1].hist(RE_durations, bins=bins, density=True, color=RE_color, alpha=0.7, label='RE')
axes[0][2].hist(TT_durations, bins=bins, density=True, color=TT_color, alpha=0.7, label='TT')
axes[0][0].axvline(np.mean(TR_durations), color='k', linestyle='dashed', linewidth=1, label=f'TR Mean ({np.mean(TR_durations):.3f}s)')
axes[0][1].axvline(np.mean(RE_durations), color='k', linestyle='dashed', linewidth=1, label=f'RE Mean ({np.mean(RE_durations):.3f}s)')
axes[0][2].axvline(np.mean(TT_durations), color='k', linestyle='dashed', linewidth=1, label=f'TT Mean ({np.mean(TT_durations):.3f}s)')

# Plot the kdes in the second row
sns.kdeplot(data=data_dataframe['TR'], ax=axes[1][0], color=TR_color, fill=True, alpha=0.8, linewidth=2, multiple='stack', edgecolor='white', bw_adjust=1.6, clip=(0, 20))
sns.kdeplot(data=data_dataframe['RE'], ax=axes[1][1], color=RE_color, fill=True, alpha=0.8, linewidth=2, multiple='stack', edgecolor='white', bw_adjust=1.6, clip=(0, 20))
sns.kdeplot(data=data_dataframe['TT'], ax=axes[1][2], color=TT_color, fill=True, alpha=0.8, linewidth=2, multiple='stack', edgecolor='white', bw_adjust=1.6, clip=(0, 20))

# Plot the kdes overlapping the histograms in the third row
axes[2][0].hist(TR_durations, bins=bins, density=True, color=TR_color, alpha=0.7, label='TR')
axes[2][1].hist(RE_durations, bins=bins, density=True, color=RE_color, alpha=0.7, label='RE')
axes[2][2].hist(TT_durations, bins=bins, density=True, color=TT_color, alpha=0.7, label='TT')
sns.kdeplot(data=data_dataframe['TR'], ax=axes[2][0], color="black", fill=False, alpha=0.8, linewidth=2, linestyle='-', bw_adjust=1.6, clip=(0, 20))
sns.kdeplot(data=data_dataframe['RE'], ax=axes[2][1], color="black", fill=False, alpha=0.8, linewidth=2, linestyle='-', bw_adjust=1.6, clip=(0, 20))
sns.kdeplot(data=data_dataframe['TT'], ax=axes[2][2], color="black", fill=False, alpha=0.8, linewidth=2, linestyle='-', bw_adjust=1.6, clip=(0, 20))

for ax in axes[0].flatten():
    ax.legend()
    ax.set_ylabel('Frequency')
    ax.grid()

for ax in axes[1].flatten():
    ax.set_ylabel('Kernel Density Estimate')
    ax.grid()

for ax in axes[2].flatten():
    ax.set_xlabel('Duration (s)')
    ax.set_ylabel('KDE and Frequency')
    ax.grid()

fig.suptitle('Bout Durations histogram (normalized) and KDE for each session (TR, RE, TT)', fontsize=14)
plt.xlim(0, 20)
plt.tight_layout()
if save_figures:
    plt.savefig(os.path.join(figures_folder, 'Bout Durations histogram (normalized) and KDE for each session (TR, RE, TT).png'))
    plt.close("all")
    print("Histograms, KDEs and superimposed CDFs plotted successfully!")
plt.close("all")

# Plot the histograms, kdes and superimposed cdfs for each animal --------------------------------------------------------
for animal in range(len(paired_data)):
    animal_mean_tr = np.mean(paired_data[animal][0])
    animal_mean_re = np.mean(paired_data[animal][1])
    animal_mean_tt = np.mean(paired_data[animal][2])

    fig, axes = plt.subplots(3, 3, sharex=True, sharey=True, figsize=(15, 8))

    # PLot histograms on the first row
    axes[0][0].hist(paired_data[animal][0], bins=bins, density=True, color=TR_color, alpha=0.7, label='TR')
    axes[0][1].hist(paired_data[animal][1], bins=bins, density=True, color=RE_color, alpha=0.7, label='RE')
    axes[0][2].hist(paired_data[animal][2], bins=bins, density=True, color=TT_color, alpha=0.7, label='TT')
    axes[0][0].axvline(animal_mean_tr, color='k', linestyle='dashed', linewidth=1, label=f'TR Mean ({animal_mean_tr:.3f}s)')
    axes[0][1].axvline(animal_mean_re, color='k', linestyle='dashed', linewidth=1, label=f'RE Mean ({animal_mean_re:.3f}s)')
    axes[0][2].axvline(animal_mean_tt, color='k', linestyle='dashed', linewidth=1, label=f'TT Mean ({animal_mean_tt:.3f}s)')

    # Plot the kdes in the second row
    sns.kdeplot(data=paired_data[animal][0], ax=axes[1][0], color=TR_color, fill=True, alpha=0.8, linewidth=2, multiple='stack', edgecolor='white', bw_adjust=.6, clip=(0, 20))
    sns.kdeplot(data=paired_data[animal][1], ax=axes[1][1], color=RE_color, fill=True, alpha=0.8, linewidth=2, multiple='stack', edgecolor='white', bw_adjust=.6, clip=(0, 20))
    sns.kdeplot(data=paired_data[animal][2], ax=axes[1][2], color=TT_color, fill=True, alpha=0.8, linewidth=2, multiple='stack', edgecolor='white', bw_adjust=.6, clip=(0, 20))

    # Plot the kdes overlapping the histograms in the third row
    axes[2][0].hist(paired_data[animal][0], bins=bins, density=True, color=TR_color, alpha=0.7, label='TR')
    axes[2][1].hist(paired_data[animal][1], bins=bins, density=True, color=RE_color, alpha=0.7, label='RE')
    axes[2][2].hist(paired_data[animal][2], bins=bins, density=True, color=TT_color, alpha=0.7, label='TT')

    sns.kdeplot(data=paired_data[animal][0], ax=axes[2][0], color="black", fill=False, alpha=0.8, linewidth=1.4, linestyle='-', bw_adjust=.6, clip=(0, 20))
    sns.kdeplot(data=paired_data[animal][1], ax=axes[2][1], color="black", fill=False, alpha=0.8, linewidth=1.4, linestyle='-', bw_adjust=.6, clip=(0, 20))
    sns.kdeplot(data=paired_data[animal][2], ax=axes[2][2], color="black", fill=False, alpha=0.8, linewidth=1.4, linestyle='-', bw_adjust=.6, clip=(0, 20))

    for ax in axes[0].flatten():
        ax.legend()
        ax.set_ylabel('Frequency')
        ax.grid()

    for ax in axes[1].flatten():
        ax.set_ylabel('Kernel Density Estimate')
        ax.grid()
    
    for ax in axes[2].flatten():
        ax.set_xlabel('Duration (s)')
        ax.set_ylabel('KDE and Frequency')
        ax.grid()
    
    fig.suptitle(f'Bout Durations histogram (normalized) and KDE for each session (TR, RE, TT) for Animal {list(animals_data["treino"].keys())[animal].replace("TR", "")}', fontsize=14)
    plt.xlim(0, 20)
    plt.ylim(0, 1)
    plt.tight_layout()
    if save_figures:
        plt.savefig(os.path.join(figures_folder, f'Bout Durations histogram (normalized) and KDE for each session (TR, RE, TT) for Animal {list(animals_data["treino"].keys())[animal].replace("TR", "")}'))
        plt.close("all")
        print(f"Animal {list(animals_data['treino'].keys())[animal].replace('TR', '')} plotted successfully!")
plt.close("all")

# Plot the bout durations as a line plot for the whole experiment ------------------------------------------------------

TR_binned, TR_bins = np.histogram(TR_durations, bins=bins)
RE_binned, RE_bins = np.histogram(RE_durations, bins=bins)
TT_binned, TT_bins = np.histogram(TT_durations, bins=bins)

bin_centers = (bins[:-1] + bins[1:]) / 2

### UNCOMMENT THIS TO PLOT THE EXPLORATION BOUTS WITHOUT THE SMOOTHING
fig, ax = plt.subplots(figsize=(15, 8))
plt.plot(bin_centers, TR_binned, "-", linewidth=1.4, label="TR", color=TR_color)
plt.plot(bin_centers, RE_binned, "-", linewidth=1.4, label="RE", color=RE_color)
plt.plot(bin_centers, TT_binned, "-", linewidth=1.4, label="TT", color=TT_color)
plt.xlim(0, 10)
plt.legend()
plt.xlabel('Duration (s)')
plt.ylabel('Frequency')
plt.title('Bout Durations for each session (TR, RE, TT) - Unsmoothed')
plt.tight_layout()
if save_figures:
    plt.savefig(os.path.join(figures_folder, 'Bout Durations for each session (TR, RE, TT) - Unsmoothed.png'))
    plt.close("all")
    print("Unsmoothed bout durations plotted successfully!")
plt.close("all")

# Interpolate the lines for smoother decay
TR_spline = make_interp_spline(bin_centers, TR_binned, k=3)
RE_spline = make_interp_spline(bin_centers, RE_binned, k=3)
TT_spline = make_interp_spline(bin_centers, TT_binned, k=3)

# Generate new x values for smooth curves
x_smooth = np.linspace(bin_centers.min(), bin_centers.max(), 300)
TR_smooth = TR_spline(x_smooth)
RE_smooth = RE_spline(x_smooth)
TT_smooth = TT_spline(x_smooth)

# Plot the smoothed lines
fig, ax = plt.subplots(figsize=(15, 8))
plt.plot(x_smooth, TR_smooth, "-", linewidth=1.1, label="TR", color=TR_color)
plt.plot(x_smooth, RE_smooth, "-", linewidth=1.1, label="RE", color=RE_color)
plt.plot(x_smooth, TT_smooth, "-", linewidth=1.1, label="TT", color=TT_color)
plt.xlim(0, 10)
plt.legend()
plt.xlabel('Duration (s)')
plt.ylabel('Frequency')
plt.title('Bout Durations for each session (TR, RE, TT) - Smoothed')
plt.tight_layout()
if save_figures:
    plt.savefig(os.path.join(figures_folder, 'Bout Durations for each session (TR, RE, TT) - Smoothed.png'))
    plt.close("all")
    print("Smoothed bout durations plotted successfully!")
plt.close("all")

# Plot the bout durations as a line plot for each animal ----------------------------------------------------------------
for animal in range(len(paired_data)):
    TR_binned = paired_bins[animal][0]
    RE_binned = paired_bins[animal][1]
    TT_binned = paired_bins[animal][2]

    bin_centers_bouts = (bins[:-1] + bins[1:]) / 2

    # Interpolate the lines for smoother decay
    TR_spline = make_interp_spline(bin_centers_bouts, TR_binned, k=3)
    RE_spline = make_interp_spline(bin_centers_bouts, RE_binned, k=3)
    TT_spline = make_interp_spline(bin_centers_bouts, TT_binned, k=3)

    # Generate new x values for smooth curves
    x_smooth = np.linspace(bin_centers_bouts.min(), bin_centers_bouts.max(), 200)
    TR_smooth = TR_spline(x_smooth)
    RE_smooth = RE_spline(x_smooth)
    TT_smooth = TT_spline(x_smooth)

    # Plot the smoothed lines
    fig, ax = plt.subplots(figsize=(15, 8))
    plt.plot(x_smooth, TR_smooth, "-", linewidth=1.1, label="TR", color=TR_color)
    plt.plot(x_smooth, RE_smooth, "-", linewidth=1.1, label="RE", color=RE_color)
    plt.plot(x_smooth, TT_smooth, "-", linewidth=1.1, label="TT", color=TT_color)
    plt.xlim(0, 10)
    ax.xaxis.set_major_locator(MultipleLocator(0.5))  # Major ticks every 1 unit (adjust if needed)
    ax.tick_params(axis='x', which='both', direction='in', length=6)
    plt.legend()
    plt.xlabel('Duration (s)')
    plt.ylabel('Frequency')
    plt.title(f'Bout Durations for Animal {list(animals_data["treino"].keys())[animal].replace("TR", "")} (Smoothed)')
    plt.tight_layout()
    if save_figures:
        plt.savefig(os.path.join(figures_folder, f'Bout Durations for Animal {list(animals_data["treino"].keys())[animal].replace("TR", "")} (Smoothed)'))
        plt.close("all")
        print(f"Animal {list(animals_data['treino'].keys())[animal].replace('TR', '')} plotted successfully!")
plt.close("all")

# Plot the KDE for the whole experiment -----------------------------------------------------------------------------------
fig, ax_kde = plt.subplots(figsize=(15, 8))
sns.kdeplot(
    data=data_dataframe,
    palette=[TR_color, RE_color, TT_color],
    fill=True,
    alpha=0.8,
    linewidth=.5,
    multiple="stack",
    edgecolor="white",
    bw_adjust=1.6,
    clip=(0, 20),
)
ax_kde.xaxis.set_major_locator(MultipleLocator(0.5))  # Major ticks every 1 unit (adjust if needed)
ax_kde.tick_params(axis='x', which='both', direction='out', length=6)
ax_kde.set_xlabel("Duration (s)", fontsize=12)
ax_kde.set_ylabel("Density", fontsize=12)
ax_kde.set_xlim(0, 15)
ax_kde.set_title("Normalized KDE for Bout Duration histogram in each session (TR, RE, TT)", fontsize=14)
plt.tight_layout()
if save_figures:
    plt.savefig(os.path.join(figures_folder, 'Normalized KDE for Bout Duration histogram in each session (TR, RE, TT).png'))
    plt.close("all")
    print("KDE for the whole experiment plotted successfully!")
plt.close("all")

# Plot the bout durations for the whole experiment ----------------------------------------------------------------
multi_x = [TR_durations, RE_durations, TT_durations]
fig, ax = plt.subplots(figsize=(15, 8))
multi_x_bin_counts, multi_x_bins, _ = ax.hist(multi_x, bins=bins, color=[TR_color, RE_color, TT_color], alpha=0.9, label=['TR', 'RE', 'TT'])

# Calculate bin centers
multi_x_bin_centers_temp = (multi_x_bins[:-1] + multi_x_bins[1:]) / 2
multi_x_bin_centers = np.insert(multi_x_bin_centers_temp, 0, 0)

# Set custom x-ticks at bin centers
bin_labels = [f"{x:.1f}" if x != 0 else None for x in bins]
ax.set_xticks(multi_x_bin_centers, bin_labels)
ax.set_xlim(0, 15)
ax.set_xlabel('Duration (s)')
ax.set_ylabel('Frequency')
ax.set_title('Bout Duration histogram for each session stacked (TR, RE, TT)')
ax.legend()
ax.grid()
plt.tight_layout()
if save_figures:
    plt.savefig(os.path.join(figures_folder, 'Bout Duration histogram for each session stacked (TR, RE, TT).png'))
    plt.close("all")
    print("Bout Duration histogram for each session stacked (TR, RE, TT) plotted successfully!")
plt.close("all")