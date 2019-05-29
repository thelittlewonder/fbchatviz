import json
import os
import sys
import re
import datetime
from collections import Counter
import plotly.graph_objs as go
import plotly.io as pio
from wordcloud import WordCloud
import numpy as np
from PIL import Image, ImageDraw, ImageFont

#give error if no argument given
if len(sys.argv) < 2:
    print("Usage: ``%s filename.json``" % sys.argv[0])
    sys.exit(1)

#Read JSON data
with open(sys.argv[1], 'r') as f:
    chat_data = json.load(f)

#read participants from the JSON
participants_data = chat_data['participants']
sender = participants_data[0]['name']
receiver = participants_data[1]['name']

#create directory to save plots
save_path='plots/'+sender
os.mkdir(save_path)

#declare data elements
messages_data = chat_data['messages']
messages_sent = []
messages_received = []

photos_exchanged = {}
shared_links = {}
messages_timestamps = {}
messages_days = {}
messages_years = {}
messages_months = {}
total_words = {}

#classify messages as received or sent
for message in messages_data:
    if message['sender_name']==sender:
        messages_received.append(message)
    else:
        messages_sent.append(message)

#function to get stats for sent and received types of messages
def get_stats(message_data, message_type):
    photos = []
    links = []
    words = []
    days = []
    months = []
    years = []
    timestamps = []
    for message in message_data:
        #classify photos
        if 'photos' in message:
            photos.append(message)
        #search for links using regex and append
        if 'content' in message:
            if bool(re.search("(?P<url>https?://[^\s]+)", message['content'])):
                links.append(message)
            #add individual word strings
            words += (message['content'].split())
        #get time specific stats
        days.append(datetime.datetime.fromtimestamp(message['timestamp_ms']/1000.0).strftime("%A"))
        months.append(datetime.datetime.fromtimestamp(message['timestamp_ms']/1000.0).strftime("%B"))
        years.append(datetime.datetime.fromtimestamp(message['timestamp_ms']/1000.0).strftime("%Y"))
        timestamps.append(datetime.datetime.fromtimestamp(message['timestamp_ms']/1000.0))
        #timestamps.append(datetime.datetime.fromtimestamp(message['timestamp_ms']/1000.0).strftime("%B-%Y"))
        #copy to global objects
        photos_exchanged[message_type]=photos
        shared_links[message_type]=links
        total_words[message_type]=words
        messages_days[message_type]=days
        messages_years[message_type]=years
        messages_months[message_type]=months
        messages_timestamps[message_type]=timestamps

#run the function on all , received and sent messages
get_stats(messages_data,'total')
get_stats(messages_received,'received')
get_stats(messages_sent,'sent')

#Plotting Year Data

trace1 = go.Bar(
    x=list(dict(sorted(dict(Counter(messages_years['sent'])).items())).keys()),
    y=list(dict(sorted(dict(Counter(messages_years['sent'])).items())).values()),
    name='Sent by ' + receiver.split()[0],
    marker=dict(
        color='rgb(239,86,117)',
    )
)
trace2 = go.Bar(
    x=list(dict(sorted(dict(Counter(messages_years['received'])).items())).keys()),
    y=list(dict(sorted(dict(Counter(messages_years['received'])).items())).values()),
    name='Sent by ' + sender.split()[0],
    marker=dict(
        color='rgb(59,89,152)',
    )
)

data = [trace1, trace2]
layout = go.Layout(
    barmode='stack',
    title=go.layout.Title(
        text='Number of Messages per Year',
        xref='paper',
        x=0
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text='Year'
        ),
        dtick=1
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text='Number of Messages'
        )
    )
)

fig = go.Figure(data=data, layout=layout)
pio.write_image(fig, save_path+'/Year-Wise-Comparison.png')


##Plotting Month Data

const_months = ['January','February','March','April','May','June','July','August','September','October','November','December']

trace1 = go.Bar(
    x=list(dict(sorted(dict(Counter(messages_months['sent'])).items(),key =lambda x:const_months.index(x[0]))).keys()),
    y=list(dict(sorted(dict(Counter(messages_months['sent'])).items(),key =lambda x:const_months.index(x[0]))).values()),
    name='Sent by ' + receiver.split()[0],
    marker=dict(
        color='rgb(239,86,117)',
    )
)
trace2 = go.Bar(
    x=list(dict(sorted(dict(Counter(messages_months['received'])).items(),key =lambda x:const_months.index(x[0]))).keys()),
    y=list(dict(sorted(dict(Counter(messages_months['received'])).items(),key =lambda x:const_months.index(x[0]))).values()),
    name='Sent by ' + sender.split()[0],
    marker=dict(
        color='rgb(59,89,152)',
    )
)

data = [trace1, trace2]
layout = go.Layout(
    barmode='stack',
    title=go.layout.Title(
        text='Number of Messages per Month',
        xref='paper',
        x=0
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text='Month'
        )
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text='Number of Messages'
        )
    )
)

fig = go.Figure(data=data, layout=layout)
pio.write_image(fig, save_path+'/Month-Wise-Comparison.png')


##Plotting Days Data

const_days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

trace1 = go.Bar(
    x=list(dict(sorted(dict(Counter(messages_days['sent'])).items(),key =lambda x:const_days.index(x[0]))).keys()),
    y=list(dict(sorted(dict(Counter(messages_days['sent'])).items(),key =lambda x:const_days.index(x[0]))).values()),
    name='Sent by ' + receiver.split()[0],
    marker=dict(
        color='rgb(239,86,117)',
    )
)
trace2 = go.Bar(
    x=list(dict(sorted(dict(Counter(messages_days['received'])).items(),key =lambda x:const_days.index(x[0]))).keys()),
    y=list(dict(sorted(dict(Counter(messages_days['received'])).items(),key =lambda x:const_days.index(x[0]))).values()),
    name='Sent by ' + sender.split()[0],
    marker=dict(
        color='rgb(59,89,152)',
    )
)

data = [trace1, trace2]
layout = go.Layout(
    barmode='stack',
    title=go.layout.Title(
        text='Number of Messages per Day',
        xref='paper',
        x=0
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text='Day'
        )
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text='Number of Messages'
        )
    )
)

fig = go.Figure(data=data, layout=layout)
pio.write_image(fig, save_path+'/Day-Wise-Comparison.png')


#Plotting different types of text types

number_of_total_messages = len(messages_data)
number_of_photos = len(photos_exchanged['total'])
number_of_links = len(shared_links['total'])
number_of_texts = number_of_total_messages - number_of_photos - number_of_links  

fig = {
  "data": [
    {
      "values": [number_of_photos, number_of_links, number_of_texts],
      "labels": ['Photos','Links','Plain Texts'],
      "marker": {'colors':['#EF5675','#ffa600', '#3B5998']},
      "type": "pie"
    }],
    "layout": {
        "title":"Different Types of Messages"
    }
}

pio.write_image(fig, save_path+'/Types-of-Messages.png')


#Plotting message frequency

def sorted_time_stamps(timestamps,type):
    timestamps[type]=sorted(timestamps[type])
    a = []
    for time in timestamps[type]:
        a.append(time.strftime("%B-%Y"))
    timestamps[type]=a
    
sorted_time_stamps(messages_timestamps,'total')
sorted_time_stamps(messages_timestamps,'sent')
sorted_time_stamps(messages_timestamps,'received')

list(dict(Counter(messages_timestamps['sent'])).keys())


trace1 = go.Scatter(
    x = list(dict(Counter(messages_timestamps['sent'])).keys()),
    y = list(dict(Counter(messages_timestamps['sent'])).values()),
    mode = 'lines+markers',
    name = 'Messages sent by ' + receiver.split()[0],

    marker=dict(
        color='rgb(239,86,117)',
    )
)

trace2 = go.Scatter(
    x = list(dict(Counter(messages_timestamps['received'])).keys()),
    y = list(dict(Counter(messages_timestamps['received'])).values()),
    mode = 'lines+markers',
    name = 'Messages sent by ' + sender.split()[0],
    marker=dict(
        color='rgb(59,89,152)',
    )
)

layout = go.Layout(
    margin=go.layout.Margin(
        b=120,
        l=75
    ),
    title=go.layout.Title(
        text='Number of Messages over time',
        xref='paper',
        x=0
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text='Number of Messages'
        )
    )
)

data = [trace1, trace2]

fig = go.Figure(data=data,layout=layout)
pio.write_image(fig, save_path+'/Frequency-of-Messages-over-time.png')

#plotting wordcloud
a = list(dict(sorted(dict(Counter(total_words['total'])).items(), key=lambda x: x[1], reverse=True)).keys())[:25]
seperator = ' '
sentence = (seperator.join(a))

fb_mask = np.array(Image.open("images/fb-mask.png"))

wc = WordCloud(background_color="white", mask=fb_mask,
               contour_width=3, contour_color='steelblue')

# generate word cloud
wc.generate(sentence)

#save word cloud
wc.to_file(save_path+'/Common-Words.png')

#create combined image
# create background image object with the input image
combined_image = Image.open('./images/base.png')
 
# initialise the drawing context with the combined image object as background
drawing_context = ImageDraw.Draw(combined_image)

# create font object with the font file and specify
font_h1 = ImageFont.truetype('./fonts/SourceSansPro-Regular.ttf', size=32)
font_h2 = ImageFont.truetype('./fonts/SourceSansPro-Bold.ttf', size=40)
font_h3 = ImageFont.truetype('./fonts/SourceSansPro-Regular.ttf', size=24)

#define colors
h1_color = 'rgb(51, 51, 51)'
blue_color = 'rgb(59, 89, 152)'
pink_color = 'rgb(239, 86, 117)'
h3_color = 'rgb(102, 102, 102)'

##title
drawing_context.text((50, 50), 'Your Facebook Chat Numbers with', fill=h1_color, font=font_h1)
drawing_context.text((50, 98), sender, fill=blue_color, font=font_h2)

##stats heading
drawing_context.text((50, 210), 'Total Messages', fill=h3_color, font=font_h3)
drawing_context.text((307, 210), 'Messages Sent', fill=h3_color, font=font_h3)
drawing_context.text((560, 210), 'Messages Received', fill=h3_color, font=font_h3)

##stats
drawing_context.text((50, 252), str(len(messages_data)), fill=h1_color, font=font_h2)
drawing_context.text((307, 252), str(len(messages_sent)), fill=blue_color, font=font_h2)
drawing_context.text((560, 252), str(len(messages_received)), fill=pink_color, font=font_h2)

##open and paste other plots
year_wise = Image.open(save_path+'/Year-Wise-Comparison.png')
month_wise = Image.open(save_path+'/Month-Wise-Comparison.png')
day_wise = Image.open(save_path+'/Day-Wise-Comparison.png')
time_wise = Image.open(save_path+'/Frequency-of-Messages-over-time.png')
type_wise = Image.open(save_path+'/Types-of-Messages.png')
combined_image.paste(year_wise,(50,366))
combined_image.paste(month_wise,(50,922))
combined_image.paste(day_wise,(50,1478))
combined_image.paste(time_wise,(50,2034))
combined_image.paste(type_wise,(50,2590))

combined_image.save(save_path+'/_Summary_.png',optimize=True)
combined_image.show
#print success message
print('Charts saved to Plots/' + sender)