# Parchment
## Introduction:

Parchment is, parchment, the type of thing you can write something on.

## Features:
* Help you organize short ideas, words you think is worth through your day by day work.


## Requirements:

* TODO

## Getting started:

* Download source code:
```shell
cd ~
git clone git@github.com:zz090923610/parchment.git
cd parchment
```


* setup git backend server.
```shell script
# login as a sudo user on backend machine
sudo apt-get install git-core
sudo useradd git
passwd git
sudo passwd git
sudo mkdir /home/git
sudo chown git /home/git/

# on any client machine, upload public key.
cat id_rsa.pub | ssh git@ip "mkdir -p ~/.ssh && cat >>  ~/.ssh/authorized_keys"
```

## Commands:

* repo management:
```shell script
parchment_repo create "topic"
parchment_repo delete "topic"
parchment_repo push "topic"
parchment_repo pull "topic"
```

* add new item:

Three types of records are there. 

"words" is a couple words which as short as 
terminal command line parameter allows.

"para" which is a paragraph, maybe even longer,
a txt file will be created and an editor will be 
launched for content.

"ref" is a reference. It can be a general type
file, and will be copied to the repo for further
reference.

```shell script
parchment_words "topic" "content"
parchment_para "topic" "title"
parchment_ref "topic" "ref_path"

```


Now you are ready to roll.
* [MarkdownURLExample](https://fakeurl.com)

