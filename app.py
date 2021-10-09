import streamlit as st 
import pandas as pd
import functions
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff


st.sidebar.title('Olympic Analysis')
st.sidebar.image('image.jpg')

user_menu=st.sidebar.selectbox('Select an Option',('Medal Tally','Country-wise Analysis','Athlete-wise Analysis','Overall-Analysis'))

athletes=pd.read_csv('athlete_events.csv')
noc=pd.read_csv('noc_regions.csv')

medal_tally,df=functions.preprocess(athletes,noc)

if user_menu == 'Medal Tally':
    st.title('Overall Medal Tally')
    athletes=pd.read_csv('athlete_events.csv')
    noc=pd.read_csv('noc_regions.csv')
    medal_tally,df=functions.preprocess(athletes,noc)
    st.table(medal_tally)

if user_menu == 'Overall-Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Top Stats')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)
    
    st.title('Number of Palyers Particpated from different Countries')
    athletes_number=df['NOC'].value_counts()[:20]
    fig=px.bar(athletes_number,
            orientation='h',
            labels=dict(x="Persons", y="Countries")
            )
    fig.update_layout(
    xaxis_title="Count Of Paticipants",
    yaxis_title="Countries",
    template = 'simple_white',
    # update chart aesthetics
    title=dict(font=dict(family='Rockwell', size=20))
    )
    st.plotly_chart(fig)

    # plot
    st.title('Medal Scored by Different Countries')
    top_n = 20

    # filter data
    fig5_data = medal_tally[:top_n].sort_values(by='Total', ascending=True)

    # plot
    fig5 = go.Figure(
        data = [
            # data for gold medals 
            go.Bar(
                name='Gold', 
                y=fig5_data['Country'], 
                x=fig5_data['Gold_medal'],
                orientation='h', 
                marker=dict(color='gold', line=dict(color='black', width=2))
            ),
            # data for silver medals 
            go.Bar(
                name='Silver', 
                y=fig5_data['Country'], 
                x=fig5_data['Silver_medal'],
                orientation='h', 
                marker=dict(color='silver', line=dict(color='black', width=2))
            ),
            # data for bronze medals 
            go.Bar(
                name='Bronze', 
                y=fig5_data['Country'], 
                x=fig5_data['Bronze_medal'],
                orientation='h', 
                marker=dict(color='chocolate', line=dict(color='black', width=2))
            )
        ]
    )
    # update chart aesthetics
    fig5.update_layout(
        barmode='stack',
        margin = dict(pad=5),
        title = dict(
            text=f'Medal distribution of Top {top_n} countries ranked',
            font=dict(family='Rockwell', size=20)
        ),
        font = dict(family='Verdana', size=12),
        height = 800, 
        width = 750, 
        template = 'simple_white', 
        legend = dict(title='Medal'),
        xaxis = dict(range=(0, 2000))
    )
    st.plotly_chart(fig5)

    st.title('Number of Athletes (country wise) competing in different sports')
    fig=px.treemap(
    data_frame = df, 
    path = ['Sport', 'NOC'],
    height = 700)
    st.plotly_chart(fig)

    st.title('Top Performing Athletes')
    athletes=pd.read_csv('athlete_events.csv')
    noc=pd.read_csv('noc_regions.csv')
    data=functions.top_performers(athletes,noc)
    st.table(data.head(20))

    nations_over_time = functions.data_over_time(df,'region')
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time = functions.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.title("Events over the years")
    st.plotly_chart(fig)

    athlete_over_time = functions.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="Name")
    st.title("Athletes over the years")
    st.plotly_chart(fig)

if user_menu == 'Country-wise Analysis':

        st.sidebar.title('Country-wise Analysis')

        country_list = df['region'].dropna().unique().tolist()
        country_list.sort()

        selected_country = st.sidebar.selectbox('Select a Country',country_list)

        country_df = functions.yearwise_medal_tally(df,selected_country)
        fig = px.line(country_df, x="Year", y="Medal")
        st.title(selected_country + " Medal Tally over the years")
        st.plotly_chart(fig)

        st.title(selected_country + " excels in the following sports")
        pt = functions.country_event_heatmap(df,selected_country)
        fig, ax = plt.subplots(figsize=(20, 20))
        ax = sns.heatmap(pt,annot=True)
        st.pyplot(fig)

        st.title("Top 10 athletes of " + selected_country)
        top10_df = functions.most_successful_countrywise(df,selected_country)
        st.table(top10_df)

if user_menu == 'Athlete-wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = functions.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(temp_df['Weight'],temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = functions.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)






    