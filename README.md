# si507_final_Chuhan Kelly Hou


# si507_final_Chuhan Kelly Hou


This project is a semantic analysis project that mainly visualized the words importances through their occurrence frequencies.

"	Data sources: MIT the Media lab
      o	main link: https://www-prod.media.mit.edu/research/?filter=groups
      o	required modules that needed to run this program is indicated in the requirements.txt 
      "	note, for mac users, there might be problems installing matplotlib. Here is the potential solution https://stackoverflow.com/questions/21784641/installation-issue-with-matplotlib-python
"	Programs 
      o	final_scrape.py
          "	The file used to crawling MIT the media lab webpages 
          "	2 json files were written out
          "	Media.json 
      o	Nicely formatted data scraped from the web 
          "	Hashtag.json
      o	Supplemental file for reference. Also formatted. 
      o	final_nb.py
          "	The main filed that written with all the required functionality 
          "	Set up the database in sqlite as media.db
          "	3 tables (labs,projects,hashtags)
          "	Added plotting functions 
          "	Plot out bar plot of lab sizes and labs'hashtags numbers. Also, plot out a table for a better view
              o	Plot_lab_size()
              o	Plot_lab_hashnum()
              o	Plot_table()
              "	Plot word cloud for each lab based on the project briefs of each lab 
              o	Plot_cloud()
              "	Have interaction prompt to interact with users 
      o	final_nb_test.py
            "	the unnitest file to test final_nb.py 
If you still have questions, don't wait and shoot me an email at chuhan@umich.edu 


Thank you! 
Happy Spring (Finally)





