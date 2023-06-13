import os
import subprocess
import tkinter as tk
import cv2
import face_recognition
from tensorflow.python.user_ops.ops.gen_user_ops import Fact

import utils
from PIL import Image,ImageTk
from test import  test
from lit import add_user
from  lit import recognize
import pickle
from username import voice_label


class App:

    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+500+500")
        # T = tk.Text(self.main_window, height=5, width=52)
        # l = tk.Label(self.main_window, text="Fact of the Day")
        # l.pack()
        # T.insert(tk.END, Fact)
        # create the label widget for "Hello clients!"
        # hello_label = tk.Label(self.main_window, text="Hello clients!", font=("Arial", 24))
        # hello_label.place(x=10, y=10)  # use place() to position the label widget
        #
        # # create the label widget for the webcam feed
        # self.webcam_label = utils.get_img_label(self.main_window)
        # self.webcam_label.place(x=10, y=50)  #
        hello_label = tk.Label(self.main_window,
                               text="Hello customer!, Welcome to Lotus Bank of India",
                               font=("Arial", 24))
        hello_label.place(x=10, y=10)  # use place() to position the label widget
        self.verify_main_window = utils.get_button(self.main_window, 'Verify', 'green', self.verify,fg='black')
        self.verify_main_window.place(x=750, y=200)

        # self.logout_button_main_window = utils.get_button(self.main_window, 'logout', 'red', self.logout)
        # self.logout_button_main_window.place(x=750, y=300)

        self.register_new_user_button_main_window = utils.get_button(self.main_window, 'Register', 'gray',
                                                                    self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=750, y=300)
        # with open('variable_value.pickle', 'rb') as f:
        #     voice_iden = pickle.load(f)
        # with open('variable_value.pickle', 'rb') as f:
        #     face_iden = pickle.load(f)
        # print(face_iden+" dds "+ voice_iden)
        # if face_iden == voice_iden and face_iden is not None and voice_iden is not None and face_iden !="no_persons_found" and voice_iden !="no_persons_found":
        #     self.continue_next = utils.get_button(self.main_window, 'Continue', 'red', self.next_page)
        #     self.continue_next.place(x=750, y=400)
        #
        # else:
        #     pass




        self.webcam_label = utils.get_img_label(self.main_window)
        self.webcam_label.place(x=40, y=100, width=700, height=400)

        self.add_webcam(self.webcam_label)

        self.db_dir='./db'
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)
    def next_page(self):
        self.nex_window = tk.Tk()
        self.nex_window.geometry("1200x520+350+100")

    def add_webcam(self,label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()

        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    def login(self):
        label = test(
            image=self.most_recent_capture_arr,
            model_dir='C:\\Users\\swaro\\PycharmProjects\\pythonProject2\\Silent-Face-Anti-Spoofing\\resources\\anti_spoof_models',
            device_id=0
        )
        #
        # if label == 1:
        #
        #     name = utils.recognize(self.most_recent_capture_arr, self.db_dir)
        #
        #     if name in ['unknown_person', 'no_persons_found']:
        #         utils.msg_box('Ups...', 'Unknown user. Please register new user or try again.')
        #     else:
        #         utils.msg_box('Welcome back !', 'Welcome, {}.'.format(name))
        #
        #
        # else:
        #     utils.msg_box('Hey, you are a spoofer!', 'You are fake !')
        # unknown_img_path = "./.tmg.jpg"
        # cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)
        # pth = "C:\\Users\\swaro\\PycharmProjects\\pythonProject2\\db"
        # output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))
        # # name=output.split(",")
        # print(output)
        # label = test(
        #     image=self.most_recent_capture_arr,
        #     model_dir='C:\\Users\\swaro\\PycharmProjects\\pythonProject2\\Silent-Face-Anti-Spoofing\\resources\\anti_spoof_models',
        #     device_id=0
        # )
        if label==1:
            unknown_img_path = "./.tmg.jpg"
            cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)
            output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))
            name = output.split(",")[1][:-4]
            print(name)
            os.remove(unknown_img_path)

            # Find all the faces in the image using the default HOG-based model.
            # This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
            # See also: find_faces_in_picture_cnn.py
            # face_locations = face_recognition.face_locations(image)

            # print("I found {} face(s) in this photograph.".format(len(face_locations)))

            # print(output)
        #     name=output.split(',')[1][:-5]
        #     print(name)
            if name in ['unknown_person','no_person_found']:
                utils.msg_box("Unknow use or person not found "," try again")
            else:
                utils.msg_box("Welcome!","Hi ,{}.".format(name))
                face_iden=name
                with open('variable_value.pickle', 'wb') as f:
                    pickle.dump(face_iden, f)
            # os.remove(unknown_img_path)
        else:
            utils.msg_box("fake yo", " you are fake")

    def verify(self):
        self.verify_new_user_window = tk.Toplevel(self.main_window)
        self.verify_new_user_window.geometry("1200x520+500+500")
        hello_label = tk.Label(self.verify_new_user_window, text="Hello customer!, Please click Face Verification after 5 seconds. Thank You", font=("Arial", 24))
        hello_label.place(x=10, y=10)  # use place() to position the label widget

        # create the label widget for the webcam feed
        self.webcam_label = utils.get_img_label(self.verify_new_user_window)
        self.webcam_label.place(x=10, y=50)  #

        self.login_button_main_window = utils.get_button(self.verify_new_user_window, 'Face Verification', 'green', self.login)
        self.login_button_main_window.place(x=450, y=100)
        self.voice_button_main_window = utils.get_button(self.verify_new_user_window, 'Voice Verification', 'green', self.recognize)
        self.voice_button_main_window.place(x=450, y=200)
        self.voice_button_main_window = utils.get_button(self.verify_new_user_window, 'Check Status ', 'green',
                                                         self.status)
        self.voice_button_main_window.place(x=450, y=300)

        # with open('variable_value.pickle', 'rb') as f:
        #     identity = pickle.load(f)
        # with open('variable_value.pickle', 'rb') as f:
        #     voice_iden = pickle.load(f)
        # with open('variable_value.pickle', 'rb') as f:
        #     face_iden = pickle.load(f)
        # voice_iden = None
        # face_iden = None



    def status(self):
        pass
    def recognize(self):
        recognize()
    def logout(self):
        pass
    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+370+120")

        self.accept_voice_register_new_user_window = utils.get_button(self.register_new_user_window, 'Voice', 'green',
                                                                       self.register_voice)
        self.accept_voice_register_new_user_window.place(x=750, y=300)

        self.accept_button_register_new_user_window = utils.get_button(self.register_new_user_window, 'Submit Face data', 'green',
                                                                      self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=200)

        self.try_again_button_register_new_user_window = utils.get_button(self.register_new_user_window, 'Try again',
                                                                         'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        self.capture_label = utils.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = utils.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=50)

        self.text_label_register_new_user = utils.get_text_label(self.register_new_user_window,
                                                                'Enter your name:')
        self.text_label_register_new_user.place(x=750, y=0)

    def register_voice(self):
        add_user()

    def add_img_to_label(self,label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()
    def accept_register_new_user(self):


        name = self.entry_text_register_new_user.get(1.0, "end-1c")
        # embeddings = face_recognition.face_encodings(self.register_new_user_capture)[0]
        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)), self.register_new_user_capture)
        # file = open(os.path.join(self.db_dir, '{}.pickle'.format(name)), 'wb')
        # pickle.dump(embeddings, file)
        with open('variable_value.pickle', 'wb') as f:
            pickle.dump(name, f)

        self.register_new_user_window.destroy()
        # embeddings = face_recognition.face_encodings(self.register_new_user_capture)[0]
        # #
        #
        # # pickle.dump(embeddings, file)
        # #
        # # Load the jpg file into a numpy array
        path="C:\\Users\\swaro\PycharmProjects\\pythonProject2\\db\\"
        image = face_recognition.load_image_file(path+'{}.jpg'.format(name))
        #
        # # Find all the faces in the image using the default HOG-based model.
        # # This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
        # # See also: find_faces_in_picture_cnn.py
        face_locations = face_recognition.face_locations(image)
        #
        print("I found {} face(s) in this photograph.".format(len(face_locations)))
        file_path="C:\\Users\\swaro\PycharmProjects\\pythonProject2\\db\\"+name+".jpg"
        if(len(face_locations)==1):
            utils.msg_box('Face Data Submitted', 'Now submit the voice data')
        else:
            os.remove(file_path)
            utils.msg_box('Failed to submit the data', 'More than 1 person detected in the photo. Please try again')
            print("File deleted successfully")
            # with open('variable_value.pickle', 'rb') as f:
            #     voice_iden = pickle.load(f)
            # with open('variable_value.pickle', 'rb') as f:
            #     face_iden = pickle.load(f)
            # voice_iden=None
            # face_iden=None

        #
        self.register_new_user_window.destroy()
    def try_again_register_new_user(self):

        self.register_new_user_window.destroy()
    def start(self):
        self.main_window.mainloop()

if __name__ == "__main__":
    app = App()
    app.start()
