# Xmas Xpress
Website Link: https://xmasxpress2.herokuapp.com/ <br>
Custom Domain(not deployed): http://xmasxpress.us/ <br>
Video Link: https://www.youtube.com/watch?v=G5zqPTBA2BQ&feature=emb_logo <br>

## Inspiration
* We were inspired by the holiday themed hackathon to make a secret santa but a virtual one with tons of security and more features.
* Since the majority of things are virtual now-a-days, why not a virtual secret santa ?

## What it does
* A user has to sign up and log in to use this site.
* Once logged in, a user can create a ‘room’ where there can be many users present or can join an already existing room by using the password given to him.
* If a user creates a room, he can send room invites via email for people to join his room.
* A user can only join a room if he knows the normal password of the room.
* There is also a master password which is only known to the creator of the room which can be used to do the following features:
  * Delete a room
  * Assign secret santa and send out mails accordingly 
  * Update Room details
  * Send Invites
* The secret santa assignment is done in such a way that every person in the group can give gifts to one more person whose name is sent via email. Each given user does not know who his gift is coming from though.
* The page also shows gift recommendations according to the budget set up by the room creator.

## How we built it
We used Django
Python
HTML
CSS
Bootstrap4
Javascript
anime.js
svg


## Challenges we ran into
* This is our first ‘big’ project in terms of using django and hence we ran into a lot of trouble in creating the models and views.
* This was also our first time deploying a django project to a real world domain,i.e, the linking part with [http://xmasxpress.us/] proved quite difficult. We succedded in creating a local deployment, however linking was not made possible.


## What we learned
We Learned a lot about django and python because the majority of our project backend depended on django. We also learnt about svg animations and some more css animations.

## What's next for Xmas Xpress 
There is a lot more ground for XmasXpress to cover. Our future plans for XmasXpress include sending cryptocurrency directly to friends on festive occasions, creating a custom domain with the domain in-hand, enhancing the frontend UI even more,etc.

