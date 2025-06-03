import google.generativeai as genai

genai.configure(api_key="AIzaSyD-58W-1EKXszcDKe7UlB5ON_Vwe3eyzWI")

for model in genai.list_models():
    print(model.name)