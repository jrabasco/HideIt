#!/usr/bin/python3.4

import os

class ProgressBar:
    def __init__(self, task_number, bar_opening="[", bar_ending="]", empty_char="-", filled_char="=",
                 update_rate=0, percent_precision=1, display_percent=True, display_absolute_progress=True, bar_length=0,
                 enable_front_char=False, front_char=">"):

        self.__task_number = task_number
        self.__bar_opening = bar_opening
        self.__bar_ending = bar_ending
        self.__empty_char = empty_char
        self.__filled_char = filled_char
        self.__update_rate = update_rate
        self.__percent_precision = str(percent_precision)
        self.__display_percent = display_percent
        self.__display_absolute_progress = display_absolute_progress

        if bar_length > 0:
            self.__bar_length = min(bar_length, self.__compute_max_length())
        else:
            self.__bar_length = self.__compute_max_length()

        self.__enable_front_char = enable_front_char

        self.__front_char = front_char

    def begin(self):
        self.__update_count = 0
        self.__current_length = 0
        self.__current_progress = 0
        print(self.__get_bar_string(), end='\r')

    def add_progress(self, inc=1):
        increment = inc if inc > 0 else 1
        if self.__current_progress < self.__task_number:
            prev_percent = self.__get_percent_progress()
            self.__current_progress = min(self.__task_number, self.__current_progress + increment)
            self.__update_count += increment
            new_length = int(self.__get_progress() * self.__bar_length)
            if self.__update_rate > 0:
                need_to_update = self.__update_count >= self.__update_rate
            else:
                need_to_update = new_length > self.__current_length or prev_percent != self.__get_percent_progress()
            if need_to_update or self.__current_progress == self.__task_number:
                self.__update_count = 0
                self.__current_length = new_length
                end_char = "\r" if self.__current_progress < self.__task_number else "\n"
                print(self.__get_bar_string(), end=end_char)

    def __get_progress(self):
        return float(float(self.__current_progress) / float(self.__task_number))

    def __get_percent_progress(self):
        format_string = "{0:." + self.__percent_precision + "f}"
        return format_string.format(self.__get_progress() * 100) + "%"

    def __get_progress_fraction(self):
        return str(self.__current_progress) + "/" + str(self.__task_number)

    def __get_bar_string(self):
        diff = self.__bar_length - self.__current_length - (1 if self.__enable_front_char else 0)
        progresses = ""
        if self.__display_percent:
            progresses += " : " + self.__get_percent_progress()
            progresses += " (" + self.__get_progress_fraction() + ")" if self.__display_absolute_progress else ""
        elif self.__display_absolute_progress:
            progresses += " : " + self.__get_progress_fraction()
        front_char = self.__front_char if (
            self.__enable_front_char and self.__current_progress < self.__task_number) else ""
        return ( self.__bar_opening + self.__current_length * self.__filled_char + front_char +
                 diff * self.__empty_char + self.__bar_ending + progresses )

    def __compute_max_length(self):

        sz = None

        try:
            sz = os.get_terminal_size().columns
        except:
            pass

        if sz is None:
            sz = 80

        max_length = int(sz)
        max_length -= (len(str(self.__task_number)) * 2 + 1) if self.__display_absolute_progress else 0
        max_length -= len(self.__bar_opening)
        max_length -= len(self.__bar_ending)
        max_length -= (5 + int(self.__percent_precision)) if self.__display_percent else 0
        max_length -= 1 if int(self.__percent_precision) > 0 else 0
        max_length -= 3 if (self.__display_percent and self.__display_absolute_progress) else 0
        max_length -= 2 if (self.__display_percent or self.__display_absolute_progress) else 0
        return max_length - 1
