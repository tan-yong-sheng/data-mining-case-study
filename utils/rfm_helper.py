import pandas as pd
import numpy as np
# Note: the dataset is already an aggregated dataset by customer_id, so I don't need to perform groupby() operation


def perform_ecomm_rfm_analysis(df, 
                columns=["CustomerID", "LastPurchaseDate", 
                         "TotalPurchases", "TotalSpent"]):
    # Note: LastPurchaseDate is actually OrderLastPurchase
    rfm_df = df[columns].copy()

    # Rename columns to match RFM convention
    rfm_df.columns = [columns[0], 'recency', 'frequency', 'monetary']

    # Ensure columns are numeric
    rfm_df['recency'] = rfm_df['recency'].astype(float)
    rfm_df['frequency'] = rfm_df['frequency'].astype(float)
    rfm_df['monetary'] = rfm_df['monetary'].astype(float)
    print("Step 1: Data prepared")

    # Calculate recency quantiles with dynamic bin handling
    recency_bins = pd.qcut(rfm_df['recency'], q=4, duplicates='drop')
    rfm_df['RecencyQuantile'] = pd.qcut(
        rfm_df['recency'], q=4, labels=range(len(recency_bins.cat.categories), 0, -1), duplicates='drop'
    ).astype(int)
    print("Step 2: Recency quantiles calculated")

    # Calculate frequency quantiles with dynamic bin handling
    frequency_bins = pd.qcut(rfm_df['frequency'], q=4, duplicates='drop')
    rfm_df['FrequencyQuantile'] = pd.qcut(
        rfm_df['frequency'], q=4, labels=range(1, len(frequency_bins.cat.categories) + 1), duplicates='drop'
    ).astype(int)
    print("Step 3: Frequency quantiles calculated")

    # Calculate monetary quantiles with dynamic bin handling
    monetary_bins = pd.qcut(rfm_df['monetary'], q=4, duplicates='drop')
    rfm_df['MonetaryQuantile'] = pd.qcut(
        rfm_df['monetary'], q=4, labels=range(1, len(monetary_bins.cat.categories) + 1), duplicates='drop'
    ).astype(int)
    print("Step 4: Monetary quantiles calculated")

    # Segment customers
    def segment_customer(row):
        try:
            if row['MonetaryQuantile'] >= 3 and row['FrequencyQuantile'] >= 3:
                return 'High Value Customer'
            elif row['FrequencyQuantile'] >= 3:
                return 'Loyal Customer'
            elif row['RecencyQuantile'] <= 1:
                return 'At Risk Customer'
            elif row['RecencyQuantile'] >= 3:
                return 'Persuadable Customer'
            else:
                return 'Average Customer'
        except Exception as e:
            print(f"Error in segmentation logic for row: {row}, Error: {e}")
            return 'Unknown'

    rfm_df['RFMCustomerSegment'] = rfm_df.apply(segment_customer, axis=1)
    print("Step 5: Customer segmentation completed")

    # Merge back with original data
    df_engineered = df.merge(
        rfm_df[[columns[0], 'RFMCustomerSegment', 'RecencyQuantile', 'FrequencyQuantile', 'MonetaryQuantile']], 
        on=columns[0], how='left'
    )
    print("Step 6: Merged results with original data")
    
    return df_engineered