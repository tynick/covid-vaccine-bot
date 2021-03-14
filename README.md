# covid-vaccine-bot

Python application that can be deployed to Heroku to find vaccine volunteer opportunities.

Checkout [Using Python to get an early covid vaccine post on tynick.com](https://tynick.com/blog/03-13-2021/using-python-to-get-an-early-covid-vaccine/") for all details.

## Table of Contents

- [covid-vaccine-bot](#covid-vaccine-bot)
  - [Table of Contents](#table-of-contents)
  - [Differences between this fork and the original](#differences-between-this-fork-and-the-original)
  - [Getting Started](#getting-started)
    - [Making sense of the log output](#making-sense-of-the-log-output)
  - [Architecture](#architecture)
    - [Why use Tor? What is it?](#why-use-tor-what-is-it)
    - [Using this Tor proxy will make me anonymous now! Mission accomplished. Right?](#using-this-tor-proxy-will-make-me-anonymous-now-mission-accomplished-right)
    - [So how do I do anything on the internet without being tracked online?](#so-how-do-i-do-anything-on-the-internet-without-being-tracked-online)
  - [What are the different files/changes in this repository, compared to the original?](#what-are-the-different-fileschanges-in-this-repository-compared-to-the-original)
    - [Added: Dockerfile](#added-dockerfile)
    - [Added: `docker-compose.yml`](#added-docker-composeyml)
    - [Added: `.dockerignore` and `.gitignore`](#added-dockerignore-and-gitignore)
    - [Modified: `covid-vaccine-bot.py`](#modified-covid-vaccine-botpy)
    - [Added: `Makefile`](#added-makefile)
  - [Final notes](#final-notes)

## Differences between this fork and the original

[Tynick](https://tynick.com)'s original work is an excellent, minimalist solution that contains only the bare minimum needed to run the project and get the job done. While we were chatting about this bot, I found that I wanted to run it too, but I didn't want to have both of our bots running simultaneously, and I didn't want to get my IP address on a blocklist.

So, I dockerized it, pointed it to a local Tor proxy (included in this repo), added some environment variable configuration, and wrapped everything together in a docker compose file. See the [architecture](#architecture) section for details. My hope is that the audience reading Tynick's original post might want to take things a little further and see a version of the app that has a bit extra added on top.

I hope readers find this iteration on the project useful! [Tynick](https://tynick.com) and I had a blast with this project and we were also happy to help friends get vaccinated.

## Getting Started

This setup requires Docker, Docker compose, and optionally, GNU Make.

* If you don't have Docker, visit [get.docker.com](https://get.docker.com) and follow the install steps in the comments at the top of the file
  * Helpful advice if you can't find it: It be something like `curl <script>` followed by `sh get-docker.sh`
* If you don't have Docker compose, visit the [official installation instructions](https://docs.docker.com/compose/install/) page for compose.
* If you don't have GNU Make, or are not sure how to check if you have it, simply run the command `make -h` in your terminal. You should see some help text print out in your terminal.
  * If you definitely don't have it, installation steps vary from platform, but if you're on a system like Ubuntu you can run `sudo apt install make` - see [here](https://askubuntu.com/questions/161104/how-do-i-install-make#272020).

First, make a copy of `.env.sample.env` into the file `.env`:

```bash
cp .env.sample.env .env
```

Modify the values in it to correspond to your Slack and Twilio configuration - if you're not using one of the services such as Twilio, you can leave its values blank:

```bash
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/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
TWILIO_ACCOUNT_SID=xyz
TWILIO_AUTH_TOKEN=xyz
TWILIO_TARGET_NUMBER=+15555555555
TWILIO_SOURCE_NUMBER=+15555555555
```

> *Note: Do not use quotes.*

Next, if you have `make` installed, run the commands:

```bash
make pull # this will fail to pull the vaccine-bot image, that's expected - building it next
make build-image
make run
make logs # optional: will follow logs
```

If you don't have `make`, that's OK - the bash commands that it runs are contained in the `Makefile` and you can still do everything as follows:

```bash
docker-compose pull # this will fail to pull the vaccine-bot image, that's expected - building it next
docker build -t covid-vaccine-bot:latest .
docker-compose up -d
docker-compose logs -f # follows logs
```

### Making sense of the log output

Take a look at the below logs, which are captured from running `docker-compose logs -f` (or `make logs` if you're using the `Makefile`). This is fairly normal. The following is happening, in order:

* The COVID vaccine bot is running, and is trying to make a request to the volunteer website.
* The COVID vaccine bot's requests are failing (hence why we see exceptions occurring), because the `tor-privoxy` service hasn't started yet.
* The `tor-privoxy` service finally starts up, as indicated by the fact that we see messages coming from the service.
* The COVID vaccine bot starts to succeed, because the Tor connection has been established successfully.

> *Note: Tor will always take a few moments to start up. This is because it is creating and securing a circuit (as well as a couple other things), which is a set of 3 networked devices in the Tor network that the `tor-privoxy` service will make its requests through. You can see this with the Tor browser on startup too.*

```
covid-vaccine-bot    | During handling of the above exception, another exception occurred:
covid-vaccine-bot    |
covid-vaccine-bot    | Traceback (most recent call last):
covid-vaccine-bot    |   File "/src/covid-vaccine-bot.py", line 66, in <module>
covid-vaccine-bot    |     vaccine_site_info = get_site(site_url)
covid-vaccine-bot    |   File "/src/covid-vaccine-bot.py", line 58, in get_site
covid-vaccine-bot    |     response = requests.get(url, headers=headers)
covid-vaccine-bot    |   File "/usr/local/lib/python3.9/site-packages/requests/api.py", line 76, in get
covid-vaccine-bot    |     return request('get', url, params=params, **kwargs)
covid-vaccine-bot    |   File "/usr/local/lib/python3.9/site-packages/requests/api.py", line 61, in request
covid-vaccine-bot    |     return session.request(method=method, url=url, **kwargs)
covid-vaccine-bot    |   File "/usr/local/lib/python3.9/site-packages/requests/sessions.py", line 542, in request
covid-vaccine-bot    |     resp = self.send(prep, **send_kwargs)
covid-vaccine-bot    |   File "/usr/local/lib/python3.9/site-packages/requests/sessions.py", line 655, in send
covid-vaccine-bot    |     r = adapter.send(request, **kwargs)
covid-vaccine-bot    |   File "/usr/local/lib/python3.9/site-packages/requests/adapters.py", line 510, in send
covid-vaccine-bot    |     raise ProxyError(e, request=request)
covid-vaccine-bot    | requests.exceptions.ProxyError: HTTPSConnectionPool(host='www.handsonphoenix.org', port=443): Max retries exceeded with url: /opportunity/a0N1J00000QGgU1UAL (Caused by ProxyError('Cannot connect to proxy.', OSError('Tunnel connection failed: 503 Forwarding failure')))
tor-privoxy          |
tor-privoxy          |  * /proc is already mounted
tor-privoxy          |  * /run/openrc: creating directory
tor-privoxy          |  * /run/lock: creating directory
tor-privoxy          |  * /run/lock: correcting owner
tor-privoxy          |  * Starting privoxy ... [ ok ]
tor-privoxy          |  * Setting up Tor control relay ... [ ok ]
tor-privoxy          |  * /var/lib/tor: correcting owner
tor-privoxy          |  * /run/tor: creating directory
tor-privoxy          |  * /run/tor: correcting owner
tor-privoxy          |  * Starting tor ... [ ok ]
tor-privoxy          |    OpenRC 0.39.2.7e1d41d609 is starting up Linux 5.8.0-44-generic (x86_64) [DOCKER]
tor-privoxy          |
tor-privoxy          |  * Caching service dependencies ... [ ok ]
covid-vaccine-bot    | getting site...
covid-vaccine-bot    | site retrieved...
covid-vaccine-bot    | nothing was available
covid-vaccine-bot    | getting site...
covid-vaccine-bot    | site retrieved...
covid-vaccine-bot    | There is an opening at State Farm Stadium. Check https://www.handsonphoenix.org/opportunity/a0N1J00000NW4CHUA1 for more info.
```

## Architecture

![Architecture diagram showing the services in this repository](docs/architecture.png)

The vaccine bot relies on the `tor-privoxy` service being alive in order to make its outbound requests, including Slack and Twilio.

> *Note: It's posible Twilio may reject requests from behind the Tor network. I haven't tested it, but Slack appears to work.*

### Why use Tor? What is it?

If you aren't familiar with [Tor](https://www.torproject.org/), you should take a moment to read and understand what it is. I'll try and summarize.

For all intents and purposes, Tor is a couple things:

* It's a couple thousand systems run by regular people like you and I, or run by corporations or other entities.
* It's a protocol for taking your network requests and bouncing them around those thousands of systems across the world, to form a "circuit".
* It is also a means to access _hidden services_, or _Onion sites_, which are long URLs that differ from a typical `xyz.com` website: `3g2upl4pq6kufc4m.onion` - this is the [DuckDuckGo](https://duckduckgo.com) hidden service, for example.
  * Most hidden services have much longer names.
  * Hidden services are more or less randomly generated names (there is a lot of cryptography behind it).
  * Some hidden services, like Facebook, used brute force to randomly generate hidden service names until they got one they like: `facebookcorewwwi.onion`

Tor helps you become a bit more "anonymous" on the web. Normally, when you visit a webpage, the traffic first gets relayed by your internet service provider (such as Cox or Comcast), out to the world wide web, and to the destination. When you visit Tor, the traffic does technically also go through your ISP, but there are so many layers of cryptography and network trickery at work that they have no realistic way of knowing what you're doing, and effectively, they cannot monitor you.

However, simply proxying requests through Tor (like we are in this project) will **NOT** make you anonymous on the web. There's so much more to it than that.

In order to be anonymous in the real world, you might first try putting on a face covering. If you're the only person wearing a face covering in public, you're not really anonymous - you're actually unique, because you're sticking out like a sore thumb. Just because your face isn't visible, it *doesn't make you anonymous*.

Let's take the analogy a bit further. Suppose you are wearing a face covering, and *everyone else around you* is *also* wearing a face covering. Suddenly, your anonymity has increased.

### Using this Tor proxy will make me anonymous now! Mission accomplished. Right?

Not exactly. When our requests are proxied through Tor in this setup, we aren't really taking proper steps to "blend in with the crowd" by any means.

**The only reason Tor comes in handy in this architecture is to grant us a different IP address.**

Effectively, we could replace the Tor Docker service in this architecture with a VPN, and it would actually be *better*. However, for the sake of expediency, and for the sake of advocating the use of Tor, I decided to shoehorn it into this project. **You should not use Tor if you don't have to.** People in the real world depend on Tor for their livelihood, and other people dedicate their time to offering their devices to others out of the goodness of their hearts.

### So how do I do anything on the internet without being tracked online?

First off, let's agree on something: Just because you might "have nothing to hide", doesn't mean that you "should expose everything you do online to everyone". That's a big discussion in and of itself for another time.

In order to actually be anonymous online and browse the web (via a web browser), and following our analogy from earlier, everyone has to:

* Hide their face with a good face covering.
* Have the same physique.
* Wear the same clothing.
* Walk the same way.
* Talk to no one on the way to the destination.
* Make no indication of where you're going to anyone watching until you're at your destination.

**All of this is done for you with the [Tor browser](https://www.torproject.org/download/).**

The Tor browser should not be reconfigured **at all** from its defaults. By assimilating yourself into the masses, you have the ability to go where you want to go without the feeling of being watched, tracked, or potentially regretting clicking on an ad or page you didn't mean to click. You can explore that rabbit hole without fear of becoming targeted by ads.

I won't be writing an in-depth guide on Tor here, but there are lots of resources online that can help you learn.

## What are the different files/changes in this repository, compared to the original?

### Added: Dockerfile

The Dockerfile contains a standard automation for (somewhat) efficiently building the Python-based Docker image for this project. I definitely recommend you read the comments in the Dockerfile - I tried to annotate things to be as helpful as possible.

### Added: `docker-compose.yml`

The `docker-compose.yml` file is very important - in it, it contains two services, which are just containers that are configured to work together:

* the `tor-privoxy` service, discussed above
* the `covid-vaccine-bot` service itself

Take a look at this file and read each of my comments. Hopefully you'll learn something new!

### Added: `.dockerignore` and `.gitignore`

The `.dockerignore` file is similar to `.gitignore`, if you're familiar with it:

* `.dockerignore` instructs the `docker build` command to ignore files that match the patterns specified in this file.
  * This is useful because sometimes your repository contains large files that your Docker image might not even need in the first place.
* `.gitignore` instructs git to exclude specified files; in this case, we ignore the `.env` file because it contains secret Slack webhooks and account credentials for Twilio.

### Modified: `covid-vaccine-bot.py`

I added some simple logic to handle environment variables, which are defined in the `.env` file and automatically propagated into the container at runtime via Docker compose. Additionally, my Python auto-formatter did some code reformatting.

Specifically, `os.environ.get('ENV_VARIABLE', '')` is good practice, because if you just try to access a Python dictionary by a key that doesn't exist, it throws an exception:

```python
os.environ['NON_EXISTENT_KEY'] # throws exception, halts your code
os.environ.get('NON_EXISTENT_KEY', '') # simply returns '', much better
```

### Added: `Makefile`

The `Makefile` is pretty simple. If you're not familiar with them, Makefiles allow developers to put frequently used commands/automated tasks into a single place. One of the best features about it is that you can use tab auto-completion out of the box by just simply defining a section, such as:

```Makefile
build-image:
	docker build -t covid-vaccine-bot:latest .
```

And you can execute this command by running:

```bash
make build-image  # try tab completing as you type
```

## Final notes

I'll reiterate: [Tynick](https://tynick.com) did a fantastic job with this project - he was able to automate a tool to get multiple people a COVID vaccine! We both had a great time expanding and bringing this tool to our friends, and we feel honored to have helped get people vaccinated AND volunteering.

I hope you've found this writeup informative. If you have any questions, visit [charlesmknox.com](https://charlesmknox.com) and use any of the social contact URLs on the landing page. You can also visit [charlesmknox.com/about](https://charlesmknox.com/about) to find ways to support me.
