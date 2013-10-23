# AndBang Alfred
An Alfred workflow for interacting with [andbang.com](https://andbang.com).

## Install
Download and install the [workflow file](https://github.com/lukekarrys/andbang-alfred/raw/master/dist/AndBang.alfredworkflow).

## How to use

Basic usage: `! [team name] [command]`

### First
You will need to follow the auth instructions to save a token. Type `!` and the workflow will take care of the rest.

### If you have more than 1 team
After typing `!` you will see entries for each of your teams. Tab will autocomplete your team name. Typing will filter your teams.

### If you have 1 team
There will be no need or prompt to type your team name. All commands will apply to your one team.

### Commands

- `tasks` will show you all tasks for your selected team. There are different ways to interact with them:
  - Selecting an item will ship it.
  - Selecting with `ALT` will later it.
  - Selecting with `SHIFT` will activate it.
  - Selecting with `CTRL` will delete it.
  - Typing more after `tasks` will:
    - filter your tasks by title against what you typed
    - bring up an extra option to `create` a new task with that as the title

- `notifications` will show you all the current notifications for a team

- `teams` Use this if you have added/removed teams and wish to update your cached teams.
- `members` Use this if you have added/removed team members and wish to update your cached team members.
- `token` Use this to manually get a new token

## License
MIT
