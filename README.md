Real-Time News Summarization and Sentiment Analysis Dashboard
1. Overview
 * This project will involve the design and implementation of a real-time news monitoring system that fetches current news from around the globe, summarizes each article using Natural Language Processing, analyzes the sentiment, and then displays the results on a live interactive dashboard.
* The system provides summarized information in concise form to the user, along with the     polarity of the sentiment-such as positive, negative, or neutral-to provide an overview of the trending news without needing to go through full articles. The dashboard supports dynamic topic filtering, real-time updating, and offers several forms of visual representation, such as sentiment distribution charts and source frequency graphs. It will be developed in Python using Hugging Face's NLP transformer models, sentiment classifiers, and Streamlit for UI.

2. Key Features

  1.Real-time news extraction from trusted News APIs
  2.Automatic text summarization using pretrained transformer models
  3.Sentiment classification for each summarized article
  4.Topic-based filtering (e.g., General, Sports, Business, Technology, Health, Entertainment, Science)
  5.Live dashboard that refreshes periodically
  6.Interactive charts to visualize sentiment trends and article distributions

  3. System Workflow

  The project consists of a three-stage processing pipeline:

   3.1 Data Acquisition

  News articles are retrieved in real-time from the NewsAPI by the system. The system collects article title, description, source name, publication date, and article URL. Retrieved articles will be temporarily stored in a raw dataset file in the JSON format.

   3.2 Text Preprocessing and Summarization

   The retrieved text will be sanitized to remove unwanted symbols, trailing spaces, and non-informative content. The summarization will be conducted by a generative transformer-based summarization model (Hugging Face: BART / T5) that will create succinct, readable summaries for each news article.

   3.3 Sentiment Analysis and Dashboard

  Sentiment classification will establish that the summarized text is positive, negative, or neutral. The processed results will be displayed at the front on a Streamlit dashboard with numerical insight, comparison charts, topic-based filtering options, as well as the news summary list.

  4. Dependencies Required:

   Python 3.10 or above
   Streamlit (for dashboard)
   Requests (for API communication)
   Transformers and Torch (for summarization and sentiment models)
   Pandas and JSON (for dataset handling)
   Matplotlib / Plotly (for charts)
   Langdetect (for filtering non-English content)
   python-dotenv (for secure API key handling)

   5. Setup Instructions 

   5.1 Creation of Project Environment

   A dedicated virtual environment should be created for isolating project dependencies. After creating the environment, install the necessary dependencies from the requirements.txt file.

   5.2 Configuration of API key

  The system will utilize the NewsAPI key to retrieve live news. The key should be stored securely using a file called .env in the project directory.This assures that the key will not be exposed in public repository files

  5.3 Project Structure
  Main components of the project include: 

  Script to fetch news and save raw dataset
  Script to process, summarize, and annotate news
  Streamlit application to display dashboard

 6. Instructions for Execution 

  The process of executing the project contains three stages: 

   Stage 1: Download Live News

   The first step is to execute the file which is responsible for communicating with the News API and saving the raw articles. This action will create the file titled raw_articles.json. 

   Stage 2: Process and Summarize News 

   Then, you should run the processing file that will: 

        Read the raw data 
        Clean or filter the data 
        Produce the summaries 
        Perform sentiment classifications  

   This action will create another data file titled processed.json. 

   Stage 3: Launch the Dashboard

   Finally, you will run the Streamlit application. The dashboard will load the data produced in Step 2, and it will allow for: 

       Viewing summaries 
       Filtering by topic 
       Viewing sentiment distributions 
       Viewing frequency statistics of sources

   The dashboard continues running to allow it to be refreshed at any time so that new data can be downloaded.
   
 7. Usage Guidelines

  The user selects the news topic of interest using a dropdown menu.
  The system fetches the latest articles related to the chosen topic.
  Summaries and sentiment results are displayed instantly.
  Sentiment charts visually indicate the emotional tone of aggregated news.

  The dashboard also shows source credibility trends and count insights.


