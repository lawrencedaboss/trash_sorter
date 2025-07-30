import tkinter as tk
from tkinter import messagebox
import ast, operator as op
import random

# safe eval support
ALLOWED_OPS = {
    ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
    ast.Div: op.truediv, ast.Pow: op.pow, ast.Mod: op.mod,
    ast.FloorDiv: op.floordiv, ast.USub: op.neg
}

def safe_eval(expr):
    def _eval(node):
        if isinstance(node, ast.Num):
            return node.n
        if isinstance(node, ast.BinOp):
            return ALLOWED_OPS[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp):
            return ALLOWED_OPS[type(node.op)](_eval(node.operand))
        raise ValueError("Unsupported expression.")
    tree = ast.parse(expr, mode='eval').body
    return _eval(tree)

class ChatCalc(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("👋 Chat Calculator")
        self.geometry("450x450")
        self.resizable(False, False)

        self.history = []
        self.user_name = None
        self._build_ui()
        self._post("Calc", "Hi! I’m Bob the builder 🤖 What’s your name?")

    def _build_ui(self):
        self.chat = tk.Text(self, state="disabled", wrap="word", padx=10, pady=10)
        self.chat.pack(fill="both", expand=True)

        # color tags
        self.chat.tag_config("You", foreground="blue")
        self.chat.tag_config("Calc", foreground="dark green", font=("Helvetica", 10, "italic"))
        self.chat.tag_config("Typing", foreground="gray")

        frame = tk.Frame(self)
        frame.pack(fill="x", pady=5)
        self.entry = tk.Entry(frame)
        self.entry.pack(side="left", fill="x", expand=True, padx=5)
        self.entry.bind("<Return>", self._on_enter)
        tk.Button(frame, text="Send", command=self._on_enter).pack(side="right", padx=5)

    def _post(self, speaker, msg, tag=None):
        self.chat.configure(state="normal")
        tag = tag or speaker
        self.chat.insert("end", f"{speaker}: {msg}\n\n", tag)
        self.chat.configure(state="disabled")
        self.chat.see("end")

    def _typing_indicator(self):
        self._post("Calc", "typing...", tag="Typing")
        self.chat.after(500, lambda: self._clear_typing())

    def _clear_typing(self):
        self.chat.configure(state="normal")
        self.chat.delete("end-3l", "end")  # remove last "typing..."
        self.chat.configure(state="disabled")

    def _on_enter(self, event=None):
        msg = self.entry.get().strip()
        if not msg:
            return
        self.entry.delete(0, tk.END)

        self._post("You", msg)
        # if first message: capture name
        if self.user_name is None:
            self.user_name = msg.split()[0].capitalize()
            self._typing_indicator()
            self.after(600, lambda: self._post("Calc",
                f"Nice to meet you, {self.user_name}! Type any math expression or `/help` to get started."))
            return

        # handle commands / chatter or calculation
        lower = msg.lower()
        if msg.startswith("/"):
            self._typing_indicator()
            self.after(300, lambda: self._handle_command(msg))
        elif any(g in lower for g in ("hi", "hello", "hey")):
            self._typing_indicator()
            self.after(300, lambda: self._post("Calc",
                f"Hey {self.user_name}! Ready to crunch some numbers? 😃"))
        elif any(t in lower for t in ("thank", "thx")):
            self._typing_indicator()
            self.after(300, lambda: self._post("Calc",
                "You’re welcome! Anything else I can calculate?"))
        else:
            self._typing_indicator()
            self.after(400, lambda: self._compute(msg))

    def _handle_command(self, cmd):
        if cmd == "/help":
            text = (
                "Enter any math expression (e.g. 2*(3+4)).\n"
                "Commands:\n"
                "  /history – show past calculations\n"
                "  /clear   – clear the chat window\n"
                "  /help    – this message"
            )
            self._post("Calc", text)

        elif cmd == "/history":
            if not self.history:
                self._post("Calc", "No history yet. Try calculating something!")
            else:
                hist = "\n".join(self.history[-10:])
                self._post("Calc", f"Here are your last {len(self.history[-10:])} results:\n{hist}")

        elif cmd == "/clear":
            self.chat.configure(state="normal")
            self.chat.delete("1.0", "end")
            self.chat.configure(state="disabled")
            self._post("Calc", f"Chat cleared. What shall we calculate next, {self.user_name}?")

        else:
            self._post("Calc", f"Unknown command: `{cmd}`. Type `/help` to see commands.")

    def _compute(self, expr):
        try:
            result = safe_eval(expr)
            reply = f"{expr} = {result}"
            self.history.append(reply)
            self._post("Calc", reply + " 👍")
        except ZeroDivisionError:
            self._post("Calc", "Oops! Division by zero isn’t allowed.")
        except Exception:
            self._post("Calc", "I couldn’t parse that. Try a simple arithmetic expression or `/help`.")

if __name__ == "__main__":
    ChatCalc().mainloop()
