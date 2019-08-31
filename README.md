# cloudsek
Submission of task for cludsek

This application incorporates two api_endpoints. 1. /download 2. /track/
1. download/
  This api uses POST method and takes a url of file to be downloaded as request body input. 
  This keeps the track of the chunk downloaded of file so far time to time.
  It returns the track_id for the current downloading file which can be used to see the downloading status of the file later on
2. track/
  This api endpoint uses GET method and takes track_id as parameter and returns the current progress in % of file being downloaded.
