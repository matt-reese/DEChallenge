## Objective

**Write a python script that ingests data from one of the external vendor's data sources and combine that data with our internal data set.** This combined data set should allow data team members to compare the active users of the different platforms. The script should finish in less than one hour.

## Requirements


1. The script can run in an environment with limited amounts of memory. The final solution should avoid reading all the rows from either source at one time. For example, reading in 10% of database rows and 10% of API rows and then do the matching would be acceptable. Reading in 100% of either source prior to matching would not be acceptable.
2. Pretend that the current date is 2017-02-02. There are references in the assignment that will confirm that as the "current" date.

## Details from Product Manager

Hey DE,

A vendor (Friendly Vendor) recently agreed to make their data available for us to use. Their dataset includes their users and information about whether or not the user is currently active (active within the last 30 days) on their platform. We plan on using their user data combined with our user data to measure the health of the two business. This will potentially let us predict churn on our platform based on the user's activity on Friendly Vendor's platform (if there is a correlation).

Our immediate use case requires having both sets of users and their active status from the two platforms matched up and available in our warehouse. If we establish a correlation between the two platforms then I'm confident we will want to start gathering more data.

As you build out your pipeline please keep in mind that both platforms expect their user bases to expand significantly over the upcoming year.

Below is the email I received from Friendly Vendor about the different ways of retrieving the data:

## Email from Friendly Vendor

Hey,

We have arranged for you to have access to our data! We don’t have any authentication requirements to access the data so you can directly access the following API publicly.

[User Activity API](http://REDACTED.com/users)

This REST API endpoint contains our users and their activity status. Add `?page=X` at the end of the URL to page through the users. For example `http://REDACTED.com/users?page=3` to view the third page. This directly accesses our database and we plan on creating new endpoints (such as v2, v3, etc.) if we want to make any breaking changes in the future.

Thanks,

Friendly Vendor

## Expected Output from Python Script:

**Elapsed Time:** `X minutes, X seconds` *<- Time it took to run the entire script*

**Total Matches:** `X` *<- Total number of rows matched between the Doximity dataset and the vendor dataset*

**Sample Output:** `<10 JSON formatted rows>` *<- Example of the rows that would be loaded to the warehouse*

**SQL DDL:** `CREATE TABLE…` *<- The DDL that would have been used to create the warehouse table. The overall table structure is what we will look at, this doesn't actually have to run.*

## What to Submit

1. The Python script(s) you wrote to solve this problem.
2. A `requirements.txt` file containing a list of packages required to run your script.
3. An `output.txt` file containing the output from your script that matches the expected output above.
4. An `instructions.txt` file containing instructions on how to run your submission.
5. (Optional) A `feedback.txt` file containing any thoughts or feedback from the assignment or anything you would like the reviewers to consider when reviewing. If you are making any assumptions please include them here.
