import time
import win32gui
import pyautogui
import keyboard
import win32con

from screeninfo import get_monitors



# Global variables
hotkey_down = "win+pagedown"  # Change this to your desired hotkey combination
hotkey_up = "win+pageup"  # Change this to your desired hotkey combination

# hotkey_down = "ctrl+alt+n"
# hotkey_up = "ctrl+alt+m"
monitors = get_monitors()
print(f'{len(monitors)=}')
win_list = []

excluded_windows = [
    'Windows Input Experience',
    'MainWindow',
    'NVIDIA GeForce Overlay',
    'Program Manager',
    'Windows Shell Experience Host'
]

# config ... this will be it's own file later
side_width = 250
y_spread = 150
window_size = (250,500)

def cb_for_wl(hwnd, win_list):
    if win32gui.IsWindowVisible(hwnd):
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y

        title = win32gui.GetWindowText(hwnd)

        # print("Window:" ,title)
        # print("\tLocation: (%d, %d)" % (x, y))
        # print("\t    Size: (%d, %d)" % (w, h))

        if len(title) > 0 and title not in excluded_windows:
            if (x+y) != -64000:
                win_list.append({'id': hwnd,'title':title,'x':x,'y':y,'w':w,'h':h})

        # if rect[0] < 0 and rect[2] > 0:
        #     print('Docked Window:',title)
        #     win32gui.BringWindowToTop(hwnd)
        #     win32gui.SetActiveWindow(hwnd)
        #     pyautogui.hotkey('win', 'left')
        #     # pyautogui.press('winleft')
        #     # time.sleep(0.25)
        #     # pyautogui.press('left')

        # if y < 0:
        #     print('Max Window:',title)
        #     win32gui.BringWindowToTop(hwnd)
        #     win32gui.SetActiveWindow(hwnd)
        #     pyautogui.hotkey('win', 'down')
        #     # pyautogui.press('win')
        #     # time.sleep(0.25)
        #     # pyautogui.press('down')

        # if (x+y) != 0 and (x+y) != -64000 and len(title) > 0:
        #     print(hwnd)
        #     print("Window:" ,title)
        #     print("\tLocation: (%d, %d)" % (x, y))
        #     print("\t    Size: (%d, %d)" % (w, h))
        #     win_list.append({'id': hwnd,'text':win32gui.GetWindowText(hwnd),'x':x,'y':y,'w':w,'h':h})

def get_win_list():
    result = []
    win32gui.EnumWindows(cb_for_wl, result)
    return result

# import ctypes

# # Constants for SystemParametersInfo
# SPI_SETANIMATION = 0x0049
# SPI_GETANIMATION = 0x0048
# SPIF_UPDATEINIFILE = 0x01
# SPIF_SENDCHANGE = 0x02

# # Define the ANIMATIONINFO structure
# class ANIMATIONINFO(ctypes.Structure):
#     _fields_ = [("cbSize", ctypes.c_uint), ("iMinAnimate", ctypes.c_int)]

# def set_animation(enable):
#     # Create an instance of ANIMATIONINFO
#     animation_info = ANIMATIONINFO()
#     animation_info.cbSize = ctypes.sizeof(ANIMATIONINFO)
#     animation_info.iMinAnimate = int(enable)

#     # Set the animation setting
#     ctypes.windll.user32.SystemParametersInfoW(
#         SPI_SETANIMATION, 
#         animation_info.cbSize, 
#         ctypes.byref(animation_info), 
#         SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
#     )

def move_window(hwnd, x, y, w, h,index:int=0,title:str=""):
    print(index,title,x,y,w,h)
    
    win32gui.MoveWindow(hwnd, x, y, w, h, True)
    


def is_fullscreen(x, y, w, h):
    return x == 0 and y == 0 and w == monitors[0].width and h == monitors[0].height


def num_to_location(num,monitor_0_width,quarter_width,quarter_height):
    x,y = num%4 ,num//4
    return monitor_0_width + (quarter_width * x),quarter_height * y


def move_windows_2monitors(index,w):
    # print(index,w)

    if index == 0 :
        move_window(w['id'],0,0,monitors[0].width, monitors[0].height - 75,index=index,title=w['title'])
        setFocus(w['id'])
    else:
        i = index - 1
        qw = int(monitors[0].width/4)
        qh = int(monitors[0].height/4)
        x,y = num_to_location(i,monitors[0].width,qw,qh)
        move_window(w['id'],int(x),int(y),qw,qh,index=index,title=w['title'])
        # setFocus(w['id'])


def move_windows():
    global win_list
    # set_animation(False)
    for index, w in enumerate(win_list):
        # time.sleep(0.1)
        try:
            # if is_fullscreen(w['x'], w['y'], w['w'], w['h']):
            #     win32gui.ShowWindow(w['id'], win32con.SW_MINIMIZE)
            #     win32gui.ShowWindow(w['id'], win32con.SW_RESTORE)
            if len(monitors) == 2:
                move_windows_2monitors(index,w)
            else:
                if is_fullscreen(w['x'], w['y'], w['w'], w['h']):
                    print(f"Skipping full-screen window: {w['title']}")
                    continue
                if index == 0 :
                    move_window(w['id'],0,0,monitors[0].width - side_width, monitors[0].height,index=index,title=w['title'])
                else:
                    move_window(w['id'],monitors[0].width - side_width,(y_spread*(index-1)),window_size[0],window_size[1],index=index,title=w['title'])
                    # setFocus(w['id'])
        except Exception as e:
            print(e)
            del(win_list[index])
            move_windows()
    # set_animation(True)

    
    print("-"*20)

# def setFocus(id):
#     focused = False
#     error_count = 0 
#     while focused == False:
#         try:
#             win32gui.SetForegroundWindow(win_list[0]['id'])
#             focused = True
#             print('errors',error_count)
#         except:
#             error_count += 1
#             time.sleep(0.1)
            
def setFocus(hwnd):

    focused = False
    error_count = 0 
    while focused == False:
        if error_count >= 3:
            print(f'{error_count=}')
            print('you were switching too fast')
            break
        try:
            # win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            # win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            # win32gui.SetForegroundWindow(win_list[0]['id'])
            focused = True
            # print('errors',error_count)
        except:
            error_count += 1
            time.sleep(0.1)




def find_new_windows(wl):
    nwl = get_win_list()

    wtitles = [w['id'] for w in wl]

    for w in nwl:
        if w['id'] in wtitles:
            pass # do nothing
        else:
            wl.insert(0,w)
    
    return wl


def rotUp():
    print('rotUp')
    global win_list
    win_list = find_new_windows(win_list)
    
    win_list = win_list[1:] + [win_list[0]]
    move_windows()

    # print(win_list)
    setFocus(win_list[0]['id'])


def rotDown():
    print('rotDown')
    global win_list
    win_list = find_new_windows(win_list)
    
    win_list = [win_list[-1]] + win_list[:-1]
    move_windows()

    # print(win_list)
    setFocus(win_list[0]['id'])
            

def main():
    global win_list
    global hotkey_up
    global hotkey_down
    win_list = get_win_list()
    # print(len(win_list))
    print(*win_list,sep='\n')
    # print(*get_win_list(),sep='\n')

    

    keyboard.add_hotkey(hotkey_down, callback=rotDown)
    keyboard.add_hotkey(hotkey_up, callback=rotUp)

    keyboard.wait()

    # win_list = get_win_list()
    # print(len(win_list))
    # print(*win_list,sep='\n')

    # move_windows(win_list)

    # win_list = get_win_list()
    # print(*win_list,sep='\n')

if __name__ == '__main__':
    main()