import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:

        try:
            # user input for city filter
            city = input('Would you like to explore data from Chicago, New York City or Washington?\n').title()
        except ValueError:
            print("Invalid input")

        if city not in {"Chicago", "New York City", "Washington"}:
            print("Oops, that's not a valid city!")
            continue
        else:
            print("You have chosen {}.".format(city))
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:

        try:
            # user input for month filter
            month = input('Enter a month from January to June, or all:\n').title()
        except:
            print("Invalid input")

        if month not in {"January", "February", "March", "April", "May", "June", "All"}:
            print("Oops, that's not a valid entry!")
            continue
        else:
            print("You have chosen {}.".format(month))
            break


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:

        try:
            # user input for day filter
            day = input('Enter the day of the week:\n').title()
        except ValueError:
            print("Invalid input")

        if day not in {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"}:
            print("Oops, that's not a day!")
            continue
        else:
            print("You have chosen {}.".format(day))
            break

    print('-'*40)
    return city, month, day




def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert times into datetime format
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["End Time"] = pd.to_datetime(df["End Time"])

    # create columns for month, day and hour
    df["month"] = df["Start Time"].dt.month
    df["day"] = df["Start Time"].dt.weekday_name
    df["hour"] = df["Start Time"].dt.hour

    # filter by month
    if month != "All":

        months = ["January", "February", "March", "April", "May", "June"]
        month = months.index(month) + 1
        df = df[df["month"] == month]

    # filter by day
    if day == ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]:

        df = df[df["day"] == day.title()]
        print("You have chosen to filter by: \nCity: {}\nMonth: {}\nDay: {}".format(city, month, day))


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print("The most common month is: ", df["month"].mode()[0])

    # TO DO: display the most common day of week
    print("The most common day of the week is: ", df["day"].mode()[0])

    # TO DO: display the most common start hour
    print("The most common start hour is: ", df["hour"].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most commonly used start station is: ", df["Start Station"].mode()[0])

    # TO DO: display most commonly used end station
    print("The most commonly used end station is: ", df["End Station"].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    # This answer came from https://stackoverflow.com/a/50848470, as I was using .mode and couldn't figure out why it wasn't working. My googling came across the answer.
    count = df.groupby(["Start Station","End Station"]).size().nlargest(1)
    print("The most commonly used start and end combination of stations is: ", count)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print("The total travel time was: ", df["Trip Duration"].sum())

    # TO DO: display mean travel time
    print("The mean travel time was: ", df["Trip Duration"].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    if "Gender" not in df.columns:
        print("Unfortunately there are no user statistics available for Washington.\n")
        return None

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("Count of user types: ", df["User Type"].count())

    # TO DO: Display counts of gender
    print("Count of genders: ", df["Gender"].count())

    # TO DO: Display earliest, most recent, and most common year of birth
    print("Earliest birth year: ", df["Birth Year"].min())
    print("Most recent birth year: ", df["Birth Year"].max())
    print("Most common birth year: ", df["Birth Year"].mode())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        while True:
            n = 5
            try:
                source_file = input("Would you like to view the first 5 lines of data from the source file?\n").title()
            except ValueError:
                print("Invalid input")

            if source_file == "Yes":
                print("Here are the first 5 lines of the source file:", df.head())

                while True:
                    try:
                        sf2 = input("Would you like to view 5 more lines of data?\n").title()
                    except ValueError:
                        print("Invalid input")

                    if sf2 == "Yes":
                        n = n + 5
                        print("Here are {} lines of the source file:".format(n), df.head(n))
                        continue
                    else:
                        break

            else:
                print("You have chosen to stop viewing the source file.")
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
