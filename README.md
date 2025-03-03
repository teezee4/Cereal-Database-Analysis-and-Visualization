# Cereal Database Analysis Tool

## Project Description

This Python application provides an interactive interface for analyzing nutritional data of various cereals stored in a MySQL database. It combines SQL queries, data analysis, and visualization techniques to offer insights into cereal nutritional content and consumer ratings.

### Key Features:

- **Database Integration**: Utilizes PyMySQL to connect to a local MySQL database containing detailed cereal nutritional information.
- **Statistical Analysis**: Implements linear regression to predict cereal ratings based on nutritional factors like sugar and fiber content.
- **Data Visualization**: Creates scatter plots using Matplotlib to illustrate relationships between nutritional values and consumer ratings.
- **Comprehensive Queries**: Offers a range of both non-relational and relational queries, allowing users to explore the data from various angles.

### Non-Relational Queries:

1. Sugar Content Rating Estimator: Uses linear regression to predict a cereal's rating based on its sugar content.

2. Sugar Content vs. Rating Visualizer: Creates a scatter plot showing the relationship between cereal ratings and sugar content.

3. Fiber Content Rating Estimator: Employs linear regression to predict a cereal's rating based on its fiber content.

4. Fiber Content vs. Rating Visualizer: Generates a scatter plot displaying the relationship between cereal ratings and fiber content.

5. High-Calorie Cereal Finder: Identifies and displays cereals that exceed a user-specified calorie threshold per cup.

### Relational Queries:

6. Low-Calorie, High-Protein Cereal Identifier: Pinpoints cereals with less than 100 calories but more than 2g of protein.

7. Protein-to-Sugar Ratio Ranker: Calculates and ranks cereals based on their protein-to-sugar ratio, displaying the top 10.

8. Protein Density Analyzer: Lists the top 5 cereals with the most protein per cup of serving.

9. Shelf Placement Rating Analyzer: Calculates and displays the average rating for cereals on each shelf level.

10. Carbohydrate-to-Fat Ratio Ranker: Ranks cereals based on their carbohydrate-to-fat ratio, showing the top 10.

## Technical Details

- **Language**: Python 3.x
- **Database**: MySQL
- **Libraries**: PyMySQL, pandas, NumPy, scikit-learn, Matplotlib

## How to Use

1. Ensure you have a MySQL database set up with the cereal nutritional data.
2. Install required Python libraries: `pip install pymysql pandas numpy scikit-learn matplotlib`
3. Update the database connection details in the script.
4. Run the script and follow the on-screen menu to select and execute queries.

This project demonstrates proficiency in SQL, data analysis, and Python programming, making it an excellent addition to any data science or software development portfolio.
