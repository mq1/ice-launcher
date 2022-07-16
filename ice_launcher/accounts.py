from typing import Any, List, TypedDict, cast
from customtkinter import CTkFrame, CTkLabel, CTkButton
from ice_launcher import __version__
from threading import Thread
import webbrowser
from os import path
from http.server import BaseHTTPRequestHandler, HTTPServer
from minecraft_launcher_lib import microsoft_account as msa
from minecraft_launcher_lib.microsoft_types import CompleteLoginResponse
import tomli
import tomli_w


__client_id__ = '0018ddff-bd2f-4cc6-b220-66f6a4462a5c'
__redirect_uri__ = 'http://localhost:3003'


class Document(TypedDict):
    version: int
    accounts: List[CompleteLoginResponse]


def new_document():
    doc: Document = {"version": 1, "accounts": []}

    with open("accounts.toml", "wb") as f:
        tomli_w.dump(cast(dict[str, Any], doc), f)
    
    return doc


def read_document():
    if not path.exists("accounts.toml"):
        doc = new_document()

    with open("accounts.toml", "rb") as f:
        doc: Document = cast(Document, tomli.load(f))
    
    return doc


def write_document(doc: Document):
    with open("accounts.toml", "wb") as f:
        tomli_w.dump(cast(dict[str, Any], doc), f)


class CallbackHandler(BaseHTTPRequestHandler):
    code_verifier: str

    def do_GET(self):
        auth_code = msa.get_auth_code_from_url(self.path)
        assert(auth_code is not None)
        login_data = msa.complete_login(__client_id__, __redirect_uri__, auth_code, self.code_verifier)

        doc = read_document()
        doc["accounts"].append(login_data)
        write_document(doc)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><head><title>Login</title></head>")
        self.wfile.write(b"<body><p>You have been logged in.</p>")
        self.wfile.write(b"<p>You can close this window.</p>")
        self.wfile.write(b"</body></html>")

        killer = Thread(target=self.server.shutdown)
        killer.daemon = True
        killer.start()


class Accounts(CTkFrame):
    doc: Document

    def __init__(self, master):
        super().__init__(master=master)

        self.doc = read_document()

        self.heading = CTkLabel(
            master=self,
            height=100,
            fg_color=("white", "gray38"),  # <- custom tuple-color
            text_font=("Roboto Medium", -20),  # font name and size in px
            text="Accounts",
        )
        self.heading.pack(pady=20, padx=20, fill="x")

        self.accounts_list = CTkFrame(master=self)
        self.accounts_list.pack(pady=10, padx=20, fill="x")

        self.add_account_button = CTkButton(
            master=self,
            text="Add Account",
            command=self.add_account,
        )
        self.add_account_button.pack(pady=10, padx=20, fill="x")

        self.update_accounts_list()

    def add_account(self):
        state = msa.generate_state()
        code_verifier, code_challenge, code_challenge_method = msa.generate_pkce()
        login_url = msa.get_login_url(__client_id__, __redirect_uri__, state, code_challenge, code_challenge_method)

        webbrowser.open(login_url)
        handler = CallbackHandler
        handler.code_verifier = code_verifier
        httpd = HTTPServer(("127.0.0.1", 3003), handler)
        httpd.serve_forever()

    def update_accounts_list(self):
        self.accounts_list.destroy()
        self.accounts_list = CTkFrame(master=self)
        self.accounts_list.pack(pady=10, padx=20, fill="x")

        for account in self.doc["accounts"]:
            account_label = CTkLabel(master=self.accounts_list, text=account["name"])
            account_label.pack(pady=10, padx=20, fill="x")
