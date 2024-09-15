import streamlit as st
import pandas as pd
import plotly.express as pl
import matplotlib.pyplot as plt
import json

# first find a average for global sales
columns_to_be_removed = ['NA_Sales','JP_Sales','Other_Sales']

st.title('Statistics For Games')

full_df = pd.read_csv('vgsales.csv')
st.sidebar.header('Filter The Game')
platform = st.sidebar.selectbox('Platform',['All'] + list(full_df['Platform'].unique()))
yeari = st.sidebar.selectbox('Year',['All'] + list(full_df['Year'].unique()))
new_genre = st.sidebar.selectbox('Genre',['All'] + list(full_df['Genre'].unique()))
new_publisher = st.sidebar.selectbox('Publisher',['All'] + list(full_df['Publisher'].unique()))
the_new_df = full_df.copy()
if platform != 'All':
    the_new_df = the_new_df[the_new_df['Platform'] == platform]
if yeari != 'All':
    the_new_df = the_new_df[the_new_df['Year'] == yeari]
if new_genre != 'All':
    the_new_df = the_new_df[the_new_df['Genre'] == new_genre]
if new_publisher != 'All':
    the_new_df = the_new_df[the_new_df['Publisher'] == new_publisher]


the_df = the_new_df.drop(columns=[col for col in columns_to_be_removed if col in full_df.columns])
total_games = the_df.shape[0]
global_sales = the_df['Global_Sales'].sum()
eu_sales = round(the_df['EU_Sales'].sum(),2)



col1,col2,col3 = st.columns(3)
col1.metric('Total Games',total_games)
col2.metric('EU Sales',eu_sales)
col3.metric('Global Sales',global_sales)
# top 10 ranked games
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")

st.subheader('Games Review')



col1,col2 = st.columns(2)


with col1:
    st.header('Top 10 Ranked Games')
    top_ranked = the_df['Name'].value_counts().head(10) # value counts takes the
    st.bar_chart(top_ranked)

with col2:
    st.header('Top 10 Games With The Most Sales')
    top_sales = the_df.groupby('Name')['Global_Sales'].sum().head(10)
    ordering = top_sales.sort_values(ascending=False)
    st.bar_chart(ordering)

# vertical padding
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")

st.subheader('Genres & Publishers')
colon,colona2 = st.columns(2)
colors_sequence = ['#07013d','#054752','#ffd9d0','#282b2b','#170062']
colors_sequence2 = ['#07013d','#054752']

with colon:
    take_most = the_df['Genre'].value_counts().head(5)
    take_most_df = take_most.reset_index()
    take_most_df.columns = ['Genre','Count']
    fig = pl.pie(take_most_df,names='Genre',values='Count',title='Top 5 Genres',color='Genre',color_discrete_sequence=colors_sequence)
    st.plotly_chart(fig)
    st.text("")

with colona2:
    the_df_instead = the_df['Publisher'].value_counts().head(2)
    the_df_instead_indexing = the_df_instead.reset_index() # converts series into data frame
    # and in the previous series in the_df_instead the publishers name was the index
    # so now reseting it the index of the series becomes an column in the data frame
    the_df_instead_indexing.columns = ['Publisher','Count']
    figura = pl.pie(the_df_instead_indexing,names='Publisher',values='Count',title='Top 2 Publishers',color='Publisher',color_discrete_sequence=colors_sequence2)
    st.plotly_chart(figura)

# find the neweest game
st.subheader('Top 5 Latest Games')
[kolona1] = st.columns(1)

with kolona1:
    newest_game = the_df.sort_values(by='Year', ascending=False)

    the_top_5 = newest_game.drop_duplicates(subset='Year').head(5)

    datat = {
        'Name':[name for name in the_top_5['Name']],
        'Year':[year for year in the_top_5['Year']]
    }

    into_data_frames = pd.DataFrame(datat)
    st.bar_chart(into_data_frames)

st.text(' ')
st.text(' ')
st.text(' ')
st.text(' ')
st.text(' ')


st.subheader('See Games Of The Genre You Want')
[coll2] = st.columns(1)
with coll2:
    filter_by_genre = st.selectbox('Genre',the_df['Genre'].unique())
    #display all the names
    get_all = the_df[the_df['Genre'] == filter_by_genre]
    st.write(get_all)

st.text(' ')
st.text(' ')
st.text(' ')
st.text(' ')
st.text(' ')

st.subheader('See The Platform')
[coll3] = st.columns(1)
with coll3:
    filter_by_platform = st.selectbox('Platform',the_df['Platform'].unique())
    get_data = the_df[the_df['Platform'] == filter_by_platform]
    st.write(get_data)


#
st.sidebar.header('Add A Game We Are Missing!')
with st.sidebar.form('Add Game'):
    game_name = st.text_input('Game Name')
    game_platform = st.text_input('Game Platform')
    game_genre = st.text_input('Genre')
    game_publisher = st.text_input('Publisher')
    game_year = st.number_input('Year',min_value=1975,max_value=2024,step=1)
    game_rank = st.slider('The Rank',min_value=the_df['Rank'].max(),max_value=the_df['Rank'].max() * 50,value=the_df['Rank'].max())
    european_sales = st.slider('Eu Sales',min_value=0.1,max_value=the_df['EU_Sales'].max(),value=0.1)
    global_sale = st.slider('Global Sales',min_value=0.1,max_value=the_df['Global_Sales'].max(),value=0.1)
    the_submit = st.form_submit_button('Add Game')


if the_submit:
    the_data_to_be_added = {
        'Rank':game_rank,
        'Name':game_name,
        'Platform':game_platform,
        'Year':game_year,
        'Genre':game_genre,
        'Publisher':game_publisher,
        'EU_Sales':european_sales,
        'Global_Sales':global_sale
    }

    names = list(the_df['Name'])
    if game_name not in names:
        the_df = pd.concat([pd.DataFrame(the_data_to_be_added,index=[0]),the_df],ignore_index=False)
        the_df.to_csv('vgsales.csv',index=False)

        st.sidebar.success('Added')
    else:
        st.sidebar.info('Game Alredy In DataSet')




st.sidebar.header('Save Your Favourite Game')

with st.sidebar.form('Fav Game'):
    game_name = st.text_input('Enter The Name')
    rank_game = st.number_input('Enter The Rank',step=1)
    the_submit = st.form_submit_button('Add')
def saving():
    if the_submit:
        if game_name in list(the_df['Name']) and rank_game in list(the_df['Rank']):
            with open('myFile.json', 'r+') as file:
                notIn = False
                the_data_set = the_df[the_df['Name'] == game_name]
                the_full_data = {
                    'Rank':str(the_data_set['Rank'].tolist()[0]),
                    'Name':str(the_data_set['Name'].tolist()[0]),
                    'Platform':str(the_data_set['Platform'].tolist()[0]),
                    'Year':str(the_data_set['Year'].tolist()[0]),
                    'Genre':str(the_data_set['Genre'].tolist()[0]),
                    'Publisher':str(the_data_set['Publisher'].tolist()[0]),
                    'EU_Sales':str(the_data_set['EU_Sales'].tolist()[0]),
                    'Global_Sales':str(the_data_set['Global_Sales'].tolist()[0])
                }
                reading = file.read()
                if not reading:
                    the_list = []
                    the_list.append(the_full_data)
                    into_json = json.dumps(the_list)
                    file.write(into_json)
                    st.sidebar.success('You Made It')
                else:
                    getting = list(json.loads(reading))
                    getting.append(the_full_data)
                    loading = list(json.loads(reading))
                    for game in loading:
                        st.write(game['Rank'].split(' '))
                        if str(int(rank_game)) == game['Rank'] and game_name == game['Name']:
                            notIn = True
                            break
                    if not notIn:
                        with open('myFile.json','w') as f:
                            f.write(json.dumps(getting))

                        st.sidebar.info('Good Second One')
                    else:
                        st.sidebar.info('Sorry Alredy Added')
        else:
            st.sidebar.info('We Dont Have That Game In Dataset')

saving()

if st.button('See Favourites'):
    the_column,the_second = st.columns([1,3])
    with the_second:
        st.header('Your Personal Games!j')
    with open('myFile.json') as file:
        list_with_games = []
        reading = json.loads(file.read())
        the_ranks = the_df['Rank']
        inside_game = False
        for game in reading:
            to_int = int(game['Rank'])
            get_name = game['Name']
            get_data = the_df[(the_df['Rank'] == to_int) & (the_df['Name'] == get_name)]
            ready_to_be_filtered = {
                'Rank':get_data['Rank'].tolist()[0],
                'Name':get_data['Name'].tolist()[0],
                'Platform':get_data['Platform'].tolist()[0],
                'Year':get_data['Year'].tolist()[0],
                'Genre':get_data['Genre'].tolist()[0],
                'Publisher':get_data['Publisher'].tolist()[0],
                'EU_Sales':get_data['EU_Sales'].tolist()[0],
                'Global_Sales':get_data['Global_Sales'].tolist()[0]
            }
            if len(list_with_games) > 0:
                for game in list_with_games:
                    if game['Rank'] == ready_to_be_filtered['Rank']:
                        inside_game = True
            if not inside_game:
                list_with_games.append(ready_to_be_filtered)


        into_df = pd.DataFrame(list_with_games)


    st.text(' ')
    st.text(' ')
    st.text(' ')
    st.text(' ')
    st.text(' ')


    kolona_1,kolona_2 = st.columns(2)
    with kolona_1:
        st.subheader('Top 3 Of Your Favourites Games(Globally)')
        filtering = into_df.groupby('Name')['Global_Sales'].sum().head(3)
        sorting = filtering.sort_values(ascending=False)
        st.bar_chart(sorting)
    with kolona_2:
        st.subheader('Top 3 Of Your Favourites Games(In Eu)')
        filtering = into_df.groupby('Name')['EU_Sales'].sum().head(3)
        sorting = filtering.sort_values(ascending=False)
        st.bar_chart(sorting)


    st.text(' ')
    st.text(' ')
    st.text(' ')
    st.text(' ')
    st.text(' ')


    kolona_1_publishers,kolona_2_genres = st.columns([1,1])

    with kolona_1_publishers:
        st.subheader('Publishers You Like The Most')
        filtering = into_df['Publisher'].value_counts().head(len(list_with_games)).reset_index()
        filtering.columns = ['Publisher','Count']
        the_pie = pl.pie(filtering,names='Publisher',title='Top Publishers',color_discrete_sequence=pl.colors.sequential.Viridis)
        st.plotly_chart(the_pie)


    with kolona_2_genres:
        st.subheader('Genres You Like The Most')
        filtering = into_df['Genre'].value_counts().head(len(list_with_games)).reset_index()
        filtering.columns = ['Genre','Publishers']
        the_pie = pl.pie(filtering,names='Genre',title='Top Genres',color_discrete_sequence=pl.colors.sequential.Plasma)
        st.plotly_chart(the_pie)

    [second_last] = st.columns(1)
    with second_last:
        st.subheader('All Your Favourite Games')
        st.write(into_df)























