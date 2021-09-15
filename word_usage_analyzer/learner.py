import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import LinearSVC
from spacy import displacy

from _spacy import spacify

example_text = """
In den letzten Jahren entstand der florierende Handel, an dem sich sogar asiatische Restaurants beteiligen, die hier an Sommerwochenenden informelle Außenstellen betreiben. 
Andere KöchInnen reisen im Sommer eigens mit einem Touristenvisum aus Thailand an. 
Und: Zu den ThailänderInnen sind inzwischen AnbieterInnen aus Korea, Vietnam, den Philippinen, Kambodscha, Laos, Brasilien und Japan gestoßen.
"""

doc = spacify(example_text)

print(doc)

# # Read in data
# data = pd.read_csv('clean_data.csv')
# texts = data['text'].astype(str)
# y = data['is_offensive']
#
# # Vectorize the text
# vectorizer = CountVectorizer(stop_words='english', min_df=0.0001)
# X = vectorizer.fit_transform(texts)
#
# # Train the model
# model = LinearSVC(class_weight="balanced", dual=False, tol=1e-2, max_iter=1e5)
# cclf = CalibratedClassifierCV(base_estimator=model)
# cclf.fit(X, y)
#
# # Save the model
# joblib.dump(vectorizer, 'vectorizer.joblib')
# joblib.dump(cclf, 'model.joblib')