import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

day_df = pd.read_csv("day.csv")

datetime_columns = ["dteday"]
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)
 
for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo
    st.image("lovbike.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )


main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]


def create_daily_bike_users_df(df):
    daily_bike_users_df = df.resample(rule='D', on='dteday').agg({
        "total_casual": "sum"
    })
    daily_bike_users_df = daily_bike_users_df.reset_index()
    daily_bike_users_df.rename(columns={
        "total_registered": "registered"
    }, inplace=True)
    
    return daily_bike_users_df


st.header('Bike Sharing Dashboard :sparkles:')

st.subheader("Daily Bike-Sharing")
col1, col2, col3 = st.columns(3)
 
with col1:
    total_casual = main_df.casual.sum()
    st.metric("Total Casual", value=total_casual)
 
with col2:
    total_registered = main_df.registered.sum() 
    st.metric("Total Registered", value=total_registered)

with col3:
    total_cnt = main_df.cnt.sum()
    st.metric("Total Users bike-share", value=total_cnt)


st.subheader("Days with high and low numbers of bike share system user")

sort_sewa_df = day_df.groupby("weekday").cnt.max().sort_values(ascending=False).reset_index()
fig, ax = plt.subplots(figsize=(10, 5))
colors=["#D3D3D3", "#72BCD4", "#D3D3D3", "#D3D3D3","#D3D3D3", "#D3D3D3", "#FF5733"]
sns.barplot(x="weekday", y="cnt", data=sort_sewa_df, color="cyan", ax=ax, palette=colors)
ax.set_xlabel("A days", fontsize=15)
ax.set_ylabel("Number of Tenants (cnt)", fontsize=15)
ax.set_title("User Based Bike Sharing System by Days", fontsize=25)
ax.tick_params(axis="y", labelsize=15)
ax.tick_params(axis="x", labelsize=15)
ax.legend(loc='upper right')

st.pyplot(fig) 


st.subheader("The effect of temperature on the number of bike sharing system")

fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(x="temp", y="cnt", data=day_df, color="blue", ax=ax, hue="temp")
sns.regplot(x='temp', y='cnt', data=day_df, color="grey")
ax.set_title('The Relationship between Temperature and The Number of Bike Rentals', fontsize=20)
ax.set_xlabel("Temperature", fontsize=15)
ax.set_ylabel("Number of Tenants (cnt)", fontsize=15)

st.pyplot(fig)

st.caption('Copyright (c) Dicoding 2024')