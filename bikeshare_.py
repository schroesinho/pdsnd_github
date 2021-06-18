import time
import calendar
import pandas as pd

# define potential user input
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTH_DATA = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
WEEKDAY_DATA = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
SHOW_ROWS = ['yes', 'no']


def get_filters():

    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # request user input (city, month, weekday)
    print('Hello! Let\'s explore some US bikeshare data!')
    city = input("Please choose which city data to analyse. Options are Chicago, New York City, Washington: ").lower()
    cities = list(CITY_DATA.keys())

    # make sure only predefined input as defined above is chosen
    while not(city in cities):
        city = input("Input is not part of the options Chicago, New York City, Washington, "
                     "Must be a typo as no case sensitivity is applied. Please re-enter city name: ").lower()

    month = input("Please choose which month between January and June to analyse "
                  "or enter all to analyse all months at once: ").lower()
    while not (month in MONTH_DATA):
        month = input(
            "Input is not part of the options {}. Must be a typo as no case sensitivity is applied. "
            "Please re-enter month name: ".format(MONTH_DATA)).lower()

    day = input("Please choose the weekday of interest or enter all to analyse all weekdays at once: ").lower()
    while not (day in WEEKDAY_DATA):
        day = input(
            "Input is not part of the options {}. Must be a typo as no case sensitivity is applied. "
            "Please re-enter weekday name: ".format(WEEKDAY_DATA)).lower()

    print('-'*40)
    print('get_filters done')
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
    print('read_csv done')

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract hour, month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['hour'] = df['Start Time'].dt.hour
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    # show slices of five raw data rows per user request
    show5 = input("Would you like to see five rows of the raw data?").lower()
    # show_counter is used to derive which 5 rows to show in below print statement, initial set = 1 for first five rows
    show5_counter = 1
    # make sure only predefined input is chosen
    while not(show5.lower() in SHOW_ROWS):
        show5 = input("Input is neither yes nor no, please choose one of those options.").lower()
    while show5.lower() == 'yes':
        # print "next" five rows
        print(df.iloc[(show5_counter-1)*5:show5_counter*5, ])
        show5 = input("Would you like to see another 5 rows of data?").lower()
        while not(show5.lower() in SHOW_ROWS):
            show5 = input("Input is neither yes nor no, please choose one of those options.").lower()
        # if user choice is still "yes" shift the rows to be shown in next print statement by multiplier of 5
        show5_counter += 1

    print('load_data done')
    return df


def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    # track start time to calculate time required for calculations
    start_time = time.time()
    # define the mode of the column month, limit to month number via [0] and convert to name
    popular_month = calendar.month_name[df['month'].mode()[0]]
    # print results, case separation to phrase sentences with 'all' correctly
    if day == 'all' and month == 'all':
        print('The most common month for sharing bikes on all days in {} is {}'
              .format(city.title(), popular_month))
    elif month == 'all':
        print('The most common month for sharing bikes on a {} in {} is {}'
              .format(day.title(), city.title(), popular_month))
    else:
        print('It is meaningless to search for the most common month as a month has been specified for filtering!')

    # define the mode of the column day of week, limit to the day via [0]
    popular_day = df['day_of_week'].mode()[0]
    # print results, case separation to phrase sentences with 'all' correctly
    if day == 'all' and month == 'all':
        print('The most common day for sharing bikes during all months in {} is {}'
              .format(city.title(), popular_day))
    elif day == 'all':
        print('The most common day for sharing bikes during {} in {} is {}'
              .format(month.title(), city.title(), popular_day))
    else:
        print('It is meaningless to search for the most common weekday as a day has been specified for filtering!')

    # define the mode of the column hour, limit to hour number via [0]
    popular_hour = df['hour'].mode()[0]
    # print results, case separation to phrase sentences with 'all' correctly
    if month == 'all' and day == 'all':
        print('The most common hour for sharing bikes during all months across weekdays in {} is {}'
              .format(city.title(), popular_hour))
    elif month == 'all':
        print('The most common hour for sharing bikes on a {} in {} is {}'
              .format(day.title(), city.title(), popular_hour))
    elif day == 'all':
        print('The most common hour for sharing bikes during {} in {} is {}'
              .format(month.title(), city.title(), popular_hour))
    else:
        print('The most common hour for sharing bikes during {} on a {} in {} is {}'
              .format(month.title(), day.title(), city.title(), popular_hour))
    # track computation time (compare start_time above) & print
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, city, month, day):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    # track start time to calculate time required for calculations
    start_time = time.time()
    # define the mode of the column start station, limit to its name number via [0]
    popular_start = df['Start Station'].mode()[0]
    # print results, case separation to phrase sentences with 'all' correctly
    if month == 'all' and day == 'all':
        print('The most common starting station for trips with shared bikes during all months across weekdays '
              'in {} is {}'.format(city.title(), popular_start))
    elif month == 'all':
        print('The most common starting station for trips with shared bikes on a {} in {} is {}'
              .format(day.title(), city.title(), popular_start))
    elif day == 'all':
        print('The most common starting station for trips with shared bikes during {} in {} is {}'
              .format(month.title(), city.title(), popular_start))
    else:
        print('The most common starting station for trips with shared bikes during {} on a {} in {} is {}'
              .format(month.title(), day.title(), city.title(), popular_start))

    # define the mode of the column end station, limit to its name number via [0]
    popular_end = df['End Station'].mode()[0]
    # print results, case separation to phrase sentences with 'all' correctly
    if month == 'all' and day == 'all':
        print('The most common end station for trips with shared bikes during all months across weekdays in {} is {}'
              .format(city.title(), popular_end))
    elif month == 'all':
        print('The most common end station for trips with shared bikes on a {} in {} is {}'
              .format(day.title(), city.title(), popular_end))
    elif day == 'all':
        print('The most common end station for trips with shared bikes during {} in {} is {}'
              .format(month.title(), city.title(), popular_end))
    else:
        print('The most common end station for trips with shared bikes during {} on a {} in {} is {}'
              .format(month.title(), day.title(), city.title(), popular_end))

    # define the maximum index of dataset grouped by start and end station (counts),
    # read out this tuple in two separate variables
    popular_combi_start, popular_combi_end = df.groupby(['Start Station', 'End Station'])['Start Station']\
        .count().idxmax()
    # print results, case separation to phrase sentences with 'all' correctly
    if month == 'all' and day == 'all':
        print('The most common start- and end station combination for trips with shared bikes during all months '
              'across weekdays in {} is from {} to {}'.format(city.title(), popular_combi_start, popular_combi_end))
    elif month == 'all':
        print('The most common start- and end station for trips with shared bikes on a {} in {} is from {} to {}'
              .format(day.title(), city.title(), popular_combi_start, popular_combi_end))
    elif day == 'all':
        print('The most common start- and end station for trips with shared bikes during {} in {} is from {} to {}'
              .format(month.title(), city.title(), popular_combi_start, popular_combi_end))
    else:
        print('The most common start- and end station for trips with shared bikes '
              'during {} on a {} in {} is from {} to {}'
              .format(month.title(), day.title(), city.title(), popular_combi_start, popular_combi_end))
    # track computation time (compare start_time above) & print
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, city, month, day):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    # track start time to calculate time required for calculations
    start_time = time.time()
    # calculate the total time of all trips in the dataframe
    travel_sec = df['Trip Duration'].sum()

    # to prepare conversion of seconds to days / hours / minutes: define how many seconds each of these is having
    sec_per_day = 60*60*24
    sec_per_hr = 60*60
    sec_per_min = 60

    # define number of days in the total travel time by division, cutting of decimals and
    # setting to integer for better text read
    travel_days = int(travel_sec//sec_per_day)
    # hrs: how many seconds are left once days are extracted, afterwards convert these to hours
    travel_hrs = int((travel_sec % sec_per_day)//sec_per_hr)
    # minutes: how many seconds are left once hours are extracted, afterwards convert these to minutes
    travel_mins = int((travel_sec % sec_per_hr)//sec_per_min)
    # seconds: same pattern, remainder of above
    travel_secs = int((travel_sec % sec_per_min))

    # print results, case separation to phrase sentences with 'all' correctly
    if month == 'all' and day == 'all':
        print('The total travel time of trips with shared bikes during all months across weekdays '
              'in {} is {} day(s), {} hour(s), {} minute(s), {} second(s)'
              .format(city.title(), travel_days, travel_hrs, travel_mins, travel_secs))
    elif month == 'all':
        print('The total travel time of trips with shared bikes on a {} in {} '
              'is {} day(s), {} hour(s), {} minute(s), {} second(s)'
              .format(day.title(), city.title(), travel_days, travel_hrs, travel_mins, travel_secs))
    elif day == 'all':
        print('The total travel time of trips with shared bikes during {} in {} '
              'is {} day(s), {} hour(s), {} minute(s), {} second(s)'
              .format(month.title(), city.title(), travel_days, travel_hrs, travel_mins, travel_secs))
    else:
        print('The total travel time of trips with shared bikes during {} on a {} in {} '
              'is {} day(s), {} hour(s), {} minute(s), {} second(s)'
              .format(month.title(), day.title(), city.title(), travel_days, travel_hrs, travel_mins, travel_secs))

    # define the mean of all trips in dataframe
    travel_sec = df['Trip Duration'].mean()

    # compare above: slicing the seconds in days, hours and minutes.
    # As above variables are not used anymore overwrite those is ok
    travel_days = int(travel_sec//sec_per_day)
    travel_hrs = int((travel_sec % sec_per_day)//sec_per_hr)
    travel_mins = int((travel_sec % sec_per_hr)//sec_per_min)
    travel_secs = int((travel_sec % sec_per_min))

    # print results, case separation to phrase sentences with 'all' correctly
    if month == 'all' and day == 'all':
        print('The average travel time of trips with shared bikes during all months across weekdays '
              'in {} is {} day(s), {} hour(s), {} minute(s), {} second(s)'
              .format(city.title(), travel_days, travel_hrs, travel_mins, travel_secs))
    elif month == 'all':
        print('The average travel time of trips with shared bikes on a {} '
              'in {} is {} day(s), {} hour(s), {} minute(s), {} second(s)'
              .format(day.title(), city.title(), travel_days, travel_hrs, travel_mins, travel_secs))
    elif day == 'all':
        print('The average travel time of trips with shared bikes during {} '
              'in {} is {} day(s), {} hour(s), {} minute(s), {} second(s)'
              .format(month.title(), city.title(), travel_days, travel_hrs, travel_mins, travel_secs))
    else:
        print('The average travel time of trips with shared bikes during {} on a {} '
              'in {} is {} day(s), {} hour(s), {} minute(s), {} second(s)'
              .format(month.title(), day.title(), city.title(), travel_days, travel_hrs, travel_mins, travel_secs))

    # track computation time (compare start_time above) & print
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city, month, day):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    # track start time to calculate time required for calculations
    start_time = time.time()
    # extract user types per dataframe via group by statement.
    # As Start Station is filled for each trip use this variable
    # remove indices and convert to string to make readable in print statement
    user_types = df.groupby(['User Type'], as_index=False)['Start Station'].count()\
        .rename(columns={'Start Station': 'Total_Numbers'}).to_string(index=False)

    # print results, case separation to phrase sentences with 'all' correctly
    if month == 'all' and day == 'all':
        print('The following user types were counted while analysing trips with shared bikes '
              'during all months across weekdays in {}: \n \n {}'
              .format(city.title(), user_types))
    elif month == 'all':
        print('The following user types were counted while analysing trips with shared bikes on a {} in {}: \n \n {}'
              .format(day.title(), city.title(), user_types))
    elif day == 'all':
        print('The following user types were counted while analysing trips with shared bikes during {} in {}: \n \n {}'
              .format(month.title(), city.title(), user_types))
    else:
        print('The following user types were counted while analysing trips with shared bikes '
              'during {} on a {} in {}: \n \n {}'.format(month.title(), day.title(), city.title(), user_types))

    # handle special case wahington where gender and date of birth information are missing in the data set
    if city == 'washington':
        print('No information on gender and date of birth available in the dataset for Washington')
    else:
        # extract genders per dataframe via group by statement.
        # As Start Station is filled for each trip use this variable
        # remove indices and convert to string to make readable in print statement
        genders = df.groupby(['Gender'], as_index=False)['Start Station'].count().rename(
            columns={'Start Station': 'Total_Numbers'}).to_string(index=False)
        # print results, case separation to phrase sentences with 'all' correctly
        if month == 'all' and day == 'all':
            print('The following genders were counted while analysing trips with shared bikes '
                  'during all months across weekdays in {}: \n \n {}'.format(city.title(), genders))
        elif month == 'all':
            print('The following genders were counted while analysing trips with shared bikes on a {} in {}: \n \n {}'
                  .format(day.title(), city.title(), genders))
        elif day == 'all':
            print('The following genders were counted while analysing trips with shared bikes during {} in {}: \n \n {}'
                  .format(month.title(), city.title(), genders))
        else:
            print('The following genders were counted while analysing trips with shared bikes '
                  'during {} on a {} in {}: \n \n {}'.format(month.title(), day.title(), city.title(), genders))

        # define smallest, most occuring and highest year of birth
        youngest_yob = int(df['Birth Year'].max())
        oldest_yob = int(df['Birth Year'].min())
        most_yob = int(df['Birth Year'].mode())

        # print results, case separation to phrase sentences with 'all' correctly
        if month == 'all' and day == 'all':
            print('The youngest customer renting a bike during all months across weekdays in {} was borne in {}, '
                  'the oldest in {} and the most customers were born in {}:'
                  .format(city.title(), youngest_yob, oldest_yob, most_yob))
        elif month == 'all':
            print('The youngest customer renting a bike in {} on a {} was borne in {}, '
                  'the oldest in {} and the most customers were born in {}'
                  .format(city.title(), day.title(),  youngest_yob, oldest_yob, most_yob))
        elif day == 'all':
            print('The youngest customer renting a bike in {} during {} was borne in {}, '
                  'the oldest in {} and the most customers were born in {}'
                  .format(city.title(), month.title(), youngest_yob, oldest_yob, most_yob))
        else:
            print('The youngest customer renting a bike in {} during {} on a {} was borne in {}, '
                  'the oldest in {} and the most customers were born in {}'
                  .format(city.title(), month.title(), day.title(), youngest_yob, oldest_yob, most_yob))
    # track computation time (compare start_time above) & print
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        # main script: run functions defined above in correct order
        # assign returned city, month and day as used in all functions
        city, month, day = get_filters()

        df = load_data(city, month, day)

        time_stats(df, city, month, day)
        station_stats(df, city, month, day)
        trip_duration_stats(df, city, month, day)
        user_stats(df, city, month, day)
        # offer restart
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

# run main script


if __name__ == "__main__":
    main()
