# Citation for app.py:
# Date: 3/1/2024
# Adapted from app.py in bsg_people_app from CS340 Flask Starter App
# Source: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py



from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os
from flask import jsonify



# This configures the flask app to use the mySQL database. 

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = '****'
app.config['MYSQL_PASSWORD'] = '****' 
app.config['MYSQL_DB'] = '***'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"


mysql = MySQL(app)

#routes
#routes to homepage. This renders the index file

@app.route('/')
def root():
    return render_template('index.j2')


#This route is when the user visits the classes page. It handles the READ and ADD functionality. 
@app.route("/classes", methods = ["POST", "GET"])
def classes():
    if request.method == "GET":
        
        #This code stores the SQL query in a variable valled query 2
        query2 = "SELECT Classes.classID, Classes.type, Classes.classDate, Classes.classTime, Classes.cost, Classes.level, CONCAT(Trainers.firstName, ' ', Trainers.lastName) as trainerName, Classes.gymID FROM Classes JOIN Trainers ON Classes.trainerID = Trainers.trainerID ORDER BY Classes.classID ASC"
        # This is a cursor object that connects to our database. 
        cursor = mysql.connection.cursor()
        #This line execute the query stored in query2. It gets sent to the server
        cursor.execute(query2)
        #This line fetches all the rows from the query and stores it in a class_data variable. 
        class_data= cursor.fetchall()
        
        
        #This block of code gets all the different specialists from trainers and stores it in a varibale specialist_data. It will be used populate the drop down menu in jinja template. 
        query3 = "SELECT DISTINCT specialistType FROM Trainers"
        cursor = mysql.connection.cursor()
        cursor.execute(query3)
        specialist_data= cursor.fetchall()
        
        #This block of code gets the gymID and address from the gyms and stores it in a variable gym_data. It will be used populate the drop down menu in the jinja template. 
        query4= "SELECT gymID, CONCAT(gymID, ' - ', address) as Info FROM Gyms"
        cursor = mysql.connection.cursor()
        cursor.execute(query4)
        gym_data = cursor.fetchall()
        # print(gym_data)

        #This line renders classes.j2 and sends the data from the previous queries to the class.j2. 
        return render_template("classes.j2", classes=class_data, gyms = gym_data, specialists = specialist_data)

    #This code is called when the user clicks the create button (name = "Add Class")
    if request.method == "POST":
        if request.form.get("Add Class"): 
            #All the user inputs are stored in varibales. Inside the [] is the input name value ( ex. name = "classType")
            classType = request.form["classType"]
            classDate = request.form["classDate"]
            classTime = request.form["classTime"]
            cost = request.form["cost"]
            level = request.form["level"]
            trainerID = request.form["trainerID"]
            gymID = request.form["gymID"]

            #This block of code takes the user selections and uses them as VALUES to go into the Classes page. 
            query4 = "INSERT INTO Classes(type, classDate, classTime, cost, level, trainerID, gymID) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor = mysql.connection.cursor()
            #The execute takes the values in the variables defined above to execute the query stored in query4.
            cursor.execute(query4, (classType, classDate, classTime, cost, level, trainerID, gymID))
            #commit is used to tell the database to make the changes listed in the Insert query. 
            mysql.connection.commit()

            return redirect("/classes")


#This route is called when edit is clicked on the table. The classID of that particular row is passed here.
#It handles the UPDATE functionality. 
@app.route("/edit_classes/<int:classID>", methods = ["POST", "GET"])
def edit_classes(classID):

    #This block of code gets the classes data of the classID the user selected and will be display it on a table (READ functionality)
    if request.method == "GET":
        query =  "SELECT Classes.classID, Classes.type, Classes.classDate, Classes.classTime, Classes.cost, Classes.level, CONCAT(Trainers.firstName, ' ', Trainers.lastName) as trainerName, Classes.gymID FROM Classes JOIN Trainers ON Classes.trainerID = Trainers.trainerID WHERE classID = %s" %(classID)
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        class_data= cursor.fetchall()
        
        #This block of code gets all the different specialists from trainers and stores it in a varibale specialist_data. 
        query2 = "SELECT DISTINCT specialistType FROM Trainers"
        cursor = mysql.connection.cursor()
        cursor.execute(query2)
        specialist_data= cursor.fetchall()
        # print(specialist_data)

        #This is a hard coded list of all the levels the gym offers. It will be used to iterate through in the jinja template  
        levels = ["Beginner", "Intermediate", "Advanced"]
        

        #This block of code gets the other trainers that match the specialist type of the class selected.
        #For example: The user wants to edit a weightlifting class. The User wants to now update the trainer. THe user will only be able to select other weightlifting trainers. They cannot select a crossfit or cardo trainer to train this class. 
        query3= "SELECT trainerID, CONCAT(firstName, ' ', lastName) as trainerName, specialistType, level, gymID FROM Trainers WHERE specialistType = (SELECT type FROM Classes WHERE classID = %s)"
        cursor = mysql.connection.cursor()
        cursor.execute(query3, (classID,))
        other_trainers = cursor.fetchall() 
        

        #This block of code gets the gym ID and address from the gyms. It will be used to populate a drop down menu.
        query4= "SELECT gymID, CONCAT(gymID, ' - ', address) as Info FROM Gyms"
        cursor = mysql.connection.cursor()
        cursor.execute(query4)
        gym_data = cursor.fetchall()
        

        #This line renders the edit classes template and sends the data from the previous queries to the template. 
        return render_template("edit_classes.j2", class_data =class_data, specialists = specialist_data, levels=levels, other_trainers=other_trainers, gym_data = gym_data)

    #This method is called if the user wants to update a class. 
    if request.method == "POST":
        #All the user inputs are stored in varibales. Inside the [] is the input name value (input for classType had a name = "classType")
        if request.form.get("Update Class"):
            classID = request.form["classID"]
            classType = request.form["classType"]
            classDate = request.form["classDate"]
            classTime = request.form["classTime"]
            cost = request.form["cost"]
            level = request.form["level"]
            trainerID = request.form["trainerID"]
            gymID = request.form["gymID"]

            #This block of code takes the user selections and uses them as VALUES to go into the Classes page. 
            query = "UPDATE Classes SET type = %s, classDate = %s, classTime = %s, cost = %s, level = %s, trainerID = %s, gymID =%s  WHERE classID = %s"
            cursor = mysql.connection.cursor()
            #The execute takes the values in the variables defined above to execute the query stored in query. Commit then tells the database to make the changes listed in the Update statement. 
            cursor.execute(query, (classType, classDate, classTime, cost, level, trainerID, gymID, classID))
            mysql.connection.commit()

            return redirect("/classes")



#This route is called by the classes.j2 template. It will get all the trainers that match the users selections for gymID, level, and specialistType. 
@app.route("/trainer_filter", methods = ["POST", "GET"])
def get_filter_data():
    #This stores the user selections in varibles. 
    if request.method == "POST":
        gymID = request.form['gymID']
        level = request.form['level']
        specialistType = request.form['classType']
        
        #This block of code will get the trainers that match the search criteria. 
        query = "SELECT trainerID, CONCAT(firstName, ' ' ,lastName) as trainerName from Trainers WHERE gymID = %s AND level =%s AND specialistType =%s " 
        cursor = mysql.connection.cursor()
        cursor.execute(query, (gymID, level, specialistType))
        trainer_filter_data = cursor.fetchall()
        
        
        #This line will put that data as a list of dictionaries and store it in a varibale called trainers
        trainers = [{'trainerID': trainer['trainerID'], 'trainerName': trainer['trainerName']} for trainer in trainer_filter_data]
        

        # Convert the trainers to JSON format and send it back the template. 
        json_data = json.dumps(trainers)
        

        return json_data
        

        


#This route is called when the user presses the delete button. The classID of that row is passed to this route and used to delete that particular class.
#This route hands the DELETE functionality of the Classes page 
@app.route("/delete_class/<int:classID>")
def delete_class(classID):
    query = "DELETE FROM Classes WHERE classID =%s"
    cursor = mysql.connection.cursor()
    cursor.execute(query, {classID,})
    mysql.connection.commit()
    return redirect("/classes")



#This route handles the gyms READ and ADD functionality.
@app.route("/gyms", methods =["POST", "GET"])
def gyms():
    # Grab membership data and send to template to display
    if request.method == "GET":
        # mySQL query to grab all memberships data from database
        query = "SELECT * FROM Gyms"
        # cursor object (part of mySQL) connects to our database
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall() 
        # pass all query data from database to the template as variable memberships
        return render_template("gyms.j2", gym_data=data)

    # create/add a new gym
    if request.method == "POST":
        # execute if user presses the Add Membership button
        if request.form.get("Add_Gym"):
            # grab user form inputs
            address = request.form["address"]
            phone = request.form["phone"]
            manager = request.form["manager"]

            query = "INSERT INTO Gyms (address, phone, manager) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (address, phone, manager))
            mysql.connection.commit()

            return redirect("/gyms")

@app.route("/edit_gym/<int:gymID>", methods = ["POST", "GET"])
def edit_gym(gymID):
    if request.method == "GET":
        query = "SELECT * FROM Gyms WHERE gymID = %s" % (gymID)
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        #Mysql query to get the gymID for the dropdown.
        query2 = "SELECT gymID from Gyms"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        gymno = cur.fetchall()
        # render the edit gym page passing our query data and gym ID to edit gym template. 
        return render_template("edit_gym.j2", data=data, gymno=gymno)

    if request.method == "POST":
        #if user clicks Update Gym button
        if request.form.get("Update_Gym"):
            # grab user form inputs
            gymID = request.form["gymID"]
            address = request.form["address"]
            phone = request.form["phone"]
            manager = request.form["manager"]

            query = "UPDATE Gyms SET address=%s, phone=%s, manager=%s WHERE gymID = %s;"
            cursor = mysql.connection.cursor()
            cursor.execute(query, (address, phone, manager, gymID))
            mysql.connection.commit()

            return redirect("/gyms")




    
# This route handles the READ and ADD functionality of the trainers table.
@app.route("/trainers", methods = ["POST", "GET"])
def trainers():
    #This method gets the the trainer information which will be used to populate the table in the jinja template
    if request.method == "GET":
        query = "SELECT * FROM Trainers"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        trainer_data = cursor.fetchall()
        

        #This block of code selects all the gyms information and stores it a variable. 
        query2 = "SELECT * from Gyms"
        cursor = mysql.connection.cursor()
        cursor.execute(query2)
        gym_data = cursor.fetchall()
        print(gym_data)
        

        #This line renders the trainers.j2 template and gets the data from the previous queries to the template. 
        return render_template("trainers.j2", trainers=trainer_data, gyms=gym_data)

    
    #This method is called if the user clicks the create trainer button (name = "Add Trainer")
    if request.method == "POST":
        if request.form.get("Add Trainer"):
            #The user selections are stored in variables
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            specialistType = request.form["specialistType"]
            specialistType = specialistType.capitalize()
            level = request.form["level"]
            gymID = request.form["gymID"]


            #This block of code takes the user selections and uses them as VALUES to go into the Trainers page. 
            query3 = "INSERT INTO Trainers(firstName, lastName, specialistType, level, gymID) VALUES (%s, %s, %s, %s, %s) "
            cursor = mysql.connection.cursor()
            #This line execute the query using the values stored in the varibales defined above. Commit then tells the database to make the changes listed in the Insert query. 
            cursor.execute(query3, (firstName, lastName, specialistType, level, gymID ))
            mysql.connection.commit()

            return redirect("/trainers")
            


#This route is when the user clicks the edit button on a row of the trainers table. The trainerID will get passed to this route. 
@app.route("/edit_trainer/<int:trainerID>", methods = ["POST", "GET"])
def edit_trainer(trainerID):
    #This method selects the trainer information that matches the trainerID that was passed in. This will be used to display the table on the edit page. 
    if request.method == "GET":
        query = "SELECT * FROM Trainers WHERE trainerID = %s" % (trainerID)
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        trainer_data = cursor.fetchall()
        
        #This block of code will get all the gym info from each gym and store it in a variable. 
        query2 = "SELECT * from Gyms"
        cursor = mysql.connection.cursor()
        cursor.execute(query2)
        gym_data = cursor.fetchall() 

        #This is a hard coded list of levels that is stored in a variable and will be sent to the template
        levels = ["Beginner", "Intermediate", "Advanced"]
        
        #The line renders a template and sends the data sets from the previous queries to the template. 
        return render_template('edit_trainers.j2', trainer_data=trainer_data, gyms = gym_data, levels=levels) 


    #This method is called if the user clicks the update button (name = "Update Trainer")
    if request.method == "POST":
        if request.form.get("Update Trainer"): 
            #The user selections are stored in variables. 
            trainerID = request.form["trainerID"]
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            specialistType = request.form["specialist"]
            level = request.form["level"]
            gymID = request.form["gymID"]

            #This query sets up a update statement with placeholders for the attributes. 
            query = "UPDATE Trainers SET firstName =  %s, lastName = %s, specialistType = %s, level = %s, gymID = %s WHERE trainerID = %s"
            cursor = mysql.connection.cursor()
            #The query is execute with the variables defined above. Thesee will be inserted into the placeholders. Commit then tells the database to make the changes listed in the Update statement. 
            cursor.execute(query, (firstName, lastName, specialistType, level, gymID, trainerID))
            mysql.connection.commit()

            return redirect("/trainers")

            

#This route is for when the user clikcs the delete button for a particlar row in the trainer table. The trainerID of the row gets passed into this route and is used for the delete statement
#This route handles the DELETE functionality in the trainers table
@app.route("/delete_trainer/<int:trainerID>")
def delete_trainer(trainerID):
    query = "DELETE FROM Trainers WHERE trainerID = %s"
    cursor = mysql.connection.cursor()
    cursor.execute(query, (trainerID,))
    mysql.connection.commit()
    return redirect("/trainers")



#This route handles the READ and UPDATE functionality of the Customers table
@app.route("/customers", methods = ["POST", "GET"])
def customers():
    #This method selects the customer data and membership tier data to display on a table on the jinja template
    if request.method == "GET":
        query = "SELECT Customers.customerID,Customers.firstName, Customers.lastName, Customers.email, Customers.phone, Memberships.tier FROM Customers LEFT JOIN Memberships ON Customers.memID = Memberships.memID ORDER BY Customers.customerID ASC;"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        customer_data = cursor.fetchall()
        
        
        #This block of code gets all the information about memberships and stores it in a variable
        query2 = "SELECT * FROM Memberships"
        cursor = mysql.connection.cursor()
        cursor.execute(query2)
        data = cursor.fetchall()
        
        #This line renders the customers.j2 template and sends the datasets from the previouss queries to the template. 
        return render_template('customers.j2', customers=customer_data, data=data)


    #This method is called when the customer clicks the create button on the customers page. The name value is "Add customer"
    if request.method == "POST":
        if request.form.get("Add Customer"):
            #The user selections of the Add Customer form are stored in variables.  
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            email = request.form["email"]
            phone = request.form["phone"]
            memID = request.form["tier"]

            #This query sets up a update statement with placeholders for the attributes. 
            query3 = "INSERT INTO Customers (firstName, lastName, email, phone, memID) VALUES (%s, %s, %s, %s, %s)"
            cursor = mysql.connection.cursor()
            #The query is execute with the variables defined above. Thesee will be inserted into the placeholders. Commit then tells the database to make the changes listed in the Update statement. 
            cursor.execute(query3, (firstName, lastName, email, phone, memID))
            mysql.connection.commit()

            #After inserting the user is taken back to the customers page. 
            return redirect("/customers")

    
#This route is for when the user clikcs the delete button for a particlar row in the customer table. The customerID of the row gets passed into this route and is used for the delete statement
#This route handles the DELETE functionality in the customer table
@app.route("/delete_customer/<int:customerID>")
def delete_customer(customerID):
    query = "DELETE FROM Customers WHERE customerID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (customerID,))
    mysql.connection.commit()
    return redirect("/customers")


#This route handles the UPDATE functionality of the customer page. It is used when a user clicks the edit button of a particilar row in the customers table. The customerID of that row is also passed to this route.
@app.route("/edit_customer/<int:customerID>", methods = ["POST", "GET"])
def edit_customer(customerID):
    #This method gets the customer data for the particular row that was selected based on the customerID. This info will be used to populate a table. 
    if request.method == "GET":
        query = "SELECT Customers.customerID,Customers.firstName, Customers.lastName, Customers.email, Customers.phone, Memberships.tier FROM Customers LEFT JOIN Memberships ON Customers.memID = Memberships.memID WHERE customerID = %s" %(customerID) #A little confused on how the last part of this line works. 
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        customer_data = cursor.fetchall()
        

        #This block of code selects all information about memberships and stores it in a variable.
        query2 = "SELECT * FROM Memberships"
        cursor = mysql.connection.cursor()
        cursor.execute(query2)
        membership_data = cursor.fetchall()
        
        #This line renders a template and sends the datasets of the previoius queries to the template
        return render_template("edit_customers.j2", customer_data=customer_data, memberships = membership_data)


    #This method is called when the user clicks the update trainer trainer button
    if request.method == "POST":
        if request.form.get("Update Customer"):
            #The user selections are stored in variables. 
            customerID = request.form["customerID"]
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            email = request.form["email"]
            phone = request.form["phone"]
            memID = request.form["tier"]
            
            #This conditional checks if the user selected None for the membership. If so it means the memID is null and it gets updated accordingly using placeholders and the variables defined above. 
            if memID == "NULL": 
                query = "UPDATE Customers SET Customers.firstName = %s, Customers.lastName = %s, Customers.email = %s, Customers.phone=%s, Customers.memID=NULL WHERE customerID = %s"
                cursor = mysql.connection.cursor()
                cursor.execute (query, (firstName, lastName, email, phone, customerID))
                mysql.connection.commit()

            ##This query sets up a update statement with placeholders for the attributes.
            else: 
                query = "UPDATE Customers SET firstName = %s, lastName = %s, email = %s, phone=%s, memID = %s WHERE customerID = %s"
                cursor = mysql.connection.cursor()
                #The query will execute with the variables defined above. These will be inserted into the placeholders. Commit then tells the database to make the changes listed in the Update statement. 
                cursor.execute (query, (firstName, lastName, email, phone, memID, customerID))
                mysql.connection.commit()

        #The user is taken back to the customer page after the update is made. 
        return redirect("/customers")



#This route handles the READ and ADD functionality of the Customer Classes page. 
@app.route("/customerclasses", methods =["POST", "GET"])
def customerclasses():
     # Grab data and send to template to display
    if request.method == "GET":
        # first grab customerclassID PK from intersection table
        query = "SELECT CustomerClasses.customerclassID, CONCAT(Classes.type, ' - ', Classes.level, ' - ', Classes.classDate, ' at ', Classes.classTime, ' - Gym ', Classes.gymID) as ClassInfo, CONCAT(Customers.firstName, ' ', Customers.lastName) as Name FROM CustomerClasses INNER JOIN Customers ON Customers.customerID=CustomerClasses.customerID JOIN Classes ON Classes.classID=CustomerClasses.classID ORDER BY customerclassID ASC"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall() 

        # uncomment next 2 lines and comment out above line + final line to view json data
        # results = json.dumps(cur.fetchall())
        # return results 

        # next 2 queries populate the dropdown in add form
        query2 = "SELECT * FROM Classes ORDER BY type, gymID, classDate, classTime"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        classdata = cur.fetchall()
        

        query3 = "SELECT * FROM Customers"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        customerdata = cur.fetchall()
        

        return render_template("customerclasses.j2", data=data, classdata=classdata, customerdata=customerdata)

    if request.method == "POST":
        # execute if user presses the Add button
        if request.form.get("Enroll"):
            # grab user form inputs 
            customerID = request.form["customerID"]
            classID = request.form["classID"]

            query = "INSERT INTO CustomerClasses (customerID, classID) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (customerID, classID))
            mysql.connection.commit()

            return redirect("/customerclasses")
        



# This route is called when the user clicks the edit button on a particular row of the customer classes table. The customerclassID is passed to this route.
@app.route("/edit_cc/<int:customerclassID>", methods = ["POST", "GET"])
def edit_cc(customerclassID):
    if request.method == "GET":
        query = "SELECT CustomerClasses.customerclassID, CONCAT(Classes.type, ' - ', Classes.level, ' - ', Classes.classDate, ' at ', Classes.classTime) as ClassInfo, CONCAT(Customers.firstName, ' ', Customers.lastName) as Name FROM CustomerClasses INNER JOIN Customers ON Customers.customerID=CustomerClasses.customerID JOIN Classes ON Classes.classID=CustomerClasses.classID WHERE customerclassID=%s;" % (customerclassID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall() 
        
         # next 2 queries populate the dropdown in edit form
        query2 = "SELECT * FROM Classes"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        classdata = cur.fetchall()
        

        query5 = "SELECT CustomerClasses.customerclassID, CONCAT(Classes.type, ' - ', Classes.level, ' - ', Classes.classDate, ' at ', Classes.classTime, ' - Gym ', Classes.gymID) as ClassInfo, CONCAT(Customers.firstName, ' ', Customers.lastName) as Name, Customers.customerID, Classes.classID FROM CustomerClasses INNER JOIN Customers ON Customers.customerID=CustomerClasses.customerID JOIN Classes ON Classes.classID=CustomerClasses.classID;"
        cur = mysql.connection.cursor()
        cur.execute(query5)
        datatest = cur.fetchall() 
        
        query3 = "SELECT customerID, CONCAT(firstName,' ',lastName) as Name FROM Customers"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        customerdata = cur.fetchall()
        

        return render_template("edit_cc.j2", data=data, classdata=classdata, customerdata=customerdata, datatest=datatest)

    if request.method == "POST":
        if request.form.get("Update_CC"):
            # grabs user changes
            customerID = request.form["customerID"]
            classID = request.form["classID"]

            query = "UPDATE CustomerClasses SET customerID = %s, classID = %s WHERE customerclassID = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (customerID, classID, customerclassID))
            mysql.connection.commit()

        return redirect("/customerclasses")



#This route is for when the user clikcs the delete button for a particlar row in the customer classes table. The customerclassID of the row gets passed into this route and is used for the delete statement
#This route handles the DELETE functionality in the Customer Classes table
@app.route("/delete_cc/<int:customerclassID>")
def delete_cc(customerclassID):
    query = "DELETE FROM CustomerClasses WHERE customerclassID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (customerclassID,))
    mysql.connection.commit()

    return redirect("/customerclasses")



#This route handles the READ and ADD functionality of the memberships page. 
@app.route("/memberships", methods = ["POST", "GET"])
def memberships():
    #This method gets all the memberships information and stores it in variable. It will be used to populate a table. 
    if request.method == "GET":
        query = "SELECT * FROM Memberships;"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        memberships_data = cursor.fetchall()
        
        return render_template('memberships.j2', memberships=memberships_data)

    #This method is called when the user clicks the add membership button (name="Add Memberships")
    if request.method =="POST":
        if request.form.get("Add Memberships"):
            #The user selections are stored in variables
            tier = request.form["memTier"]
            length = request.form["length"]
            cost = request.form["cost"]

            #This query sets up a update statement with placeholders for the attributes. 
            query = "INSERT INTO Memberships (tier, length, cost) VALUES (%s,%s,%s)"
            cursor = mysql.connection.cursor()
            #This line executes the query with the variables defined above passed in to replace the placeholders
            cursor.execute(query, (tier, length, cost))
            mysql.connection.commit()

            return redirect("/memberships")


#This route is called when the user clicks the edit button on a particular row of the memberships table. The memID of that row is passed in to the route. 
#This route handles the UPDATE functionality of the memberships. 
@app.route("/edit_membership/<int:memID>", methods = ["POST", "GET"])
def edit_membership(memID):
    if request.method == "GET":
        #This method geta ll the membership information based on the memID selected. It is used to populate a table. 
        query = "SELECT * FROM Memberships WHERE memID = %s" % (memID)
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
    
        #This block of code gets all the tier names from the memberships. It will be used for a drop down menu 
        query2 = "SELECT tier from Memberships"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        tier_data = cur.fetchall()

        #This line renders the edit memberships template and passes the data sets defined above to the template
        return render_template("edit_membership.j2", data=data, tier_data=tier_data)


    if request.method == "POST":
        #This method is called if the user clicks the Update Membership button
        if request.form.get("Update Membership"):
            #The user selected variables are stored in variables. 
            memID = request.form["memID"]
            tier = request.form["tier"]
            length = request.form["length"]
            cost = request.form["cost"]

            #This block of code updates the membership table with placeholders passed in as values. 
            query = "UPDATE Memberships SET tier= %s, length=%s, cost =%s WHERE memID = %s"
            cursor = mysql.connection.cursor()
            #This executes the query with the variables defined above to replace the placeholders.  Commit then tells the database to make the changes listed in the Update statement.
            cursor.execute(query, (tier, length, cost, memID))
            mysql.connection.commit()
            
            #The user is then redirected to the memberships page
            return redirect("/memberships")

        

#This route is for when the user clikcs the delete button for a particlar row in the memberships table. The memID of the row gets passed into this route and is used for the delete statement
#This route handles the DELETE functionality in the memberships table
@app.route("/delete_membership/<int:memID>")
def delete_membership(memID):
    query = "DELETE FROM Memberships WHERE memID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (memID,))
    mysql.connection.commit()

    return redirect("/memberships")




# Listener
if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    app.run(port=6569, debug=True)
