Spotify Playlist Parser 
--
![spotify image with logo and brand name](https://storage.googleapis.com/pr-newsroom-wp/1/2023/05/Spotify_Full_Logo_RGB_Green.png)
Get the tracks on the playlist returns the tags for tracks and names 

- does all the work without the spotify api 
- unlimited request locally 
- fast ( works through scraping and parsing the html file of playlist website ) 

things that have been implemented ( **for the python3 and fastapi server** ) 

- get the tracks and the tags as json for the usage in the frontend 
- get the tag for the particular track name in the playlist 
- get the album cover link for the track 
- get the download link for the track ( this is very slow takes around 3-4 secs ) 

things that can be implemented ( **for both golang ( gin ) and python3 server** )

- make the download link generation faster 
- use coroutines or threading for background queueing for track downloads in the static folder 
