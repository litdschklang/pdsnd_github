import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'D:/python/all-project-files/chicago.csv',
              'new york city': 'D:/python/all-project-files/new_york_city.csv',
              'washington': 'D:/python/all-project-files/washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Good day! Let\'s explore some US bikeshare data together!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('\nWould you like to see data for Chicago, New York City, or Washington?\n').lower()
        city_list = ["chicago", "new york city", "washington"]
        if city not in city_list:
            print("Sorry, the city you typed does not exist in our database. Please try again.")
            continue
        else:
            break

    # get user input for filter criteria
    while True:
        filtered_criteria = input('\nWould you like to filter the data by month, day, or not at all? Type "both" for both, type "none" for not at all:\n').lower()
        criteria_list = ['day','month','both','none']
        if filtered_criteria not in criteria_list:
            print('Sorry, the criteria you typed does not exist! Please try again.')
            continue
        elif filtered_criteria == 'day':
            month = 'all'
            break
        elif filtered_criteria == 'month':
            day = 'all'
            break
        elif filtered_criteria == 'none':
            month = 'all'
            day = 'all'
            break
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while filtered_criteria == 'month' or filtered_criteria == 'both':
        month = input('\nPlease enter a month (From "January" till "June"):\n').lower()
        month_list = ['january', 'february', 'march', 'april', 'may', 'june']
        if month not in month_list:
            print("Sorry, the month you typed does not exist. Please try again")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while filtered_criteria == 'day' or filtered_criteria == 'both':
        day = input('\nPlease enter a day of week (From "Monday" till "Sunday"):\n').lower()
        day_list = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        if day not in day_list:
            print("Sorry, the day you typed does not exist. Please try again")
            continue
        else:
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

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek


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
        days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        day = days.index(day) + 1
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month_index = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    popular_month = months[popular_month_index - 1]

    # display the most common day of week
    popular_day_index = df['day_of_week'].mode()[0]
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    popular_day = days[popular_day_index - 1]

    # display the most common start hour

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]
    
    print('Most Frequent Start Hour:', popular_hour)
    if len(np.unique(df['month'])) == 1:
        print('')
    else:
        print('Most Frequent Start month:', popular_month)
    
    if len(np.unique(df['day_of_week'])) == 1:
        print('')
    else:
        print('Most Frequent Start day of week:', popular_day)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    print('Most Popular Track: From "{}" to "{}"'.format(popular_start_station, popular_end_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total trip duration is {} seconds".format(np.sum(df['Trip Duration'])))

    # display mean travel time
    print("Average trip duration is {} seconds".format(np.mean(df['Trip Duration'])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # print value counts for each user type
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    if 'Gender' in df:
        user_gender = df['Gender'].value_counts()
        print(user_gender)
    else:
        print('User Gender Information Not Available For This City!')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_date = df['Birth Year'].min()
        most_recent_data = df['Birth Year'].max()
        most_commen_year = df['Birth Year'].mode()[0]
        print('Earliest User Birth Date Is: ', int(earliest_date))
        print('Most Recent User Birth Date Is: ', int(most_recent_data))
        print('Most Common Year Of Birth Is: ', int(most_commen_year))
    else:
        print('User Birth Information Not Available For This City!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def read_raw_data(df):
    """Displays raw data to the user."""
    read_data = input('\nWould you like to check 5 lines of the raw data? Enter yes or no.\n')
    if read_data.lower() == 'yes':
        print(df.head(5))
        i = 5
        while True:
            continue_read = input('\nContinue read the next 5 lines? Enter yes or no.\n')
            if continue_read.lower() == 'yes':
                    print(df.loc[i:i + 4,:])
                    i += 5
                    continue
            else:
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if df.empty:
            print('There is no data according to the chosen criteria!')
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            read_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
