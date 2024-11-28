FROM ubuntu:24.04
RUN apt-get update && \
    apt-get install --no-install-recommends --yes openjdk-21-jdk
WORKDIR /src
ENTRYPOINT ["./gradlew", "--no-daemon", "test", "--info"]
