# last.fm Artist Recommender

This project is an extension of the final project for CSC 466 (Knowledge Discovery From Data) at Cal Poly, [original repo found here](https://github.com/abarbieu/music-recommender)

# Contents

1. [Dataset Generation](#dataset-generation)
2. [Notes on Usernames](#notes-on-usernames)
3. [Datasets Provided](#datasets-provided)
    1. [artists.tsv](#artiststsv)
    2. [lastfm_user_scrobbles_10k100_2021.csv](#lastfmuserscrobbles10k1002021csv)
    3. [lastfm_user_scrobbles_10k200_through2021.csv](#lastfmuserscrobbles10k200through2021csv)
    4. [usernames.csv](#usernamescsv)



# Dataset generation

This extension moves away from the [original kaggle dataset](https://www.kaggle.com/pcbreviglieri/lastfm-music-artist-scrobbles) by scraping usernames from lastfm with beautiful soup via top listeners of top artists and user neighbors. These usernames are then used in lastfm API calls to gather a list of top artists and scrobbles, and could be used to gather user demographics, top songs, individual scrobbles, and more.

## Notes on Usernames

With millions of users, it is hard to get a representative dataset from lastfm. This project was conducted with my own lastfm account in mind, so usernames were gathered first by scraping lastfm's own neighbor's page in a breadth first search. The neighbors page lists lastfm's guess at the 50 users who are most similar to you in their listening habits. This was done by exploring my neighbors, then their neighbors, and onwards, expanding the username set by 50^n at each n degrees of seperation. This was done in the hopes that users similar to me would be gathered and thus artist recommendations would be naturally skewed towards accuracy.

To avoid complete bias, the top 1000 artists of 2021 were gathered from the lastfm API and the top 150 listeners of each artist were added to the username datset. Ideally, these usernames would then be explored via neighborhood searches.

Finally, users were also gathered via my top 833 artist's top listeners in the same manner as above.

In total, this resulted in the following usernames being gathered:

* My top artist's top 150 listeners:
    * ~70k usernames
* My neighborhood searches + key user searches:
    * ~250k usernames
* Top 150 listeners of top artists:
    * ~150k usernames

Of these usernames, only ~150k unique usernames were saved in the usernames.csv file, of which only 10k users were used for the first run of artist recommendation. Hopefully these are representative, but further work may be done to expand on this.

All username sources were saved, so further analysis could be done on the efficacy of recommendation based on which users were used.

# Datasets provided

## artists.tsv

* **Description:**
    * Tab seperated list of artist names linked to their ID
* **Format**
    * ID\tArtist Name
    * **eg:** 182 \t Jacob Collier
* **Use**
    * To simplify and compress files containing artist (artist names can be very messy including pipes, commas, special characters, etc.)

## lastfm_user_scrobbles_10k100_2021.csv

* **Description:**
    * 10,000 user's top 100 artists and #listens of the year 2021
    * Gathered via API calls on each user in usernames.csv in order
* **Format**
    * user_id,artist_id,scrobbles
    * **eg:** 194,8242,1002
* **Use**
    * To build a sparse matrix representing user artist listens that can be used in collaborative filtering
* **Sparse Matrix**
    * **Format:** Each row represents a unique user, each column represents a unique artist, each cell represents the number of times that user listened to that artist

## lastfm_user_scrobbles_10k200_through2021.csv

* **Description:**
    * The same format and use as 10k100_2021 but contains 10k user's top 200 artists from user account creation to 2021

## usernames.csv

* **Description:**
    * The same format and use as artists.csv but matches user_id to username