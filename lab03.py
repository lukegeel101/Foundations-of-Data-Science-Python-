#!/usr/bin/env python
# coding: utf-8

# # Lab 3: Tables
# 
# This lab is to be taken on Friday 9/23. Students should submit the lab on Gradescope when done
# 
# Welcome to lab 3!  This week, the lab will continue the focus on *tables*, which let us work with multiple arrays of data.  Tables are described in [Chapter 6](https://umass-data-science.github.io/190fwebsite/textbook/06/tables/) of the text.
# 
# First, set up the tests and imports by running the cell below.

# In[1]:


import otter
from datascience import *
import numpy as np
grader = otter.Notebook()


# # 1. Using lists
# 
# A *list* is another Python sequence type, similar to an array. It's different than an array because the values it contains can all have different types. A single list can contain `int` values, `float` values, and strings. Elements in a list can even be other lists! A list is created by giving a name to the list of values enclosed in square brackets and separated by commas. For example, `values_with_different_types = ['190', F, ['lab', 3]]`
# 
# Lists can be useful when working with tables because they can describe the contents of one row in a table, which often  corresponds to a sequence of values with different types. A list of lists can be used to describe multiple rows.
# 
# Each column in a table is a collection of values with the same type (an array). If you create a table column from a list, it will automatically be converted to an array. A row, on the ther hand, mixes types.
# 
# Here's a table from Chapter 5. (Run the cell below.)

# In[2]:


# Run this cell to recreate the table
flowers = Table().with_columns(
    'Number of petals', make_array(8, 34, 5),
    'Name', make_array('lotus', 'sunflower', 'rose')
)
flowers


# **Question 1.1.** Create a list (use []) that describes a new fourth row of this table. The details can be whatever you want, but the list must contain two values: the number of petals (an `int` value) and the name of the flower (a string). For example, your flower could be "pondweed"! (A flower with zero petals)

# In[6]:


my_flower = [100,'rose']
my_flower


# In[7]:


grader.check("q1.1")


# **Question 1.2.** `my_flower` fits right in to the table from chapter 5. Complete the cell below to create a table of seven flowers that includes your flower as the fourth row followed by `other_flowers`. You can use `with_row` to create a new table with one extra row by passing a list of values and `with_rows` to create a table with multiple extra rows by passing a list of lists of values.

# In[14]:


# Use the method .with_row(...) to create a new table that includes my_flower 

four_flowers = flowers.with_row(my_flower)

# Use the method .with_rows(...) to create a table that 
# includes four_flowers followed by other_flowers

other_flowers = [[10, 'lavender'], [3, 'birds of paradise'], [6, 'tulip']]

seven_flowers = four_flowers.with_rows(other_flowers)
seven_flowers


# In[15]:


grader.check("q1.2")


# ## 2. Analyzing datasets
# With just a few table methods, we can answer some interesting questions about the IMDb dataset. This data set includes information about movie ratings.

# In[16]:


imdb = Table.read_table("imdb.csv")
imdb


# If we want just the ratings of the movies, we can get an array that contains the data in that column:

# In[17]:


imdb.column("Rating")


# The value of that expression is an array, exactly the same kind of thing you'd get if you typed in `make_array(8.4, 8.3, 8.3, [etc])`.
# 
# **Question 2.1.** Find the rating of the highest-rated movie in the dataset.
# 
# *Hint:* Think back to the functions you've learned about for working with arrays of numbers.  Ask for help if you can't remember one that's useful for this.

# In[23]:


highest_rating = max(imdb["Rating"])
highest_rating


# In[24]:


grader.check("q2.1")


# That's not very useful, though.  You'd probably want to know the *name* of the movie whose rating you found!  To do that, we can sort the entire table by rating, which ensures that the ratings and titles will stay together. Note that calling sort creates a copy of the table and leaves the original table unsorted.

# In[25]:


imdb.sort("Rating")


# Well, that actually doesn't help much, either -- we sorted the movies from lowest -> highest ratings.  To look at the highest-rated movies, sort in reverse order:

# In[26]:


imdb.sort("Rating", descending=True)


# (The `descending=True` bit is called an *optional argument*. It has a default value of `False`, so when you explicitly tell the function `descending=True`, then the function will sort in descending order.)
# 
# So there are actually 2 highest-rated movies in the dataset: *The Shawshank Redemption* and *The Godfather*.
# 
# Some details about sort:
# 
# 1. The first argument to `sort` is the name of a column to sort by.
# 2. If the column has strings in it, `sort` will sort alphabetically; if the column has numbers, it will sort numerically.
# 3. The value of `imdb.sort("Rating")` is a *copy of `imdb`*; the `imdb` table doesn't get modified. For example, if we called `imdb.sort("Rating")`, then running `imdb` by itself would still return the unsorted table.
# 4. Rows always stick together when a table is sorted.  It wouldn't make sense to sort just one column and leave the other columns alone.  For example, in this case, if we sorted just the "Rating" column, the movies would all end up with the wrong ratings.
# 
# **Question 2.2.** Create a version of `imdb` that's sorted chronologically, with the earliest movies first.  Call it `imdb_by_year`.

# In[31]:


imdb_by_year = imdb.sort("Year", descending=False)
imdb_by_year


# In[32]:


grader.check("q2.2")


# **Question 2.3.** What's the title of the earliest movie in the dataset?  You could just look this up from the output of the previous cell.  Instead, write Python code to find out.
# 
# *Hint:* Starting with `imdb_by_year`, extract the Title column to get an array, then use `item` to get its first item.

# In[33]:


earliest_movie_title = Table.column(imdb_by_year, "Title").item(0)
earliest_movie_title


# In[34]:


grader.check("q2.3")


# ## 3. Finding pieces of a dataset
# Suppose you're interested in movies from the 1940s.  Sorting the table by year doesn't help you, because the 1940s are in the middle of the dataset.
# 
# Instead, we use the table method `where`.

# In[35]:


forties = imdb.where('Decade', are.equal_to(1940))
forties


# Ignore the syntax for the moment.  Instead, try to read that line like this:
# 
# > Assign the name **`forties`** to a table whose rows are the rows in the **`imdb`** table **`where`** the **`'Decade'`**s **`are` `equal` `to` `1940`**.
# 
# **Question 3.1.** Compute the average rating of movies from the 1940s.
# 
# *Hint:* The function `np.average` computes the average of an array of numbers.

# In[42]:


average_rating_in_forties = np.average(forties["Rating"])
average_rating_in_forties


# In[43]:


grader.check("q3.1")


# Now let's dive into the details a bit more.  `where` takes 2 arguments:
# 
# 1. The name of a column.  `where` finds rows where that column's values meet some criterion.
# 2. Something that describes the criterion that the column needs to meet, called a predicate.
# 
# To create our predicate, we called the function `are.equal_to` with the value we wanted, 1940.  We'll see other predicates soon.
# 
# `where` returns a table that's a copy of the original table, but with only the rows that meet the given predicate.
# 
# **Question 3.2.** Create a table called `ninety_nine` containing the movies that came out in the year 1999.  Use `where`.

# In[44]:


ninety_nine = imdb.where('Year', are.equal_to(1999))
ninety_nine


# In[45]:


grader.check("q3.2")


# So far we've only been finding where a column is *exactly* equal to a certain value. However, there are many other predicates.  Here are a few:
# 
# |Predicate|Example|Result|
# |-|-|-|
# |`are.equal_to`|`are.equal_to(50)`|Find rows with values equal to 50|
# |`are.not_equal_to`|`are.not_equal_to(50)`|Find rows with values not equal to 50|
# |`are.above`|`are.above(50)`|Find rows with values above (and not equal to) 50|
# |`are.above_or_equal_to`|`are.above_or_equal_to(50)`|Find rows with values above 50 or equal to 50|
# |`are.below`|`are.below(50)`|Find rows with values below 50|
# |`are.between`|`are.between(2, 10)`|Find rows with values above or equal to 2 and below 10|
# 
# The textbook section on selecting rows has more examples.
# 

# **Question 3.3.** Using `where` and one of the predicates from the table above, find all the movies with a rating higher than 8.5.  Put their data in a table called `really_highly_rated`.

# In[46]:


really_highly_rated = imdb.where('Rating', are.above(8.5))
really_highly_rated


# In[47]:


grader.check("q3.3")


# **Question 3.4.** Find the average rating for movies released in the 20th century and the average rating for movies released in the 21st century for the movies in `imdb`.
# 
# *Hint*: Think of the steps you need to do (take the average, find the ratings, find movies released in 20th/21st centuries), and try to put them in an order that makes sense.

# In[57]:


average_20th_century_rating = np.average(imdb.where('Year', are.below(2000))["Rating"])
average_21st_century_rating = np.average(imdb.where('Year', are.above_or_equal_to(2000))["Rating"])
print("Average 20th century rating:", average_20th_century_rating)
print("Average 21st century rating:", average_21st_century_rating) 


# In[58]:


grader.check("q3.4")


# The property `num_rows` tells you how many rows are in a table.  (A "property" is just a method that doesn't need to be called by adding parentheses.)

# In[59]:


num_movies_in_dataset = imdb.num_rows
num_movies_in_dataset


# **Question 3.5.** Use `num_rows` (and arithmetic) to find the *proportion* of movies in the dataset that were released in the 20th century, and the proportion from the 21st century.
# 
# *Hint:* The *proportion* of movies released in the 20th century is the *number* of movies released in the 20th century, divided by the *total number* of movies.

# In[61]:


proportion_in_20th_century = imdb.where('Year', are.below(2000)).num_rows / imdb.num_rows
proportion_in_21st_century = imdb.where('Year', are.above_or_equal_to(2000)).num_rows / imdb.num_rows
print("Proportion in 20th century:", proportion_in_20th_century)
print("Proportion in 21st century:", proportion_in_21st_century)


# In[62]:


grader.check("q3.5")


# **Question 3.6.** Here's a challenge: Find the number of movies that came out in *even* years.
# 
# *Hint:* The operator `%` computes the remainder when dividing by a number.  So `5 % 2` is 1 and `6 % 2` is 0.  A number is even if the remainder is 0 when you divide by 2.
# 
# *Hint 2:* `%` can be used on arrays, operating elementwise like `+` or `*`.  So `make_array(5, 6, 7) % 2` is `array([1, 0, 1])`.
# 
# *Hint 3:* Create a column called "Year Remainder" that's the remainder when each movie's release year is divided by 2.  Make a copy of `imdb` that includes that column.  Then use `where` to find rows where that new column is equal to 0.  Then use `num_rows` to count the number of such rows.

# In[71]:


year_remainder = imdb["Year"] % 2
imdb2 = imdb
imdb2['year_remainder'] = year_remainder
num_even_year_movies = imdb2.where('year_remainder', are.equal_to(0)).num_rows
num_even_year_movies


# In[72]:


grader.check("q3.6")


# ## 4. Summary
# 
# For your reference, here's a table of all the functions and methods we have covered in class and in the lab.
# 
# |Name|Example|Purpose|
# |-|-|-|
# |`Table`|`Table()`|Create an empty table, usually to extend with data|
# |`Table.read_table`|`Table.read_table("my_data.csv")`|Create a table from a data file|
# |`with_columns`|`tbl = Table().with_columns("N", np.arange(5), "2*N", np.arange(0, 10, 2))`|Create a copy of a table with more columns|
# |`column`|`tbl.column("N")`|Create an array containing the elements of a column|
# |`sort`|`tbl.sort("N")`|Create a copy of a table sorted by the values in a column|
# |`where`|`tbl.where("N", are.above(2))`|Create a copy of a table with only the rows that match some *predicate*|
# |`num_rows`|`tbl.num_rows`|Compute the number of rows in a table|
# |`num_columns`|`tbl.num_columns`|Compute the number of columns in a table|
# |`select`|`tbl.select("N")`|Create a copy of a table with only some of the columns|
# |`drop`|`tbl.drop("2*N")`|Create a copy of a table without some of the columns|
# |`take`|`tbl.take(np.arange(0, 6, 2))`|Create a copy of the table with only the rows whose indices are in the given array|
# 
# <br/>

# ---
# 
# To double-check your work, the cell below will rerun all of the autograder tests.

# In[73]:


grader.check_all()


# In[ ]:




