
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

tables = pd.read_html("https://en.wikipedia.org/wiki/List_of_countries_by_carbon_dioxide_emissions")
countries = tables[1]

# columns nieuwe namen gegeven
countries.columns = [
                    "country",
                    "fossil1990",
                    "fossil2005",
                    "fossil2017",
                    "2017_world_%",
                    "2017_vs_1990",
                    "2017_pla",
                    "2017_pc",
                    "2018_total_inc",
                    "2018_total_ex"
                    ]

# alleen de landen filteren + sorteren op comission
countries = countries.loc[3:, :]
countries = countries.drop(67)  # European Union uit de lijst gehaald


# Chart 1 CO2 of the biggest countries

def chart1():
    countries_sorted = countries.sort_values(by=['fossil2017'], ascending=False).head(5)
    biggest_countries = countries_sorted.loc[:, ["country", "fossil1990", "fossil2005", "fossil2017"]]
    years = biggest_countries.columns[1:]

    for index, row in biggest_countries.iterrows():
        plt.plot(years, row[1:], label=row[0])

    plt.title('CO2 of the biggest countries')
    plt.xlabel('Years')
    plt.ylabel('Amount of Co2')
    plt.legend(loc="center left", bbox_to_anchor=(1, 0.5), fancybox=True)
    plt.tight_layout()
    plt.show()


chart1()

# Chart 2 top 3 beste en slechtste landen relatief gezien


def emission_bigger_5(emission):
    return emission > 5


def calc_relative_emission(country):
    for index, row in country.iterrows():
        relative_2005 = round((country.fossil2005[index] / country.fossil1990[index])*100)
        relative_2017 = round((country.fossil2017[index] / country.fossil1990[index])*100)
        relative2005_list.append(relative_2005)
        relative2017_list.append(relative_2017)


# filteren alle landen met een lage emission
countries_groter_5 = countries.loc[countries.fossil1990.apply(emission_bigger_5)]
relative2005_list = []
relative2017_list = []

# itereren door alle landen heen, en we gooien de relative waardes in 2 lijsten
calc_relative_emission(countries_groter_5)

# we maken 3 nieuwe kolommen aan en voegen de lijsten toe aan de dataframe
countries_groter_5.insert(loc=1, column="relative1990", value=100)
countries_groter_5.insert(loc=2, column="relative2005", value=relative2005_list)
countries_groter_5.insert(loc=3, column="relative2017", value=relative2017_list)

# filteren de 3 beste en de 3 slechte landen
best_countries = countries_groter_5.sort_values(by=['relative2017']).head(3)
worst_countries = countries_groter_5.sort_values(by=['relative2017']).tail(3)

# mergen er een dataframe van
countries_merge = pd.merge(best_countries, worst_countries, how="outer")

# we maken hier de data die we nodig hebben voor de chart
countries_merge = countries_merge.loc[:, ["country", "relative1990", "relative2005", "relative2017"]]
years = ["1990", "2005", "2017"]

# en hier maken we de chart
for index, row in countries_merge.iterrows():
    plt.plot(years, row[1:], label=row[0])

plt.title('top 3 best and wors countries')
plt.xlabel('Years')
plt.ylabel('Relative')
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5), fancybox=True)
plt.tight_layout()
plt.show()