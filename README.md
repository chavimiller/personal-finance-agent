# personal-finance-agent

## An AI agent built in Python that reads CSV files of bank and credit card statements, cleans up the data, and automatically sorts your expenses so you can see where your money is going

The purpose of this project is to learn and implement a useful AI agent for reading through bank and credit card statements to help with tracking personal finances.

The first step of this project is to successfully read and extract the correct data from the CSV files.

Using Streamlit and pandas, I can successfully read the csv files and display the data in a table in a web browser page, however I am currently hard-coding the program to set row 3 as the column headers for simplicity at this stage. Later, I will have the AI agent detect the column headers. The headers successfully were set in the correct order, with the direction of Hebrew (right-to-left) accounted for.

Next I tested some different ways of organizing the data, first by categorizing spending per month. Next I would like to plot out the income per month, and finally the net amount.
