FROM python:3.10
LABEL Maintainer="valtrois"

COPY entrypoint.sh /entrypoint.sh
RUN chmod 755 /entrypoint.sh

# this commands prevent container from closing
CMD ["tail", "-f", "/dev/null"]
ENTRYPOINT ["/entrypoint.sh"]
