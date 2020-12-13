# import necessary modules
from builtins import enumerate
from itertools import chain

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, date, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='Na')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()


today = datetime.today().date()


def todaytask():
    rows = session.query(Table).filter(Table.deadline == today).all()
    print("Today {} {}:".format(today.strftime("%d"), today.strftime("%b")))
    if len(rows) == 0:
        print("Nothing to do!")
    else:
        for i, task in enumerate(rows, start=1):
            if str(task.deadline) == str(date.today()):
                print("{}. {}".format(i, task.task))
    print()


def weekstask():
    for i in range(7):
        date = today + timedelta(days=i)
        rows = session.query(Table).filter(Table.deadline == date).all()
        print("{} {} {}:".format(date.strftime("%A"),
                                 date.strftime("%d"), date.strftime("%b")))
        if len(rows) == 0:
            print("Nothing to do!")
        else:
            for j, task in enumerate(rows, start=1):
                if str(task.deadline) == str(date):
                    print("{}. {}".format(j, task.task))
        print()


def alltasks():
    rows = session.query(Table).order_by(Table.deadline).all()
    if len(rows) == 0:
        print("Nothing to do!")
    else:
        print("All tasks:")
        for i, task in enumerate(rows, start=1):
            print("{}. {}. {} {}".format(i, task.task,
                                         task.deadline.strftime("%d"), task.deadline.strftime("%b")))
    print()


def missedtaks():
    rows = session.query(Table).filter(Table.deadline < today).all()
    print("Missed tasks:")
    if len(rows) == 0:
        print("Nothing is missed!")
        print()
    else:
        for i, task in enumerate(rows, start=1):
            print("{}. {}. {} {}".format(i, task.task,
                                         task.deadline.strftime("%d"), task.deadline.strftime("%b")))
        session.query(Table).filter(Table.deadline < today).delete()
        session.commit()
        print()


def addtask():
    print("Enter task")
    work = input()
    print("Enter deadline")
    due_date = input().split('-')
    due_date = list(map(int, due_date))
    new_row = Table(task=work, deadline=datetime(
        due_date[0], due_date[1], due_date[2]))
    session.add(new_row)
    session.commit()
    print("The task has been added!")
    print()


def deletetask():
    rows = session.query(Table).order_by(Table.deadline).all()
    if len(rows) == 0:
        print("Nothing to delete")
    else:
        print("Choose the number of the task you want to delete:")
        taskDict = {}
        for i, task in enumerate(rows, start=1):
            taskDict[i] = task.task
            print("{}. {}. {} {}".format(i, task.task,
                                         task.deadline.strftime("%d"), task.deadline.strftime("%b")))
        choice = int(input())
        session.query(Table).filter(Table.task == taskDict[choice]).delete()
        session.commit()
        print("The task has been deleted!")
    print()


def menu():
    while True:
        print("1) Today's tasks")
        print("2) Week's tasks")
        print("3) All tasks")
        print("4) Missed tasks")
        print("5) Add task")
        print("6) Delete task")
        print("0) Exit")

        choice = int(input())

        if choice == 1:
            todaytask()
        if choice == 2:
            weekstask()
        if choice == 3:
            alltasks()
        if choice == 4:
            missedtaks()
        if choice == 5:
            addtask()
        if choice == 6:
            deletetask()
        if choice == 0:
            print('Bye!')
            session.close()
            exit(0)


if __name__ == '__main__':
    menu()
