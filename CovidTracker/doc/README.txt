COVID Vaccine Data Tracker
Authors: Roopa Srinivas, Sophie Lin, Nodoka Shibasaki
Revision: 05/23/2021

Introduction: 

Our project is a COVID vaccination tracking map. It utilizes an interactive map that displays statistics about the COVID vaccine in various states in the United States. Our program reads data from the CDC website and constantly updates the statistics and other information. Some examples of these statistics are whether the number of COVID cases in that state has increased or decreased from the previous day to the current day (and by how much), the number of COVID vaccines administered in that state, the percent of vaccines given from each company, and just some basic facts about each company’s vaccine. The user will be able to select a state or region in the United States, then our program will read live data from the CDC website, and display it to the user in a presentable way. There is also a page with more information about the vaccines and links to CDC websites to allow the user to research about it themselves. 
Our program is meant to spread information about the COVID vaccines and it is meant to be used by anybody who wants to learn more about the actual numbers and information about the vaccine. Since a lot of misinformation is spreading around on the internet about COVID, this program will compile information and statistics from multiple government official sources to make sure the information is accurate.
About 1 in 4 people living in the United States don’t believe in the COVID vaccine and in wearing masks. Because these people believe in neither receiving the COVID vaccine nor wearing masks and following proper COVID guidelines, they spend time with their friends who also might not follow these guidelines. This causes more and more people to get sick with the virus causing herd immunity to be put at risk. At least 70-80% of people have to gain immunity, or else herd immunity will be very difficult to obtain within the country. We hope this project sheds some light on this enormous issue and keeps people informed about the vaccine and encourages them to get it as well.

Instructions:

When the user runs the COVID Vaccine Data Tracker, the main menu appears on the screen. From there, the user can click buttons to see the instructions, map, or more information about the vaccines.  On the map page, the user will need to click on the drop-down menu on the top right to go to different pages such as facts about vaccines, country-wide statistics, and facts about different states. All facts and statistics will be retrieved from the CDC website. If a user goes to a state page, the user will see the name of the state on top, followed by a graph-based on CDC statistics, percentages, and number of vaccinated people in the state. The user will need to select the “back” button to go back to the home page and the “quit” button to quit the program. To zoom in and out, the user will need to click on the up and down arrows. 

Features List (THE ONLY SECTION THAT CANNOT CHANGE LATER):
Must-have Features:
Something that allows us to read data live from a website
The information should be updated consistently and frequently from the website.
Facts about the vaccines
The page will include chemicals of each vaccination and their success rate and eligibility (12 and above are only allowed to get Pfizer vaccines).
Information for individual states 
Find a way to bring the user to individual states with information. 
Each state will include facts and statistics on the state.
Takes the user to another page with statistics about the single state
The statistics page will include different types of information like the percentage of vaccines out of the whole country that has been given, the actual number of vaccines given, and the number of vaccines.
 Country-wide statistics
The project will include the total number of vaccines administered, the total number of vaccines distributed, breakdown of vaccine companies’ vaccinations (percentage-wise), and more.

Want-to-have Features:
 Retrieve graphs and statistics from CDC data sets
We would use buttons for the particular forms of statistics and it would take you to another page with the current data and graphs.
 Mouse interactions
We would allow the user to hover over a certain state and it will show a brief version of the statistics and the user can also click on the state itself, which would bring them to another page that has more detailed information. This would require us (group members) to calculate the actual coordinates of each state (which would be irregularly shaped).
 An interactive map has at least 4 different options
Our map would have statistics state-wise and also region-wise (West, Southwest, Midwest, Northeast, and Southeast). Both these maps would include information about whether the number of cases has increased or decreased since the previous day, the percentage of vaccines that have been administered, and which type of vaccine (which company) is the most “popular” in that particular state/region.
Vaccination sites
We would create another map that would allow the user to view all the vaccination sites in the state selected.
We would show statistics based on the number of people who have received their first dose of the vaccine vs. the second dose of the vaccine vs. people who haven’t received the vaccine at all.
A larger map
We would like to include the whole of North America in our map if possible (not just the United States)
Color each state based on a percentage of vaccinated people in that state
We would color-code each state on a scale of light-green to dark-green based on the percentage of vaccinated people in that state
Interactive key
The user would be able to press certain buttons to change the information displayed on the map. The user could change the color of the map, or view statistics from previous days, weeks, or months.
Statistics based on each month
The user would be able to choose a certain month within the duration of the vaccines being available until the present and then they would be able to view the statistics of the vaccines given during that month.

Stretch Features:
 Use a larger map (world map) and include statistics for all the countries.
For countries besides North America, statistics only for the country as a whole and not for every state.
 On the drop-down menu, including a new page called “COVID rules”
What places are open?
Restaurants, arcades, amusement parks, etc.
What are the mask and social distancing requirements?
The rule would be the national wide rule.
If there are any exceptions amongst states, those will be stated as an exception.
Publish it into a website
We would build a website in HTML and CSS and “publish” our project there. We would integrate our map and all the information included in our project onto a website.

Class List:
Frame- the frame of the State and Map class 
Country - the interactive country map
State - each state with their information (50 objects for this)
Stats - fetches data from website
StatesGraphics - organizes the data into graphs
DrawingSurface-draws the main page and transitions between pages, also detects user interactions
Main - main class to call the drawing surface
MoreInfo - displays information about vaccinations, links to CDC webpages for more specific info about each vaccine

Credits:

Sophie
DrawingSurface class
Frame class
Transitions between all pages 
Buttons and user interaction- open dropdown button, back button, map button, more information button, instructions button
Instructions page on how to use the program
Designed graphics and layout of pages
Main menu graphics
Edited presentation video

Roopa
Get and format state and country map images
State class
Country class
MoreInfo class
Frame class
Main class
DrawingSurface class
Made dropdown

Nodoka
WriteInfo method in the country class
StatesGraphics and Stats methods
Find the information and statistics
Design and code the page
The reader of the retrieved data
Create and statistics and graphs
Calculating prediction 
Hovering 
links the website information
link the information so it consistently updates
Get the data to be saved

We all led part of the project, but also helped each other when needed.
Sources:
Research:
https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/index.html
https://covid.cdc.gov/covid-data-tracker/#datatracker-home
https://covid.cdc.gov/covid-data-tracker/#testing_testsper100k30day
Vaccines by states- https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/us_state_vaccinations.csv
Cases by state- https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv
Vaccine data of United States- https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/country_data/United%20States.csv
Cases of country- https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv
learning more about covid-19- https://www.youtube.com/watch?v=FVIGhz3uwuQ

Coding Help:
Linking buttons to a webpage- https://stackoverflow.com/questions/10967451/open-a-link-in-browser-with-java-button
Save graph to image- https://processing.org/reference/save_.html
Write an image to a file- https://examples.javacodegeeks.com/core-java/io/java-imageio-write-image-to-file/
Image syntax- https://docs.oracle.com/javase/8/docs/api/java/awt/image/BufferedImage.html
Working with the TreeMap- https://stackabuse.com/java-how-to-get-keys-and-values-from-a-map/
Timer task java- https://docs.oracle.com/javase/7/docs/api/java/util/TimerTask.html

Images:
Map images- https://suncatcherstudio.com/patterns/us-states/

Outside Help:
Mr. Shelby
Roopa’s brother (Kishore)
Roopa’s parents
Stack Overflow
Processing website
