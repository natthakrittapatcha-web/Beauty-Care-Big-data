# analyze_reviews_from_json.py

import pandas as pd
import glob
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

def clean_text(text):
    return BeautifulSoup(str(text), "html.parser").get_text().strip()

def load_all_json(folder):
    all_files = glob.glob(os.path.join(folder, "*.json"))
    dfs = [pd.read_json(file) for file in all_files]
    return pd.concat(dfs, ignore_index=True)

def generate_wordclouds(df, output_dir):
    df['clean_text'] = df['text'].apply(clean_text)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    summary = []

    for cat in df['new_main_category'].dropna().unique():
        for tag in df['tag'].dropna().unique():
            for sent in df['sentiment'].dropna().unique():
                subset = df[
                    (df['new_main_category'] == cat) &
                    (df['tag'] == tag) &
                    (df['sentiment'] == sent)
                ]

                if not subset.empty:
                    text = ' '.join(subset['clean_text'].tolist())

                    wordcloud = WordCloud(
                        width=800, height=400,
                        background_color='white',
                        stopwords='english'
                    ).generate(text)

                    filename = f"{cat}_{tag}_{sent}.png".replace(" ", "_")
                    path = os.path.join(output_dir, filename)
                    wordcloud.to_file(path)

                    summary.append({
                        'category': cat,
                        'tag': tag,
                        'sentiment': sent,
                        'review_count': len(subset),
                        'wordcloud_file': filename
                    })

    return pd.DataFrame(summary)

if _name_ == "_main_":
    input_folder = "data/merged_reviews.json"
    output_folder = "data/wordcloud_output"

    print("Loading .json files...")
    df = load_all_json(input_folder)

    print("Generating wordclouds...")
    summary_df = generate_wordclouds(df, output_folder)

    summary_df.to_csv(os.path.join(output_folder, "summary.csv"), index=False)
    print("Done. Wordclouds and summary.csv are saved in:", output_folder)