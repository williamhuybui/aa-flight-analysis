# American Airline Flight Analysis

<img src="Picture/dashboard.jpg" alt="Italian Trulli">

## Inspiration
Have you ever wonder:

How many people travel during COVID, on the Christmas, July 4th, or New Year?

Where do people want to travel from your city?

What is the current level of crowdness at the airport?

The dashboard will answer all of these questions

## What it does
My project provides analytical insights through 3 plots.
1) Date, hour, day of the month, month, year versus the total number of depart flight

2) Number of arrival flight from a given city to others city 

3) Total flight summary from 4 big cities

## How I got the data set

The [dataset](https://github.com/AmericanAirlines/Flight-Engine) comes from American Airlines in the TAMUHack competition 202

I first ran the flight engine npm locally and get the JSON file. Then I use data processing techniques to convert JSON to a clean tabular form and save it as a CSV file. More detail can be found in the query_data.py

## Challenges I ran into

There is 3 major issue:
* **Dataset missing information:** This data has incorrect longitude. So I have to manually fix it. Also, this is just a mock dataset and does not capture trend.

* **Dash components:** Having done a few dash projects before, I understand how much challenge it is to finish the dashboard in one day.

* **Version conflict:** I was not too familiar with version control, and there are many library distribution conflicts I saw while deploying this dashboard.

## What I learned
* Preparation is so important. I learned and concluded that my next dashboard workflow should be: 

1) Data acquisition

2) Brainstorm about ideas and Data Exploratory (At least 25% of time)

3) Dashboard layout, UI/UX

4) Work on each component of the dashboard

5) Put things together

6) Test and deploy

This workflow would save me so much time and my final product will look better

## What's next
I will master my dashboard skill and learn more about Dash bootstrap. I also have interest in web development. 

## Get started
I uploaded the dashboard [here](https://aa-flight-analysis.herokuapp.com)

My code is also well documented if you want to visit them
