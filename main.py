import re
import tkinter as tk

matches = []
contadorLlaves = 0

def obtenerValor(valor):
    global contadorLlaves
    global matches
    if re.match(r"#\w+",valor):
        macro:str = [x for x in matches if x.startswith(f"#macro.{valor[1:]}")]
        var0 = macro[0].split(" ")
        idx = matches.index(macro[0])
        #matches.pop(idx)
        return obtenerValor(var0[1])
    else:        
        return valor
    
def read_text(_text):
    text = _text
    old_text = ""
    
    # Obtener los valores de las claves
    ran_key = int(text[3:6])
    ran_key1 = int(text[:3])
    ran_key2 = int(text[len(text) - 3:])
    
    # Extraer la porción de texto intermedio
    text = text[6:len(text) - 3]
    next_pos = 0
    
    # Decodificar el texto
    while next_pos < len(text):
        char = text[next_pos:next_pos + 3]
        next_pos += 3
        
        # Calcular la diferencia de las claves
        key_diff = abs(ran_key2 - ran_key1) if (ran_key2 - ran_key1) > 0 else -(ran_key2 - ran_key1)
        
        # Convertir el caracter numérico en carácter de texto y agregar a old_text
        old_text += chr(int(char) - ran_key - key_diff)
    
    return old_text

def send_message():
    global matches
    global contadorLlaves
    # Obtenemos el texto del input
    input_text = input.get("1.0", tk.END)
    pattern = re.compile(r"(#macro\.[^#]*#endmacro|#define\.\w+\([^)]+\)|#\w+\([^)]+\)|#\w+)", re.DOTALL)
    matches = re.findall(pattern, input_text)

    patternMacros1 = re.compile(r"(#\w+\([^)]+\))", re.DOTALL)
    for index, match in enumerate(matches):
        if patternMacros1.search(match):
            define:str = [x for x in matches if x.startswith(f"#define.{match[1:5]}")]
            var0 = re.split(r"\(|\)",match)[1].split(",")
            var1:str = re.split(r"\(|\)",define[0])[1].replace("%1",var0[0]).replace("%2",var0[1])
            var1 = var1.replace("  "," ")
            matches[index] = var1.strip()
    
    
    patternMacros2 = re.compile(r"(#\w+[^.]+)", re.DOTALL)
    Texto:str = ""
    for index, match in enumerate(matches):
        #if patternMacros2.search(match):
        if not match.startswith("#macro") and not match.startswith("#define"):
            #print(match)
        #    macro:str = [x for x in matches if x.startswith(f"#macro.{match[1:]}")]
            #print(macro)
        #    var0 = match.split(" ")
            valor = obtenerValor(match)

            if valor in [";","{","}"]:
                if valor == "{":
                    contadorLlaves += 1
                elif valor == "}":
                    contadorLlaves -= 1
                    #if Texto[len(Texto)-1:] == " ":
                    Texto = Texto[:len(Texto)-1]
                elif valor == ";":
                    if Texto[len(Texto)-1:] == " ":
                        Texto = Texto[:len(Texto)-1]
                valor += "\n"
                for i in range(contadorLlaves):
                    valor = valor + "\t"
            elif valor in [":","::","."]:
                if Texto[len(Texto)-1:] == " ":
                    Texto = Texto[:len(Texto)-1]
            elif valor in ["("]:
                valor = valor
            elif valor in [")"]:
                if Texto[len(Texto)-1:] == " ":
                    Texto = Texto[:len(Texto)-1]
                #Texto = Texto[:len(Texto)-1]
                valor = valor + " "
            else:
                valor = valor + " "

            Texto = Texto + valor
            #if re.match(r"#\w+",var0[1]):
            #    macro:str = [x for x in matches if x.startswith(f"#macro.{var0[1][1:]}")]
            #    print(macro)


    patternMacros3 = re.compile(r"(DTCACPClient::readText \([^)]+\))", re.DOTALL)
    readText = re.findall(patternMacros3,Texto)

    for index, match in enumerate(readText):
        var0 = re.split(r"\(|\)",match.replace("'","").replace(" ",""))[1].split("+")
        numero = "".join(var0)
        nuevoTexto = read_text(numero)
        Texto = Texto.replace(match,f"'{nuevoTexto}'")

    output.delete("1.0", tk.END)
    output.insert(tk.END, Texto)


def clear_text():
    input.delete("1.0", tk.END)
    output.delete("1.0", tk.END)

window = tk.Tk()
window.title("Macro Processor")
window.geometry("1200x600")

input = tk.Text(bg='white')
output = tk.Text(bg='white')
send_button = tk.Button(text="Send", command=send_message)
clear_button = tk.Button(text="Clear", command=clear_text)

input.grid(row=0, column=0, sticky="nsew")
output.grid(row=1, column=0, sticky="nsew")

# Botón para enviar mensaje
send_button.grid(row=0, column=1, padx=10, pady=10)
clear_button.grid(row=1, column=1, padx=10, pady=10)

window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure((0,1), weight=1, uniform=1)

window.mainloop()
