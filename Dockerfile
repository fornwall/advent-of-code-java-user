FROM ubuntu:23.04
RUN apt-get update && \
    apt-get install --no-install-recommends --yes openjdk-17-jdk
WORKDIR /src
ENTRYPOINT ["./gradlew", "--no-daemon", "test", "--info"]
