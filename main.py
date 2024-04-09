from datetime import datetime
import sys

from googleapiclient.discovery import build
from api_requests import handle_post
from spreadsheet_defs import handle
from authorize import get_creds

if len(sys.argv) < 2:
    print("Usage: python3 main.py <DATE>")
    sys.exit()

SPREADSHEET_DATE = sys.argv[1]
SPREADSHEET_DATE_ONLY = SPREADSHEET_DATE[:SPREADSHEET_DATE.find(' ')]
SPREADSHEET_NAME = SPREADSHEET_DATE + " - Lista de Presença"


def main():
    creds = get_creds()
    drive_service = build("drive", "v3", credentials=creds)
    sheets_service = build("sheets", "v4", credentials=creds)

    rows = handle(drive_service, sheets_service, SPREADSHEET_NAME)

    for row in rows:
        if row[0:1] and len(row[0:1][0]) > 0:
            teacher_name = row[0:1][0]
            teacher = None
            teacher = handle_post("teachers", {"name": teacher_name.capitalize()}, {"name": teacher_name})

        if row[2:3] and len(row[2:3][0]) > 4 and teacher is not None:
            interactive_group = None
            interactive_group_time = row[2:3][0]
            try:
                datetime.strptime(interactive_group_time, "%H:%M")
            except ValueError:
                raise Exception("Unexpected group time format.")
            
            interactive_group_date_time = SPREADSHEET_DATE_ONLY + " " + interactive_group_time
            interactive_group_name = teacher['name'] + " " + interactive_group_date_time
            interactive_group_data = {
                "name": interactive_group_name,
                "dateTime": interactive_group_date_time,
                "teacherId": teacher['id']
                }
            interactive_group = handle_post("groups", interactive_group_data, {"name": interactive_group_name})

        if row[6:7] and interactive_group is not None:
            student = None
            student_name = row[6:7][0]
            student_registration_id = row[7:8][0]
            student_data = {
                "name": student_name, 
                "registrationId": student_registration_id, 
                "interactiveGroupId": interactive_group['id']
                }
            student = handle_post("students", student_data, {"name": student_name})
                
            if row[11:12] and student is not None:
                lesson_name = row[11:12][0]
                lesson_data = {
                    "name": lesson_name, 
                    "dateTime": interactive_group_date_time, 
                    "studentId": student['id']
                    }
                handle_post("lessons", lesson_data, {"name": lesson_name})
    
if __name__ == "__main__":
    main()
    