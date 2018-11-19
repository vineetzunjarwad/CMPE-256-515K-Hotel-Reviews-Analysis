import pandas as pd
import math
import numpy as np
from flask import Flask
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from geopy.geocoders import Nominatim
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask_cors import CORS
from flask import request

app = Flask(__name__)
CORS(app)


@app.route("/suggestions")
def hello():
    user_nationality = request.args.get('nationality')
    city_name = request.args.get('city')

    hotel_review_dataframe = pd.read_csv('../input/Hotel_Reviews.csv')
    hotel_review_dataframe = hotel_review_dataframe[np.isfinite(hotel_review_dataframe['lat'])]
    hotel_review_dataframe = hotel_review_dataframe[np.isfinite(hotel_review_dataframe['lng'])]

    hotel_review_dataframe1 = hotel_review_dataframe.groupby(['Hotel_Name', 'Reviewer_Nationality', 'lat', 'lng']).agg({
        'Negative_Review': ', '.join, 'Positive_Review': ', '.join}).reset_index()

    hotel_review_dataframe1['review_text'] = hotel_review_dataframe1['Positive_Review'].astype(str) + \
                                             hotel_review_dataframe1['Negative_Review'].astype(str)

    hotel_review_dataframe2 = hotel_review_dataframe1[
        hotel_review_dataframe1['Reviewer_Nationality'].str.contains(user_nationality)]

    sia = SentimentIntensityAnalyzer()

    compound_value = []

    for index, row in hotel_review_dataframe2.iterrows():
        compound_value.append(sia.polarity_scores(row['review_text'])['compound'])

    se = pd.Series(compound_value)

    hotel_review_dataframe2['compound_value'] = se.values

    hotel_review_dataframe2 = hotel_review_dataframe2.sort_values(['compound_value'], ascending=[False])

    latitude, longitude = destination_lat_lng("Paris")
    print(latitude, longitude)

    distance_list = []

    for lat1, lon1, hotel, reviewer_nationality, positive_review, negative_review, review_text, compound_value in zip(
            hotel_review_dataframe2.lat, hotel_review_dataframe2.lng, hotel_review_dataframe2.Hotel_Name,
            hotel_review_dataframe2.Reviewer_Nationality, hotel_review_dataframe2.Negative_Review,
            hotel_review_dataframe2.Positive_Review, hotel_review_dataframe2.review_text,
            hotel_review_dataframe2['compound_value']):
        dist = distance(lat1, lon1, latitude, longitude)
        distance_list.append({'Hotel_Name': hotel, 'Distance': dist, 'Reviewer_nationality': reviewer_nationality,
                              'positive_review': positive_review, 'negative_review': negative_review,
                              'review_text': review_text, 'compound_value': compound_value})

    nearest_hotel = pd.DataFrame(distance_list)

    nearest_hotel1 = nearest_hotel[nearest_hotel['compound_value'] >= 0.9]
    nearest_hotel1 = nearest_hotel1.sort_values(['Distance', 'compound_value'], ascending=[True, False])
    nearest_top_hotel = nearest_hotel1.head(20)

    Hotel_distance_list = nearest_top_hotel[['Hotel_Name', 'Distance']]
    jsonList = Hotel_distance_list.to_json(orient='values')
    return jsonList
    # return "Hello World"


def destination_lat_lng(Location):
    lat_lng_locator = Nominatim()
    destination = lat_lng_locator.geocode(Location)
    return destination.latitude, destination.longitude


def distance(lat1, lon1, lat2, lon2):
    radius = 6371  # km 6371
    dlat = math.radians(lat2 - lat1)  # latitude converted into radians
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d


@app.route("/recommendations")
def recommendation():

    hotel_name = request.args.get('hotelName')

    hotel_review_dataframe4 = pd.read_csv('../input/Hotel_Reviews.csv')
    hotel_review_dataframe5 = hotel_review_dataframe4.groupby(['Hotel_Name']).agg({
        'Negative_Review': ', '.join, 'Positive_Review': ', '.join}).reset_index()

    # extracting new columne review_text by merging postitive and negative review column
    hotel_review_dataframe5['review_text'] = hotel_review_dataframe5['Positive_Review'].astype(str) + \
                                             hotel_review_dataframe5['Negative_Review'].astype(str)

    # Removing the stop words and combining all the CountVectorizer and TfidfTransformer
    tf_idf_vectorizer = TfidfVectorizer(stop_words='english')

    # Replace Na words with ''
    hotel_review_dataframe5['review_text'] = hotel_review_dataframe5['review_text'].fillna('')

    # Learn vocabulary and idf  and return term-document matrix
    term_document_matrix = tf_idf_vectorizer.fit_transform(hotel_review_dataframe5['review_text'])

    # Print the shape of tfidf_matrix which has around 8100 words
    term_document_matrix.shape
    # used cosine similarity method to compute the similarity between hotels
    cosine_similar = cosine_similarity(term_document_matrix, term_document_matrix)

    hotel_name_series = pd.Series(hotel_review_dataframe5.index,
                                  index=hotel_review_dataframe5['Hotel_Name']).drop_duplicates()

    # Method which takes the index of user hotel as input and calculate the similar hotels
    def recommend_cosine(title, cosine_sim=cosine_similar):

        idx = hotel_name_series[title]
        sim_scores = list(enumerate(cosine_sim[idx]))

        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Similarity scores of the 10 most similar hotels
        sim_scores = sim_scores[1:11]

        # Get the hotel indexes
        hotel_indices = [i[0] for i in sim_scores]

        # Return the top 10 most similar hotel across Europe
        return hotel_review_dataframe5['Hotel_Name'].iloc[hotel_indices]

    # user input hotel name 11 cadogan garden and get top 10 similar hotel based on user review
    sds = recommend_cosine(hotel_name)
    jsonList = sds.to_json(orient='values')

    return jsonList


if __name__ == "__main__":
    app.run()