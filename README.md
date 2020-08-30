# DjangoSpotipy

DjangoSpotipy is a Web Application built using Django which uses Spotify's Web API to discover artists and albums. It lets a user add songs to their favorites/collection which they can access later under their profile page. This Django project has one app which is named `app`.

#### Spotify API

In `utils.py`, I have created a python class `SpotifyAPI` which helps in requesting data from Spotify's web API. Instantiating this class requires `client_id` & `client_secret` which are obtained by creating an account on Spotify's website. The class uses these credentials to generate an `access token` which is valid for 3600 seconds. This class performs authorization only when the access token expires. 

#### Models

The `app` contains two models - `User` and `Song`. `User` is an instance of `AbstractUser` provided by Django. Song contains the collections created by the users on this platform. 

#### HTML & JavaScript

All the html templates used in this project are contained in `app/templates/app` directory. Moreover, the javascript is contained inside script tags within these templates.  

#### Search

When a user visits `/` route, they see a search bar wherein they can search for an artist or album by selecting the dropdown menu. Once they make a search, on the backend, Django app makes a request to Spotify's API and the results are displayed in either `/artist` or `album` depending on the user's search. 

#### Artist
When a user makes a search for artist, they will be redirected to `/artist` route which displays all the relevant results. The template is designed such that it shows only 5 results per page using Django's pagination class. Clicking on any artist would take the user to that specific artist's webpage. Now, this webpage shows all the details about that artist along with their top rated songs. The webpage allows the ability to play a preview of each song and if they like a song, they can click on `Add to favorites` button to add that song into their collection.  

#### Album
When a user makes a search for album, they will be redirected to `/album` route which displays all the relevant results. The template is designed such that it shows only 5 results per page using Django's pagination class. Clicking on any album would take the user to that specific album's webpage. Now, this webpage shows all the songs in that album and provides the users with the ability to play a preview of each song and if they like a song, they can use the button to add it to their collection. 

#### Directories and Files

* `urls.py` - This file contains the `SpotifyAPI` that I build for talking to Spotify's API.
* `models.py` - It has the two models described above.
* `views.py` - Contains all the views used in this web application.
* `templatetags` - Created this directory for creating a custom template `favorites`.
* `requirements.txt` - Contains all the packages needed for running this application. 

#### Distinctiveness & Complexity
I believe this project is distinct and complex from any other projects in this course due to the following reasons -  

1. Spotify API - To complete this project, I faced several challenges getting access to and using Spotify's Web API. Its authentication process took me sometime to figure out. Moreover, the authentication is valid for only 3600 seconds or 1 hr. Thus, I have built the `SpotifyAPI` class in `utils.py` such that, if the authentication expires, it would automatically redo the authentication process. 

2. Json Data - It is easy to work with JSON data when the number of elements are few. But working with the data returned by Spotify was a little time consuming since it returned huge amount of json data. I had to look for relevant pieces and use them in my application.

3. Template Tag - I had to build a custom simple template tag to be able to find weather a user has already added a particular song to their favorite list or not. To be able to do this, I had to read through Django's official documentation and experiment.

4. Audio Tags - I have learned to use audio tags in html templates for this project. They lets a user play preview of a song and if they like it, they can add it to their collection.