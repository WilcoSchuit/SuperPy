During my time trying to complete this assignment I noticed a lot of people advised to use Pandas when working with csv files. Although I was told not to dig into Pandas as it still might be too complex to understand for a beginner like me, I still decided to give it a shot. I was able to implement Pandas for calculating the revenue, the costs and the profit. I'd read through the lines within the csv files and sum the values(prices) of each product/line where the buy or sell dates would match the date that was inserted by the user in the command line.
I've been struggling a lot with getting the inventory to work, but with a bit of help I managed to get it to work eventually. First I created a function 'generate_inventory' which requires 3 arguments: bought_csv, sold_csv and day. The function loops through bought.csv and checks if the buy date for each product is less or equal than the date inserted by the user, if that date is less than the expiration date and appends the product data to an inventory list. It then loops through sold.csv and checks if the sell date for each product is less or equal than the date inserted by the user. If true, it will remove the product from the inventory list. I then created a function 'update_inventory' which requires 2 arguments: inventory and day. It generates the inventory list with the previous mentioned function. It loops through that list, extracts the data for each product that's required to generate a report and appends that data to a temporary list: temp_inventory. Next it loops through temp_inventory, counts the duplicate products in the list and appends that count to another list: temp_updated_inventory. It eventually loops through that list and if the product doesn't exist in updated_inventory it gets added. That way there won't be any duplicate lines shown when generating the inventory report.
I also noticed that when trying to return the profit of a given date, there's a possibility the output will be negative. The profit wont be a profit, but a loss. I used Rich to show the output text in bright red whenever the profit turns out to be a loss and bright green if it turns out to actually be a profit.