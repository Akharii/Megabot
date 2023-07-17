# set base image (host OS)

FROM python:3

# set the working directory in the container
WORKDIR /code

# copy the python package to the working directory
COPY megabot/ megabot/

# install the megabot package
RUN pip install .

# command to run on container start
CMD [ "python", "-m", "megabot" ]
