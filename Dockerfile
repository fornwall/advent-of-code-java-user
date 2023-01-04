FROM ubuntu:22.10
RUN apt-get update && \
    apt-get install --no-install-recommends --yes openjdk-17-jdk
WORKDIR /src
ENV GRADLE_OPTS="-Xmx2048m"
ENTRYPOINT ["./gradlew", "--no-daemon", "test", "--info"]
