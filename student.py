import csv
from abc import ABC, abstractmethod

class Student(ABC):

    def __init__(self, Student_ID, FName, LName,Programme, Math, Eng, Science):
        self.__Student_ID = Student_ID
        self.__FName = FName
        self.__LName = LName
        self.__Programme = Programme
        self.__Math = self.Validate_Mark(Math)
        self.__Eng = self.Validate_Mark(Eng)
        self.__Sci = self.Validate_Mark(Science)

    @staticmethod
    def Validate_Mark(mark):
        if isinstance(mark, bool) or not isinstance(mark, (int, float)):
            raise ValueError("Marks must be numeric.")

        if not 0 <= mark <= 100:
            raise ValueError("Marks must be between 0 and 100.")

        return float(mark)

    def Get_ID(self):
        return self.__Student_ID

    def Get_FName(self):
        return self.__FName

    def Get_LName(self):
        return self.__LName

    def Get_Programme(self):
        return self.__Programme

    def Get_Marks(self):
        return {
            "Mathematics": self.__Math,
            "English": self.__Eng,
            "Science": self.__Sci
        }

    # Encapsulation
    def Add_Update(self):
        Student_ID = input("Enter Student ADM: ").strip()
        FName = input("Enter first name: ").strip()
        LName = input("Enter last name: ").strip()
        Programme = input("Enter programme: ").strip()

        if not all([Student_ID, FName, LName, Programme]):
            raise ValueError("Student details cannot be empty.")

        # Validate all new marks before updating
        Math = self.Validate_Mark(float(input("Mathematics marks: ")))
        Eng = self.Validate_Mark(float(input("English marks: ")))
        Sci = self.Validate_Mark(float(input("Science marks: ")))

        self.__Student_ID = Student_ID
        self.__FName = FName
        self.__LName = LName
        self.__Programme = Programme
        self.__Math = Math
        self.__Eng = Eng
        self.__Sci = Sci

    # Update marks separately
    def Update_Marks(self, Math, Eng, Science):
        self.__Math = self.Validate_Mark(Math)
        self.__Eng = self.Validate_Mark(Eng)
        self.__Sci = self.Validate_Mark(Science)

    # Calculate average
    def Average_Calc(self):
        marks = [self.__Math, self.__Eng, self.__Sci]
        return sum(marks) / len(marks)

    # Calculate grade
    def Grade_Calc(self):
        average = self.Average_Calc()

        if average < 0 or average > 100:
            return "Invalid"
        elif average < 40:
            return "F"
        elif average < 50:
            return "D"
        elif average < 60:
            return "C"
        elif average < 70:
            return "B"
        else:
            return "A"
        
    @staticmethod
    def Average_Flexible(*marks):
        # Allow a list or tuple of marks
        if len(marks) == 1 and isinstance(marks[0], (list, tuple)):
            marks = tuple(marks[0])

        if not marks:
            raise ValueError("Enter at least one mark.")

        validated = [
            Student.Validate_Mark(mark) for mark in marks
        ]

        return sum(validated) / len(validated)

    # TASK 2: Abstract method
    @abstractmethod
    def Student_Type(self):
        """Return a descriptive type name for concrete student classes."""
        return "Student"
    
    def display_performance(self):
        return (
            f"{self.Student_Type()}: {self.Get_FName()} "
            f"{self.Get_LName()} | "
            f"Average: {self.Average_Calc():.2f} | "
            f"Grade: {self.Grade_Calc()}"
        )

    # Base report
    def Report(self):
        marks = self.Get_Marks()

        return (
            "\n======== STUDENT RESULTS AND INFO ========\n"
            f"ADM: {self.Get_ID()}\n"
            f"Name: {self.Get_FName()} {self.Get_LName()}\n"
            f"Programme: {self.Get_Programme()}\n"
            f"Student Type: {self.Student_Type()}\n"
            f"Math: {marks['Mathematics']:.2f}\n"
            f"Eng: {marks['English']:.2f}\n"
            f"Sci: {marks['Science']:.2f}\n"
            f"Average: {self.Average_Calc():.2f}\n"
            f"Grade: {self.Grade_Calc()}\n"
        )

class AIU(Student):

    def __init__(self, Student_ID, FName, LName, Programme,Math, Eng, Science, Year):
        super().__init__(Student_ID, FName, LName, Programme,Math, Eng, Science)
        self.Year = Year

    def Student_Type(self):
        return "AIU Student"
    # Override Report to add the academic year
    def Report(self):
        return super().Report() + f"Academic Year: {self.Year}\n"

class ScholarshipStudent(AIU):

    def __init__(self, Student_ID, FName, LName, Programme,Math, Eng, Science, Year, scholarship_amount):
        super().__init__(Student_ID, FName, LName, Programme,Math, Eng, Science, Year)

        if (
            isinstance(scholarship_amount, bool)
            or not isinstance(scholarship_amount, (int, float))
            or scholarship_amount < 0
        ):
            raise ValueError("Scholarship amount must be non-negative.")

        self.__scholarship_amount = scholarship_amount

    def Get_Scholarship_Amount(self):
        return self.__scholarship_amount

    def is_eligible(self):
        return self.Average_Calc() >= 85

    # Override the parent method
    def Student_Type(self):
        return "Scholarship Student"

    # Override Report with scholarship-specific information
    def Report(self):
        report = super().Report()

        eligibility = "Yes" if self.is_eligible() else "No"

        return (
            report
            + f"Scholarship Amount: KSh "
              f"{self.Get_Scholarship_Amount():,.2f}\n"
            + f"Scholarship Eligible: {eligibility}\n"
        )
    def display_performance(self):
        status = "Eligible" if self.is_eligible() else "Not eligible"

        return (
            f"{super().display_performance()} | "
            f"Scholarship Eligibility: {status}"
        )

class Perf_Analyzer:

    def __init__(self, students):
        self.students = list(students)

    def highest_average(self):
        if not self.students:
            return None

        return max(self.students, key=lambda s: s.Average_Calc())

    def lowest_average(self):
        if not self.students:
            return None

        return min(self.students, key=lambda s: s.Average_Calc())

    def class_average(self):
        if not self.students:
            return 0.0

        return sum(
            student.Average_Calc() for student in self.students
        ) / len(self.students)

class StudentReports:

    def __init__(self, analyzer):
        self.analyzer = analyzer

    def generate_report(self, student):
        print(student.Report())

    def generate_class_summary(self):
        highest = self.analyzer.highest_average()
        lowest = self.analyzer.lowest_average()

        print("\n======== CLASS PERFORMANCE SUMMARY ========")

        if highest is None:
            print("No students available.")
            return

        print(
            f"Highest Average: {highest.Get_FName()} "
            f"{highest.Get_LName()} - "
            f"{highest.Average_Calc():.2f}"
        )

        print(
            f"Lowest Average: {lowest.Get_FName()} "
            f"{lowest.Get_LName()} - "
            f"{lowest.Average_Calc():.2f}"
        )

        print(
            f"Overall Class Average: "
            f"{self.analyzer.class_average():.2f}"
        )

def load_students(filename):
    students = []

    with open(filename, mode="r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file, skipinitialspace=True)

        if reader.fieldnames:
            reader.fieldnames = [
                heading.strip() for heading in reader.fieldnames
            ]

        required_columns = {
            "StudentID", "FName", "LName", "Programme",
            "Math", "English", "Science"
        }

        if not reader.fieldnames or not required_columns.issubset(
            reader.fieldnames
        ):
            print("CSV headings found:", reader.fieldnames)
            raise ValueError("The CSV file has missing column headings.")

        for row_number, row in enumerate(reader, start=2):
            try:
                student_id = row["StudentID"].strip()
                fname = row["FName"].strip()
                lname = row["LName"].strip()
                programme = row["Programme"].strip()

                if not all([student_id, fname, lname, programme]):
                    raise ValueError("Student details cannot be empty.")

                math = Student.Validate_Mark(float(row["Math"]))
                english = Student.Validate_Mark(float(row["English"]))
                science = Student.Validate_Mark(float(row["Science"]))

                average = (math + english + science) / 3

                # The CSV does not contain a Year column.
                year = "Not specified"

                if average >= 85:
                    student = ScholarshipStudent(
                        student_id, fname, lname, programme,
                        math, english, science, year,
                        scholarship_amount=50000
                    )
                else:
                    student = AIU(
                        student_id, fname, lname, programme,
                        math, english, science, year
                    )

                students.append(student)

            except (ValueError, TypeError, KeyError) as error:
                raise ValueError(
                    f"Invalid data on CSV row {row_number}: {error}"
                ) from error

    return students

def main():

    try:
        students = load_students("student.csv")

        if not students:
            print("The CSV file contains no student records.")
            return

        # TASK 5: Demonstrate polymorphism
        print("\n========== POLYMORPHISM DEMONSTRATION ==========")

        for student in students:
            print(student.display_performance())

        # TASK 3: Analyze student performance
        analyzer = Perf_Analyzer(students)

        # TASK 7: Generate individual reports and summary
        reports = StudentReports(analyzer)

        print("\n========== INDIVIDUAL STUDENT REPORTS ==========")

        for student in students:
            reports.generate_report(student)

        reports.generate_class_summary()

        # TASK 6: Demonstrate flexible arguments
        print("\n========== FLEXIBLE AVERAGE DEMONSTRATION ==========")

        print("Three separate marks:", Student.Average_Flexible(75, 80, 70))
        print("List of marks:", Student.Average_Flexible([75, 80, 70]))
        print("Five separate marks:", Student.Average_Flexible(70, 75, 80, 85, 90))

    except (OSError, ValueError) as error:
        print(f"Error: {error}")

if __name__ == "__main__":
    main()
