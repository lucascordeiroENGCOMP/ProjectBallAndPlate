"""
# -*- coding: utf-8 -*- codigo UTF8 //
"""

from threading import Thread
import time
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import urllib  # for reading image from URL]
import serial
import time
import  tkinter as  tk
from tkinter import messagebox
from platform import python_version




def openCamera():
        # Construir o argumento analisar e analisar os argumentos
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

            #cv2.nameWindow("camera", cv2.WINDOW_NORMAL)







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
                    print("x=", int(x), "y=", int(y), "Coordenadas = ", center)  # Printa as coordenadas {, "raio=", int(radius)}
                    print("FPS:", camera.get(cv2.CAP_PROP_FPS))
                    cv2.putText(frame, "blue ball", (int(x - radius), int(y - radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                colors["blue"], 2)


            # imprime o quadro na ''tela
            #cv2.imshow("Frame", frame)
            #cv2.nameWindow(frame, cv2.WINDOW_NORMAL)

            key = cv2.waitKey(1) & 0xFF
            # se a tecla 'q' for pressionada, o loop é quebrado
            if key == ord("q"):
                break

        cv2.imshow("frame",frame)
        # limpa a camera e fecha todas as janelas abertas
        camera.release()
        cv2.destroyAllWindows()


def main(args):

	root = tk.Tk()
	root.title("www.cadernodelaboratorio.com.br")
	root.geometry("400x400")



	lbl1= tk.Label(root, text="Pressione o mouse e veja o que ocorre", bg="red", fg="white")
	minhaTela = tk.Frame(root)

	lbl1.pack( padx= "10", pady="10")
	minhaTela.pack( padx= "5", pady="5",expand=1, fill="both")


	minhaTela.bind('<Button-1>',mouseBotaoEsquerdoPressionado)
	minhaTela.bind('<Button-2>',mouseBotaoMeioPressionado)
	minhaTela.bind('<Button-3>',mouseBotaoDireitoPressionado)


	tk.mainloop()

	return 0

def mouseBotaoEsquerdoPressionado(event):
	msg= ('Você pressionou o botão esquerdo em %d , %d') % (event.x, event.y)
	messagebox.showinfo("Olá", msg)
        openCamera()


def mouseBotaoMeioPressionado(event):
	msg= ('Você pressionou o botão meio em %d , %d') % (event.x, event.y)
	messagebox.showinfo("Olá", msg)


def mouseBotaoDireitoPressionado(event):
	msg= ('Você pressionou o botão direito em %d , %d') % (event.x, event.y)
	messagebox.showinfo("Olá", msg)


if __name__ == '__main__':
    import sys
    print ("Versão Python: ", python_version())   #somente para verificar que estamos no ambiente virtual python 3.5
    sys.exit(main(sys.argv))