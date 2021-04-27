
# twittrender.py
"""Generates a colorful wordcloud image from location-based trending Twitter topics.
   Choose from list of countries or cities. Wordcloud will be shaped in the image of the selected region. 
   A csv file containing the data will also be created.
"""

from wordcloud import WordCloud
from operator import itemgetter
import csv
import imageio
import tweepy
import keys

print('\n\nWould you like to examine the Twitter trends in a country or a city?')
print('[1] for country\n[2] for city')

try:
    area_type = int(input('What do you choose?'))
    if area_type not in [1, 2]:
        raise ValueError

except ValueError:
    print('You must choose 1 or 2')

if area_type == 1:
    print('\n\nChoose:\n1) Australia\n2) Canada\n3) France\n4) India\n' 
          '5) Mexico\n6) South Africa\n7) UK\n8) USA\n9) Whole World')

    try:
        country_choice = int(input('What do you choose?'))
        if country_choice not in [i for i in range(1, 10)]:
            raise ValueError

    except ValueError:
        print('You must choose from the options above.')

    if country_choice == 1:
        woeid = 23424748
        placename = 'Australia'
        mask_image = imageio.imread('./masks/australia.png')

    if country_choice == 2:
        woeid = 23424775
        placename = 'Canada'
        mask_image = imageio.imread('./masks/canada.png')

    elif country_choice == 3:
        woeid = 23424819
        placename = 'France'
        mask_image = imageio.imread('./masks/france.png')

    elif country_choice == 4:
        woeid = 23424748
        placename = 'India'
        mask_image = imageio.imread('./masks/india.png')

    elif country_choice == 5:
        woeid = 23424900
        placename = 'Mexico'
        mask_image = imageio.imread('./masks/mexico.png')

    elif country_choice == 6:
        woeid = 23424942
        placename = 'South Africa'
        mask_image = imageio.imread('./masks/southafrica.png')

    elif country_choice == 7:
        woeid = 23424975
        placename = 'UK'
        mask_image = imageio.imread('./masks/uk.png')

    elif country_choice == 8:
        woeid = 23424977
        placename = 'USA'
        mask_image = imageio.imread('./masks/usa.png')

    elif country_choice == 9:
        woeid = 1
        placename = 'Whole World'
        mask_image = imageio.imread('./masks/world.png')

elif area_type == 2:
    print('\n\nChoose:\n1) Albuquerque\n2) Boston\n3) Chicago\n4) Denver\n5) New York City\n6) San Francisco\n7) Kansas City, MO')

    try:
        state_choice = int(input('What do you choose?'))
        if state_choice not in [1, 2, 3, 4, 5, 6, 7]:
            raise ValueError

    except ValueError:
        print('You must choose from the options above.')

    if state_choice == 1:
        woeid = 2352824
        placename = 'Albuquerque'
        mask_image = imageio.imread('./masks/newmexico.png')

    elif state_choice == 2:
        woeid = 2367105
        placename = 'Boston'
        mask_image = imageio.imread('./masks/massachusetts.png')

    elif state_choice == 3:
        woeid = 2379574
        placename = 'Chicago'
        mask_image = imageio.imread('./masks/illinois.png')

    elif state_choice == 4:
        woeid = 2391279
        placename = 'Denver'
        mask_image = imageio.imread('./masks/colorado.png')

    elif state_choice == 5:
        woeid = 2459115
        placename = 'New York City'
        mask_image = imageio.imread('./masks/newyork.png')

    elif state_choice == 6:
        woeid = 2487956
        placename = 'San Francisco'
        mask_image = imageio.imread('./masks/california.png')

    elif state_choice == 7:
        woeid = 2430683
        placename = 'Kansas City'
        mask_image = imageio.imread('./masks/missouri.png')

    else:
        print('I have not entered those codes yet.')

# setting up Twitter authorization
auth= tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret)
auth.set_access_token(keys.access_token, keys.access_token_secret)

# creating Tweepy API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

trends = api.trends_place(id=woeid) # returns a list/array of Trend objects
trends_list = trends[0]['trends'] # creating list of trend dictionaries
timestamp = trends[0]['as_of'] # pulling timestamp from trends object
timestamp = timestamp.replace(':', '_') # cleaning timestamp so it can be used in file names

for trend in trends_list: # changing tweets with no registered volume to 5000 for ordering & WordCloud sizing
    if trend['tweet_volume'] == None:
        trend['tweet_volume'] = 5000

trends_list.sort(key=itemgetter('tweet_volume'), reverse=True) # Ordering list by tweet_volume

topics = {} # initializing topics dict for our WordCloud
for trend in trends_list: # creating key & value pairs from data in trends_list
    topics[trend['name']] = trend['tweet_volume']

# Creating WordCloud object
wordcloud = WordCloud(width=1500, height=1500, prefer_horizontal=0.5, min_font_size=8,
                      colormap='prism', background_color='black', mask=mask_image)

wordcloud = wordcloud.fit_words(topics) # using topics dict to populate WordCloud object
wordcloud = wordcloud.to_file(f'IMG/{placename}_TwitTrender_WordCloud_{timestamp}.png') # exporting WordCloud file to img folder

# creating topics_list for csv export & converting tweet_volumes with 5000 back to accurate representation
topics_list = []
for t, v in topics.items():
    if v < 10000:
        v = '<10K'
    tv_list = [t, v]
    topics_list.append(tv_list)

# Creating csv file
with open(f'./CSV/{placename}_TwitTrender_{timestamp}.csv', mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(topics_list)

# Print out of Topics & Volume
print('\n\n')
print(f'{placename} trending tweet topics\n')
print(f'{"TOPIC":>35}  {"VOLUME":<20}\n')
for trend in trends_list:
    if trend["tweet_volume"] == 5000:
        print(f'{trend["name"]:>35}: {"<10K":<20}')
    
    else:
        print(f'{trend["name"]:>35}: {trend["tweet_volume"]:<20}')
print('')

print(f"Your {placename} Word Cloud is now in the 'IMG' folder.\n Your csv file is in the 'CSV' folder.")