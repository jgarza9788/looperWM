import time
import win32gui
import pyautogui
import keyboard
from screeninfo import get_monitors

# Global variables
hotkey_down = "win+pagedown"  # Change this to your desired hotkey combination
hotkey_up = "win+pageup"  # Change this to your desired hotkey combination

# hotkey_down = "ctrl+alt+n"
# hotkey_up = "ctrl+alt+m"
monitors = get_monitors()
win_list = []

excluded_windows = [
    'Windows Input Experience',
    'MainWindow',
    'NVIDIA GeForce Overlay',
    'Program Manager'
]

def cb_for_wl(hwnd, win_list):
    if win32gui.IsWindowVisible(hwnd):
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y

        title = win32gui.GetWindowText(hwnd)

        print("Window:" ,title)
        print("\tLocation: (%d, %d)" % (x, y))
        print("\t    Size: (%d, %d)" % (w, h))

        if len(title) > 0 and title not in excluded_windows:
            win_list.append({'id': hwnd,'title':title,'x':x,'y':y,'w':w,'h':h})

        if rect[0] < 0 and rect[2] > 0:
            print('Docked Window:',title)
            win32gui.BringWindowToTop(hwnd)
            win32gui.SetActiveWindow(hwnd)
            pyautogui.press('win')
            time.sleep(0.25)
            pyautogui.press('left')

        if y < 0:
            print('Max Window:',title)
            win32gui.BringWindowToTop(hwnd)
            win32gui.SetActiveWindow(hwnd)
            pyautogui.press('win')
            time.sleep(0.25)
            pyautogui.press('down')

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

def move_window(hwnd, x, y, w, h):
    win32gui.MoveWindow(hwnd, x, y, w, h, True)


def move_windows(wl):
    for index,w in enumerate(wl):
        # time.sleep(0.1)
        print('moving:',w)
        if index == 0 :
            move_window(w['id'],0,0,monitors[0].width - 800, monitors[0].height)
            win32gui.BringWindowToTop(w['id'])
            win32gui.SetActiveWindow(w['id'])
        else:
            h = monitors[0].height//len(wl)
            move_window(w['id'],monitors[0].width - 800,(h*(len(wl) - index-1)),800,h)


def rotDown():
    global win_list
    # if event.event_type == keyboard.KEY_DOWN:
    print('rotDown')
    win_list = win_list[1:] + [win_list[0]]
    move_windows(win_list)

def rotUp():
    global win_list
    # if event.event_type == keyboard.KEY_DOWN:
    print('rotUp')
    win_list = [win_list[-1]] + win_list[:-1]
    move_windows(win_list)

def main():
    global win_list
    global hotkey_up
    global hotkey_down
    win_list = get_win_list()
    print(len(win_list))
    print(*win_list,sep='\n')
    print(*get_win_list(),sep='\n')

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