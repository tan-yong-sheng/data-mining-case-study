import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot_distributions(df, variables):
    """
    Plots the distribution of segments and variables for a DataFrame.

    Args:
        df (pd.DataFrame): DataFrame with a 'Segment' column and other variables.
        variables (list of str): List of column names to create barplots.
    """
    num_variables = len(variables)
    cols = min(num_variables + 1, 3)
    rows = (num_variables + 1 + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(18, rows * 6))
    axes = axes.flatten()

    # Pie chart for segment distribution
    segment_counts = df['Segment'].value_counts()
    axes[0].pie(segment_counts, labels=segment_counts.index, autopct='%1.1f%%', startangle=90)
    axes[0].set_title('Segment Distribution')

    for i, variable in enumerate(variables, start=1):
        # Create bins to represent the variables
        variable_bins = pd.cut(df[variable], bins=10, labels=False)

        # Group the count of each variable bin by segment
        grouped_data = df.groupby(['Segment', variable_bins]).size().unstack(fill_value=0)

        # Normalize to percentage
        grouped_data = grouped_data.div(grouped_data.sum(axis=1), axis=0) * 100
        
        # Create the stacked bar chart and get the plot object
        plot_obj = grouped_data.plot(kind='bar', stacked=True, ax=axes[i], legend=True)
        
        # Add the legend title to be the variable name
        axes[i].legend(title = variable)
        
        axes[i].set_ylabel('Percent (Sum)')
        axes[i].set_xlabel('Segment')  # Changed to just 'Segment'
        axes[i].set_title(f'Variable = {variable}')
    
    # remove unused axes
    for j in range(num_variables + 1, rows*cols):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()
    


def plot_histogram_distributions(df, variables, title="Cluster Histogram Distributions vs. Overall Distribution"):
    """
    Plots the distribution of specified variables across different segments, comparing them to the overall distribution.

    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame containing segment data, must contain a column named "Segment", and the specified variables.
    variables : list of str
        A list of column names in 'df' to be plotted, where each will be considered a feature of the segments.
    title : str, optional
        The title to be set at the top of the visualization. Default is "Cluster Histogram Distributions vs. Overall Distribution"
    """

    # Get unique segments
    segments = df['Segment'].unique()

    # number of rows and columns for the grid of plots
    n_rows = len(segments)
    n_cols = len(variables)

    # Create figure and subplots
    fig, axes = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(15, 10))
    plt.subplots_adjust(hspace=0.5, wspace=0.3)

    for i, segment in enumerate(segments):
        for j, feature in enumerate(variables):
            ax = axes[i, j]  # Accessing the current subplot in the grid

            # Filter data for the current segment
            segment_data = df[df['Segment'] == segment][feature]

            # Get overall distribution of the feature
            overall_data = df[feature]

            # Calculate bin edges for histograms
            min_value = min(overall_data.min(), segment_data.min())
            max_value = max(overall_data.max(), segment_data.max())
            bins = np.linspace(min_value, max_value, 10)  # Adjust the number of bins

            # Plot segment's histogram
            segment_counts, _ = np.histogram(segment_data, bins=bins)
            segment_percent = (segment_counts / len(segment_data)) * 100
            ax.bar(bins[:-1], segment_percent, width=(bins[1] - bins[0]),
                   alpha=0.7, edgecolor='black', label='Segment', color='royalblue')

            # Plot overall distribution
            overall_counts, _ = np.histogram(overall_data, bins=bins)
            overall_percent = (overall_counts / len(overall_data)) * 100
            ax.plot(bins[:-1], overall_percent, color='firebrick', linewidth=2, label='Overall')

            # Set axis labels and title
            if i == n_rows - 1:
                ax.set_xlabel(feature)
            if j == 0:
                ax.set_ylabel('Percent')
                ax.text(-0.55, 0.5, f'Segment: {segment}\nCount: {len(segment_data)}\nPercent: {len(segment_data) / len(df) * 100:.1f}',
                        transform=ax.transAxes,
                        verticalalignment='center', horizontalalignment='right')

            ax.set_title(feature if i == 0 else "")

    plt.suptitle(title, y=0.03)  # title of the entire image
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # Sample Data (replace with your actual data)
    # make sure that data is loaded in dataframe with columns: "Segment","Annual Income","Spending Score","Age"

    data = {
        'Segment': [1, 1, 1, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5],
        'Annual Income': [20, 30, 40, 60, 80, 50, 70, 90, 100, 120, 150, 25, 50, 75],
        'Spending Score': [10, 20, 30, 70, 80, 40, 60, 90, 20, 40, 90, 10, 40, 70],
        'Age': [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 20, 30, 60]
    }
    df = pd.DataFrame(data)

    # Features to plot
    features = ["Annual Income", "Spending Score", "Age"]

    # Create the plot
    plot_segment_distributions(df, features)