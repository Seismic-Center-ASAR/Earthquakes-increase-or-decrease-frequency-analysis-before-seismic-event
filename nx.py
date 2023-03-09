import pandas as pd
import matplotlib.pyplot as plt

# Load data from text file
df = pd.read_csv('data.txt', delimiter='\s+')

# Remove leading/trailing whitespace from column names
df.columns = df.columns.str.strip()

# Drop duplicates
#df = df.drop_duplicates(subset='DATE')

# Convert DATE column to datetime
df['DATE'] = pd.to_datetime(df['DATE'])


# Sort data by DATE
df = df.sort_values('DATE')

# Reset index
df = df.reset_index(drop=True)

# Calculate time intervals in Hz
df['Hz'] = 1 / df['DATE'].diff().dt.total_seconds().fillna(0)

# Identify 5 magnitude events
mag_5_events = df[df['MAG'] >= 5]['DATE']

# Identify frequency decrease/increase before 5 magnitude events
events = []
for date in mag_5_events:
    date_index = df[df['DATE'] == date].index[0]
    freq_before_event = df.loc[date_index-1, 'Hz']
    freq_after_event = df.loc[date_index, 'Hz']
    if freq_before_event > freq_after_event:
        events.append(f"Frequency decreased from {freq_before_event:.8f} Hz to {freq_after_event:.8f} Hz before 5 magnitude event on {date}")
    elif freq_before_event < freq_after_event:
        events.append(f"Frequency increased from {freq_before_event:.8f} Hz to {freq_after_event:.8f} Hz before 5 magnitude event on {date}")
    else:
        events.append(f"No frequency change before 5 magnitude event on {date}")

# Write events to file
print(df.loc[date_index-1, 'DATE'], df.loc[date_index, 'DATE'])
print(df.loc[date_index-1, 'Hz'], df.loc[date_index, 'Hz'])

with open('events.txt', 'w') as f:
    f.write('\n'.join(events))

# Create a scatter plot of frequency and magnitude
plt.scatter(df['Hz'], df['MAG'], s=5)

# Set plot title and labels
plt.title('Earthquake Frequency vs. Magnitude')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')

# Set x and y limits
plt.xlim(0, 0.00002)#plt.xlim(0, 0.0002) #default
plt.ylim(2, 8)

# Display the plot
plt.show()
