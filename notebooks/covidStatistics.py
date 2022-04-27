#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from ipywidgets import interact

data = pd.read_csv("../data/covid-data.csv")

df = pd.DataFrame(data)

index_countries = df[((df['iso_code'].str.contains('OWID')))]
index_owid = df[((df['iso_code'].str.contains('OWID') == False))]


# In[3]:


country_df = pd.DataFrame(df.location)
country_df = country_df.rename(columns={'location': 'country'})
country_df['confirmed'] = df.total_cases
country_df['deaths'] = df.total_deaths
country_df['date'] = pd.to_datetime(df.date)
country_df.head()

country_df = country_df.drop(index_countries.index)

sorted_country_df = country_df.sort_values('confirmed', ascending=False).query("date == '2022-04-11'")
sorted_country_df


# In[4]:


fig = px.scatter(sorted_country_df.head(100), x='country', y='confirmed', size='confirmed', color='country',
                 hover_name='country', size_max=100, title="Confirmed cases by country")

fig.show()


# In[6]:


owid_df = pd.DataFrame(df.location)
owid_df = owid_df.rename(columns={'location': 'country'})
owid_df['confirmed'] = df.total_cases
owid_df['deaths'] = df.total_deaths
owid_df['date'] = pd.to_datetime(df.date)
owid_df.head()

owid_df = owid_df.drop(index_owid.index)

sorted_owid_df = owid_df.sort_values('confirmed', ascending=False).query("date == '2022-04-11'")
sorted_owid_df


# In[7]:


fig = px.scatter(sorted_owid_df, x='country', y='confirmed', size='confirmed', color='country', hover_name='country',
                 size_max=100, title="Confirmed cases by owid filter")

fig.show()


# In[8]:


confirmed_df = pd.DataFrame()

confirmed_df['country'] = df.location
confirmed_df['confirmed'] = df.total_cases
confirmed_df['deaths'] = df.total_deaths
confirmed_df['vaccinations'] = df.total_vaccinations
confirmed_df['date'] = df.date
confirmed_df.drop(index_countries.index)

confirmed_df.head()


# In[9]:


from plotly.offline import iplot


def plot_cases_for_country(country):
    fig = go.Figure()
    dfi = confirmed_df.query(f"country == '{country}'")
    fig.add_trace(
        go.Scatter(x=dfi.date, y=dfi.confirmed, name="Confirmed cases", mode='lines', connectgaps=True,
                   marker=dict(color="green")))
    fig.add_trace(
        go.Scatter(x=dfi.date, y=dfi.deaths, name="Confirmed deaths", mode='lines', connectgaps=True,
                   marker=dict(color="red")))

    fig.update_layout(title=f"Confirmed cases and deaths for {country}")

    iplot(fig)


plot_cases_for_country('Sweden')


# In[10]:


from plotly.subplots import make_subplots
def plot_compare_country_cases(country, country2):
    dfi = confirmed_df.query(f"country == '{country}'")
    dfi2 = confirmed_df.query(f"country == '{country2}'")

    fig = make_subplots(cols=2,rows=1)
    fig.add_trace(
        go.Scatter(x=dfi.date, y=dfi.confirmed, name=f"Confirmed cases for '{country}'", mode='lines', connectgaps=True,
                   marker=dict(color="blue")),col=1,row=1)
    fig.add_trace(
        go.Scatter(x=dfi.date, y=dfi.deaths, name=f"Confirmed deaths for '{country}'", mode='lines', connectgaps=True,
                   marker=dict(color="blue")),col=2,row=1)

    fig.add_trace(
        go.Scatter(x=dfi.date, y=dfi2.confirmed, name=f"Confirmed cases for '{country2}'", mode='lines',
                   connectgaps=True,
                   marker=dict(color="green")),col=1,row=1)
    fig.add_trace(
        go.Scatter(x=dfi.date, y=dfi2.deaths, name=f"Confirmed deaths for '{country2}'", mode='lines', connectgaps=True,
                   marker=dict(color="green")),col=2,row=1)

    fig.update_layout(title=f"Confirmed cases and deaths for {country} and {country2}")

    iplot(fig)


plot_compare_country_cases('France', 'Germany')
interact(plot_compare_country_cases,country='Finland',country2='Sweden')


# In[37]:


vaccinations_df = pd.DataFrame()

vaccinations_df['country'] = df.location
vaccinations_df['tests_per_case'] = df.tests_per_case
vaccinations_df['tests_positive_rate'] = df.positive_rate * df.tests_per_case
vaccinations_df['date'] = df.date
vaccinations_df.drop(index_countries.index)

vaccinations_df.head()


# In[44]:


def plot_test_for_country(country):
    dfi = vaccinations_df.query(f"country == '{country}'")
    fig = px.pie(dfi, values='tests_per_case', names='date')

    fig.show()


plot_test_for_country('Finland')

