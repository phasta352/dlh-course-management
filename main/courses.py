#!/usr/bin/env python3
from abc import ABC, abstractmethod

# Base class for courses with common attributes and methods
class Course:
    def __init__(self, course_id, title, price, capacity):
        if price < 0:
            raise ValueError("Price cannot be negative.")
        elif capacity <= 0:
            raise ValueError("Capacity cannot be negative.")
        
        self.course_id = course_id
        self.title = title
        self.set_price(price)
        self.set_capacity(capacity)

    def set_price(self, price):
        if price < 0:
            raise ValueError("Price cannot be negative.")
        self.__price = price

    def set_capacity(self, capacity):
        if capacity <= 0:
            raise ValueError("Capacity cannot be negative.")
        self.__capacity = capacity

    def get_price(self):
        return self.__price

    def get_capacity(self):
        return self.__capacity

    @abstractmethod
    def joining_instructions(self):
        pass

    def __str__(self):
        return f"{self.course_id}: {self.title} - ${self.get_price()} ({self.get_capacity()} seats available)"

# Subclasses for specific course types with additional attributes and methods
class OnlineCourse(Course):
    def __init__(self, course_id, title, price, capacity, meeting_link):
        super().__init__(course_id, title, price, capacity)
        self.meeting_link = meeting_link

    def joining_instructions(self):
        return f"Join online using this link: {self.meeting_link}"

class ClassroomCourse(Course):
    def __init__(self, course_id, title, price, capacity, room_number, address):
            super().__init__(course_id, title, price, capacity)
            self.room_number = room_number
            self.address = address

    def joining_instructions(self):
        return f"You can find the class in room {self.room_number} at {self.address}"
