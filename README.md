# Brightsign-Updater
A method to automate the updating of Brightsign media players' firmware.

# Goals
My main goal was to alleviate the pain of updating every brightsign I have manually without paying for their paid plan. With this, all I need is a csv of all my players' IP addresses. I went a little O-O in my solution but I liked how it worked in practice. Should still make it a little nicer to use but overall pretty happy with everything so far.

# How it works
*brightsign.py* contains a class that represents a brightsign player. The class has one method, update(), that is used by the user.
This method handles the update process of the brightsign.
It checks that the player can be updated and that it isn't already on the latest version, along side some other checks.

The player works with brightsign players on the local network and calls it's local API, as opposed to the BSN API.
The program calls the update endpoint which downloads the specified (or default) firmware version on the player, installs, and restarts the player.

## Logging
This program has a primitive logging system if you choose to use it.

# Conclusion
This is a very simple implementation, but can certainly help your workflow.
I have a spreadsheet of IP addresses of my Brightsign players, so in a main script I create a *brightsign* object for each and then update it before iterating along.
