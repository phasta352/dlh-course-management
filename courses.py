from abc import ABC, abstractmethod

class Course:
    def __init__(self, course_id, title, price, capacity):
        if price < 0:
            raise ValueError("Price cannot be negative.")
        elif capacity <= 0:
            raise ValueError("Capacity cannot be negative.")
        
        self.course_id = course_id
        self.title = title
        self.__price = price
        self.__capacity = capacity 

    @abstractmethod
    def joining_instructions(self):
        pass

    def __str__(self):
        return f"{self.course_id}: {self.title} - ${self.price} ({self.capacity} seats available)"

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

# courses = [OnlineCourse("C001", "Python Basics", 150, 10, "www.teams.com/join/C001"),
#            ClassroomCourse("C002", "Python Intermediate", 200, 30, "C2.02.05", "14 Prte de France, 4360 Esch-Belval Esch-sur-Alzette")]

# for course in courses:
#     print(f"{course.title}: {course.joining_instructions()}")