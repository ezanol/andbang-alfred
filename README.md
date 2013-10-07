# AndBang Alfred
An Alfred workflow for interacting with [andbang.com](https://andbang.com).

## Install
Download and install the [workflow file](https://github.com/lukekarrys/andbang-alfred/raw/master/dist/AndBang.alfredworkflow).

## How to use

Basic usage: `&! [team name] [command]`

### First
`&! TOKEN`

Run the above where `TOKEN` is your generated auth token from [https://apps.andyet.com](https://apps.andyet.com/). When this is complete you will see a notification popup that your token is valid and your teams have been saved.

### If you have more than 1 team
After typing `&!` you will see entries for each of your teams. Tab will autocomplete your team name.

### If you have 1 team
There will be no need or prompt to type your team name. All commands will apply to your one team.

### Commands

- `tasks` Tasks will show you all tasks for your selected team. There are different ways to interact with them:
  - Selecting an iteam will ship it.
  - Selecting with `CTRL` will later it.
  - Typing more after `tasks` will bring up an extra option to `create` a new task with that as the title.

- `teams` Use this if you have added/removed teams and wish to update your cached teams.

## License
MIT
