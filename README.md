## Installation
# Show the status of various SaaS service at the CLI

### Getting started
- brew install pipx (macOS)
- scoop install pipx (Windows)
- pipx ensurepath


### Install the weather cli app
- pipx install git+https://github.com/zerowon01/servstat.git
- servstat --file /path/to/sites.csv
 
:fireworks: Voila, your statuses from various SaaS services!

### Regarding input file
- CSV
- Service|URL|NormalStatus|Remarks
 * "Normal Status" refers to a string you expect to find in the status page indicating a "normal" status.
 
:weary: Watch out . .
Some sites load the DOM via AJAX so you can't scrape the status.