# etlJiraSmartsheetFunction

Pass issues data from Jira to Smartsheets

# alethix_jira_smartsheet_etl

Load data to smartsheet from jira

# Add your SSH key to the ssh-agent

If you created your key with a different name, or if you are adding an existing key that has a different name, replace id_ed25519 in the command with the name of your private key file (instructions here: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent).

    $ ssh-keygen -t ed25519 -C "your_email@example.com"
    > Generating public/private algorithm key pair.
    > Enter a file in which to save the key (/home/you/.ssh/algorithm): [Press enter]
    > Enter passphrase (empty for no passphrase): [Type a passphrase]
    > Enter same passphrase again: [Type passphrase again]

    $ eval "$(ssh-agent -s)"
    > Agent pid ####

    $ ssh-add ~/.ssh/id_ed25519

# Set your git user details

Setting your Git user details for every repository on your computer:

    $ git config --global user.name "username"
    $ git config --global user.email "user@company.ext"

Use Git SSH (not https) for git clone operation:

    $ git clone git@github.com:<organization>/<REPOSITORY>.git -b production

# Environment Setup

On Debian/Ubuntu systems, you need to install the python3-venv,
python3-pip packages using the following command. You may need to use sudo with this command.

    $ apt install python3.8-venv python3-pip

After installing the packages, recreate your virtual environment by first creating a venv folder.

    $ python3 -m venv venv

Activate virtual environement.

    $ <WORKING_DIRECTORY>/venv/bin/activate

Install python package dependencies listed in requirements.txt

    $ pip -r .<REPOSITORY>/requirements.txt

Additionally, include environment variables for application API calls in WORKING_DIRECTORY/REPOSITORY/.env file:

    USERNAMEJIRA=<jira_user_name>
    USERKEYJIRA=<jira_user_password>
    USERNAMESMARTSHEET=<smartsheet_user_name>
    USERKEYSMARTSHEET=<smartsheet_user_password>
    USERURLSMARTSHEET=<smartsheet_url>

# Add job details to jobs.json file.

Application loops over the list of jobs within the job_details object.

    {
        "job_details": [
            {
                "id": "string",
                "jria_url": "string",
                "name": "string",
                "query": "string",
                "max_results": "intiger",
                "target_sheet_id": "string",
                "smartsheet_url": "string"
            }
        ]
    }

# Schedule cron job

Write out current crontab

    $ crontab -l > local_cron

Echo new cron into cron file

    $ echo "5 5 * * 0 python3 <WORKING_DIRECTORY>/<REPOSITORY>/app/main.py" >> local_cron

Install new cron file

    $ crontab local_cron

Remove new/temp cron file

    $ rm local_cron

Verify changes have been made to crontab file

    $ crontab -l
    -- or --
    $ crontab -e

Ensure cron is running

    $ sudo service cron start
