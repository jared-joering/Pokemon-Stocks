### About
I'm currently developing a project to make sense of the nonsensical: a trading card market.  I've long been a fan of Pokémon, stretching back to my days as a kid rewatching the same VHS a hundred times.  When COVID hit, I jumped back into the hobby of collecting cards when I found a ton of them in my closet and ever since then, I've been trying to 'collect 'em all'.

Unfortunately, the market has been incredibly volatile as most have lately.  Scalper and resellers are prolifically involved with manipulation and it has just been a hassle to find cards, much less a deal.  So, I thought about how I could help myself and my friends.  Enter this project, where I aim to catalog some 15,000+ cards by logging some specifics into a SQL database through an API and then scraping price points gathered from multiple sources for the past 3 years into a separate, more dynamic table that I can add into with a Python script at weekly, monthly, and semi-annual intervals.  At least, those are my aims.

With all that data in-hand, I plan on conducting EDA with Python, pandas, seaborn, matplotlib, and more and we'll see where we go from there.  I also plan on using regression analysis and deep learning to try to see if I can map future-trends in the market and capitalize when need be.  All of this and then some is listed below.  This project has barely started 'walking', so a lot of these may never be realized.


##### Project Goals:
	- Make a database ('Pokemon MEGA Bank') that is
		* The database will house 15,000 individual rows (cards) immediately, and will grow as new card sets release.
		* These will be entered in via a script that calls an API which adds to the list every month or so.
			i. The API will have the immediate prices, but I'm looking for a history and that will be fulfilled via three scrapers.
				a. This data will be historical and nature and the cutoff point will be around when prices normalized from the COVID boom.
		* There will be hundreds of columns - eventually, or immediately - that've been entered in via scrapers.
			i. I don't know if said scrapers will be automatic or triggered.
				a. If they're automatic, then...
					> TCGPlayer will be annually.
					> Price Charting will be semi-annually.
					> eBay is yet-to-be-determined.
	- The goal is to house a sort of Pokémon 'stock' monitor, with historical prices dating back to 2022 and on.
	- I will conduct an Exploratory Data Analysis (EDA) on it with Python, pandas, and matplotlib.
	- I'll also use Time-Series Forecasting to forecast future trends.
		* Research: moving averages, ARIMA, and exponential smoothing.
	- Additionally, I'll deepen my analysis with more complex techniques like regression analysis that factors in external variables like set rotations or grading trends, economic indicators, and supply-and-demand shifts.
	- After all of that, and as a bonus difficulty, I'll use more advanced techniques like machine learning (LTSM networks) to capture complex patterns.  I'll also use tools like Tableau for ongoing monitoring so that I can quickly spot changes in market dynamics.


##### To-Do (Week #1: 8/18 - 8/24):
	- Create, test, and load a script that will load all cards into the MEGA Bank


### Data Dictionary(-ies)
'cards' table:
| Column Name | Description | Data Type |
| --- | --- | --- |
| id | Unique identifier for the object. | string | - Primary Key
| name | The name of the card. | string |
| supertype | The supertype of the card, such as Pokémon, Energy, or Trainer. | string |
| subtypes | A list of subtypes, such as Basic, EX, Mega, Rapid Strike, etc. | string[] (an array of strings) |
| set_obj | The set details embedded into the card. | string | - a subheading of "set", known as "name"
| series | The series the set comes from. | string | - a subheading of "set", known as "series"
| card_number | The specific number of the card. | string |
| printed_total | The total number of cards in the set. | string |
| artist | The artist of the card. | string |
| rarity | The rarity of the card, such as "Common" or "Rare Rainbow". | string |

'prices' table: