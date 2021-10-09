import pandas as pd
def preprocess(athletes,noc):
    df=athletes.merge(noc,on="NOC",how='left')
    df=df[df['Season']=='Summer']
    df.drop_duplicates(inplace=True)
    df1=df.drop_duplicates(subset=['Team','NOC','Year','Season','City','Sport','Event','Medal'])
    gold=df1[df1['Medal'] == 'Gold']['NOC'].value_counts().reset_index().rename(columns={'index':'Country','NOC':'Gold_medal'})
    silver=df1[df1['Medal'] == 'Silver']['NOC'].value_counts().reset_index().rename(columns={'index':'Country','NOC':'Silver_medal'})
    bronze=df1[df1['Medal'] == 'Bronze']['NOC'].value_counts().reset_index().rename(columns={'index':'Country','NOC':'Bronze_medal'})
    medal=gold.merge(silver,on='Country',how='left')
    medal_tally=medal.merge(bronze,on='Country',how='left')
    medal_tally.fillna(0,inplace=True)
    medal_tally['Silver_medal']=medal_tally['Silver_medal'].astype(int)
    medal_tally['Bronze_medal']=medal_tally['Bronze_medal'].astype(int)
    medal_tally['Total']=medal_tally['Gold_medal']+medal_tally['Silver_medal']+medal_tally['Bronze_medal']
    return medal_tally,df
    
def top_performers(athletes,noc):
    df=athletes.merge(noc,on="NOC",how='left')
    df=df[df['Season']=='Summer']
    df.drop_duplicates(inplace=True)
    gold=df[df['Medal'] == 'Gold'][['Name','Sport','region']].value_counts().reset_index().rename(columns={0:'Gold_medal'})
    silver=df[df['Medal'] == 'Silver']['Name'].value_counts().reset_index().rename(columns= {'index':'Name','Name':'Silver_medal'})
    bronze=df[df['Medal'] == 'Bronze']['Name'].value_counts().reset_index().rename(columns= {'index':'Name','Name':'Bronze_medal'})
    data=gold.merge(silver,on='Name')
    athletes_medal=data.merge(bronze,on='Name')
    athletes_medal['Total'] = athletes_medal['Gold_medal']+athletes_medal['Silver_medal']+athletes_medal['Bronze_medal']
    return athletes_medal

def data_over_time(df,col):

    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('index')
    nations_over_time.rename(columns={'index': 'Edition', 'Year': col}, inplace=True)
    return nations_over_time

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final