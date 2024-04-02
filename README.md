# running_text_generator
Test task for IT-Solution

Build docker image `docker build -t running_text_generator .`

Start docker image `docker run -p 7000:7000 running_text_generator`

Generate video by using `http://127.0.0.1:7000/generate-video/?runtext=<Text for app>`
