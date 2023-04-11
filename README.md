# Password Manager

* It helps in organizing and storing your passwords of different sites and whenever required you can copy it.
* It is very handy to use, you can add new passwords, you can delete useless paswords, you can update, and copy you password.

## How to start ?

1. Open the create_db.py file run it on terminal, needed database will be created.
2. Now, open secure.py file run it on terminal a secret.key file will be created
3. Open main.py file run it. Boom!!, Application is started.

## How to use ?

* There are two entry fields:
  * Entry for SiteName
  * Entry for Password
* If you want to add new password for any site, enter the Sitename and Password you want to store and click on the Add button a Re-enter Password Page will Popup, enter the password again and Submit your data will be added to the database and besides there is a tree view, your data will be appended there.
* If you want to delete any data select it on the tree view and click on the Delete button, your data will be permanently deleted.
* If you want to update any data just double click on the any data in the tree view, it will get the details to the entry boxes, if you want to change the Sitename do so and re enter the password or want to change the password change it and click on the Update button and your data will be Updated.
* If you want to copy any Password enter the Sitename click on the Search button if data exists a Popup will come asking to copy the Password, click on yes and Boom!! Password is copied!

## How does it works ?

#### Add :

Once add button is clicked it will get the Sitename and Password, now using encrypt_message() function from secure.py it will encrypt the Password and now it will pass these values to add_record() function in db.py and a display_data() function will run to display all the current values to the tree view.

#### Delete :

Once delete button is clicked it will get the Srno of the data and will pass it to the delete_record() function in db.py which will delete the record from the database.

#### Update :

When you double tap on any data in the tree view it will retrieve the details and display it in the entry boxes now when you click Update button after makin necessary changes oonce again it will make the password secure and encrypt and will pass these values to update_record() function in db.py which will update the record in database and display on the tree view.

#### Copy :

Enter the sitename you want to copy the password click on Search button if data exists it will ask you to copy or not, if yes then it will get the srno of the data pass it to specific_record() function from db.py which will return the data of that specific site. Now, we have encrypted password which we got from the database now we will pass these encrypted password to a function decrypt_message() from secure.py it will return the original password which will be copied to your clipboard. Now, you can paste it anywhere.