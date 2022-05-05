import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random as rd


def state_query():
    # State Query
    st.subheader("State:")
    state = st.selectbox("Select the State: ",
                         ('AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN',
                          'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH',
                          'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT',
                          'VT', 'VA', 'WA', 'WV', 'WI', 'WY')
                         )
    return state


def readdata():
    df = pd.read_csv('Fast_Food_Restaurants_8000_sample (1).csv',
                     usecols=['name', 'address', 'categories', 'city', 'country', 'latitude', 'longitude', 'postalCode', 'province', 'websites'])
    # read the CSV file
    df.drop_duplicates(inplace=True)
    # remove duplicate data
    df = pd.DataFrame(df, columns=['name', 'address', 'categories', 'city', 'country', 'latitude', 'longitude', 'postalCode', 'province', 'websites'])
    return df


def local_map(sample):

    indexlist = sample.index.tolist()
    generator = rd.choice(indexlist)

    if st.button("Generate a Restaurant"):
        st.header(sample['name'][generator])
        st.write(sample['address'][generator], ",", sample['city'][generator], sample['postalCode'][generator])
        lon = sample['longitude'][generator]
        lat = sample['latitude'][generator]
        cord_data = pd.DataFrame({'longitude': [lon], 'latitude': [lat]})
        st.map(cord_data)


def state_freq_bar(sample, selection):
    st.title("Restaurant Count in the Area")
    fig, axs = plt.subplots()
    st.subheader(f"by {selection}")
    rest_freq = sample['name'].value_counts()
    x = sample['name'].unique()
    axs.bar(x, rest_freq, width=.25)
    plt.xticks(rotation=90)
    st.pyplot(fig)


def pie_chart(data, state):
    st.title("Distribution of Fast food by State")
    pie_dist = data[data['province'] == state]
    rest_count = pie_dist['name'].value_counts()
    fig, axs = plt.subplots()
    rest_count_list = pie_dist['name'].unique()
    axs.pie(rest_count, labels=rest_count_list)
    axs.set_title("Distribution of Restaurants by State")
    axs.legend(loc='upper right')
    st.pyplot(fig)
    st.write(rest_count)


def us_freq_bar(data):
    st.title("Restaurant Frequency in each State")
    x = data['name'].unique()
    option = st.selectbox(
     'Which Restaurant', x)
    fig, axs = plt.subplots()
    st.header(f"{option} Frequency by State")

    rest_freq_data = data[data['name'] == option]
    rest_freq = rest_freq_data['province'].value_counts()
    x = rest_freq_data['province'].unique()
    axs.bar(x, rest_freq, width=.25)
    plt.xticks(fontsize=5, rotation=45)
    st.pyplot(fig)
    st.write(rest_freq)


def main():
    st.image('./image.jpeg')
    st.title("Don't know where to eat?")
    st.header("We're here to help!")
    data = readdata()
    state = state_query()
    # input a zip code box
    zipcode = st.text_input('Enter a Zip-Code', '35215')
    st.write(f"We are currently looking at {state} in {zipcode}")
    selection = st.radio("How do you want to view the frequency chart by?", ('State', 'ZipCode'))
    if selection == 'State':
        sample = data[data['province'] == state]
    else:
        sample = data[data['postalCode'] == zipcode]
    img_select = st.sidebar.selectbox("Choose a Graph:", ["Map", "Restaurants in each State", "Pie Chart", "State Frequency of each Restaurant"])
    if img_select == "Map":
        local_map(sample)
    elif img_select == "Restaurants in each State":
        state_freq_bar(sample, selection)
    elif img_select == "Pie Chart":
        pie_chart(data, state)
    else:
        us_freq_bar(data)


main()
