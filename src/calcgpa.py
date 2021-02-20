"""
calcgpa.py
    Calculates GPA of certain courses according to a query.
"""

import argparse
from sys import exit
from os import path


def filter_courses(original_courses_list, year, upper_bound, lower_bound, semester):
    """
    Returns the filtered list of courses by fulfilling ALL of the filter demands specified in the command line.
    """
    filtered_courses_list = []

    for course in original_courses_list:
        if year is not None and course.year != year:
            continue
        if upper_bound is not None and course.grade > upper_bound:
            continue
        if lower_bound is not None and course.grade < lower_bound:
            continue
        if semester is not None and course.semester != semester:
            continue
        filtered_courses_list.append(course)

    return filtered_courses_list


def print_output(filtered_courses_list):
    """
    Beautifully prints the details for the filtered courses list.
    """

    if not filtered_courses_list:
        print("No courses matched the query.")
        return

    max_name_length = max([len(course.name) for course in filtered_courses_list])

    print(" Sem  | Course ID | Pts | " +
          " " * ((max_name_length - 11) // 2 + (max_name_length - 1) % 2) + "Course Name" + " " * ((max_name_length - 11) // 2) +
          " | Grade")
    print("______|___________|_____|" + "_" * (max_name_length + 2) + "|______")

    for course in filtered_courses_list:
        print(str(course.year) + course.semester, end=" | ")
        print(course.cid, end=" |  ")
        print(course.creditpts, end="  | ")
        print(course.name, end=" " * (max_name_length - len(course.name) + 1) + "| ")

        print(course.grade)

    print("\nGPA: " + ("%.3f" % calculate_weighted_average(filtered_courses_list)))


def calculate_weighted_average(filtered_courses_list):
    """
    Calculates the weighted average grade for the input courses list.
    """
    total_creditpts = 0
    weighted_average = 0

    for course in filtered_courses_list:
        total_creditpts += course.creditpts

    for course in filtered_courses_list:
        weighted_average += ((course.creditpts /
                              total_creditpts) * course.grade)

    return weighted_average


class ParseError(Exception):
    def __init__(self, filename):
        msg = f"calcgpa: error: '{filename}' is not of valid format."
        super().__init__(msg)


class Course:
    def __init__(self, semester, year, cid, creditpts, name, grade):
        self.semester = semester
        self.year = year
        self.cid = cid
        self.creditpts = creditpts
        self.name = name
        self.grade = grade


def parse_datafile(datafile):
    """
    Read the datafile and create a list of courses.
    """
    lines = datafile.readlines()[1:]  # ignore first line
    datafile.close()

    course_list = []
    for i, line in enumerate(lines):
        line = line.strip()
        if not line or line[0] in ('#', '-', '_'):  # ignore lines that begin with '#', '-' or '_'
            continue
        cells = line.split('|')
        try:
            # put stripped content of each cell in corresponding variable
            full_semester, cid, creditpts, name, grade = tuple(map(lambda cell: cell.strip(), cells))
            semester = full_semester[-1]
            year = full_semester[:-1]
            if grade != '???':
                course_list.append(
                    Course(semester, int(year), cid, int(creditpts), name, int(grade)))
        except:
            print(ParseError(path.basename(datafile.name)))
            exit(1)

    return course_list


def get_args():
    """Initialize argument parser and receive filename from user.
    """
    parser = argparse.ArgumentParser(
        description='Calculates various grade statistics.')
    parser.add_argument('datafile', type=argparse.FileType('r'),
                        help='name of the file in which the data is stored')
    parser.add_argument('-y', '--year', metavar='YYYY', type=int,  #
                        help='filter by year')
    parser.add_argument('-ub', '--upper-bound', metavar='0-100', type=int,  #
                        help='filter by grade upper bound (inclusive)')
    parser.add_argument('-lb', '--lower-bound', metavar='0-100', type=int,
                        help='filter by grade lower bound (inclusive)')
    parser.add_argument('-s', '--semester', metavar='A|B|C', type=str,
                        help='filter by semester')
    return parser.parse_args()


def main():
    args = get_args()
    courses_list = parse_datafile(args.datafile)  # get courses
    filtered_courses_list = filter_courses(  # filter courses
        courses_list, args.year, args.upper_bound, args.lower_bound, args.semester)
    print_output(filtered_courses_list)  # show gpa


if __name__ == "__main__":
    main()
