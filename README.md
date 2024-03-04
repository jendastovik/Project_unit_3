# GUI application for small business to manage their inventory and sales

# Criteria A: Planning
## Problem Definition
My client, who is an international businessman is planning on expanding his business in Frisbees. He needs a professional way not only to keep track of his orders and inventory but also an option to create a customizable item that will be added to the order. There is a need for accounts that the users can create with the key provided and log in with. After the login, the client himself and his closest coworkers can manage different orders, Finances, and inventory. The client also requires functionality to create new frisbees by choosing from different colors and shapes of disks. My client also wants to implement some marketing strategies such as a point system to keep customers entertained or special seasonal sales. Finally, the application is required to allow users to insert the name of a region they’re from, based on which there will be a specific image on the frisbee generated. This should solve the problem of a strenuous and inefficient paper-based system of keeping track of orders and lead to major time savings and error elimination.

## Proposed Solution
I’m proposing creating a GUI application because it’s going to allow the client and the customers to clearly and easily communicate. Information will be saved in a database for greater safety and fast access.[^1]

It was decided to use Python because it’s favored for GUI development due to its readable syntax, extensive libraries to choose from, cross-platform compatibility, robust community support, and seamless integration with other technologies. Its simplicity and versatility make it an excellent choice for creating graphical user interfaces for applications across different operating systems[^2]. Compared to the alternative C or C++, which share similar features, Python is a high-level programming language (HL) with high abstraction[^3]. For example, memory management is automatic in Python whereas it is the responsibility of the C/C++ developer to allocate and free up memory[^4], this could result in faster applications but also memory problems. In addition, an HL language will allow me and future developers to extend the solution or solve issues promptly.
Secondly, the choice was made to use KivyMD, a Material Design extension for the Kivy framework which offers a Pythonic solution for GUI development[^5]. Leveraging the simplicity of Python, KivyMD provides a set of pre-designed UI components with a modern Material Design aesthetic. This framework is known for its flexibility, and ability to create visually appealing and mainly responsive interfaces[^6].

Lastly, the preference for SQLite as the designated data storage solution, as opposed to alternatives like CSV files, online databases, and MySQL, is rooted in a thorough consideration of multiple factors. SQLite was selected due to its lightweight nature, making it an ideal choice for scenarios where a dedicated database server might be deemed excessive, particularly in the context of local hosting[^7]. Much like the rationale behind choosing Python for GUI development, SQLite aligns seamlessly with the project's requirements, offering simplicity, ease of use, and effortless integration across diverse platforms[^8]. The decision to opt for SQLite over CSV files ensures a structured and efficient data storage mechanism while favoring it over online databases and MySQL provides a self-contained, serverless solution with minimized dependencies[^9]. The avoidance of MySQL is particularly motivated by SQLite's suitability for local hosting, offering minimal configuration requirements, transactional capabilities, and reduced overhead without the need for a full-fledged database server[^10]. In essence, SQLite strikes a balance between simplicity, efficiency, and local hosting requirements, making it the optimal choice over MySQL and other alternatives.

[^1]: Rouse, Margaret. “Graphical User Interface.” Techopedia, 28 May 2021, www.techopedia.com/definition/5435/graphical-user-interface-gui. Accessed 4 Mar. 2024.
[^2]: Team, DataFlair. “What Is Python GUI Programming - Python Tkinter Tutorial - DataFlair.” DataFlair, 18 May 2018, www.data-flair.training/blogs/python-gui-programming/. Accessed 4 Mar. 2024.
[^3]: Python Geeks. “Advantages of Python | Disadvantages of Python.” Python Geeks, Python Geeks, 25 June 2021, www.pythongeeks.org/advantages-disadvantages-of-python/. Accessed 4 Mar. 2024.
[^4]: Real Python. “Python vs C++: Selecting the Right Tool for the Job.” Realpython.com, Real Python, 11 Sept. 2019, www.realpython.com/python-vs-cpp/#memory-management. Accessed 4 Mar. 2024.
[^5]: “KivyMD 2.0.1.Dev0 Documentation.” Readthedocs.io, 2022, www.kivymd.readthedocs.io/en/latest/. Accessed 4 Mar. 2024.
[^6]: GfG. “Building a Simple Application Using KivyMD in Python.” GeeksforGeeks, GeeksforGeeks, 12 May 2021, www.geeksforgeeks.org/building-a-simple-application-using-kivymd-in-python/. Accessed 4 Mar. 2024.
[^7]: “SQLite Home Page.” Sqlite.org, 2024, www.sqlite.org/. Accessed 4 Mar. 2024.
[^8]: “What Is MySQL? A Beginner-Friendly Explanation.” Kinsta®, 3 July 2023, kinsta.com/knowledgebase/what-is-mysql/. Accessed 4 Mar. 2024.
[^9]: “MySQL.” Mysql.com, 2024, www.mysql.com/. Accessed 4 Mar. 2024.
[^10]: GfG. “Difference between MySQL and SQLite.” GeeksforGeeks, GeeksforGeeks, 7 May 2020, www.geeksforgeeks.org/difference-between-mysql-and-sqlite/. Accessed 4 Mar. 2024.

## Design Statement
I will design a graphical user interface application. This application will be run locally on a computer and will allow users to do all mentioned tasks. All the data will be stored in also locally run database.

## Success Criteria
1. Solution provides a way for the user of the software to track the inventory of materials
2. Solution provides a way for the user to create an item sold by the company from the materials
3. Solution provides a way to track orders and keep track of the budget
4. Solution allows the user to sign in with a password and username and create new accounts for their employees
5. Solution informs the user of the time and date of the last log-in
6. Solution enables the user to create new distributors and customers, who can gather points based on which they get discounts
7. While creating an item, Solution allows to add an image generated based on the name of the region provided

# Criteria B: Design
## System Diagram
## Wireframe
## Flow Diagram
## ER Diagram
## UML Diagram

## Record of Tasks
## Test Plan

# Criteria C: Development
## Existing Tools
## List Of Techniques Used

## Development

