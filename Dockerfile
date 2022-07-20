FROM nikolaik/python-nodejs

# EXPOSE 8088

ARG JAR_FILE=play-with-friends-server/build/libs/play-with-friends-server-0.0.1-all.jar

COPY ${JAR_FILE} app.jar

CMD java -jar /app.jar $PORT