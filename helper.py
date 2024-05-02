from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

def fetchStats(selectedUser, df):    
    if selectedUser != 'Overall':
        df = df[df['user'] == selectedUser]
                 
    # fetch the number of messages
    numMessages = df.shape[0]
    
    # fetch the total number of words
    words = [ ]
    for message in df ['message']:
        words.extend(message.split())
        
        
    # fetch number of media messages
    numberMediaMessages = df[df['message'] == '<Media omitted>\n'].shape[0]
    
    # fetch number of links shared
    extractor = URLExtract()
    links = []

    for message in df['message']:
        links.extend(extractor.find_urls(message))
    
    return numMessages, len (words) , numberMediaMessages, len(links)

def mostBusyUsers(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'count':'percent(%)'})
    return x, df


def createWorldCloud(selectedUser, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selectedUser != 'Overall':
        df = df[df['user'] == selectedUser]
    
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'This message was edited\n']
    temp = temp[temp['message'] != 'This message was deleted\n']
        
    def removeStopWords(message):
        words = []
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
        return " ".join(words)
            
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp["message"].apply(removeStopWords)
    df_wc = wc.generate(temp['message'].str.cat(sep= " "))
    
    return df_wc

def mostCommonWords(selectedUser, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selectedUser != 'Overall':
        df = df[df['user'] == selectedUser]
    
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'This message was edited\n']
    temp = temp[temp['message'] != 'This message was deleted\n']
    
    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    
    mostCommonWordsDf = pd.DataFrame(Counter(words).most_common(20))
    
    return mostCommonWordsDf

def emojiAnalysis(selectedUser, df):
    if selectedUser != 'Overall':
        df = df[df['user'] == selectedUser]
        
    emojis = []
    for message in df['message']:
        em = emoji.emoji_list(message)
        if(em):
            emojis.append(em[0]['emoji'])
            
    analysedEmojiDf = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return analysedEmojiDf
    
def monthlyTimeLine(selectedUser, df):
    if selectedUser != 'Overall':
        df = df[df['user'] == selectedUser]
        
    timeLine = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeLine.shape[0]):
        time.append(timeLine['month'][i] + "-" + str(timeLine['year'][i]))
    
    timeLine["time"] = time
    
    return timeLine

def dailyTimeLine(selectedUser, df):
    if selectedUser != 'Overall':
        df = df[df['user'] == selectedUser]
        
    dailyTimeLineDf = df.groupby("forDate").count()["message"].reset_index()
    
    return dailyTimeLineDf

def weekActivityMap(selectedUser, df):
    if selectedUser != 'Overall':
        df = df[df['user'] == selectedUser]
        
    return df["dayName"].value_counts()

def monthActivityMap(selectedUser, df):
    if selectedUser != 'Overall':
        df = df[df['user'] == selectedUser]
        
    return df["month"].value_counts()

def activityHeatMap(selectedUser, df):
    if selectedUser != 'Overall':
        df = df[df['user'] == selectedUser]
        
    activityHeatMapPivot = df.pivot_table(index='dayName', columns='period', values='message', aggfunc = 'count').fillna(0)
    
    return activityHeatMapPivot
    