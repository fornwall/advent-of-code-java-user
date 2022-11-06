FROM ubuntu:22.04
RUN apt-get update && \
    apt-get install --no-install-recommends --yes openjdk-17-jdk
WORKDIR /src
ENV GRADLE_OPTS="-Xmx1024m"
ENTRYPOINT ["./gradlew", "test", "--info"]
