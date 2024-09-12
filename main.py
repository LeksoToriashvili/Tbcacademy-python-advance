import requests
import tkinter
from tkinter import ttk

SOURCE_URL = "https://nbg.gov.ge/gw/api/ct/monetarypolicy/currencies/en/json"

currency_data = [
            {
                "code": "EUR",
                "quantity": 1,
                "rate": 2.9792,
                "name": "Euro",
            },
            {
                "code": "USD",
                "quantity": 1,
                "rate": 2.6956,
                "name": "US Dollar",
            }
        ]


def currency_selected():
    if combobox_currency.get() == "GEL":
        label_currency["text"] = "GEL"
    else:
        for item in currency_data:
            if item["code"] == combobox_currency.get():
                label_currency["text"] = item["name"]


def converted_selected():
    if combobox_converted.get() == "GEL":
        label_converted["text"] = "GEL"
    else:
        for item in currency_data:
            if item["code"] == combobox_converted.get():
                label_converted["text"] = item["name"]


def on_convert_button_click():
    try:
        from_currency = combobox_currency.get()
        to_currency = combobox_converted.get()
        number = float(entry_currency.get())

        #convert to GEL
        if not from_currency == "GEL":
            for item in currency_data:
                if item["code"] == from_currency:
                    number = number * (item["rate"] / item["quantity"])

        #convert from GEL
        if not to_currency == "GEL":
            for item in currency_data:
                if item["code"] == to_currency:
                    number = number * (item["quantity"] / item["rate"])

        entry_converted.delete(0, 'end')
        entry_converted.insert(0, str(number))

        label["text"] = "Converted successfully"
    except Exception as e:
        label["text"] = "Something went wrong. Try again."


def on_clear_button_click():
    entry_currency.delete(0, 'end')
    entry_converted.delete(0, 'end')
    label["text"] = "Cleared!"
    label_currency["text"] = "GEL"
    label_converted["text"] = "GEL"
    currency_info()


def currency_info():
    global currency_data

    try:
        r = requests.get(SOURCE_URL)

        data = r.json()[0]
        data = data["currencies"]

        currency_data = data
        label["text"] = "Currency info updated successfully"
    except Exception as e:
        label["text"] = "Problem updating currency info"

    currency_names = ["GEL"] + [item["code"] for item in currency_data]
    combobox_currency["values"] = currency_names
    combobox_converted["values"] = currency_names
    combobox_currency.set("GEL")
    combobox_converted.set("GEL")


root = tkinter.Tk()
root.title("Currency Converter")
frame_convert = tkinter.Frame(root, bg="#123456")
frame_convert.pack()
frame_update = tkinter.Frame(root, bg="#113360")
frame_update.pack()

entry_currency = tkinter.Entry(frame_convert)
entry_currency.grid(row=0, column=0, padx=0, pady=5)
combobox_currency = ttk.Combobox(frame_convert, width=4, state="readonly")
combobox_currency.grid(row=0, column=1, pady=5)
button_convert = tkinter.Button(frame_convert, text="Convert", command=on_convert_button_click)
button_convert.grid(row=0, column=2, padx=5, pady=5)
combobox_converted = ttk.Combobox(frame_convert, width=4, state="readonly")
combobox_converted.grid(row=0, column=3, pady=5)
entry_converted = tkinter.Entry(frame_convert)
entry_converted.grid(row=0, column=4, padx=0, pady=5)
label_currency = tkinter.Label(frame_convert, text="GEL")
label_currency.grid(row=1, column=0, padx=0, pady=5)
label_converted = tkinter.Label(frame_convert, text="GEL")
label_converted.grid(row=1, column=4, padx=0, pady=5)
combobox_currency.bind('<<ComboboxSelected>>', lambda x: currency_selected())
combobox_converted.bind('<<ComboboxSelected>>', lambda x: converted_selected())

button_clear = tkinter.Button(frame_update, text="Clear", command=on_clear_button_click, width=10)
button_clear.grid(row=0, column=0, padx=5, pady=5)
label = tkinter.Label(frame_update, text="status", width=43)
label.grid(row=0, column=1, padx=5, pady=5)

currency_info()


root.mainloop()
