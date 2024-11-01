
import pandas as pd

def calculate_demographic_data(print_data=True):
    print("Loading data...")        
    df = pd.read_csv('D:/boilerplate-demographic-data-analyzer/adult.data.csv')
    print("Data loaded successfully. Sample data:")
    print(df.head())

    # How many people of each race are represented in this dataset? This should be a Pandas series with race names as the index labels. (race column)
    race_count = df['race'].value_counts()
    if print_data:
        print("Q1. Number of each race:\n", race_count) 
    
    # What is the average age of men?
    average_age_men = df[df['sex'] == 'Male']['age'].mean()
    if print_data:
        print("Q2. Average age of men:", average_age_men)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = (df['education'] == 'Bachelors').mean() * 100
    if print_data:
        print(f"Q3. Percentage of people who have a Bachelor's degree: {percentage_bachelors:.2f}%")

    # What percentage of people with advanced education (Bachelors, Masters, or Doctorate) make more than 50K?
    higher_education = df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])
    higher_education_rich = (df[higher_education]['salary'] == '>50K').mean() * 100
    if print_data:
        print(f"Q4. Percentage of people with advanced education (Bachelors, Masters, or Doctorate) that earn >50K: {higher_education_rich:.2f}%")

    #What percentage of people without advanced education make more than 50K?
    lower_education_rich = round((df[~higher_education]['salary'] == '>50K').sum() / len(df[~higher_education]) * 100, 1)
    if print_data:
        print(f"Q5. Percentage of people without advanced education that earn >50K: {lower_education_rich:.2f}%")

    #What is the minimum number of hours a person works per week?
    min_work_hours = df['hours-per-week'].min()
    if print_data:
        print(f"Q6. Min work time: {min_work_hours} hours/week")

    # What percentage of the people who work the minimum number of hours per week have a salary of more than 50K?
    num_min_workers = df[df['hours-per-week'] == min_work_hours]
    rich_percentage = (num_min_workers['salary'] == '>50K').mean() * 100
    if print_data:
        print(f"Q7. Percentage of the people who work the minimum number of hours per week have a salary of more than 50K: {rich_percentage:.2f}%")



    # What country has the highest percentage of people that earn >50K and what is that percentage?
    country_earning = df.groupby('native-country')['salary'].value_counts(normalize=True).unstack(fill_value=0)
    country_earning['rich_percentage'] = country_earning['>50K'] * 100
    highest_earning_country = country_earning['rich_percentage'].idxmax()
    highest_earning_country_percentage = country_earning['rich_percentage'].max()
    if print_data:    
        print("Q8A. Country with highest percentage of rich:", highest_earning_country)
        print(f"Q8B. Highest percentage of rich people in country: {highest_earning_country_percentage:.2f}%")

    # Most popular occupation for those who earn >50K in India
    top_IN_occupation = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')]['occupation'].mode()[0]
    if print_data:    
        print("Q9. Top occupations in India:", top_IN_occupation)

    # Return the results as a dictionary for testing
    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage': highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation,
    }

# Call the function
calculate_demographic_data()
  





import pandas as pd
import unittest


class DemographicAnalyzerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(Cls):
        Cls.data = calculate_demographic_data(print_data = False)

    def test_race_count(self):
        actual = self.data['race_count'].tolist()
        expected = [27816, 3124, 1039, 311, 271]
        race_message = "Expected race count values to be {}".format(expected)
        self.assertCountEqual(actual, expected, msg=race_message)
        
    def test_average_age_men(self):
        actual = self.data['average_age_men']
        expected = 39.4
        average_message = "Expected different value for average age of men."
        self.assertAlmostEqual(actual, expected, places=1, msg=average_message)

    def test_percentage_bachelors(self):
        actual = self.data['percentage_bachelors']
        expected = 16.4 
        percentage_message = "Expected different value for percentage with Bachelors degrees."
        self.assertAlmostEqual(actual, expected, places=1, msg=percentage_message)

    def test_higher_education_rich(self):
        actual = self.data['higher_education_rich']
        expected = 46.5
        higher_message = "Expected different value for percentage with higher education that earn >50K."
        self.assertAlmostEqual(actual, expected, places=1, msg=higher_message)
  
    def test_lower_education_rich(self):
        actual = self.data['lower_education_rich']
        expected = 17.4
        test_lower_message = "Expected different value for percentage without higher education that earn >50K."
        self.assertAlmostEqual(actual, expected, places=1, msg=test_lower_message)

    def test_min_work_hours(self):
        actual = self.data['min_work_hours']
        expected = 1
        test_min_message = "Expected different value for minimum work hours."
        self.assertAlmostEqual(actual, expected, places=1, msg=test_min_message)     

    def test_rich_percentage(self):
        actual = self.data['rich_percentage']
        expected = 10
        test_rich_message = "Expected different value for percentage of rich among those who work fewest hours."
        self.assertAlmostEqual(actual, expected, msg=test_rich_message)   

    def test_highest_earning_country(self):
        actual = self.data['highest_earning_country']
        expected = 'Iran'
        highest_earning_string = "Expected different value for highest earning country."
        self.assertEqual(actual, expected, highest_earning_string)   

    def test_highest_earning_country_percentage(self):
        actual = self.data['highest_earning_country_percentage']
        expected = 41.9
        test_highest_message = "Expected different value for highest earning country percentage."
        self.assertAlmostEqual(actual, expected, places=1, msg=test_highest_message)   

    def test_top_IN_occupation(self):
        actual = self.data['top_IN_occupation']
        expected = 'Prof-specialty'
        top_IN_string = "Expected different value for top occupations in India."
        self.assertEqual(actual, expected, top_IN_string)      

if __name__ == "__main__":
    unittest.main()

