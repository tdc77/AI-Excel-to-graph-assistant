AI EXCEL to graph assistant. Uses openAI_API will need API key.



Its best to put excel file in same folder as progam as it seems to have trouble finding it if not.




Put your OPEN_AI key in the .env file.




![AI_KEY](https://github.com/user-attachments/assets/104a6184-fd48-44cf-a003-5dab77076032)






As I mentioned put excel file in same dir as program for best results.



![FolderLOc](https://github.com/user-attachments/assets/03920766-cd09-47a5-bb9e-41aedd18a123)





If you do you can just copy path and put where you need the path in the prompt.



![copypath](https://github.com/user-attachments/assets/30875902-f674-4a55-9fee-363a4b6fac50)



When dont it will say Finished with the info it used for shhet and columns for debugging purposes.
scroll up a bit and you should also see the name it gave to your graph pic.



![Finished](https://github.com/user-attachments/assets/315baf49-2472-4338-98a4-3c719f8ebfff)




It will put the pic in your documents folder, with a funny name.



![picpath](https://github.com/user-attachments/assets/d5d964cd-925f-4c0c-8b6e-8c1798de1502)







It will save your chart as a png file.



![chartsave](https://github.com/user-attachments/assets/3c5b41f1-42c6-490c-a3a7-cb50f89a117b)





I have included my test excel file for testing.



TEST PROMPTS:
Here are the prompts I used so it works. Change the items in quotation marks for your needs.

I need to create a line graph from an excel file located at "your path here". Use sheet name 'Your sheet name", x axis use column 'column for data" and for y axis use column "other column for data".

I need to create a scatter plot from an excel file located at "your path here". Use sheet name 'Your sheet name", x axis use column 'column for data" and for y axis use column "other column for data"

I need to create a bar graph from an excel file located at "your path here". Use sheet name 'Your sheet name", x axis use column 'column for data" and for y axis use column "other column for data"
