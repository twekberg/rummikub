# rummikub
Collects stats after playing rummikub.

# Retrieving This Repository

This uses the normal git clone command:

	cd ~/src
	$ git clone git@github.com:twekberg/rummikub.git

# Create A Virtualenv And Install Dependencies

Run these commands:

    python -m venv rummikub-env
    See note
    source rummikub-env/bin/activate
    pip install pip -U # Latest pip
    pip install -r requirements.txt


Note:

If the rummikub-env/bin directory doesn't exist, run the following commands
to activate the venv.

    dos2unix rummikub-env/Scripts/activate
    source rummikub-env/Scripts/activate
