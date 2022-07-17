from customtkinter import CTk, CTkButton, CTkFrame
from ice_launcher.instances import Instances
from ice_launcher.news import News
from ice_launcher.settings import Settings
from ice_launcher.about import About
from ice_launcher.accounts import Accounts


class App(CTk):
    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.title("PyMinecraftLauncher")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.navigator = CTkFrame(master=self, width=180, corner_radius=0)  # type: ignore
        self.navigator.grid(row=0, column=0, sticky="nswe")

        self.instances_button = CTkButton(
            master=self.navigator, text="Instances", command=self.open_instances
        )
        self.instances_button.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="nswe")

        self.news_button = CTkButton(
            master=self.navigator, text="News", command=self.open_news
        )
        self.news_button.grid(row=1, column=0, pady=10, padx=20)

        self.accounts_button = CTkButton(
            master=self.navigator, text="Accounts", command=self.open_accounts
        )
        self.accounts_button.grid(row=2, column=0, pady=10, padx=20)

        self.settings_button = CTkButton(
            master=self.navigator, text="Settings", command=self.open_settings
        )
        self.settings_button.grid(row=3, column=0, pady=10, padx=20)

        # empty row as spacing
        self.navigator.grid_rowconfigure(4, weight=1)

        self.about_button = CTkButton(
            master=self.navigator, text="About", command=self.open_about
        )
        self.about_button.grid(row=5, column=0, pady=(10, 20), padx=20)

        self.open_instances()

    def on_closing(self, event=0):
        self.destroy()

    def open_instances(self):
        self.main_frame = Instances(master=self)
        self.main_frame.grid(row=0, column=1, pady=20, padx=20, sticky="nswe")

    def open_news(self):
        self.main_frame = News(master=self)
        self.main_frame.grid(row=0, column=1, pady=20, padx=20, sticky="nswe")

    def open_accounts(self):
        self.main_frame = Accounts(master=self)
        self.main_frame.grid(row=0, column=1, pady=20, padx=20, sticky="nswe")

    def open_settings(self):
        self.main_frame = Settings(master=self)
        self.main_frame.grid(row=0, column=1, pady=20, padx=20, sticky="nswe")

    def open_about(self):
        self.main_frame.destroy()
        self.main_frame = About(master=self)
        self.main_frame.grid(row=0, column=1, pady=20, padx=20, sticky="nswe")


if __name__ == "__main__":
    app = App()
    app.mainloop()
