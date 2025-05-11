import tkinter as tk
from tkinter import messagebox


class SistemaExpertoElectronicaGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema Experto - Diagnóstico de Fallas Electrónicas")
        self.master.geometry("700x600")
        self.master.configure(bg="#f0f0f0")

        self.variables = {
            'A': 'Dispositivo no enciende',
            'B': 'Sin energía de entrada',
            'C': 'LED no enciende',
            'D': 'Fusible dañado',
            'E': 'Olor a quemado',
            'F': 'Componente visualmente dañado',
            'G': 'Zumbido',
            'H': 'Voltaje incorrecto',
            'I': 'Capacitor reventado',
            'J': 'Sin continuidad en fuente',
            'K': 'Corto en componente',
            'L': 'Sin caída de voltaje',
            'M': 'Circuito no funciona',
            'N': 'Resistencia fuera de valor',
            'O': 'Afecta el circuito',
            'P': 'Transistor en corto',
            'Q': 'Voltaje de regulación bajo'
        }

        self.reglas = [
            {'nombre': 'R1', 'condiciones': ['A', 'B'], 'conclusion': 'Revisar el cable de alimentación, enchufe o fuente externa'},
            {'nombre': 'R2', 'condiciones': ['A', '!B', 'C'], 'conclusion': 'Posible falla en fuente interna o placa principal'},
            {'nombre': 'R3', 'condiciones': ['D', 'C'], 'conclusion': 'Reemplazar fusible y verificar continuidad'},
            {'nombre': 'R4', 'condiciones': ['D', 'E|F'], 'conclusion': 'Hay un corto circuito interno'},
            {'nombre': 'R5', 'condiciones': ['G', 'H'], 'conclusion': 'Falla en la fuente conmutada (switching)'},
            {'nombre': 'R6', 'condiciones': ['I'], 'conclusion': 'Sustituir capacitores y verificar el circuito de regulación de voltaje'},
            {'nombre': 'R7', 'condiciones': ['J'], 'conclusion': 'Verificar pistas, soldaduras frías y conexiones internas'},
            {'nombre': 'R8', 'condiciones': ['K'], 'conclusion': 'No energizar el equipo hasta reemplazar el componente afectado'},
            {'nombre': 'R9', 'condiciones': ['L', 'M'], 'conclusion': 'Componente abierto o dañado internamente'},
            {'nombre': 'R10', 'condiciones': ['N', 'O'], 'conclusion': 'Resistencia fuera de tolerancia, debe ser reemplazada'},
            {'nombre': 'R11', 'condiciones': ['P'], 'conclusion': 'Transistor en corto, debe reemplazarse'},
            {'nombre': 'R12', 'condiciones': ['Q'], 'conclusion': 'Verificar diodo zener, transistor regulador y capacitores de filtro'}
        ]

        self.check_vars = {}
        self.crear_interfaz()

    def crear_interfaz(self):
        tk.Label(self.master, text="Seleccione los síntomas observados:", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)

        frame_sintomas = tk.Frame(self.master, bg="#f0f0f0")
        frame_sintomas.pack(pady=10)

        for codigo, descripcion in sorted(self.variables.items()):
            var = tk.BooleanVar()
            cb = tk.Checkbutton(frame_sintomas, text=f"{codigo}: {descripcion}", variable=var, anchor="w", bg="#f0f0f0")
            cb.pack(fill='x', anchor='w')
            self.check_vars[codigo] = var

        tk.Button(self.master, text="Diagnosticar", command=self.diagnosticar, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=20)
        self.texto_resultado = tk.Text(self.master, height=15, wrap="word", bg="white", font=("Arial", 11))
        self.texto_resultado.pack(fill='both', padx=10, pady=5, expand=True)

        tk.Button(self.master, text="Limpiar selección", command=self.limpiar, bg="#f44336", fg="white", font=("Arial", 10)).pack(pady=5)

    def diagnosticar(self):
        hechos = {codigo: var.get() for codigo, var in self.check_vars.items()}
        diagnosticos = []

        for regla in self.reglas:
            condiciones_cumplidas = True

            for cond in regla['condiciones']:
                if cond.startswith('!'):
                    var = cond[1:]
                    if hechos.get(var, False):
                        condiciones_cumplidas = False
                        break
                elif '|' in cond:
                    opciones = cond.split('|')
                    if not any(hechos.get(op, False) for op in opciones):
                        condiciones_cumplidas = False
                        break
                else:
                    if not hechos.get(cond, False):
                        condiciones_cumplidas = False
                        break

            if condiciones_cumplidas:
                diagnosticos.append({
                    'regla': regla['nombre'],
                    'conclusion': regla['conclusion'],
                    'variables': regla['condiciones']
                })

        self.mostrar_diagnosticos(diagnosticos)

    def mostrar_diagnosticos(self, diagnosticos):
        self.texto_resultado.delete(1.0, tk.END)

        if not diagnosticos:
            self.texto_resultado.insert(tk.END, "⚠ No se encontró un diagnóstico con los síntomas seleccionados.\n")
            self.texto_resultado.insert(tk.END, "Verifique que los síntomas estén correctamente marcados.")
        else:
            for i, diag in enumerate(diagnosticos, 1):
                self.texto_resultado.insert(tk.END, f"Diagnóstico {i}:\n")
                self.texto_resultado.insert(tk.END, f"  Regla aplicada: {diag['regla']}\n")
                self.texto_resultado.insert(tk.END, f"  Condiciones cumplidas: {', '.join(diag['variables'])}\n")
                self.texto_resultado.insert(tk.END, f"  Conclusión: {diag['conclusion']}\n\n")

    def limpiar(self):
        for var in self.check_vars.values():
            var.set(False)
        self.texto_resultado.delete(1.0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaExpertoElectronicaGUI(root)
    root.mainloop()
