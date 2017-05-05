# chat robot

An interesting (indiscreet) chat robot for [stream-me-board](https://github.com/XiangPingJun/stream-me-board)
Uses [National Academy for Educational Research Segmentor](https://github.com/naernlp/Segmentor) for natural language processing.
> Warning, what it says could be totally nasty in sometimes.

## Talk what you are talking!

<img src='http://i.imgur.com/L9CYdDt.png'>

> The robot will extract the most popular noun part from chat messages and combine to a decent script.

## It will also cue you!

<img src='http://i.imgur.com/SplxupV.jpg'>

> It will randomally cue someone in the chatroom

## Installation

1. Prepare an linux machine
2. Install [python](https://www.python.org/)
3. run command
```sh
sudo apt-get install python-pip python-dev build-essential 
sudo pip install --upgrade pip 
sudo pip install --upgrade virtualenv 
sudo pip install requests==1.1.0
sudo pip install python-firebase
```

## Usage

```sh
screen -d -m python ai.py &> log.log
```

> It will start talking about every 4 minutes
