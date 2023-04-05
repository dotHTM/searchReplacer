# Search Replacer

A tool for searching and replacing in a git repository.

# Requirements

While this was written on macOS, this project requires the gnu-sed which one can install via [homebrew](https://brew.sh):

```
brew install gnu-sed
```

# Use

Create a folder for the work to be done, and create a file with a list of your repositories called "repoList" and another with a list of your your search replace strings named "sedCommand".

_Note:_ At present, only SSH urls are supported. Consider adding an ssh key to your cloud git provider settings.

Ex:

**repoList**

```
git@github.com:dotHTM/dothtm.github.io.git
git@github.com:dotHTM/bash_hacks.git
```


**sedCommand**

```
s/hello/world/g
s/foo/bar/gi
s/^\/compli\n?cated$/regex/gm
```

Then run `searchReplacer`.

A file "grepCommand" will be generated with the 'search' portions of your sed commands.

Each repo will be pulled and the search replace commands applied, then 

