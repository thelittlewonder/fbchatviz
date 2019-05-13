## Visualising Facebook Chat Data with Python and Plotly

Requirements
------------

You need Python 3.5 or later to run this script.  You can have multiple Python
versions (2.x and 3.x) installed on the same system without problems.

In Ubuntu, Mint and Debian you can install Python 3 like this:

    $ sudo apt-get install python3 python3-pip

For other Linux flavors, macOS and Windows, packages are available at

  http://www.python.org/getit/


Getting Started
------------
### Download Facebook Data 
- Download your Facebook Messaging Data by heading to [settings](https://www.facebook.com/settings?tab=your_facebook_information)
- Click Download your information.
![Download info](https://github.com/thelittlewonder/fbchatviz/raw/master/images/Readme/Readme_1.png)
- Select messages and the format as JSON.
![Format](https://github.com/thelittlewonder/fbchatviz/raw/master/images/Readme/Readme_2.png)
- Click create file.
- You will receive a notification as well as an email when your data is ready. It normally takes 15-20 minutes to combine the data.
![Notification](https://github.com/thelittlewonder/fbchatviz/raw/master/images/Readme/Readme_3.png)
- Once you have downloaded the data file, extract the folder and Navigate to Messages > Inbox.
- Here you can see the individual folders for each of your chat.
- Open any of chat folder and copy the **message_1.json** file.
- **message_1.json** is the data file we will be using to plot the charts. Place it in the fbchatviz folder. 

### Running the Script

    $ git clone https://github.com/thelittlewonder/fbchatviz.git
    $ pip install -r requirements.txt
    $ python plot.py message_1.json
