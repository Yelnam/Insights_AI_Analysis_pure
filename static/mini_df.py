import pandas as pd

# This is a temporary dataframe created for testing the abilities of a chatbot to interact with a data structure

# initialise data of lists.
data = {'Brand':['Three', 'Three', 'Three', 'Three', 'Three', 'Three', 'Three', 'Three', 'Three','Vodafone', 'Vodafone', 'Vodafone', 'Vodafone', 'Vodafone', 'Vodafone'], 
   'Sentiment':['Positive', 'Positive', 'Negative', 'Neutral', 'Neutral', 'Positive', 'Positive', 'Negative', 'Neutral', 'Neutral', 'Positive', 'Positive', 'Negative', 'Neutral', 'Neutral']}

# Create DataFrame
mini_df = pd.DataFrame(data)

brands = mini_df['Brand'].unique()

brand_counts = mini_df['Brand'].value_counts()

brand_sentiment = {brand: mini_df[mini_df['Brand'] == brand ]['Sentiment'].value_counts().to_dict() for brand in brands}

"""print(mini_df)
print('\n\n')
print(brands)
print('\n\n')
print(brand_counts)
print('\n\n')
print(brand_sentiment)
print('\n')"""