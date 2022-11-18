import pandas as pd

# For accessing websites
import requests

# For reading website
from bs4 import BeautifulSoup

# Using Vader for nlp and sentiment analysis
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# For Viewing Dataframe
from IPython.display import display



# *** ticker: stock symbol -> TSLA or GOOG or VOO


class Sentiment_Analysis:

    def __init__ (self):
        # Set up source website
        source = "https://marketwatch.com/investing/technology"
        print("Initializing source reader from: " + source)
        self.page = requests.get(source)
        self.soup = BeautifulSoup(self.page.content, "html.parser")
        
        # the class will vary based on the website
        self.article_contents = self.soup.find_all("div", class_="article__content")


    def populate_headlines(self):
        print("Reading Headlines")

        # Array Holding headlines and corresponding tickers
        self.headlines = []

        for article in self.article_contents:
            # Get the headline
            try:
                ticker = article.find("span", class_="ticker__symbol").text.strip()
            except:
                ticker = None
            
            # Get the corresponding ticker
            try:
                headline = article.find("a", class_="link").text.strip()
            except:
                headline = None

            # Remove or replace invalid tickers
            ticker = self.process_tickers(ticker)
            
            # If the headline and ticker exisit
            if ticker and headline:
                self.headlines.append([headline, ticker])
            
            
        print(self.headlines)
        columns = ["headline", "US_ticker"]
        self.headlines_df = pd.DataFrame(self.headlines, columns=columns)


    def process_tickers(self, ticker):
        replacements = {
            'SPX': 'SPY',
            'NG00' : 'UNG', 
            "BTCUSD" : None,
            "GCZ21": None,
            "HK:3333" : None,
            "DX:DAX" : None,
            "XE:VOW" : None,
            "UK:AZN" : None,
            "GBPUSD" : None,
            "CA:WEED" : None,
            "UK:UKX" : None,
            "CA:ACB" : None,
            "CA:ACB" : None,
            "CA:CL" : None,
            "BX:TMUBMUSD10Y" : None
        }
        if ticker in replacements:
            return replacements[ticker]
        else:
            return ticker
        
    
    def run_sentiment_analysis(self):
        self.vader = SentimentIntensityAnalyzer()
        self.scores = []
        for headline in self.headlines_df.loc[:,"headline"]:
            score = self.vader.polarity_scores(headline).get("compound")
            self.scores.append(score)
        self.headlines_df.loc[:,"score"] = self.scores
    

    def get_analysis_data(self):
        return self.headlines_df
        

#Testing
'''
if __name__ == "__main__":
    sa = Sentiment_Analysis()
    sa.populate_headlines()
    sa.run_sentiment_analysis()
    
    display(sa.get_analysis_data())
'''