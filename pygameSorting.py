import math
import pygame
import random
import sys
import numpy as np


def init(width=1000):
    pygame.init()
    pygame.mixer.init()

    width, height = width, 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Sorting Algorithm Visualizer")

    return [screen, width]


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)


def play_sound(frequency, duration=10, use_sound=True):
    if not use_sound:
        return

    if frequency < 200:
        frequency = 200
    elif frequency > 5000:
        frequency = 5000

    sample_rate = 44100
    t = np.linspace(0, duration / 1000, int(sample_rate * (duration / 1000)), endpoint=False)
    wave = 32767 * np.sin(2.0 * np.pi * frequency * t)
    stereo_wave = np.column_stack((wave, wave))
    sound = pygame.sndarray.make_sound(stereo_wave.astype(np.int16))
    pygame.mixer.stop()

    sound.set_volume(0.1)
    sound.play(maxtime=duration)


def update_screen(screen, arr, slowdown, index, use_sound):
    screen[0].fill(BLACK)
    num_bars = len(arr)
    bar_width = (screen[1] - 200) // num_bars - 2
    heightval = 600 / max(arr)

    for i, val in enumerate(arr):
        scaled_height = math.floor(val * heightval)
        if i == index:
            color = GREEN
        else:
            color = WHITE

        x_position = 100 + i * (bar_width + 2)
        pygame.draw.rect(screen[0], color, (x_position, 700 - scaled_height, bar_width, scaled_height))

        #ten fragment kodu to przypomnienie ze masz downa ;)
        if i == index:
            frequency = val
            play_sound(frequency, use_sound=use_sound)

    pygame.display.flip()
    pygame.time.wait(slowdown)


def finish(screen, arr, time, use_sound=True):
    screen[0].fill(BLACK)
    bar_width = ((screen[1] - 200) // len(arr)) - 2
    heightval = 600 / max(arr)

    for i, val in enumerate(arr):
        scaled_height = math.floor(val * heightval)
        pygame.draw.rect(screen[0], WHITE, (100 + i * (bar_width + 2), 700 - scaled_height, bar_width, scaled_height))

    for i, val in enumerate(arr):
        scaled_height = math.floor(val * heightval)
        pygame.draw.rect(screen[0], GREEN, (100 + i * (bar_width + 2), 700 - scaled_height, bar_width, scaled_height))
        pygame.display.flip()

        frequency = val

        play_sound(frequency, use_sound=use_sound)
        pygame.time.wait(time)
        yield


def quicksort(arr, l, r, screen, slowdown, use_sound):
    if l < r:
        partition_pos = yield from partition(arr, l, r, screen, slowdown, use_sound)
        yield from quicksort(arr, l, partition_pos - 1, screen, slowdown, use_sound)
        yield from quicksort(arr, partition_pos + 1, r, screen, slowdown, use_sound)


def partition(arr, l, r, screen, slowdown, use_sound):
    i = l
    j = r - 1
    pivot = arr[r]
    while i < j:
        while i < r and arr[i] < pivot:
            i += 1
        while j > l and arr[j] >= pivot:
            j -= 1
        if i < j:
            arr[i], arr[j] = arr[j], arr[i]
            update_screen(screen, arr, slowdown, j, use_sound)
            yield

    if arr[i] > pivot:
        arr[i], arr[r] = arr[r], arr[i]
        update_screen(screen, arr, slowdown, r, use_sound)
        yield

    return i


#postaraj sie nauczyć mniej wiecej jak
# chatgpt postanowił rozwiazac problem updatowania screena na każdym arrayu
# osobno bo jest 23:41 i mi sie nie chce myslec teraz
# ~ ode mnie do mnie jutro
def merge_sort(arr, screen, slowdown, use_sound, left=0, right=None):
    if right is None:
        right = len(arr) - 1

    if left < right:
        mid = (left + right) // 2

        yield from merge_sort(arr, screen, slowdown, use_sound, left, mid)
        yield from merge_sort(arr, screen, slowdown, use_sound, mid + 1, right)

        i = left
        j = mid + 1
        k = left
        temp_arr = arr[left:right+1]

        while i <= mid and j <= right:
            if temp_arr[i - left] < temp_arr[j - left]:
                arr[k] = temp_arr[i - left]
                i += 1
            else:
                arr[k] = temp_arr[j - left]
                j += 1
            update_screen(screen, arr, slowdown, k, use_sound)
            k += 1
            yield

        while i <= mid:
            arr[k] = temp_arr[i - left]
            update_screen(screen, arr, slowdown, k, use_sound)
            i += 1
            k += 1
            yield

        while j <= right:
            arr[k] = temp_arr[j - left]
            update_screen(screen, arr, slowdown, k, use_sound)
            j += 1
            k += 1
            yield


def bubblesort(arr, screen, slowdown, use_sound):
    swapped = True

    while swapped:
        swapped = False
        for i in range(len(arr) - 1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
                update_screen(screen, arr, slowdown, i+1, use_sound)
                yield


def swap(lst, i, j ):
    lst[i], lst[j] = lst[j], lst[i]


def siftDown(lst, i, upper, screen, slowdown, use_sound):
    while True:
        l, r = i*2+1, i*2+2
        if max(l, r) < upper:
            if lst[i] >= max(lst[l], lst[r]):
                break
            elif lst[l] > lst[r]:
                swap(lst, i, l)
                update_screen(screen, lst, slowdown, l, use_sound)
                i = l
            else:
                swap(lst, i, r)
                update_screen(screen, lst, slowdown, r, use_sound)
                i = r
        elif l < upper:
            if lst[l] >= lst[i]:
                swap(lst, i, l)
                update_screen(screen, lst, slowdown, l, use_sound)
                i = l
            else:
                break
        elif r < upper:
            if lst[r] > lst[i]:
                swap(lst, i, r)
                update_screen(screen, lst, slowdown, r, use_sound)
                i = r
            else:
                break
        else:
            break


def heapsort(lst, screen, slowdown, use_sound):
    for j in range((len(lst)-2)//2, -1, -1):
        siftDown(lst, j, len(lst), screen, slowdown, use_sound)
        yield

    for end in range(len(lst)-1, 0, -1):
        swap(lst, 0, end)
        update_screen(screen, lst, slowdown, end, use_sound)
        siftDown(lst, 0, end, screen, slowdown, use_sound)
        yield


def insertion(arr, screen, slowdown, use_sound):
    for i in range(1, len(arr)):
        j = i
        while arr[j - 1] > arr[j] and j > 0:
            arr[j], arr[j - 1] = arr[j - 1], arr[j]
            j -= 1
            update_screen(screen, arr, slowdown, j - 1, use_sound)
            yield


def selection(arr, screen, slowdown, use_sound):
    for i in range(0, len(arr) - 1):
        min_index = i
        for j in range(i + 1, len(arr)):
            if arr[min_index] > arr[j]:
                min_index = j

        arr[i], arr[min_index] = arr[min_index], arr[i]
        update_screen(screen, arr, slowdown, min_index, use_sound)
        yield


def main():
    try:
        sorting_algorithm = input("Enter sorting algorithm (quicksort, bubblesort, heapsort, insertion, selection, mergesort): ").strip().lower()
        max_value = int(input("Enter max value: "))
        amount = int(input("Enter amount of values: "))
        slowdown = float(input("Enter slowdown in seconds: "))
        use_sound_input = input("Use sound? [y/n]: ").strip().lower()
        use_sound = use_sound_input == "y"
    except ValueError:
        print("invalid numeric value")
        sys.exit()

    slowdown = int(math.floor(slowdown * 1000))

    if amount > 265:
        screen = init((amount - 265) * 3 + 1000)
    else:
        screen = init()

    finish_time = math.floor(1000 / amount)
    if finish_time < 1:
        finish_time = 1

    arr = [random.randint(1, max_value) for _ in range(amount)]

    update_screen(screen, arr, slowdown, None, use_sound)

    def start_sorting_algorithm():
        nonlocal sorting_done, finish_gen
        global sort_gen
        if sorting_algorithm == "quicksort":
            sort_gen = quicksort(arr, 0, len(arr) - 1, screen, slowdown, use_sound)
        elif sorting_algorithm == "bubblesort":
            sort_gen = bubblesort(arr, screen, slowdown, use_sound)
        elif sorting_algorithm == "heapsort":
            sort_gen = heapsort(arr, screen, slowdown, use_sound)
        elif sorting_algorithm == "insertion":
            sort_gen = insertion(arr, screen, slowdown, use_sound)
        elif sorting_algorithm == "selection":
            sort_gen = selection(arr, screen, slowdown, use_sound)
        elif sorting_algorithm == "mergesort":
            sort_gen = merge_sort(arr, screen, slowdown, use_sound)
        else:
            print("Invalid sorting algorithm")
            return

        sorting_done = False
        finish_gen = None

    start_sorting_algorithm()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    arr = [random.randint(1, max_value) for _ in range(amount)]
                    update_screen(screen, arr, slowdown, None, use_sound)
                    start_sorting_algorithm()

        if not sorting_done:
            try:
                next(sort_gen)
            except StopIteration:
                sorting_done = True
                finish_gen = finish(screen, arr, finish_time, use_sound)
        else:
            try:
                next(finish_gen)
            except StopIteration:
                pass

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
