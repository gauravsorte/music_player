from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk


root = Tk()
root.title('MP3 Player')
root.geometry('850x600')

#Initialize Pygame Mixer
pygame.mixer.init()

#add song Function
def add_song():
    song = filedialog.askopenfilename(initialdir='C:/Users/Gaurav/Music/demo/', title='Choose A Song', filetypes=(('mp3 Files', "*.mp3"), ))
    print(song)
    song = song.replace('C:/Users/Gaurav/Music/demo/', '')
    song = song.replace('.mp3', '')

    #add song to list box
    song_list_box.insert(END, song)


# add many songs to playlist
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='C:/Users/Gaurav/Music/demo/', title='Choose Songs', filetypes=(('mp3 Files', "*.mp3"), ))
    #loop thorugh song list and replace directory info and mp3 and add
    for song in songs:
        song = song.replace('C:/Users/Gaurav/Music/demo/', '')
        song = song.replace('.mp3', '')
        song_list_box.insert(END, song)

#Play Selected Song
def play():
    try:
        global stopped
        stopped = False

        song = song_list_box.get(ACTIVE)
        song = f'C:/Users/Gaurav/Music/demo/{song}.mp3'

        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)

        music_length()

        # #update slider to position
        # slider_position = int(song_length)
        # my_slider.config(to=slider_position, value=0)

        #current volume
        # current_volume = pygame.mixer.music.get_volume()
        # slider_label.config(text=current_volume * 100)

    except:
        print('Error Occur in Play')

#stop the music
global stopped
stopped = False
def stop():
    try:
        # reset slider and status bar
        status_bar.config(text='')
        my_slider.config(value=0)
        #stop song from palying
        pygame.mixer.music.stop()
        song_list_box.selection_clear(ACTIVE)

        #clear status bar
        status_bar.config(text='')

        global stopped
        stopped = True
    except:
        print('Error in Stop')

# pause the music
def pause():
    try:
        if pygame.mixer.music.get_busy():
             pygame.mixer.music.pause()
        else:
             pygame.mixer.music.unpause()
    except:
        print('Error in Pause')

def play_next_track():
    try:
        index = song_list_box.index(song_list_box.curselection())
        if index+1 < song_list_box.size():
            status_bar.config(text='')
            my_slider.config(value=0)

            next_song = song_list_box.get(index+1)

            next_song = f'C:/Users/Gaurav/Music/demo/{next_song}.mp3'
            pygame.mixer.music.load(next_song)
            pygame.mixer.music.play(loops=0)

            # move action bar in playlist listbox
            song_list_box.selection_clear(0, END)
            song_list_box.activate(index + 1)
            song_list_box.selection_set(index + 1, last=None)



    except Exception as e:
        print('Error In play_next_track', e)

def play_previous_track():
    try:
        index = song_list_box.index(song_list_box.curselection())

        if index-1 >= 0:
            status_bar.config(text='')
            my_slider.config(value=0)

            song_list_box.selection_clear(ACTIVE)
            previous_song = song_list_box.get(index-1)

            previous_song = f'C:/Users/Gaurav/Music/demo/{previous_song}.mp3'
            pygame.mixer.music.load(previous_song)
            pygame.mixer.music.play(loops=0)

            # move action bar in playlist listbox
            song_list_box.selection_clear(0, END)
            song_list_box.activate(index - 1)
            song_list_box.selection_set(index - 1,  last=None)



    except Exception as e:
        print('Error In play_previous_track', e)

#Delete a Song
def delete_song():
    stop()
    song_list_box.delete(ANCHOR)
    pygame.mixer.music.stop()


def delete_all_songs():
    stop()
    song_list_box.delete(0, END)
    pygame.mixer.music.stop()


def music_length():
    try :
        if stopped:
            return

        current_time=pygame.mixer.music.get_pos() / 1000

        # slider_label.config(text=f'Slider : {int(my_slider.get())} and Song Position : {int(current_time)}')
        converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

        #Currently Playing Song
        # current_song = song_list_box.curselection()
        song_title = song_list_box.get(ACTIVE)
        song = f'C:/Users/Gaurav/Music/demo/{song_title}.mp3'

        # load song with mutagen
        song_mut = MP3(song)
        #Get song length with mutagen
        global song_length
        song_length = song_mut.info.length
        converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

        current_time += 1

        if int(my_slider.get()) == int(song_length):
            status_bar.config(text=f'Time Collapsed :{converted_song_length} of {converted_song_length}')

        elif not pygame.mixer.music.get_busy():
            pass

        elif int(my_slider.get()) == int(current_time):
            # update slider to position
            slider_position = int(song_length)
            my_slider.config(to=slider_position, value=int(current_time))
        else:
            slider_position = int(song_length)
            my_slider.config(to=slider_position, value=int(my_slider.get()))

            converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))

            status_bar.config(text=f'Time Collapsed :{converted_current_time} of {converted_song_length}')

            next_time = int(my_slider.get()) + 1
            my_slider.config(value=next_time)



        # my_slider.config(value=int(current_time))
        # status_bar.config(text=f'Time Collapsed :{converted_current_time} of {converted_song_length}')

        # # update slider to position
        # slider_position = int(song_length)
        # my_slider.config(to=slider_position, value=int(current_time))

        status_bar.after(1000, music_length)

    except Exception as e:
        print('Error in music_length')


#create slider
def slide(x):
    # slider_label.config(text=f'{int(my_slider.get())} of {int(song_length)}')
    song = song_list_box.get(ACTIVE)
    song = f'C:/Users/Gaurav/Music/demo/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))


def volumnSlide(x):
    pygame.mixer.music.set_volume(volume_slider.get()) # set values form 0 - 1

    # current_volume = pygame.mixer.music.get_volume()
    # slider_label.config(text=int(current_volume * 100))

# Create Master Frame
master_frame = Frame(root)
master_frame.pack(pady=20)


#Create Playlist box
song_list_box = Listbox(master_frame, bg='black', fg='white', width=85, height=15, selectbackground='gray', selectforeground='black')
song_list_box.grid(row=0, column=0)

#Define Player Control Button Images
back_btn_img = PhotoImage(file='C:/Users/Gaurav/Music/images/previous_icon.png')
forward_btn_img = PhotoImage(file='C:/Users/Gaurav/Music/images/next_icon.png')
play_btn_img = PhotoImage(file='C:/Users/Gaurav/Music/images/play_icon.png')
pause_btn_img = PhotoImage(file='C:/Users/Gaurav/Music/images/pause_icon.png')
stop_btn_img = PhotoImage(file='C:/Users/Gaurav/Music/images/stop_icon.png')

# Create Player Control Frames
controls_frame = Frame(master_frame)
controls_frame.grid(row=1, column=0, pady=20)

# create volume label frame
volume_frame = LabelFrame(master_frame, text='volume')
volume_frame.grid(row=0, column=1, padx=20)


# Create Player Control Buttons
back_button = Button(controls_frame, image=back_btn_img, borderwidth=0, command=play_previous_track)
forward_button = Button(controls_frame, image=forward_btn_img, borderwidth=0, command=play_next_track)
play_button = Button(controls_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button = Button(controls_frame, image=pause_btn_img, borderwidth=0, command=pause)
stop_button = Button(controls_frame, image=stop_btn_img, borderwidth=0, command=stop)

back_button.grid(row=0, column=0, padx=10)
forward_button.grid(row=0, column=4, padx=10)
play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=1, padx=10)
stop_button.grid(row=0, column=3, padx=10)

#Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

#add Song Menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label='Add Songs', menu=add_song_menu)
add_song_menu.add_command(label='Add One Song To PlayList', command=add_song)
add_song_menu.add_command(label='Add Many Song To PlayList', command=add_many_songs)

# Create Delete song menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label='Remove Songs', menu=remove_song_menu)
remove_song_menu.add_command(label='Remove One Song', command=delete_song)
remove_song_menu.add_command(label='Remove All Songs', command=delete_all_songs)


status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)


#create slider
my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=400)# value = current position of slider
my_slider.grid(row=2, column=0, pady=10)

#create temp slider label
# slider_label = Label(root, text='0')
# slider_label.pack(pady=10)

# create volumn slider
volume_slider = ttk.Scale(volume_frame, from_=1, to=0, orient=VERTICAL, value=1, command=volumnSlide, length=200)# value = current position of slider
volume_slider.pack(pady=10)
root.mainloop()
