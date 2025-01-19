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
    

