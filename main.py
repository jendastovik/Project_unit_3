from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.datatables import MDDataTable
from my_lib import DatabaseWorker
from my_lib import make_hash
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivy.graphics import Rectangle
from kivymd.uix.menu import MDDropdownMenu
from zip_image import get_image

class TableScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_tables= None
        self.selected_rows = []
        self.new_sender_id = None
        self.new_receiver_id = None
    
    def on_pre_enter(self, *args):
        column_names= [("id", 40), ("Sender", 30), ("Receiver", 30), ("Amount", 40), ("Signature", 100), ("Employee", 30)]
        self.data_tables = MDDataTable(
            size_hint=(0.9, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            use_pagination=True,
            check=True,
            column_data=column_names
        )
        self.data_tables.bind(on_row_press=self.row_pressed)
        self.data_tables.bind(on_check_press=self.checkbox_pressed)
        self.add_widget(self.data_tables)
        self.update()

    def update(self):
        data = main.x.search("""SELECT * FROM transactions""", multiple=True)
        self.data_tables.update_row_data(None, data)
    
    def row_pressed(self, instance_table, instance_row):
        print(f"value clicked {instance_row}")
    
    def checkbox_pressed(self, instance_table, current_row):
        print(f"record checked {current_row}")
        if current_row in self.selected_rows:
            self.selected_rows.remove(current_row)
        else:
            self.selected_rows.append(current_row)
        

    def save(self):
        sender = self.ids.sender_id.text
        receiver = self.ids.receiver_id.text
        amount = self.ids.amount.text
        signature = f"sender_id {sender}, receiver_id {receiver}, amount {amount}"
        print(sender, receiver, amount)
        save_query = f"""INSERT INTO transactions (sender_id, receiver_id, amount, signature, employee_id) VALUES ({sender}, {receiver}, {amount}, '{make_hash(signature)}', {main.employee})"""
        main.x.insert(save_query)
        self.update()

    def summary(self):
        income = main.x.search("SELECT SUM(amount) FROM transactions WHERE receiver_id=1")[0]
        outcome = main.x.search("SELECT SUM(amount) FROM transactions WHERE sender_id=1")[0]
        if outcome == None: outcome = 0
        if income == None: income = 0
        self.dialog = MDDialog(
                text=f"balance: {income - outcome}\nIncome: {income}\nOutcome: {outcome}",
                size_hint=(0.7, 0.3),
            )
        self.dialog.open()

    def delete_selected(self):
        print(self.selected_rows)
        for row in self.selected_rows:
            main.x.run_query(f"DELETE FROM transactions WHERE id={row[0]}")
        self.update()

    def delete_all(self):
        main.x.run_query("DELETE FROM transactions")
        self.update()

    def open_menu(self, drop_item_element):
        users = main.x.search("SELECT first_name, last_name FROM parties", multiple=True)
        self.menu_items = [f"{user[0]} {user[1]}" for user in users]
        buttons_menu =[]
        for item in self.menu_items:
            buttons_menu.append(
                {"text": item, 
                 "on_release": lambda x = item: self.button_pressed(x, drop_item_element),
                 "viewclass": "OneLineListItem",
                 }
            )
        self.menu = MDDropdownMenu(caller=drop_item_element, items=buttons_menu, width_mult=2)
        self.menu.open()
    
    def button_pressed(self, x, drop_item_element):
        first, last = x.split(" ")
        user_id = main.x.search(f"SELECT id FROM parties WHERE first_name = '{first}' AND last_name = '{last}'")
        drop_item_element.text = str(user_id[0])
        self.menu.dismiss()

class LoginScreen(MDScreen):
    dialog=None

    def try_login(self):
        uname = self.ids.uname.text
        passwd = self.ids.passwd.text
        print(self.ids.uname.text)

        user = main.x.search(f"SELECT * FROM employees WHERE username='{uname}' AND password='{passwd}'")

        if user:
            print(f"Last login is: {user[4]}")
            self.manager.get_screen("HomeScreen").ids.log.text = f"Last login is: {user[4]}"
            self.parent.current = "HomeScreen"
            main.employee = user[0]
            self.dialog = MDDialog(
                text="Login successful",
                size_hint=(0.7, 0.3),
            )
            self.dialog.open()
        else:
            self.dialog = MDDialog(
                text="Invalid username or password",
                size_hint=(0.7, 0.3),
            )
            self.dialog.open()


    def register_btn(self):
        self.parent.current = "RegistrationScreen"

class RegistrationScreen(MDScreen):
    dialog = None
    def login_btn(self):
        self.parent.current = "LoginScreen"
    def try_register(self):
        email = self.ids.email.text
        pass1 = self.ids.pass1.text
        pass2 = self.ids.pass2.text
        uname = self.ids.uname.text
        code = self.ids.code.text
        
        if len(pass1)<8:
            self.ids.pass1.error=True
            self.ids.pass1.helper_text="Password must be at least 8 characters"
        elif pass1!=pass2:
            self.ids.pass2.error = True
            self.ids.pass2.helper_text="Password does not match. Try again."
        elif email.count("@")==0 or email.count(".")==0:
            self.ids.email.error = True
            self.ids.email.helper_text="Invalid email"
        elif main.x.search(f"SELECT * FROM employees WHERE email='{email}'"):
            self.ids.email.error = True
            self.ids.email.helper_text="Email already exists"
        elif main.x.search(f"SELECT * FROM employees WHERE username='{uname}'"):
            self.ids.uname.error = True
            self.ids.uname.helper_text="Username already exists"
        elif len(uname)<4:
            self.ids.uname.error = True
            self.ids.uname.helper_text="Username must be at least 4 characters"
        elif code != "1234":
            self.ids.code.error = True
            self.ids.code.helper_text="Invalid code"
        else:
            self.dialog = MDDialog(
                text="Registration successful",
                size_hint=(0.7, 0.3),
            )
            self.dialog.open()
            main.x.insert(f"""INSERT INTO employees (email, password, username) VALUES ('{email}', '{pass1}', '{uname}')""")
            self.parent.current = "LoginScreen"
            

class AddCustomerScreen(MDScreen):
    def create_customer(self):
        first_name = self.ids.name.text
        last_name = self.ids.surname.text
        email = self.ids.email.text
        main.x.insert(f"""INSERT INTO parties (first_name, last_name, email) VALUES ('{first_name}', '{last_name}', '{email}')""")


class CreateItemScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def open_menu(self, drop_item_element):
        users = main.x.search("SELECT first_name, last_name FROM parties", multiple=True)
        self.menu_items = [f"{user[0]} {user[1]}" for user in users]
        buttons_menu =[]
        for item in self.menu_items:
            buttons_menu.append(
                {"text": item, 
                 "on_release": lambda x = item: self.button_pressed(x, drop_item_element),
                 "viewclass": "OneLineListItem",
                 }
            )
        self.menu = MDDropdownMenu(caller=drop_item_element, items=buttons_menu, width_mult=2)
        self.menu.open()

    def button_pressed(self, x, drop_item_element):
        first, last = x.split(" ")
        user_id = main.x.search(f"SELECT id FROM parties WHERE first_name = '{first}' AND last_name = '{last}'")
        drop_item_element.text = str(user_id[0])
        self.menu.dismiss()

    def open_shape_menu(self, drop_item_element):
        self.types = main.x.search("SELECT type FROM discs", multiple=True)
        self.types = [x[0] for x in self.types]
        buttons_menu =[]
        for item in self.types:
            buttons_menu.append(
                {"text": item, 
                 "on_release": lambda x = item: self.button_pressed_shape(x, drop_item_element),
                 "viewclass": "OneLineListItem",
                 }
            )
        self.menu = MDDropdownMenu(caller=drop_item_element, items=buttons_menu, width_mult=2)
        self.menu.open()

    def button_pressed_shape(self, x, drop_item_element):
        drop_item_element.text = str(x)
        self.menu.dismiss()
    
    def update_color(self):
        try:
            self.ids.color.md_bg_color = self.ids.disc_color.text
        except:
            self.ids.disc_color.helper_text = "Invalid color"
            self.ids.disc_color.error = True

    def create_item(self):
        customer_id = self.ids.customer_id.text
        color = self.ids.disc_color.text
        zip_code = self.ids.zip.text
        types = self.ids.type.text
        type_id = main.x.search(f"SELECT id FROM discs WHERE type='{types}'")[0]
        quantity = self.ids.quantity.text
        points = main.x.search(f"SELECT points FROM parties WHERE id={customer_id}")[0]
        price = 2500
        if points >= 100:
            price -= 500
            main.x.run_query(f"UPDATE parties SET points={points-100} WHERE id={customer_id}")
        else:
            main.x.run_query(f"UPDATE parties SET points={points+10*int(quantity)} WHERE id={customer_id}")

        if zip_code:
            img_url = get_image(zip_code)
            main.x.insert(f"""INSERT INTO orders (disc_id, quantity, price, employee_id, color, image, customer_id) VALUES ({type_id}, {quantity}, {price}, {main.employee}, '{color}', '{img_url}', {customer_id})""")

            main.link = img_url
            self.parent.current = "ImageScreen"
        else:
            img_url = None
            main.x.insert(f"""INSERT INTO orders (disc_id, quantity, price, employee_id, color, image, customer_id) VALUES ({type_id}, {quantity}, {price}, {main.employee}, '{color}', '{img_url}', {customer_id})""")
            self.parent.current = "HomeScreen"
        
class ImageScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_pre_enter(self, *args):
        print(main.link)
        self.ids.image.source = main.link
        
class HomeScreen(MDScreen):
    def logout(self):
        self.parent.current = "LoginScreen"
        main.x.run_query(f"UPDATE employees SET last_login=CURRENT_TIMESTAMP WHERE id={main.employee}")

    
# This code defines a class called ViewOrderScreen, which is a screen in the application.
# It inherits from the MDScreen class.
# The ViewOrderScreen class displays a table of orders with various columns such as id, disc_type, quantity, price, etc.
# The table is implemented using the MDDataTable widget from the KivyMD library.
# The class has methods to handle events such as row press and checkbox press.
# It also provides functionality to delete selected rows or delete all rows from the table.
class ViewOrderScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_tables= None
        self.selected_rows = []

    def on_pre_enter(self, *args):
        # Define the column names and their widths for the table
        column_names= [("id", 30), ("disc_type", 40), ("quantity", 30), ("price", 30), ("employee_id", 40), ("color", 40), ("image", 40), ("customer_id", 30)]
        
        # Create an instance of MDDataTable with the specified column data
        self.data_tables = MDDataTable(
            size_hint=(0.9, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            use_pagination=True,
            check=True,
            column_data=column_names
        )
        
        # Bind the row press and checkbox press events to their respective methods
        self.data_tables.bind(on_row_press=self.row_pressed)
        self.data_tables.bind(on_check_press=self.checkbox_pressed)
        
        # Add the MDDataTable widget to the screen
        self.add_widget(self.data_tables)
        
        # Update the table with the latest data
        self.update()

    def update(self):
        # Retrieve the order data from the database and update the table
        data = main.x.search("""SELECT orders.id, discs.type, orders.quantity, orders.price, orders.employee_id, orders.color, orders.image, orders.customer_id FROM orders JOIN discs ON orders.disc_id = discs.id""", multiple=True)
        self.data_tables.update_row_data(None, data)
    
    def checkbox_pressed(self, instance_table, current_row):
        # Handle the checkbox press event
        print(f"record checked {current_row}")
        
        # If the current row is already selected, remove it from the selected_rows list
        # Otherwise, add it to the list
        if current_row in self.selected_rows:
            self.selected_rows.remove(current_row)
        else:
            self.selected_rows.append(current_row)

    def row_pressed(self, instance_table, instance_row):
        # Handle the row press event
        print(f"value clicked {instance_row}")

    def delete_selected(self):
        # Delete the selected rows from the database and update the table
        print(self.selected_rows)
        for row in self.selected_rows:
            main.x.run_query(f"DELETE FROM orders WHERE id={row[0]}")
        self.update()

    def delete_all(self):
        # Delete all rows from the database and update the table
        main.x.run_query("DELETE FROM orders")
        self.update()

class ViewPartiesScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_tables= None
        self.selected_rows = []

    def on_pre_enter(self, *args):
        column_names= [("id", 30), ("first_name", 40), ("last_name", 40), ("email", 70), ("points", 30)]
        self.data_tables = MDDataTable(
            size_hint=(0.9, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            use_pagination=True,
            check=True,
            column_data=column_names
        )
        self.data_tables.bind(on_row_press=self.row_pressed)
        self.data_tables.bind(on_check_press=self.checkbox_pressed)
        self.add_widget(self.data_tables)
        self.update()

    def update(self):
        data = main.x.search("""SELECT * FROM parties""", multiple=True)
        self.data_tables.update_row_data(None, data)
    
    def checkbox_pressed(self, instance_table, current_row):
        print(f"record checked {current_row}")
        if current_row in self.selected_rows:
            self.selected_rows.remove(current_row)
        else:
            self.selected_rows.append(current_row)

    def row_pressed(self, instance_table, instance_row):
        print(f"value clicked {instance_row}")


    def delete_selected(self):
        print(self.selected_rows)
        for row in self.selected_rows:
            main.x.run_query(f"DELETE FROM parties WHERE id={row[0]}")
        self.update()

    def delete_all(self):
        main.x.run_query("DELETE FROM parties")
        self.update()

class main(MDApp):
    x =DatabaseWorker('database.db')
    link = ""
    employee = 0
    def build(self):
        pass

test = main()
test.run()
main().x.close()