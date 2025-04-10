import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import ast

# ------------- Load dataset -------------
df = pd.read_csv("rawg_games_data.csv")

# Safely parse JSON-like columns
def parse_column(row):
    try:
        return ast.literal_eval(row)
    except:
        return []

# ------------- Parse genres and platforms -------------
df['genre_names'] = df['genres'].apply(lambda x: [g['name'] for g in parse_column(x)])
df['platform_names'] = df['platforms'].apply(lambda x: [p['platform']['name'] for p in parse_column(x)])

# Convert release date and extract year
df['released'] = pd.to_datetime(df['released'], errors='coerce')
df['release_year'] = df['released'].dt.year

# ------------- Sidebar filters -------------
st.sidebar.header("Filters")
all_genres = sorted({g for sublist in df['genre_names'] for g in sublist})
selected_genres = st.sidebar.multiselect("Filter by Genre", all_genres)

all_platforms = sorted({p for sublist in df['platform_names'] for p in sublist})
selected_platforms = st.sidebar.multiselect("Filter by Platform", all_platforms)

min_year = int(df['release_year'].min())
max_year = int(df['release_year'].max())
selected_year_range = st.sidebar.slider("Select Release Year Range", min_year, max_year, (min_year, max_year))

# ------------- Apply filters -------------
filtered_df = df[
    df['genre_names'].apply(lambda genres: all(g in genres for g in selected_genres) if selected_genres else True) &
    df['platform_names'].apply(lambda platforms: all(p in platforms for p in selected_platforms) if selected_platforms else True) &
    df['release_year'].between(selected_year_range[0], selected_year_range[1])
]

# Title and Description
st.title("🎮 Video Game Data Dashboard")
st.write("This app is the Data Exploration Project of the Video Game Data from RAWG API dataset.")

# ------------- Game Releases Over Time -------------
st.markdown("<h3 style='text-align: center; font-size:32px;'>📅 Game Releases Over Time</h3>", unsafe_allow_html=True)

release_counts = filtered_df['release_year'].value_counts().reset_index()
release_counts.columns = ['release_year', 'count']
release_counts = release_counts.sort_values('release_year')
plt.figure(figsize=(12, 8))
fig_overtime = px.bar(
    release_counts, 
    x="release_year", 
    y='count', 
    color='count',
    color_continuous_scale='viridis',
    title="Number of Game Releases by Year",
    labels={"release_year": "Release Year", "count": "Number of Games"}
)


st.plotly_chart(fig_overtime)
st.markdown("""
**Interpretation:** Game releases increased significantly after the 1990s, reflecting the rapid growth of the video game industry.
""")
st.divider()

# ------------- Top 10 Platforms (Games After 2014) -------------
st.markdown("<h3 style='text-align: center; font-size:26px;'>💻 Top 10 Platforms (Games After 2014)</h3>", unsafe_allow_html=True)
subset = filtered_df[filtered_df['release_year'] > 2014]
platform_df = subset.explode('platform_names')
top_platforms = platform_df['platform_names'].value_counts().head(10)

fig_platform = plt.figure(figsize=(10, 6))
sns.barplot(x=top_platforms.values, y=top_platforms.index, palette='magma')
plt.title('Top 10 Platforms (Games After 2014)', fontsize=16)
plt.xlabel('Number of Games')
plt.ylabel('Platform')
plt.tight_layout()
st.pyplot(fig_platform)
st.markdown("""
**Interpretation:** This bar chart reflects both popularity and quality by showing game counts across the top 10 platforms for titles released after 2014.
""")
st.divider()

# ------------- Metacritic vs User Rating -------------
st.markdown("<h3 style='text-align: center; font-size:26px;'>🎯 Metacritic vs. User Rating</h3>", unsafe_allow_html=True)
if 'metacritic' in filtered_df.columns and 'rating' in filtered_df.columns:
    fig_scatter = px.scatter(
        filtered_df, 
        x="metacritic", 
        y='rating', 
        color='release_year', 
        hover_data=['name'],
        color_continuous_scale='Plasma',
        title="Metacritic Score vs. User Rating",
        labels={"metacritic": "Metacritic Score", "rating": "User Rating"}
    )
    fig_scatter.update_layout(
    xaxis_title_font=dict(size=24, color='black'),
    yaxis_title_font=dict(size=24, color='black'),
    )
    st.plotly_chart(fig_scatter)
    st.markdown("""
    **Interpretation:** A clear positive correlation suggests games rated highly by critics also tend to receive high user ratings.
    """)
else:
    st.write("Metacritic or rating data is missing.")
st.divider()

# ------------- Rating Distribution by Genre (Violin Plot) -------------
st.markdown("<h3 style='text-align: center; font-size:26px;'>🎻 Rating Distribution by Genre (Violin Plot)</h3>", unsafe_allow_html=True)
filtered_df['genres_list'] = filtered_df['genre_names']
genre_exploded = filtered_df.explode('genres_list').reset_index(drop=True)
genre_avg = genre_exploded.groupby('genres_list')['rating'].mean().reset_index()
genre_avg.columns = ['Genre', 'AvgRating']
genre_avg = genre_avg.sort_values('AvgRating', ascending=False)

fig_violin = plt.figure(figsize=(12, 8))
sns.violinplot(data=genre_exploded, x='rating', y='genres_list', palette='rocket')
plt.title('Rating Distribution by Genre (Violin Plot)', fontsize=16)
plt.xlabel('Rating', fontsize=16)
plt.ylabel('Genre', fontsize=16)
plt.tight_layout()
st.pyplot(fig_violin)
st.markdown("""
 **Interpretation:** The violin plot provides a smooth view of rating distribution across genres, showing both spread and concentration for each genre.
""")
st.divider()

# ------------- Top 10 Most Popular Games (Lollipop Chart) -------------
st.markdown("<h3 style='text-align: center; font-size:26px;'>🔥 Top 10 Most Popular Games</h3>", unsafe_allow_html=True)
top_popular = filtered_df.nlargest(10, 'ratings_count').sort_values('ratings_count', ascending=False)
colors = sns.color_palette("cividis", len(top_popular))

fig_popular = plt.figure(figsize=(16, 10))
for i, (index, row) in enumerate(top_popular.iterrows()):
    plt.hlines(
        y=row['name'],
        xmin=0,
        xmax=row['ratings_count'],
        color=colors[i],
        alpha=0.8,
        linewidth=2
    )
    plt.scatter(
        row['ratings_count'],
        row['name'],
        color=colors[i],
        s=100
    )
plt.title('Top 10 Most Popular Games', fontsize=18)
plt.xlabel('Number of Ratings', fontsize=12)
plt.ylabel('Game', fontsize=12)
plt.tight_layout()
st.pyplot(fig_popular)
plt.clf()
st.markdown("""
**Interpretation:** Games like *GTA V* and *Witcher 3* dominate in popularity, showing broad appeal and sustained engagement.
""")
st.divider()

# ------------- Top 10 Highest Rated Games (1000+ Ratings) -------------
st.markdown("<h3 style='text-align: center; font-size:26px;'>🏆 Top 10 Highest Rated Games (1000+ Ratings)</h3>", unsafe_allow_html=True)
top_rated = filtered_df[filtered_df['ratings_count'] >= 1000].nlargest(10, 'rating').sort_values('rating', ascending=False)
fig_rated = plt.figure(figsize=(16, 10))
colors = sns.color_palette("coolwarm", len(top_rated))

for i, (index, row) in enumerate(top_rated.iterrows()):
    plt.hlines(
        y=row['name'],
        xmin=0,
        xmax=row['rating'],
        color=colors[i],
        alpha=0.8,
        linewidth=2
    )
    plt.scatter(
        row['rating'],
        row['name'],
        color=colors[i],
        s=100
    )
plt.title('Top 10 Highest Rated Games', fontsize=18)
plt.xlabel('Rating', fontsize=16)
plt.ylabel('Game', fontsize=16)
plt.tight_layout()
st.pyplot(fig_rated)
st.markdown("""
**Interpretation:** Highly rated games like *Red Dead Redemption 2*, *Portal 2*, and *Half-Life 2* reflect critical and player acclaim.
""")
st.divider()


# ------------- User Rating Breakdown by Percent (Pie Chart) -------------
st.markdown("<h3 style='text-align: center; font-size:26px;'>🥧 User Rating Breakdown by Percent (Pie Chart)</h3>", unsafe_allow_html=True)
rating_percent = {}
for row in filtered_df['ratings'].dropna():
    try:
        ratings_list = ast.literal_eval(row)
        for rating in ratings_list:
            title = rating['title']
            percent = rating.get('percent', 0)
            rating_percent[title] = rating_percent.get(title, 0) + percent
    except:
        continue

if rating_percent:
    fig_pie, ax = plt.subplots()
    ax.pie(rating_percent.values(), labels=rating_percent.keys(), autopct='%1.1f%%', startangle=140)
    ax.axis('equal')
    st.pyplot(fig_pie)
else:
    st.warning("No rating data available for current filters.")
st.divider()


# ------------- Rating Distribution -------------
st.markdown("<h3 style='text-align: center; font-size:26px;'>⭐ Rating Distribution</h3>", unsafe_allow_html=True)
if 'rating' in filtered_df.columns:
    fig_hist = px.histogram(
        filtered_df, 
        x="rating", 
        nbins=20,
        title="Distribution of User Ratings",
        labels={"rating": "User Rating"},
        color_discrete_sequence=["purple"]
    )
    st.plotly_chart(fig_hist)
    st.markdown("""
     **Interpretation:** Most user ratings cluster between 3.0 and 4.5, showing generally favorable opinions across games.
    """)
else:
    st.write("No rating data available.")
st.divider()

# Show dataset
if st.checkbox("Show Raw Dataset"):
    st.write(df)
