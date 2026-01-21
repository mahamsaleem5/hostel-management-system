import pickle

# ---------------- LINKED LIST ----------------
class Student:
    def __init__(self, sid, name, room, contact):
        self.id, self.name, self.room, self.contact = sid, name, room, contact

class Node:
    def __init__(self, student):
        self.student, self.next = student, None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, s):
        if self.search(s.id):
            print("Student ID already exists!")
            return False
        n = Node(s)
        n.next = self.head
        self.head = n
        print("Student added successfully!")
        return True

    def search(self, sid):
        cur = self.head
        while cur:
            if cur.student.id == sid:
                return cur.student
            cur = cur.next
        return None

    def delete(self, sid):
        if not self.head:
            print("No students found!")
            return None
        if self.head.student.id == sid:
            temp = self.head.student
            self.head = self.head.next
            print("Student deleted successfully!")
            return temp
        cur = self.head
        while cur.next:
            if cur.next.student.id == sid:
                temp = cur.next.student
                cur.next = cur.next.next
                print("Student deleted successfully!")
                return temp
            cur = cur.next
        print("Student not found!")
        return None

    def display(self):
        if not self.head:
            print("No students found!")
            return
        print("\n--- All Students ---")
        i, cur = 1, self.head
        while cur:
            s = cur.student
            print(f"{i}. ID:{s.id} | Name:{s.name} | Room:{s.room} | Contact:{s.contact}")
            cur, i = cur.next, i + 1

    def get_all(self):
        arr, cur = [], self.head
        while cur:
            arr.append(cur.student)
            cur = cur.next
        return arr

# ---------------- MIN HEAP ----------------
class MinHeap:
    def __init__(self):
        self.heap = []

    def insert(self, v):
        self.heap.append(v)
        i = len(self.heap) - 1
        while i > 0:
            p = (i - 1) // 2
            if self.heap[i] < self.heap[p]:
                self.heap[i], self.heap[p] = self.heap[p], self.heap[i]
                i = p
            else:
                break

    def extract_min(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        mn = self.heap[0]
        self.heap[0] = self.heap.pop()
        i = 0
        while True:
            l, r, sm = 2*i+1, 2*i+2, i
            if l < len(self.heap) and self.heap[l] < self.heap[sm]:
                sm = l
            if r < len(self.heap) and self.heap[r] < self.heap[sm]:
                sm = r
            if sm == i:
                break
            self.heap[i], self.heap[sm] = self.heap[sm], self.heap[i]
            i = sm
        return mn

    def peek(self):
        return self.heap[0] if self.heap else None

    def display(self):
        print("Available Rooms:", self.heap if self.heap else "No rooms available.")

# ---------------- QUEUE ----------------
class Complaint:
    def __init__(self, cid, sid, room, desc):
        self.cid, self.sid, self.room, self.desc = cid, sid, room, desc

class Queue:
    def __init__(self):
        self.q = []

    def enqueue(self, v): self.q.append(v)
    def dequeue(self):    return self.q.pop(0) if self.q else None

    def display(self):
        if not self.q:
            print("No complaints.")
            return
        print("\n--- Complaint Queue ---")
        for c in self.q:
            print(f"#{c.cid} | Student:{c.sid} | Room:{c.room} | {c.desc}")

# ---------------- HOSTEL SYSTEM ----------------
class HostelSystem:
    def __init__(self):
        self.students = LinkedList()
        self.rooms = MinHeap()
        for r in range(101, 121): self.rooms.insert(r)
        self.complaints, self.cid = Queue(), 1

    def add_student(self):
        try:
            sid = int(input("Student ID: "))
            name = input("Name: ")
            contact = input("Contact: ")
            room = self.rooms.extract_min()
            if room is None:
                print("No rooms available!")
                return
            s = Student(sid, name, room, contact)
            if not self.students.insert(s):
                self.rooms.insert(room)
            else:
                print("Room", room, "assigned!")
        except:
            print("Invalid input!")

    def search_student(self):
        try:
            sid = int(input("Student ID: "))
            s = self.students.search(sid)
            print(f"ID:{s.id} | Name:{s.name} | Room:{s.room} | Contact:{s.contact}" if s else "Not found!")
        except:
            print("Invalid!")

    def delete_student(self):
        try:
            sid = int(input("Enter ID: "))
            s = self.students.delete(sid)
            if s: self.rooms.insert(s.room)
        except:
            print("Invalid!")

    def search_room(self):
        try:
            room = int(input("Room Number: "))
            cur = self.students.head
            while cur:
                if cur.student.room == room:
                    print("Room occupied by", cur.student.name)
                    return
                cur = cur.next
            print("Room available" if room in self.rooms.heap else "Room not found")
        except:
            print("Invalid!")

    def add_complaint(self):
        try:
            sid = int(input("Student ID: "))
            s = self.students.search(sid)
            if not s:
                print("Student not found!")
                return
            desc = input("Issue: ")
            c = Complaint(self.cid, sid, s.room, desc)
            self.complaints.enqueue(c)
            print("Complaint #", self.cid, "added")
            self.cid += 1
        except:
            print("Invalid!")

    def resolve(self):
        c = self.complaints.dequeue()
        print("Resolved:", c.desc if c else "No complaints")

    def save(self):
        data = {
            'students': self.students.get_all(),
            'rooms': self.rooms.heap,
            'complaints': self.complaints.q,
            'cid': self.cid
        }
        pickle.dump(data, open("hostel.dat", "wb"))
        print("Data saved!")

    def load(self):
        try:
            data = pickle.load(open("hostel.dat", "rb"))
            self.students = LinkedList()
            for s in data['students']: self.students.insert(s)
            self.rooms = MinHeap()
            for r in data['rooms']: self.rooms.insert(r)
            self.complaints = Queue()
            for c in data['complaints']: self.complaints.enqueue(c)
            self.cid = data['cid']
            print("Data loaded!")
        except:
            print("No saved data found!")

# ---------------- MENU ----------------
def main():
    h = HostelSystem()
    menu = """
========== MAIN MENU ==========
STUDENT OPERATIONS:
  1. Add New Student
  2. Search Student by ID
  3. Delete Student
  4. Display All Students

ROOM OPERATIONS:
  5. Search Room Status
  6. Display Available Rooms
  7. View Next Available Room

COMPLAINT OPERATIONS:
  8. Add Complaint
  9. Resolve Complaint
  10. Display All Complaints

FILE OPERATIONS:
  11. Save Data to File
  12. Load Data from File

  0. Exit
"""
    while True:
        print(menu)
        choice = input("Enter choice: ").strip()
        if choice == '1': h.add_student()
        elif choice == '2': h.search_student()
        elif choice == '3': h.delete_student()
        elif choice == '4': h.students.display()
        elif choice == '5': h.search_room()
        elif choice == '6': h.rooms.display()
        elif choice == '7': print("Next Room:", h.rooms.peek())
        elif choice == '8': h.add_complaint()
        elif choice == '9': h.resolve()
        elif choice == '10': h.complaints.display()
        elif choice == '11': h.save()
        elif choice == '12': h.load()
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
