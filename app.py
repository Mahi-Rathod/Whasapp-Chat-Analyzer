import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue ()
    data = bytes_data.decode("utf-8")
    
    df = preprocessor.preprocess(data)
    # st.dataframe(df)
    
    #fetch users
    
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    
    user_list.insert(0, "Overall")
    selectedUser = st.sidebar.selectbox("Show Analysis WRT ", user_list)
    
    if st.sidebar.button("Show Analysis"): 
        numMessages, numWords, numberMediaMessages, numberLinksShared = helper.fetchStats(selectedUser, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.header("Total Messages")
            st.title(numMessages)
        
        with col2:
            st.header("Total Words")
            st.title(numWords)
            
        with col3:
            st.header("Media Shared")
            st.title(numberMediaMessages)
        
        with col4:
            st.header("Links Shared")
            st.title(numberLinksShared)
            
        #TimeLine
        st.title("Monthly TimeLine")
        timeline = helper.monthlyTimeLine(selectedUser,df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color= "red")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
         
        #Daily TimeLine
        st.title("Daily TimeLine")
        dailyTimeLineDf = helper.dailyTimeLine(selectedUser, df)
        fig, ax = plt.subplots()
        ax.plot(dailyTimeLineDf['forDate'], dailyTimeLineDf["message"], color = 'green')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)
         
        #Activity Map
        st.title("Activity Map")
        col1, col2 = st.columns(2)
        with col1:
            st.header("Most Busy Day")
            busyDay = helper.weekActivityMap(selectedUser, df)
            fig, ax = plt.subplots()
            ax.bar(busyDay.index, busyDay.values, color = "purple")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
            
        with col2:
            st.header("Most Busy Month")
            busyMonth = helper.monthActivityMap(selectedUser, df)
            fig, ax = plt.subplots()
            ax.bar(busyMonth.index, busyMonth.values, color = "orange")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        
        st.title("Weekly Activity Map")
        heatMap = helper.activityHeatMap(selectedUser, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(heatMap)
        st.pyplot(fig)
        
        
        # Most Active Users
        if selectedUser == "Overall":
            st.title('Most Active Users')
            x, newDf = helper.mostBusyUsers(df)
            fig, ax = plt.subplots()
            
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color = ("#E63946", "#EDAE49", "#3376BD", "#00798C","#52489C"))
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            
            with col2:
                st.dataframe(newDf)
        
        #wordCloud
        st.title("World Cloud")
        df_wc = helper.createWorldCloud(selectedUser, df)
        fig, ax = plt.subplots()
        plt.imshow(df_wc)
        st.pyplot(fig)
        
        #most common words  
        mostCommonWordsDf = helper.mostCommonWords(selectedUser, df)
        
        fig, ax = plt.subplots()
        ax.barh(mostCommonWordsDf[0], mostCommonWordsDf[1])
        
        st.title("Most Common Words")
        st.pyplot(fig)
        
        #Emoji Analysis
        
        analysedEmojiDf = helper.emojiAnalysis(selectedUser, df)
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(analysedEmojiDf)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(analysedEmojiDf[1].head(), labels = analysedEmojiDf[0].head(), autopct="%0.2f")
            plt.rcParams['font.family'] = 'Segoe UI Emoji'
            st.pyplot(fig)
            
        
        
        
        
    
