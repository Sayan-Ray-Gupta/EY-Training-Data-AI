from transformers import pipeline

# initialize the classifier
classifier = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')

# Classifying the sentiment
user_input = input("Enter a sentence: ")
result = classifier(user_input)
print(f"The result is: ", result[0]['label'])