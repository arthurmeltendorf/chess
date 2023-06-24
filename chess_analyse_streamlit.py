#!/usr/bin/env python
# coding: utf-8

# # Importing packages

# In[1]:


pip install selenium


# In[2]:


pip install streamlit_jupyter


# In[3]:


pip install altair==4


# In[4]:


import numpy as np
import pandas as pd
import csv
import datetime
import time
import os  
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st


# # Defining scrape function + login

# In[5]:


def scrape_data(username, password, pages):
    '''
    path = "/usr/local/chromedriver"
    my_username = username
    my_password = password
    base_url = "https://www.chess.com/games/archive?gameOwner=my_game&gameTypes%5B0%5D=chess960&gameTypes%5B1%5D=daily&gameType=live&page="
    login_url = "https://www.chess.com/login"

    driver = webdriver.Chrome(path)
    driver.get(login_url)
    driver.find_element("id", "username").send_keys(my_username)
    driver.find_element("id", "password").send_keys(my_password)
    driver.find_element("id", "login").click()
    time.sleep(5)
    
    # Defining all functions to get the values from the page needed 
    def get_gametime():
        game_times = []
        for i in driver.find_elements(by = By.CLASS_NAME, value = "archive-games-game-time"):
            time = i.text
            game_times.append(time)
        return game_times

    def get_usernames():
        player_names = []
        for i in driver.find_elements(by = By.CLASS_NAME, value = "user-username-component"):
            user_name = i.text
            player_names.append(user_name)            
        return player_names
    
    def get_user_ratings():
        user_ratings = []
        for i in driver.find_elements(by = By.CLASS_NAME, value = 'user-tagline-rating'):
            rating = i.text
            user_ratings.append(rating)
        return user_ratings

    def get_result(): 
        results = []
        for i in driver.find_elements(by = By.CLASS_NAME, value = 'archive-games-result-wrapper-score'):
            result = i.text
            results.append(result)
        return results

    def get_accuracy():
        overall = []
        for i in driver.find_elements(by = By.CLASS_NAME, value = 'table-text-center'):
            acc = i.text
            overall.append(acc)
        overall.pop(0)
        accuracy = overall[1::3]
        return accuracy

    def get_moves():
        overall = []
        for i in driver.find_elements(by = By.CLASS_NAME, value = 'table-text-center'):
            acc = i.text
            overall.append(acc)
        overall.pop(0)
        moves = overall[2::3]
        return moves

    def get_dates():
        dates = []
        for i in driver.find_elements(by = By.CLASS_NAME, value = 'archive-games-date-cell'):
            date = i.text
            dates.append(date)
        return dates
    
    # Iterating over the sites to get all the data and store it globally

    player_names = []
    game_times = []
    user_ratings = []
    results = []
    accuracy = []
    moves = []
    dates = []

    for i in range(0,pages):
        url = base_url + str(i)
        driver.get(url)
        while True:
            # sometimes chess.com database is overloaded, thats why while loop is needed to log in again
            if driver.find_elements(by = By.CLASS_NAME, value = 'user-tagline-rating') == []:
                login_url = "https://www.chess.com/login"
                driver.get(login_url)
                time.sleep(5)
                driver.find_element("id", "username").send_keys(my_username)
                driver.find_element("id", "password").send_keys(my_password)
                driver.find_element("id", "login").click()
                url = base_url + str(i)
                driver.get(url)
            else:
                # game time overall
                game_times += get_gametime()
                # names of both players
                player_names += get_usernames()
                # rating for both players
                user_ratings += get_user_ratings()
                # result in game in format (0/1 or 0/1)
                results += get_result()
                # accuracy per game for both players
                accuracy += get_accuracy()
                # number of moves per game
                moves += get_moves()
                dates += get_dates()
                break
                
    # Dividing the Player Names & Ratings into Player 1 and Player 2, 
    # so we can later assign them their resp. accuracies, etc

    player1 = player_names[::2]
    player2 = player_names[1::2]
    player1_rating = user_ratings[::2]
    player2_rating = user_ratings[1::2]

    # Getting the accuracy values per player using the split function

    accuracy_for_player_1 = []
    accuracy_for_player_2 = []
    for i in range(len(accuracy)):
        if accuracy[i] == "Review" or accuracy[i] == "":
            accuracy_for_player_1.append(None)
            accuracy_for_player_2.append(None)
        else:
            accuracy_for_player_1.append(accuracy[i].split()[0])
            accuracy_for_player_2.append(accuracy[i].split()[1])
        
    # Getting the results right for each game by interpreting each game result

    who_won = []
    for i in results:
        if i.split()[0] == "1":
            who_won.append("Player1")
        elif i.split()[0] == "0":
            who_won.append("Player2")
        else:
            who_won.append("Draw")
        
    # Transforming all info we have into a dataframe to now clean up all info and getting rid of player1/2 scheme

    d1  = {"player1" : player1,
          "player2" : player2,
          "player1_rating": player1_rating,
          "player2_rating": player2_rating,
          "Winner" : who_won,
          "accuracy_player1" : accuracy_for_player_1,
          "accuracy_player2" : accuracy_for_player_2}

    df = pd.DataFrame(d1)

    # Assigning all values to you or your opponent and interpreting the result ("1/0" into "Win" or "Loss")

    result = []
    for i in df.index:
        if df["player1"][i] == my_username and df["Winner"][i] == "Player1":
            result.append("Win")
        if df["player1"][i] == my_username and df["Winner"][i] == "Player2":
            result.append("Loss")
        if df["player2"][i] == my_username and df["Winner"][i] == "Player1":
            result.append("Loss")
        if df["player2"][i] == my_username and df["Winner"][i] == "Player2":
            result.append("Win")
        if df["Winner"][i] == "Draw":
            result.append("Draw")

    my_rating = []
    opponents_rating = []
    for i in df.index:
        if df["player1"][i] == my_username:
            my_rating.append(df["player1_rating"][i])
            opponents_rating.append(df["player2_rating"][i])
        else:
            my_rating.append(df["player2_rating"][i])
            opponents_rating.append(df["player1_rating"][i])

    opponent = []
    for i in df.index:
        if df["player1"][i] == my_username:
            opponent.append(df["player2"][i])
        else: 
            opponent.append(df["player1"][i])

    my_accuracy = []
    opponent_accuracy = []
    for i in df.index:
        if df["player1"][i] == my_username:
            my_accuracy.append(df["accuracy_player1"][i])
            opponent_accuracy.append(df["accuracy_player2"][i])
        else:
            my_accuracy.append(df["accuracy_player2"][i])
            opponent_accuracy.append(df["accuracy_player1"][i])
            
    # Adding all list to dataframe and dropping the old ones not needed any more

    df["Opponent"] = opponent
    df["My_Rating"] = my_rating
    df["Opponent_Rating"] = opponents_rating
    df["Result"] = result
    df["My_Accuracy"] = my_accuracy
    df["Opponent_Accuracy"] = opponent_accuracy
    df["Game Category"] = game_times
    df["Total Moves"] = moves
    df["Date"] = dates

    # Transform Ratings into strings and into positive values
    df["My_Rating"] = df["My_Rating"].str[1:-1].astype(int)
    df["Opponent_Rating"] = df["Opponent_Rating"].str[1:-1].astype(int)
    # Drop columns not needed any more
    df.drop(['player1_rating', 'player2_rating', "Winner", "accuracy_player1", "accuracy_player2", "player1", "player2"], axis=1, inplace=True)
    # Sort all columns by new order of choice
    df = df[["Date", "Game Category", "Result", "Total Moves", "Opponent", "My_Rating", "Opponent_Rating", "My_Accuracy", "Opponent_Accuracy"]]
    # Transform date column into datetime format
    df["Date"] = pd.to_datetime(df["Date"], infer_datetime_format=True)
    # Transform total moves into integer
    df["Total Moves"] = df["Total Moves"].astype(int)
    # Transform Accuracies into integer
    df["My_Accuracy"] = df["My_Accuracy"].astype(float)
    df["Opponent_Accuracy"] = df["Opponent_Accuracy"].astype(float)
    
    '''
    df = pd.read_csv('/Users/arthurmeltendorf/Downloads/my_chess_archive.csv')
    return df


# # Running streamlit app

# In[6]:


def main():
    st.title('Chess Stats Dashboard')

    # User inputs
    username = st.text_input("Enter your Chess.com username")
    password = st.text_input("Enter your Chess.com password", type='password')
    pages = st.text_input("Enter the number of pages on your chess.com archive")

    if st.button('Get Stats'):
        if username and password:
            # Scrape the data
            st.write("Fetching your chess data...")
            df = scrape_data(username, password, pages)

            # Calculate statistics
            games_played = len(df)
            years_days_played = df['Date'].max() - df['Date'].min()
            highest_ranking = df['My_Rating'].max()
            win_percentage = (df['Result'] == 'Win').mean() * 100
            
            # Display statistics at top
            st.write(f"Games Played: {games_played}")
            st.write(f"Years and Days Played: {years_days_played.days // 365} years & {years_days_played.days % 365} days")
            st.write(f"Highest Ranking Ever: {highest_ranking}")
            st.write(f"Win Percentage: {win_percentage:.2f}%")

            # Add your data analysis and visualization code here
            st.line_chart(df.set_index('Date')['My_Rating'])

        else:
            st.error('Please enter your Chess.com username and password.')

if __name__ == "__main__":
    main()


# In[ ]:





# # Login into Chess.com

# In[ ]:


path = "/usr/local/chromedriver"
my_username = "aarthuroo"
my_password = "chessbodogt97"
base_url = "https://www.chess.com/games/archive?gameOwner=my_game&gameTypes%5B0%5D=chess960&gameTypes%5B1%5D=daily&gameType=live&page="
login_url = "https://www.chess.com/login"

driver = webdriver.Chrome(path)
driver.get(login_url)
driver.find_element("id", "username").send_keys(my_username)
driver.find_element("id", "password").send_keys(my_password)
driver.find_element("id", "login").click()
time.sleep(5)


# # Extra Step: Get Premium for Chess.com, let the script click on every game in order to get additional insights such as accuracy

# In[ ]:


# This might take a while as loading each games takes around 20 seconds. 
# Suggestion is to adjust this and do this for 5 pages only and then another 5 pages.

links = []
number_of_archive_pages = 57

for i in range(0,number_of_archive_pages): 
    url = base_url + str(i)
    driver.get(url)
    time.sleep(5)
    list_of_links = driver.find_elements(By.XPATH,'//a[contains(@href,"www.chess.com/analysis/game/live/")]')
    for i in list_of_links:
        link = i.get_attribute("href")
        links.append(link)

links = [*set(links)]

for link in links:
    driver.get(link)
    time.sleep(15)
    driver.back()
    time.sleep(3)


# # Defining and executing formulas

# In[ ]:


# Defining all functions to get the values from the page needed 
def get_gametime():
    game_times = []
    for i in driver.find_elements(by = By.CLASS_NAME, value = "archive-games-game-time"):
        time = i.text
        game_times.append(time)
    return game_times

def get_usernames():
    player_names = []
    for i in driver.find_elements(by = By.CLASS_NAME, value = "user-username-component"):
        user_name = i.text
        player_names.append(user_name)            
    return player_names
    
def get_user_ratings():
    user_ratings = []
    for i in driver.find_elements(by = By.CLASS_NAME, value = 'user-tagline-rating'):
        rating = i.text
        user_ratings.append(rating)
    return user_ratings

def get_result(): 
    results = []
    for i in driver.find_elements(by = By.CLASS_NAME, value = 'archive-games-result-wrapper-score'):
        result = i.text
        results.append(result)
    return results

def get_accuracy():
    overall = []
    for i in driver.find_elements(by = By.CLASS_NAME, value = 'table-text-center'):
        acc = i.text
        overall.append(acc)
    overall.pop(0)
    accuracy = overall[1::3]
    return accuracy

def get_moves():
    overall = []
    for i in driver.find_elements(by = By.CLASS_NAME, value = 'table-text-center'):
        acc = i.text
        overall.append(acc)
    overall.pop(0)
    moves = overall[2::3]
    return moves

def get_dates():
    dates = []
    for i in driver.find_elements(by = By.CLASS_NAME, value = 'archive-games-date-cell'):
        date = i.text
        dates.append(date)
    return dates


# In[ ]:


# Iterating over the sites to get all the data and store it globally

player_names = []
game_times = []
user_ratings = []
results = []
accuracy = []
moves = []
dates = []

for i in range(0,57):
    url = base_url + str(i)
    driver.get(url)
    while True:
        # sometimes chess.com database is overloaded, thats why while loop is needed to log in again
        if driver.find_elements(by = By.CLASS_NAME, value = 'user-tagline-rating') == []:
            login_url = "https://www.chess.com/login"
            driver.get(login_url)
            time.sleep(5)
            driver.find_element("id", "username").send_keys(my_username)
            driver.find_element("id", "password").send_keys(my_password)
            driver.find_element("id", "login").click()
            url = base_url + str(i)
            driver.get(url)
        else:
            # game time overall
            game_times += get_gametime()
            # names of both players
            player_names += get_usernames()
            # rating for both players
            user_ratings += get_user_ratings()
            # result in game in format (0/1 or 0/1)
            results += get_result()
            # accuracy per game for both players
            accuracy += get_accuracy()
            # number of moves per game
            moves += get_moves()
            dates += get_dates()
            break


# # Cleaning the data

# In[ ]:


# Dividing the Player Names & Ratings into Player 1 and Player 2, 
# so we can later assign them their resp. accuracies, etc

player1 = player_names[::2]
player2 = player_names[1::2]
player1_rating = user_ratings[::2]
player2_rating = user_ratings[1::2]


# In[ ]:


# Getting the accuracy values per player using the split function

accuracy_for_player_1 = []
accuracy_for_player_2 = []
for i in range(len(accuracy)):
    if accuracy[i] == "Review" or accuracy[i] == "":
        accuracy_for_player_1.append(None)
        accuracy_for_player_2.append(None)
    else:
        accuracy_for_player_1.append(accuracy[i].split()[0])
        accuracy_for_player_2.append(accuracy[i].split()[1])


# In[ ]:


# Getting the results right for each game by interpreting each game result

who_won = []
for i in results:
    if i.split()[0] == "1":
        who_won.append("Player1")
    elif i.split()[0] == "0":
        who_won.append("Player2")
    else:
        who_won.append("Draw")


# In[ ]:


# Transforming all info we have into a dataframe to now clean up all info and getting rid of player1/2 scheme

d1  = {"player1" : player1,
      "player2" : player2,
      "player1_rating": player1_rating,
      "player2_rating": player2_rating,
      "Winner" : who_won,
      "accuracy_player1" : accuracy_for_player_1,
      "accuracy_player2" : accuracy_for_player_2}

df = pd.DataFrame(d1)


# In[ ]:


# Assigning all values to you or your opponent and interpreting the result ("1/0" into "Win" or "Loss")

result = []
for i in df.index:
    if df["player1"][i] == my_username and df["Winner"][i] == "Player1":
        result.append("Win")
    if df["player1"][i] == my_username and df["Winner"][i] == "Player2":
        result.append("Loss")
    if df["player2"][i] == my_username and df["Winner"][i] == "Player1":
        result.append("Loss")
    if df["player2"][i] == my_username and df["Winner"][i] == "Player2":
        result.append("Win")
    if df["Winner"][i] == "Draw":
        result.append("Draw")
        
my_rating = []
opponents_rating = []
for i in df.index:
    if df["player1"][i] == my_username:
        my_rating.append(df["player1_rating"][i])
        opponents_rating.append(df["player2_rating"][i])
    else:
        my_rating.append(df["player2_rating"][i])
        opponents_rating.append(df["player1_rating"][i])
        
opponent = []
for i in df.index:
    if df["player1"][i] == my_username:
        opponent.append(df["player2"][i])
    else: 
        opponent.append(df["player1"][i])
    
my_accuracy = []
opponent_accuracy = []
for i in df.index:
    if df["player1"][i] == my_username:
        my_accuracy.append(df["accuracy_player1"][i])
        opponent_accuracy.append(df["accuracy_player2"][i])
    else:
        my_accuracy.append(df["accuracy_player2"][i])
        opponent_accuracy.append(df["accuracy_player1"][i])


# In[ ]:


# Adding all list to dataframe and dropping the old ones not needed any more

df["Opponent"] = opponent
df["My_Rating"] = my_rating
df["Opponent_Rating"] = opponents_rating
df["Result"] = result
df["My_Accuracy"] = my_accuracy
df["Opponent_Accuracy"] = opponent_accuracy
df["Game Category"] = game_times
df["Total Moves"] = moves
df["Date"] = dates

# Transform Ratings into strings and into positive values
df["My_Rating"] = df["My_Rating"].str[1:-1].astype(int)
df["Opponent_Rating"] = df["Opponent_Rating"].str[1:-1].astype(int)
# Drop columns not needed any more
df.drop(['player1_rating', 'player2_rating', "Winner", "accuracy_player1", "accuracy_player2", "player1", "player2"], axis=1, inplace=True)
# Sort all columns by new order of choice
df = df[["Date", "Game Category", "Result", "Total Moves", "Opponent", "My_Rating", "Opponent_Rating", "My_Accuracy", "Opponent_Accuracy"]]
# Transform date column into datetime format
df["Date"] = pd.to_datetime(df["Date"], infer_datetime_format=True)
# Transform total moves into integer
df["Total Moves"] = df["Total Moves"].astype(int)
# Transform Accuracies into integer
df["My_Accuracy"] = df["My_Accuracy"].astype(float)
df["Opponent_Accuracy"] = df["Opponent_Accuracy"].astype(float)


# # Exploring the data

# In[ ]:


# First look
df.head(10)


# In[ ]:


df.info()


# In[ ]:


# Save it to a csv for future use
df.to_csv("my_chess_archive.csv")


# In[ ]:


# We are only analyzing 5min and 10min games, as in other categories there is not enough data to do so
df["Game Category"].value_counts()


# In[ ]:


# Splitting into two dataframes for comparability within each category
five_min_df = df.loc[df["Game Category"] == "5 min"]
ten_min_df = df.loc[df["Game Category"] == "10 min"]


# In[ ]:


# 1.0 Initial analysis
# 1.1 How did my elo move for different categories over time?
# 1.2 How much did I win/loose/draw overall?
# 1.3 How long are the games I am playing? Where do I peak? 

# 2.0 Few more thorough analyses
# 2.1 Do I win/loose/draw against better or worse players? What is my percentage there? 
# 2.2 How does my accuracy affect the result of my game? How strong is the correlation between having a higher accuracy and winning?
# 2.3 Do I play better on weekends? 
# 2.4 How dies the lenght of the game or the game category affect my accuracy? 
# 2.5 Do I adjust to the accuracy of my opponent or play constantly a similar accuracy? 


# In[ ]:


# 1.1
plt.figure(figsize=(10, 5))
sns.set_theme()

sns.lineplot(data = five_min_df,
             y = "My_Rating",
             x = "Date", 
             color = "teal")
sns.lineplot(data = ten_min_df,  
             y = "My_Rating",
             x = "Date", 
             color = "palevioletred")

plt.xlabel("Date")
plt.ylabel("Rating/Elo")
plt.title("Elo Rating over Time")
plt.legend(["5 Min", "10 min"])
plt.show()


# In[ ]:


# 1.3 
print("Median of moves per game is", five_min_df["Total Moves"].median())
print("Average moves per game are", five_min_df["Total Moves"].mean())


# In[ ]:


plt.figure(figsize=(10, 5))
sns.set_theme()

sns.scatterplot(data = five_min_df, 
                y = "My_Accuracy", 
                x = "Total Moves", 
                color = "teal")

plt.xlabel("Moves per Game")
plt.ylabel("My Accuracy")
plt.title("Elo Rating over Time")
plt.show()


# Further ideas:
# - colors (black/white)
# - country of opponent
# - blunders per game
# - best moves per game
# - mistakes per game

# In[ ]:




