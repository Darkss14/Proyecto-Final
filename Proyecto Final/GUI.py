import tkinter as tk;
from tkinter import ttk;
from criptomoneda_nodo_5000 import *;


class GUI:
    def __init__(self):
        self.root = tk.Tk();
        self.root.config(width=550,height=450,bd=15);
        self.root.title("Proyecto Final");
        self.root.config();
        self.cantidadCartera = 0;

        self.createObjects();
        self.placeObjects();
        self.run();
        pass;

    def run(self):
        json_data = {'nodes':["http://127.0.0.1:5001",
                              "http://127.0.0.1:5002",
                              "http://127.0.0.1:5003"]};
        requests.post('http://127.0.0.1:5000/connect_node',json=json_data);
        self.root.mainloop();
        pass;

    def createObjects(self):
        self.frame = tk.Frame(self.root);
        self.inputVar = tk.StringVar();
        self.strCantidadCartera = "Cantidad de Dinero en Cartera: " + str(self.cantidadCartera);
        self.valor = "";
        self.inputVar.set("0");
        self.labelCantidadIngresar = tk.Label(self.frame,text="Ingrese la cantidad a operar:");

        self.labelCantidadCartera = tk.Label(self.frame, width=30,justify=tk.LEFT);
        self.labelCantidadCartera.config(text=self.strCantidadCartera,font=("Arial",14,"italic"));

        self.label_texto = tk.Label(self.frame,textvariable=self.valor,justify=tk.CENTER,font=("Calibri",11,"bold"));
        self.inputCantidad = tk.Entry(self.frame,width=55,textvariable=self.inputVar);
        self.text_blockchain = tk.Text(width=300,height=250);

        self.scrollbar = tk.Scrollbar(self.root);
        self.scrollbar.config(command=self.text_blockchain.yview);
        self.text_blockchain.config(yscrollcommand=self.scrollbar.set,font=("Courier",9,"italic"));

        self.botonComprar = tk.Button(self.frame,text="Comprar",command=self.comprar,bg='green',width=10,justify=tk.RIGHT);
        self.botonVender = tk.Button(self.frame,text="Vender", command=self.vender, bg='red', width=10,justify=tk.LEFT);

        pass;

    def placeObjects(self):
        self.frame.place(x=0,y=0,width=450,height=350);
        self.labelCantidadCartera.place(x=100,y=40);
        self.labelCantidadIngresar.place(x=100,y=120);
        self.inputCantidad.place(x=270,y=120);
        self.text_blockchain.place(x=0,y=280);
        self.label_texto.place(x=200,y=240);
        self.botonComprar.place(x=160,y=180);
        self.botonVender.place(x=300,y=180);
        pass;

    def comprar(self):
        valor = "Compra realizada con éxito";
        cantidad = int(self.inputCantidad.get());
        self.label_texto.config(text=valor);
        self.cantidadCartera += cantidad;
        self.strCantidadCartera = "Cantidad de Dinero en Cartera: "+ str(self.cantidadCartera);
        self.labelCantidadCartera.config(text=self.strCantidadCartera);
        res = requests.get('http://127.0.0.1:5000/mine_block');
        self.text_blockchain.insert("end",str(res.json())+'\n');

        jsonData = {'sender':'Carlos','receiver':'Eric','amount':cantidad};
        res = requests.post('http://127.0.0.1:5000/add_transaction',json=jsonData);
        self.text_blockchain.insert("end",str(res.json())+'\n');
        requests.get('http://127.0.0.1:5000/replace_chain');
        self.borrar();
        pass;

    def vender(self):
        cantidad = int(self.inputCantidad.get());
        if self.cantidadCartera == 0 or cantidad > self.cantidadCartera:
            valor = "No hay fondos suficientes";
            pass;
        else:
            valor = "Venta realizada con éxito";
            self.cantidadCartera -= cantidad;
            self.strCantidadCartera = "Cantidad de Dinero en Cartera: " + str(self.cantidadCartera);
            self.labelCantidadCartera.config(text=self.strCantidadCartera);
            res = requests.get('http://127.0.0.1:5000/mine_block');
            self.text_blockchain.insert("end",str(res.json())+'\n');
            jsonData = {'sender':'Eric','receiver':'Carlos','amount':cantidad};
            res = requests.post('http://127.0.0.1:5000/add_transaction',json=jsonData);
            self.text_blockchain.insert("end",str(res.json())+'\n');
            requests.get('http://127.0.0.1:5000/replace_chain');
            pass;
        self.label_texto.config(text=valor);
        self.borrar();
        pass;

    def borrar(self):
        self.inputVar.set("0");

    pass;


if __name__ == '__main__':
    gui = GUI();
    pass;
