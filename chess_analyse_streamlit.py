
# next add session states for using category as a filter, add visualizations, dark theme, integrate selenium
import numpy as np
import pandas as pd
import csv
import datetime
import time
import os  
import streamlit as st
import matplotlib.pyplot as plt

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
    url = 'https://raw.githubusercontent.com/arthurmeltendorf/chess/main/my_chess_archive.csv'
    df = pd.read_csv(url)
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    return df

# # Running streamlit app

def main():
    st.set_page_config(layout='wide')
    st.title('Chess Stats Dashboard')

    # User inputs
    
    username = st.text_input("Enter your Chess.com username")
    password = st.text_input("Enter your Chess.com password", type='password')
    pages = st.text_input("Enter the number of pages on your chess.com archive")
    game_categories = ['1 min', '1|1', '2|1', '3 min', '3|2', '5 min', '5|5', '10 min']
    selected_game = st.selectbox('Select a Game Category:', game_categories)

    if st.button('Get Stats'):
        if username and password:
            # Scrape the data
            st.write("Fetching your chess data...")
            df = scrape_data(username, password, pages)
            filtered_df = df[df['Game Category'] == selected_game]

    
            # Calculate statistics and display statistics at top
            games_played = len(filtered_df)
            years_days_played = filtered_df['Date'].max() - filtered_df['Date'].min()
            highest_ranking = filtered_df['My_Rating'].max()
            win_percentage = (filtered_df['Result'] == 'Win').mean() * 100

            data = {
                "Games": games_played,
                "Time": (f"{years_days_played.days // 365} years & {years_days_played.days % 365} days"),
                "Highest Ranking": highest_ranking,
                "Win %": (f"{win_percentage:.2f}%"),
            }
            
            cols = st.columns(4)
            for i, (category, number) in enumerate(data.items()):
                html = f"""
                <div style='text-align: center;'>
                    <h2 style='font-size: 32px; font-weight: bold;'>{number}</h2>
                    <p style='font-size: 16px;'>{category}</p>
                </div>
                """
                cols[i].markdown(html, unsafe_allow_html=True)
    
            # Line chart
            st.line_chart(filtered_df.set_index('Date')['My_Rating'])

            # Pie chart and histogram

            plt.rcParams['figure.facecolor'] = '#262730'
            pie_colors = ['#14d8c4', '#c594ff', '#aaabab']
            hist_color = '#c594ff'
            col1, col2 = st.columns(2)

            with col1:
                results_counts = filtered_df['Result'].value_counts()
                fig1, ax1 = plt.subplots(figsize=(4, 2))
                patches, texts, autotexts = ax1.pie(results_counts, autopct='%1.1f%%', startangle=90, colors=pie_colors)
                for text in texts + autotexts:
                    text.set_color('white')  # Change text color to white
                ax1.legend(results_counts.index, loc="center left", bbox_to_anchor=(0.9, 0.5),fontsize=4)
                ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                ax1.set_facecolor('#262730')
                plt.gca().set_facecolor('#262730')
                st.pyplot(fig1)

            with col2:
                accuracy_values = filtered_df['My_Accuracy'].dropna()
                fig2, ax2 = plt.subplots(figsize=(4, 2))
                ax2.hist(accuracy_values, bins=20, edgecolor='#262730', color=hist_color)
                ax2.set_title('Accuracy')
                ax2.set_xlabel('Accuracy')
                ax2.set_ylabel('Frequency')
                ax2.set_facecolor('#262730')
                plt.gca().set_facecolor('#262730')
                st.pyplot(fig2)
        
        else:
            st.error('Please enter your Chess.com username and password.')

if __name__ == "__main__":
    main()



