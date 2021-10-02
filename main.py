import json
import svsvm
import urllib
from svsvm import Student


def write_student_data_to_json(new_data, file_path):
    with open(file_path, 'r+') as file:
        try:
            file_data = json.load(file)
            file_data["students"].append(new_data)
        except:
            file_data = {}
            file_data["students"] = []
            file_data["students"].append(new_data)

        file.seek(0)
        json.dump(file_data, file, indent=4)


def download_image(image_src, file_path):
    urllib.request.urlretrieve(image_src, file_path)


# To find viewstate and event_validation visit http://svsvm.vidyabhartiwup.org/
# Inspect the page by pressing F12
# Find viewstate with CTRL + F
viewstate = "/wEPDwUKMTU5ODgwODg2MGRk8WrbB0Ffr44vR94Ql9vJyxcKKeOwpA/0q2v3Bd0NPJ4="
event_validation = "/wEdAAY7l+Pk4oz8H0HfWduzhi93MesnWyCl+92OuOyCUhJ8S1VS6jraZV9gZQt5xkzzeiRYy22tG4iL1oTcMGDUNyc4Q9M+R09aX7xg3Y20MK3GJ6KeKEbp39eHc9mbdvkCgxA7swhe1jaUn96KCmogabE3B97ttVYy95V8fqQHYve00Q=="
# student_id = 6275
student_id = 9132
data_json_path = "data/data.json"
image_dir_path = "data/images"
should_increment = True
while (student_id < 10400):
    should_increment = True

    try:
        student = Student(
            userid=student_id,
            password=student_id,
            session="2020-2021",
            viewstate=viewstate,
            event_validation=event_validation
        )
        student_data = student.get_data()
        write_student_data_to_json(
            new_data=student_data, file_path=data_json_path)
        print(
            f"{student_data['profile']['name']} with {student.student_id} saved to json!"
        )
        try:
            download_image(student.student_image, file_path=f"{image_dir_path}/{student.student_id}.jpg")
            print(
                f"{student_data['profile']['name']}'s pic saved to images with name '{student.student_id}.jpg'!")
        except Exception as e:
            print(f"Image Error on {student.student_id}: {e}")
    except svsvm.exceptions.InvalidUserError as e:
        print(f"Error on {student_id}: {e}")
    except svsvm.exceptions.ValidationFailed as e:
        raise e
    except svsvm.exceptions.RequestException:
        print("Something went Wrong!")
        print("Retrying...")
        should_increment = False

    if (should_increment):
        student_id += 1
