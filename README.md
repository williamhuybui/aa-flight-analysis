# American Airline Flight Analysis

## Inspiration
Have you ever wonder :
How many people travel during COVID times, Christmas, or July 4th?
Where do people want to travel?
What does the flight traffic like during the early morning at the beginning of the school year each year?

My dashboard will answer it all.

## What it does
My project provides insights through 3 plots.
1) Date, hour, day of the month, month, year versus the total number of depart flight

2) Number of arrival flight from a given city to others city 

3) Total flight summary from 4 big city

## How I got the data set

The [dataset](https://github.com/AmericanAirlines/Flight-Engine) comes from American Airlines in the TAMUHack competition 202

I first ran the flight engine npm locally and get the JSON file. Then I use data processing techniques to convert JSON to a clean tabular form and save it as a CSV file. More detail can be found in the query_data.py

## Challenges I ran into

There is 3 major issue:
* **Dataset missing information:** This data has incorrect longitude. So I have to manually fix it

* **Dash components:** Having done a few dash projects before, I understand how much challenge it is to finish in one day.

* **Version conflict:** I am not too familiar with version control, and there are many library distribution conflicts I faced while deploying this dashboard.

## What I learned
* Preparation is so important. I learned and concluded that my next dashboard workflow should be: 

1) Data acquisition

2) Brainstorm about ideas and Data Exploratory (At least 2h)

3) Dashboard layout, UI/UX

4) Work on each component of the dashboard

5) Put things together

6) Test and deploy

This workflow would save me so much time and my final product will look better

## What's next
I will master my dashboard skill and learn about Dash bootstrap

## Get started
I uploaded the dashboard [here](https://aa-flight-analysis.herokuapp.com)

My code is also well documented if you want to visit them
