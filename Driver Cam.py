import time
import argparse
import imutils
import serial
import numpy as np
from pygame import mixer
import time
import cv2
from tkinter import *
import tkinter.messagebox
root=Tk()
root.geometry('500x570')
frame = Frame(root, relief=RIDGE, borderwidth=2)
frame.pack(fill=BOTH,expand=1)
root.title('Project Ball And Plate')
frame.config(background='light blue')
label = Label(frame, text="Driver Cam",bg='light blue',font=('Times 35 bold'))
label.pack(side=TOP)
# background_label = Label(frame,image=filename)
# background_label.pack(side=TOP)

def helpin():
    help(cv2)


def Contribuidores():
    tkinter.messagebox.showinfo("Project Ball And Plate\n Ranzeus Naarson Muniz \n Lucas Cordeiro Vieira")


def sobre():
    tkinter.messagebox.showinfo("Ball And Plate")


menu = Menu(root)
root.config(menu=menu)

subm1 = Menu(menu)
menu.add_cascade(label="Tools", menu=subm1)
subm1.add_command(label="Open CV Docs", command=helpin)

subm2 = Menu(menu)
menu.add_cascade(label="About", menu=subm2)
subm2.add_command(label="Driver Cam", command=sobre)
subm2.add_command(label="Contributors", command=Contribuidores)


def exitt():
    exit()


def web():

    window = Tk()
    window.title("opção")
    while True:
        capture = cv2.VideoCapture(0)

        ret, frame = capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        botao9=Button(frame,padx=5,pady=5,width=39,bg='white',fg='black',relief=GROOVE,command=running,text='Open Cam',font=('helvetica 15 bold'))
        botao9.place(x=10,y=130)
        window.update()

    capture.release()
    cv2.destroyAllWindows()


def running():
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video",
                    help="path to the (optional) video file")
    ap.add_argument("-b", "--buffer", type=int, default=64,
                    help="max buffer size")
    args = vars(ap.parse_args())

    # Defina os limites inferior e superior das cores no espaço de cores do HSV
    lower_blue = np.array([98, 109, 20])
    upper_blue = np.array([112, 255, 255])
    # lower = {'blue': (98,109,20)}
    # 'red': (166, 84, 141), 'green': (66, 122, 129), 'yellow': (23, 59, 119), 'orange': (0, 50, 80)
    # assign new item lower['blue'] = (93, 10, 0)
    # upper = {'blue': (112,255,255)}
    # 'red': (186, 255, 255), 'green': (86, 255, 255), 'yellow': (54, 255, 255), 'orange': (20, 255, 255)

    # Define cores padrão para circular ao redor do objeto
    colors = {'blue': (255, 0, 0)}
    # 'red': (0, 0, 255), 'green': (0, 255, 0), 'yellow': (0, 255, 217), 'orange': (0, 140, 255)

    # pts = deque(maxlen=args["buffer"])

    frameRate = 30
    frameWidth = 1280
    frameHeight = 720

    # Se um caminho de vídeo não foi fornecido, pegue a referência para a webcam
    if not args.get("video", False):

        camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        # camera.open(cv2.CAP_DSHOW);
        camera.set(cv2.CAP_PROP_FPS, frameRate)
        # camera.set(cv2.CAP_PROP_FOURCC,('H',2,6,4));
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, frameWidth);
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, frameHeight);
        # camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920);
        # camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080);
        print("FPS:", camera.get(cv2.CAP_PROP_FPS))

        # cv2.nameWindow("camera", cv2.WINDOW_NORMAL)







    # Caso contrário, pegue uma referência ao arquivo de vídeoelse:
    else:
        camera = cv2.VideoCapture(args["video"])

    # loop
    while True:
        # Pegue o frame atual
        (grabbed, frame) = camera.read()

        # width = int(frame.shape[1] * 75 / 100)
        # height = int(frame.shape[0] * 75 / 100)
        # dim = (width, height)

        # se estivermos vendo um vídeo e não pegarmos um quadro, chegamos ao final do vídeo
        if args.get("video") and not grabbed:
            break

        # redimensionar o quadro, borrá-lo e convertê-lo no espaço de cores HSV
        # frame = imutils.resize(frame, width=1600)
        # cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # Verifique o objeto no quadro, cria uma máscara para a cor,
        # em seguida, execute uma série de dilatações e erosões
        # para remover quaisquer pequenas bolhas deixadas na máscara
        kernel = np.ones((9, 9), np.uint8)
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Encontrar contornos na máscara e inicializar o centro atual (x, y) da bola
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # Só continua se pelo menos um contorno for encontrado
        if len(cnts) > 0:

            # Encontre o maior contorno na máscara, então usa-o para
            # calcular o círculo fechado mínimo e o centróide
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # Só continua se o raio atingir um tamanho mínimo.
            # Corrija este valor para o tamanho do seu objeto
            if radius > 0.5:
                # Desenha o círculo e o centróide no quadro e atualiza a lista de pontos rastreados
                cv2.circle(frame, (int(x), int(y)), int(radius), colors["blue"], 2)
                print("x=", int(x), "y=", int(y), "Coordenadas = ",
                      center)  # Printa as coordenadas {, "raio=", int(radius)}
                print("FPS:", camera.get(cv2.CAP_PROP_FPS))
                cv2.putText(frame, "blue ball", (int(x - radius), int(y - radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                            colors["blue"], 2)

        # imprime o quadro na ''tela
        # cv2.imshow("Frame", frame)
        # cv2.nameWindow(frame, cv2.WINDOW_NORMAL)

        key = cv2.waitKey(1) & 0xFF
        # se a tecla 'q' for pressionada, o loop é quebrado
        if key == ord("q"):
            break

    cv2.imshow("frame", frame)
    # limpa a camera e fecha todas as janelas abertas
    camera.release()
    cv2.destroyAllWindows()

def webrec():
    capture = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    op = cv2.VideoWriter('Sample1.avi', fourcc, 11.0, (640, 480))
    while True:
        ret, frame = capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', frame)
        op.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    op.release()
    capture.release()
    cv2.destroyAllWindows()

but1=Button(frame,padx=5,pady=5,width=39,bg='white',fg='black',relief=GROOVE,command=running,text='Open Cam',font=('helvetica 15 bold'))
but1.place(x=5,y=104)

but2=Button(frame,padx=5,pady=5,width=39,bg='white',fg='black',relief=GROOVE,command=webrec,text='webrec',font=('helvetica 15 bold'))
but2.place(x=5,y=176)

but3=Button(frame,padx=5,pady=5,width=5,bg='white',fg='black',relief=GROOVE,text='EXIT',command=exitt,font=('helvetica 15 bold'))
but3.place(x=210,y=478)


root.mainloop()

