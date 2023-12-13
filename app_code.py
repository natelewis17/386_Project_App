import pandas as pd
import streamlit as st
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt

# Load your dataset
url = 'https://raw.githubusercontent.com/natelewis17/STAT386_Project/main/kanji.csv'
df = pd.read_csv(url)

# Sidebar with user input
st.sidebar.title('Wikiji: Kanji Explorer')
user_input = st.sidebar.text_input('Enter a Kanji or an Enlgish Meaning', '水')

st.title(f'Kanji Explorer - Showing results for {user_input}')

# Filter the DataFrame based on user input
filtered_df = df[df['Kanji'].str.contains(user_input) | df['Meanings'].str.contains(user_input)]

# Display the filtered DataFrame
st.write(f"Showing results for: {user_input}")
st.write(filtered_df)

# More detailed information (you can customize this based on your columns)
if not filtered_df.empty:
    st.subheader('Details:')
    for index, row in filtered_df.iterrows():
        st.write(f"Kanji: {row['Kanji']}")
        st.write(f"Meanings: {row['Meanings']}")
        st.write(f"JLPT Level: N{row['JLPT']}")
        # Add more columns as needed

# Visualization of Wiki_Ranking, Novel_Ranking, Newspaper_Ranking
if not filtered_df.empty:
    st.subheader('Rankings Distribution')

    # Melt the DataFrame for Altair
    melted_df = pd.melt(filtered_df, id_vars=['Kanji'], value_vars=['Wiki_Ranking', 'Novel_Ranking', 'Newspaper_Ranking'],
                        var_name='Ranking Type', value_name='Ranking')

    # Create a grouped bar chart using Altair
    chart = alt.Chart(melted_df).mark_bar().encode(
        column='Ranking Type',
        x='Kanji',
        y='Ranking'
    ).properties(width=150)

    # Display the chart using Streamlit and Altair
    st.altair_chart(chart)

    # Sidebar with user input

# Sidebar with user input
st.sidebar.title('Wikiji: Wiki Kanji Frequency')
group_by_option = st.sidebar.selectbox('Select grouping option', ['Stroke_Count', 'JLPT', 'Grade', 'In_Joyo'])

# Group by the selected option and sum Wiki_Counts
grouped_df = df.groupby(group_by_option)['Wiki_Count'].sum().reset_index()

# Display the big title
st.title(f'Wiki Kanji Frequency - Grouped by {group_by_option}')

# Plotting
fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(x=group_by_option, y='Wiki_Count', data=grouped_df, ci=None, ax=ax)
plt.title(f'Bar Plot of Frequency Grouped by {group_by_option}')
plt.xlabel(group_by_option)
plt.ylabel('Occurrences on Sampled Wikipedia Articles')

# Display the plot using st.pyplot(fig)
st.pyplot(fig)