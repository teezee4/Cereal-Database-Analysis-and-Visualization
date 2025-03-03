!pip install pymysql
!pip install transformers
!pip install pandas pymysql scikit-learn matplotlib
import pymysql
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans


def SQL_Query(queryInput):
    try:
        connection = pymysql.connect(
            host='127.0.0.1',
            user='mp',
            passwd='eecs118',
            db='cereal_database'
        )
        print("Database connection successful!")
        
        with connection.cursor() as cursor:
            query = queryInput
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows

    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL: {e}")
    finally:
        if connection:
            connection.close()
            print("Database connection closed.")


def startMenuOptions():
    while True:
        print("\nChoose a query by entering its number.")
        print("Type in 'X' to leave the program.\n")

        print("Non-Relational Queries:")
        print("1.  Estimate the rating given the amount of sugar in a cereal.")
        print("2.  Visualize the rating of cereal given the amount of sugar.")
        print("3.  Estimate the rating given the amount of fiber in a cereal.")
        print("4.  Visualize the rating of a cereal versus the amount of fiber.")
        print("5.  Given an amount of calories, list all cereals that have over that many calories per cup.")

        print("Relational Queries:")
        print("6.  Which cereals have less than 100 calories but more than 2g of protein?")
        print("7.  Which cereals have the highest protein-to-sugar ratio?")
        print("8.  Which 5 cereals provide the most protein per cup of serving?")
        print("9. What is the average rating for cereals on each shelf level?")
        print("10. Which cereals have the highest carbohydrate-to-fat ratio?")
        
        user_input = input("Enter choice (1-10 or 'X'): ").strip()

        if user_input.lower() == 'x':
            print("Exiting the program. Goodbye!")
            break

        try:
            choice = int(user_input)
            if choice == 1:
                sugar_amount = float(input("Enter sugar value: "))
                print(f"Estimating rating for a cereal with {sugar_amount} grams of sugar...")
                result = SQL_Query(f"WITH regression_coefficients AS (SELECT SUM((sugars - (SELECT AVG(sugars) FROM cereals)) * (rating - (SELECT AVG(rating) FROM cereals))) / SUM(POWER(sugars - (SELECT AVG(sugars) FROM cereals), 2)) AS slope, (SELECT AVG(rating) FROM cereals) - (SUM((sugars - (SELECT AVG(sugars) FROM cereals)) * (rating - (SELECT AVG(rating) FROM cereals))) / SUM(POWER(sugars - (SELECT AVG(sugars) FROM cereals), 2))) * (SELECT AVG(sugars) FROM cereals) AS intercept FROM cereals) SELECT {sugar_amount} AS sugar_value, (slope * {sugar_amount} + intercept) AS estimated_rating FROM regression_coefficients;")
                print(f"Estimated Rating: {result[0][1]}")

            elif choice == 2:
                print("Visualizing the rating of cereal given grams of sugar...")
                result = SQL_Query(f"SELECT sugars, rating FROM cereals;")
                sugars = [float(row[0]) for row in result]
                ratings = [float(row[1]) for row in result]
                plt.scatter(sugars, ratings)
                plt.title("Cereal Ratings vs Sugar Content")
                plt.xlabel("Sugar Content (g)")
                plt.ylabel("Rating")
                plt.grid(True)
                plt.show()

            elif choice == 3:
                fiber_amount = float(input("Enter fiber value: "))
                print(f"Estimating rating for a cereal with {fiber_amount} grams of fiber...")
                result = SQL_Query(f"WITH regression_coefficients AS (SELECT SUM((fiber - (SELECT AVG(fiber) FROM cereals)) * (rating - (SELECT AVG(rating) FROM cereals))) / SUM(POWER(fiber - (SELECT AVG(fiber) FROM cereals), 2)) AS slope, (SELECT AVG(rating) FROM cereals) - (SUM((fiber - (SELECT AVG(fiber) FROM cereals)) * (rating - (SELECT AVG(rating) FROM cereals))) / SUM(POWER(fiber - (SELECT AVG(fiber) FROM cereals), 2))) * (SELECT AVG(fiber) FROM cereals) AS intercept FROM cereals) SELECT {fiber_amount} AS fiber_value, (slope * {fiber_amount} + intercept) AS estimated_rating FROM regression_coefficients;")
                print(f"Estimated Rating: {result[0][1]}")
            
            elif choice == 4:
                print("Visualizing the rating of cereal vs fiber value...")
                result = SQL_Query("SELECT fiber, rating FROM cereals;")
                fiber = [float(row[0]) for row in result]
                ratings = [float(row[1]) for row in result]
                plt.scatter(fiber, ratings, label="Data Points", alpha=0.7)
                plt.title("Cereal Ratings vs Fiber Content")
                plt.xlabel("Fiber Content (g)")
                plt.ylabel("Rating")
                plt.grid(True)
                plt.show()  
                
            elif choice == 5:
                calories_threshold = float(input("Enter minimum calories per cup: "))
                print(f"\nFinding cereals with more than {calories_threshold} calories per cup...")
                result = SQL_Query(f"SELECT name, calories, cups, (calories/cups) as calories_per_cup FROM cereals WHERE calories/cups > {calories_threshold} ORDER BY calories_per_cup DESC;")
                print("\nCereals Exceeding Calorie Threshold per Cup:")
                print("-" * 65)
                print(f"{'Name':<30} {'Calories':<10} {'Cups':<10} {'Cal/Cup':<10}")
                print("-" * 65)
                for cereal in result:
                        print(f"{cereal[0]:<30} {cereal[1]:<10} {cereal[2]:<10.2f} {cereal[3]:.2f}")
            
            elif choice == 6:
                print("Finding cereals with low calories and high protein content...")
                result = SQL_Query("SELECT name FROM cereals WHERE calories < 100 AND protein > 2;")
                print("\nCereals with < 100 calories and > 2g protein:")
                print("-" * 40)
                print(f"{'Name':<30}")
                print("-" * 40)
                for cereal in result:
                    print(f"{cereal[0]:<30}")

            elif choice == 7:
                print("Finding cereals with the highest protein-to-sugar ratio...")
                result = SQL_Query(f"SELECT name, protein / sugars AS protein_to_sugar_ratio FROM cereals ORDER BY protein_to_sugar_ratio DESC LIMIT 10;")
                print("\nTop 10 Cereals by Protein-to-Sugar Ratio:")
                print("-" * 50)
                print(f"{'Name':<30} {'Protein-to-Sugar Ratio':<20}")
                print("-" * 50)
                for cereal in result:
                    print(f"{cereal[0]:<30} {cereal[1]:.2f}")

            elif choice == 8:
                print("Finding cereals with highest protein content per cup serving...")
                result = SQL_Query("SELECT name, protein / cups AS protein_per_cup FROM cereals ORDER BY protein_per_cup DESC LIMIT 5;")
                print("\nTop 5 Cereals by Protein per Cup:")
                print("-" * 45)
                print(f"{'Name':<30} {'Protein per Cup (g)':<15}")
                print("-" * 45)
                for cereal in result:
                    print(f"{cereal[0]:<30} {cereal[1]:.2f}")

            elif choice == 9:
                print("Analyzing average cereal ratings by shelf placement...")
                result = SQL_Query("SELECT shelf, AVG(rating) AS average_rating FROM cereals GROUP BY shelf;")
                print("\nAverage Cereal Ratings by Shelf Level:")
                print("-" * 40)
                print(f"{'Shelf':<10} {'Average Rating':<15}")
                print("-" * 40)
                for shelf_data in result:
                    print(f"{shelf_data[0]:<10} {shelf_data[1]:.2f}")

            elif choice == 10:
                print("Finding cereals with the highest carbohydrate-to-fat ratio...")
                result = SQL_Query("SELECT name, carbo/fat AS carb_to_fat_ratio FROM cereals ORDER BY carb_to_fat_ratio DESC LIMIT 10;")
                print("\nTop 10 Cereals by Carbohydrate-to-Fat Ratio:")
                print("-" * 50)
                print(f"{'Name':<30} {'Carb-to-Fat Ratio':<20}")
                print("-" * 50)
                for cereal in result:
                        print(f"{cereal[0]:<30} {cereal[1]:.2f}")

        except ValueError:
            print("Invalid input. Please enter a valid number or 'X'.")

if __name__ == "__main__":
    startMenuOptions()