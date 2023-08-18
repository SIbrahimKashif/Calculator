import PySimpleGUI as sg

# constants
font_name = "Segoe UI Light"
button_font = (font_name, 15)
orange = "#ff9500"
grey = "#727475"
dark_grey = "#555556"


# format the number to add a ',' after every 3 digits
def format_num(num_string):
    if len(num_string) > 0:
        formatted_num = (
            "{:,}".format(float(num_string))
            if "." in num_string
            else "{:,}".format(int(num_string))
        )
        return formatted_num


# format the ans to add a ',' after every 3 digits and round it to fit on screen
def format_ans(ans, str_ans, length):
    formatted_ans = (
        "{:,}".format(round(ans, 17 - length))
        if length < 17 and len(str_ans) >= 17
        else "{:.2e}".format(ans)
        if len(str_ans) >= 17
        else "{:,}".format(ans)
    )
    return formatted_ans


# make an option to change theme by right clicking on the text box
def create_win(theme):
    sg.theme(theme)
    sg.set_options(font=(font_name, 15))
    button_size = (6, 3)

    # create the layout
    layout = [
        [
            sg.Text(
                "Calculater",
                font=(font_name, 25),
                justification="center",
                expand_x=True,
                pad=(10, 20),
                right_click_menu=theme_menu,
                key="text",
            )
        ],
        [
            sg.Button(
                "Calculate",
                key="Enter",
                expand_x=True,
                button_color=(None, dark_grey),
            ),
            sg.Button("Clear", size=(6, None), button_color=(None, dark_grey)),
            sg.Button("Del", size=(6, None)),
        ],
        [
            sg.Button(7, size=button_size, button_color=(None, grey)),
            sg.Button(8, size=button_size, button_color=(None, grey)),
            sg.Button(9, size=button_size, button_color=(None, grey)),
            sg.Button("x", key="*", size=button_size, button_color=(None, orange)),
        ],
        [
            sg.Button(4, size=button_size, button_color=(None, grey)),
            sg.Button(5, size=button_size, button_color=(None, grey)),
            sg.Button(6, size=button_size, button_color=(None, grey)),
            sg.Button("÷", key="/", size=button_size, button_color=(None, orange)),
        ],
        [
            sg.Button(1, size=button_size, button_color=(None, grey)),
            sg.Button(2, size=button_size, button_color=(None, grey)),
            sg.Button(3, size=button_size, button_color=(None, grey)),
            sg.Button("+", key="+", size=button_size, button_color=(None, orange)),
        ],
        [
            sg.Button(0, size=button_size, button_color=(None, grey)),
            sg.Button("000", size=button_size, button_color=(None, grey)),
            sg.Button(".", size=button_size, button_color=(None, grey)),
            sg.Button("-", key="-", size=button_size, button_color=(None, orange)),
        ],
    ]
    return sg.Window("Calculator", layout)


theme_menu = ["menu", ["LightGrey1", "dark", "Darkgray8", "random"]]

# create window with default theme
window = create_win("DarkGray8")

# create lists
current_num = []
operations = []
saved_ans = []

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    # create new window with new theme
    elif event in theme_menu[1]:
        window.close()
        window = create_win(event)

    # add the typed numbers to a string and display the formatted number
    elif event in ["0", "000", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]:
        current_num.append(event)
        num_string = "".join(current_num)

        formatted_num = format_num(num_string)
        # if number is too big to display on screen only show the first 17 digits
        formatted_num = (
            formatted_num[:16] if len(formatted_num) >= 17 else formatted_num
        )

        window["text"].update(formatted_num)

    # add the operators and num string to operations list
    elif event in ["*", "/", "-", "+"]:
        try:
            # use the saved ans instead of the numstring if it doesnt exists
            value = (
                saved_ans
                if len(current_num) == 0
                else current_num
                if len(saved_ans) == 0
                else None
            )

            if value:
                operations.append("".join(value))

            # empty the lists
            current_num = []
            saved_ans = []
            operations.append(event)

            # display the operators on screen
            symbol = "x" if event == "*" else "÷" if event == "/" else event
            window["text"].update(symbol)

        # handle errors
        except NameError:
            current_num = []
            operations = []
            window["text"].update("Error")

    # convert the operations list to an equaion and solve it
    elif event == "Enter":
        try:
            operations.append("".join(current_num))
            ans = eval(" ".join(operations))

            # shorten and format ans so it fits on screen
            length = len(str(ans).split(".")[0])
            str_ans = str(ans)

            if str_ans.endswith(".0"):
                ans = int(str_ans[: len(str_ans) - 2])

            formatted_ans = format_ans(ans, str_ans, length)

            # add the ans to saved ans and empty lists
            saved_ans = [str_ans]
            operations = []
            current_num = []

            # display formatted ans
            window["text"].update(formatted_ans)

        # handle errors
        except SyntaxError:
            current_num = []
            operations = []
            window["text"].update("Error: Invalid Syntax")

    # clear the lists and the text box
    elif event == "Clear":
        current_num = []
        operations = []
        saved_ans = []
        window["text"].update("")

    # delete the last typed value
    elif event == "Del":
        try:
            if len(current_num) != 0:
                current_num.pop()
                window["text"].update(format_num("".join(current_num)))
            elif len(operations) != 0:
                operations.pop()
                window["text"].update(format_num("".join(operations)))
            elif len(saved_ans) != 0:
                saved_ans = [s[:-1] for s in saved_ans]
                window["text"].update(format_num("".join(saved_ans)))
            else:
                window["text"].update("")

        # handle errors
        except ValueError:
            window["text"].update("Error")

window.close()
