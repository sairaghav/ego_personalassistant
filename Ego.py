import sys,threading,socket,os
sys.path.append('../')
from api import speaker,listener,browser,process_handler,note_taker,navigator,volume_controller,google_search,conversation,reader,videocast

def get_input():
    speak_data = listener.listen()
    while speak_data == '':
            speaker.speak('Sorry.. Can you say that again??')
            speak_data = listener.listen()
    return speak_data

def ego(data):
    global listening

    if listening == 1:
        if data in ['search']:
            speaker.speak('What do you want me to search for??')
            query = get_input()

            speaker.speak('Searching for '+query)
            threading.Thread(target=browser.browse,args=('https://www.google.com/search?q='+query,)).start()

        elif data in ['play music']:
            speaker.speak('Which song do you want me to play??')
            song = get_input()

            speaker.speak('Playing '+google_search.search(song,'video',no_of_results=1).keys()[0])
            threading.Thread(target=browser.browse,args=(google_search.search(song,'video',no_of_results=1).values()[0],)).start()
            
        elif data in ['show desktop','close window','close tab','new tab','restore tab','next tab','previous tab'] or 'switch window' in data or 'press' in data or 'scroll' in data:
            navigator.navigate(data)

        elif data in ['take notes']:
            note_taker.take_notes()

        elif 'volume' in data:
            volume_controller.controller(data)

        elif data in ['read news']:
            reader.read_news()

        elif data in ['read book']:
            reader.read_book()

        elif data.startswith('chromecast'):
            if videocast.get_cc() is None:
                speaker.speak('No chromecast devices found. Please switch on device and try again')
            else:
                speaker.speak('Searching YouTube for video')
                if 'pause' in data.replace('chromecast','').strip():
                    videocast.pause_cast_video()
                elif 'play' in data.replace('chromecast','').strip():
                    videocast.play_cast_video()
                else:
                    if len(data.replace('chromecast','').strip()) > 0:
                        video_to_search = data.replace('chromecast','').strip()
                        videocast.cast_video(video_to_search)

        elif data in ['go to sleep']:
            speaker.speak('Going to sleep..')
            listening = 0

        elif data in ['exit']:
            speaker.speak('Exiting... Goodbye!')
            listening = 0
            sys.exit(0)

        else:
            conversation.converse(data)
            
    if data in ['hi ego', 'wake up ego', 'hey ego', 'wake up', 'ego']:
        speaker.speak('Hello! I am Ego.. What can I do for you??')
        listening = 1

    elif data in ['exit']:
        speaker.speak('Exiting... Goodbye!')
        sys.exit(0)

    

if __name__ == '__main__':
    try:
        speaker.speak('Hello! I am Ego.. What can I do for you??')
        listening = 1
        
        while True:
            data = listener.listen()
            ego(data)

    except KeyboardInterrupt:
        sys.exit(0)
