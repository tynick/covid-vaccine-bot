# normally, we try to use python:alpine for smaller image sizes,
# but lxml is a dependency for this project, and it was giving me a headache
# to resolve build dependencies and failures. So I switched to the regular
# image and it worked first try. With the timeline of COVID, we can't afford
# to over-engineer these kinds of solutions.
FROM python

LABEL description="Vaccine checker."
LABEL version="0.0.1"

RUN mkdir -p /data

# prepare the directory within the image
RUN mkdir /src
WORKDIR /src

# before copying the entire directory into the image,
# first copy the requirements.txt file, and install dependencies.
# This will make it so that pip doesn't reinstall dependencies every single
# time the source code is changed, and Docker caches the layer.
COPY requirements.txt /src/requirements.txt
RUN pip3 install -r requirements.txt

# now that we've installed dependencies, copy the code in
COPY . /src

CMD [ "python3", "covid-vaccine-bot.py" ]
