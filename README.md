# veritaserum

_The truth, and nothing but the truth._

[![Drone][drone-img]][drone]

`veritaserum` recover unsends (deleted messages) in Messenger conversations,
and sends them to your Messenger inbox. Text, image, and video unsends are
all recoverable.

<br />
<p align="center">
  <img src="https://i.imgur.com/ph145q2.gif" width="520">
</p>
<br />

## Usage

Running locally, with [Python 3.7](https://www.python.org) (and
[Pipenv](https://pipenv.kennethreitz.org/en/latest/)):

```bash
$ git clone git@github.com:stevenxie/veritaserum
$ cd veritaserum

$ cat <<EOF > .env
MESSENGER_USERNAME=...
MESSENGER_PASSWORD=...
VERITASERUM_DEBUG=1
EOF

$ pipenv run python -m veritaserum
```

Or, in a container with [Docker](https://www.docker.com):

```bash
$ docker run -it --rm \
    -e MESSENGER_USERNAME=... \
    -e MESSENGER_PASSWORD=... \
    -e VERITASERUM_DEBUG=1 \
    stevenxie/veritaserum
```

<br />

## Sessions

If you're running `veritaserum` as a daemon (a long-running process) on a
remote server, consider using a stored session. This will allow you to bypass
having to enter 2FA information whenever `veritaserum` starts.

To create a session dump, use the tool
[`./util/dumpsesh.py`](./util/dumpsesh.py):

```bash
$ pipenv run python ./util/dumpsesh.py
# enter 2FA details when prompted
```

Then, encode the outputed JSON to
[`base64`](https://en.wikipedia.org/wiki/Base64):

```bash
$ echo '{ ... }' | base64

eyJoZXkiLCAidGhpcyBpcyBhIGR1bW15IGZpbGUgbG1hbyJ9...
```

And set it as the value for the environment variable `MESSENGER_SESSION`.

[drone]: https://ci.stevenxie.me/stevenxie/veritaserum
[drone-img]: https://ci.stevenxie.me/api/badges/stevenxie/veritaserum/status.svg
