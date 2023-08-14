import spacy
from textblob import TextBlob

nlp = spacy.load('en_core_web_md') 

# POS =['Epic', 'Happy', 'Hopeful', 'Laid', 'Busy', 'Frantic', 'Romantic', 'Funny', 'Glamorous', 'Mysterious', 
#     'Elegant', 'Dreamy', 'Euphoric', 'Ponderous', 'Peaceful', 'Restless', 'Running', 'Sexy', 'Smooth', 'Suspense']
# NEG=['Angry', 'Sentimental', 'Weird', 'Dark', 'Heavy', 'Sad', 'Scary','Fear']

POS = [
    'Happy',
    'Relaxed',
    'Inspired',
    'Romantix'
]

NEG = [
    'Sad',
    'Stressed',
    'Frustrated'
]

def assign_categories(user_input):
    blob = TextBlob(user_input)
    user_input_nlp = nlp(user_input)
    if blob.sentiment.polarity<0:
        similarities = [(category, user_input_nlp.similarity(nlp(category))) for category in NEG]
    else:
        similarities = [(category, user_input_nlp.similarity(nlp(category))) for category in POS]
    similarities.sort(key=lambda x: x[1], reverse=True)

    return blob.sentiment.polarity,similarities[:2]


# MOODS = ['Epic', 'Happy', 'Hopeful', 'Laid', 'Angry', 'Sentimental', 'Busy','Frantic', 'Romantic', 'Funny','Weird', 
#  'Dark', 'Glamorous', 'Mysterious', 'Elegant', 'Dreamy', 'Euphoric', 'Fear', 'Heavy','Ponderous',
#    'Peaceful', 'Restless', 'Running', 'Sad', 'Scary', 'Sexy', 'Smooth',"Suspense"]
# THEME = ['Corporate', 'Photography', 'Motivational', 'Inspiring', 'Cinematic', 'Comedy', 
#  'Cooking', 'Fashion', 'Beauty', 'Nature', 'Sports', 'Action', 'Technology', 
#  'Tutorials', 'Travel', 'Workout', 'Wellness', 'Gaming', 'Wedding', 'Romance', 
#  'Horror', 'Thriller', 'Trailers', 'Broadcasting', 'Holiday', 'Season', 
#  'Drama', 'Documentary', 'Vlogs']