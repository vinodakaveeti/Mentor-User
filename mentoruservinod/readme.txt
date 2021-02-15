This is a Django Mentor-User application which contains the following modules;

1.Two groups have been created - UserRole, MentorRole.

2.Custom user model is created with email as username.

3.Users can register and log in. All the users created from app will belong to UserRole Group.

4.Django Superuser can create Mentors. Mentors need to be manually given MentorRole.

5.Every user has a profile and each can post a query to any mentor. Document can also be attached.

6.Mentors can read the query and reply.

7.Serializers have been used for validation and save for User's query and Mentor's reply.

8.Swagger can be accessed here /api/docs/

#Steps For Installation;

1.Download or clone the project 

2.Run pip install -r requirements.txt

3.Migrate your tables using; python manage.py makemigrations then python manage.py migrate

4.Run python manage.py runserver 

5.With superuser, Create two roles (UserRole and MentorRole) and create Mentors(by checking is_Mentor=True and assigning Mentor role)

6.Register and Login with the application and New Mail button can be clicked to post a query to any of the mentors

