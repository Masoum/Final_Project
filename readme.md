# Customer churn prediction

## Objective
In this Project I would like to Explore the Data from RAWG API which is the dataset about the video gaming data. I would like to get meaningful data out of the dataset and enterprate the plot out of dataset

## Data source
I worked with dataset from this API: "https://api.rawg.io/api/games?search=action&key=API_KEY"
the dataset is saved in "rawg_games_data.csv" with over 16K row data. that made out of 400 pages of API.

The API-KEY was produced after making a new user account. The new API was added to the URL to request the data. 

## Notebooks

There are two notebooks: One for data Explority of dataset ( Masou_Final_Project.ipynb) the other for the user interaction using streamlit (Final_Project.py)

---
## Data Cleaning

Data cleaning is crucial for data analysis. The null value dropping and cleaning data was done.
The dataset originally had 33 columns, most of the columns were stingified json format. Few columns were completely empty [user_game, clip]
[esrb_rating, metacritic, and community_rating] have many missing values. Columns with complex data (e.g., ratings, genres, platforms) were in stringified JSON format have been parsed.

AFter data cleaning there is 24 feature left:

'id', 'name', 'released', 'tba', 'rating', 'rating_top', 'ratings',
'ratings_count', 'reviews_text_count', 'added', 'metacritic',
'playtime', 'suggestions_count', 'reviews_count', 'platforms', 'genres',
'esrb_rating', 'genres_list', 'platforms_list', 'year', 'release_year',
'genre_names', 'platform_names', 'esrb_rating_clean'

---

## Analysis

### **Top 10 Platforms (Games After 2014)**

![Top 10 platforms](TopPlatform.jpg)


The platform popularity chart shows the number of games available on each platform. PC comes out with the largest library of games, reflecting its open platform. Most of consoles like PlayStation 4 and Xbox One also have a very high number of games, following closely behind PC. I see that newer platforms and consoles tend to host more games than older ones.


### **Game Released Over the Years**

![Released Over Years](ReleaseByYear.jpg)


Game releases by year show a clear upward trend. Early years (1970s–1980s) saw relatively few titles, but the rate of releases accelerated in the 1990s and especially after the 2000s. This shows the growth of the video game industry, with a coming new games as gaming became more accessible and popular. 2016 is the top rate year in video gaming industry.


## **Average Rating by Genre**

![Average Rating by Genre](AveRatingByGenre.jpg)

There are some observable differences in user ratings across genres. For example, in this dataset Indie and RPG games have slightly higher average user ratings, compared to genres like Racing or Casual. However, the differences are not very large – most genres have average ratings between 3.4 and 3.6. This suggests that player satisfaction is relatively consistent across genres, with no genre dramatically outperforming others in quality.


## **User Rating vs. Metacritic Score**

![Rating vs Metacritic](RatingvsMetacritic.jpg)

The scatter plot reveals a strong positive correlation between user ratings and Metacritic scores. In general, games that score highly with critics also tend to be highly rated by players, as evidenced by the upward trend of the points. Always, there are a few outliers – some games have higher user praise than their Metacritic score would suggest (and vice versa) – but overall the agreement is significant. This trend displays that quality tends to be recognized by both players and professional critics.


## **Top Games by Rating**

![Top 10 Highest Rate](Top10HighestRate.jpg)

The chart above lists the top 10 games by average user rating. These are the games that players rated most highly (among those with a large number of ratings). We can see that critically acclaimed titles like Red Dead Redemption 2, Half-Life 2, Portal 2, and God of War (2018) top the list with average ratings around 4.5–4.7 out of 5. This indicates an overwhelmingly positive reception from the community. Many of these games are award-winning and often cited as some of the best in their genre, which aligns with their high user scores.

## **Top Games by popularity**

![Most Popular](MostPopular.jpg)

In contrast, the top 10 most popular games (by number of user ratings) highlight that the Grand Theft Auto V has the highest count of user ratings in the dataset, showing its massive popularity, followed closely by The Witcher 3: Wild Hunt. Other entries like The Elder Scrolls V: Skyrim, Minecraft, Portal 2, and Counter-Strike have very high engagement. 
Many of these popular games also appeared in the highest-rated list, displaying that games with broad appeal often have high satisfaction between players as well.

## **User Rating By Percentage**

![User Rating By Percentage](UsrRatingByPercent.jpg)

Most users rate games as 'recommended' or 'exceptional', reflecting a generally positive community sentiment.

## **Distribution of average user ratings**

![average user ratings](AveUsrRating.jpg)

The distribution of average user ratings is roughly bell-shaped and centered around 3.5 out of 5. This indicates that most games receive moderate to good user scores. The majority of ratings are in the 3–4.5 range. Very few games have extremely low (<2) or perfect 5 average understanding that outstanding games are rare in the dataset.