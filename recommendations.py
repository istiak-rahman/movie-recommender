import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display

# Use both files as arguments for function
def recommendations(path, movie_data, user_input):
    columns = ['user_id','item_id','rating','timestamp']
    df = pd.read_csv(path, sep='\t', names=columns)
    movies_df = pd.read_csv(movie_data)
    data = pd.merge(df, movies_df, on='item_id')
    # Generate new dataframe based on the average ratings columns from merged datasets
    # Add column with total ratings for that movie across both datasets
    ratings=pd.DataFrame(data.groupby('title')['rating'].mean())
    ratings['total ratings']=pd.DataFrame(data.groupby('title')['rating'].count())
    
    # Sort values based on total ratings column --- makes it easier to make correlations
    rating_based_movies = data.pivot_table(index='user_id', columns='title', values='rating')
    ratings.sort_values('total ratings', ascending=False)
    
    # Visualizing Data
    sns.set(font_scale = 1)
    plt.rcParams["axes.grid"] = False
    plt.style.use('dark_background')
    
    plt.figure(figsize=(12,4))
    plt.hist(ratings['total ratings'],bins=80,color='tab:red')
    plt.ylabel('Ratings Count', fontsize=16)
    plt.savefig('totalratingshist.jpg')

    plt.figure(figsize=(12,4))
    plt.hist(ratings['rating'],bins=80,color='tab:red')
    plt.ylabel('Average Rating', fontsize=16)
    plt.savefig('avgratinghist.jpg')
    # Joint Plot of both total and average ratings for each movie
    full_plot = sns.jointplot(x='rating', y='total ratings', data = ratings, alpha=0.5, color='tab:pink')
    full_plot.savefig('jointplot.jpg')

    if str(user_input) in list(data['title']):
        # Following section is based on user input (AKA specific movie name)
        movie_ratings = rating_based_movies[user_input]
        similarto_input = rating_based_movies.corrwith(movie_ratings)
        # Dataframe detailing the correlation of input movie to other movies in the dataset
        corr_input = pd.DataFrame(similarto_input, columns=['Correlation'])
        corr_input.dropna(inplace=True)
        corr_input.sort_values('Correlation', ascending=False)
        corr_input = corr_input.join(ratings['total ratings'])
        return corr_input[corr_input['total ratings']>100].sort_values('Correlation', ascending=False).head(10)
    else:
        return 'Entry not found in given dataset'
  

if __name__ == '__main__':
    path = 'file.tsv'
    movie_data = 'Movie_Id_Titles.csv'

    movie_choice = str(input('What movie are you thinking of? Enter in the form of MOVIE (YEAR) '))
    recommend = recommendations(path, movie_data, movie_choice)
    display(recommend)






