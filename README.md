# asssets

Tools for hoarding images.

## Installation
Requires Python 3.10 and [pipenv](https://pipenv.pypa.io/). Or you can use your own virtual environment and just install requests and pillow

If you are brave enough to try this, here's how you can get started
```bash
# get repo
git clone https://github.com/Unbundlesss/asssets.git
cd asssets

# create virtualenv with pipenv
pipenv install

# enter the virtual env
pipenv shell

# setup command. Pulls metadata, creates database.
python main.py create
```

An sqlite database is created locally to track your progress.

## Modules

### Avatar Puller
First working module so far.

- This will pull avatars from the API and store them in a local directory that you can not choose yet.
- If the user does not have an avatar, it will make a note of this in the local database and it won't
try to get their avatar again.
- Pulls avatars in chunks specified by `--limit`, default is 10. This means it will go until it gets 10 avatars, not including people who don't have one.3
- Resizes all avatars to 800x800 jpg
- Does requests in batches of 10 at a time, regardless of `--limit`
- Fully resumable

#### Crap
It will eventually only keep the resized image. But right now it keeps both, sorry.

#### Usage
```bash
python main.py avatars --limit 10000
```

## Upcoming
- Getting all jam images
- Getting all rifff images


## Credits
The lists of metadata are taken directly from [OUROVEON](https://github.com/Unbundlesss/OUROVEON)