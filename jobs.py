import sqlite3

from items import Item
from helper import create_table_row, validate_data, check_number, filter_list_to_sql

def insert_command(sys_arguement, cursor, conn, table_headers):
    #Validating Arguements
    if len(sys_arguement) > 8:
        raise IndexError("Too much arguements")
    
    #Get User data
    crude_item_data = sys_arguement[1:]

    if len(crude_item_data) > 1:
        validate_data("name", crude_item_data[1])
    
    if len(crude_item_data) > 2:
        validate_data("quanity", crude_item_data[2])
    
    if len(crude_item_data) > 3:
        validate_data("unit", crude_item_data[3])

    if len(crude_item_data) > 4:
        validate_data("building", crude_item_data[4])

    if len(crude_item_data) > 5:
        validate_data("placement", crude_item_data[5])
    
    if len(crude_item_data) > 6:
        validate_data("room", crude_item_data[6])
    
    #Proccess User insert
    sample_item = Item(*crude_item_data)
    user_readable_confirmation = sample_item.__dict__
    memmory_item = tuple(user_readable_confirmation.values())
    
    #Create item in db
    item_name = ", ".join(table_headers[1:])
    item_values = ", ".join("?" for throw_away in table_headers[1:])
    cursor.execute(
        f"INSERT INTO items ({item_name}) VALUES ({item_values})",
        memmory_item
    )
    conn.commit()
    
    #Confirming Insertation with user
    print(f"You successfully inserted: {user_readable_confirmation}")

def view_command(sys_arguements, cursor, headers_name, current_filter_list):
     #Searching Table
    if len(sys_arguements) > 3:
        raise IndexError("Too much arguements")
             
    elif len(sys_arguements) > 2:
        search_term = sys_arguements[2]
        search_term_query = list(())
        for throw_away_variable in range(len(headers_name)):
            search_term_query.append(f"%{search_term}%")
     
        search_term_query = tuple(search_term_query)
        like_statements = " OR ".join(f"{header_name} LIKE ?" for header_name in headers_name)
        filter_statements = filter_list_to_sql(current_filter_list, True)
        if filter_statements:
            like_statements = f"({like_statements})"

        search_query_string = f"SELECT * FROM items WHERE {like_statements} {filter_statements}"
     
        cursor.execute(
            search_query_string,
            search_term_query    
        )
     
    else:
        filter_statements = filter_list_to_sql(current_filter_list)

        cursor.execute(f"SELECT * FROM items {filter_statements}")
     
    items = cursor.fetchall()
             
    #Checking Results
    if len(items) < 1:
        raise sqlite3.Error("No Results")
     
    #Printing Results
    create_table_row(headers_name)
    for item in items:
        create_table_row(item)

def select_command(sys_arguements, cursor, conn, headers_name):
     #Checking selection
    if len(sys_arguements) < 3:
        raise IndexError("No selection made")
     
    #Getting Search Term
    search_term = sys_arguements[2]
    search_term_query = (search_term, search_term)
    cursor.execute(
        "SELECT * FROM items WHERE name = ? OR id = ?",
        search_term_query
    )
     
    #Checking Existence
    item = cursor.fetchone()
    if item is None:
        raise IndexError("No item with that name or id")
     
    #Doing work on selected item
    if len(sys_arguements) > 3:
        selected_job = sys_arguements[3]
     
        sample_item = Item(*item[0:])
        user_readable_confirmation = sample_item.__dict__
     
        if selected_job == "-d":
            if len(sys_arguements) > 4:
                raise IndexError("Too much arguements")
                     
            cursor.execute(
                "DELETE FROM items WHERE name = ? OR id = ?",
                search_term_query
            )
            conn.commit()
     
            print(f"Item Deleted: {user_readable_confirmation}")
     
        elif selected_job == "-e":
            if len(sys_arguements) > 6:
                raise IndexError("Too much arguements")
     
            if len(sys_arguements) < 5:
                raise IndexError("No property selected to edit")
     
            property_name = sys_arguements[4]
            if property_name in headers_name[1:]:
                if len(sys_arguements) < 6:
                    raise IndexError("No value to change to")
                         
                changed_value = validate_data(property_name, sys_arguements[5])

                query_string = f"UPDATE items SET {property_name} = ? WHERE name = ? OR id = ?"
                edit_item_query = (changed_value, *search_term_query)
                cursor.execute(
                    query_string,
                    edit_item_query
                )
                conn.commit()
     
                user_readable_confirmation[property_name] = changed_value
                print(f"Item Edited to be: {user_readable_confirmation}")
     
            else:
                raise IndexError("property name does not exist or is not editable")
     
        elif selected_job == "-iu" or selected_job == "-id":
            if len(sys_arguements) > 5:
                raise IndexError("Too much arguements")
     
            increment_value = 1
            if len(sys_arguements) > 4:
                increment_value = sys_arguements[4]
                if not increment_value.isdigit():
                    raise IndexError("Increment not a positive integer")
     
                increment_value = int(increment_value)
     
            if selected_job == "-id":
                test_result_quanity = user_readable_confirmation["quantity"] - increment_value
                if test_result_quanity < 0:
                    raise IndexError("No enough quanity to deincrement")
     
            increment_query = (increment_value, *search_term_query)
            increment_query_string = "UPDATE items SET quantity = quantity + ? WHERE name = ? OR id = ?"
            if selected_job == "-id":
                increment_query_string = "UPDATE items SET quantity = quantity - ? WHERE name = ? OR id = ?"
     
            cursor.execute(
                increment_query_string,
                increment_query
            )
            conn.commit()
     
            if selected_job == "-iu":
                user_readable_confirmation["quantity"] += increment_value
     
            else:
                user_readable_confirmation["quantity"] -= increment_value
     
            print(f"Item Incremented to be: {user_readable_confirmation}")
     
        else:
            raise IndexError("Invalid Job")
     
    else:
        create_table_row(headers_name)
        create_table_row(item)

def filter_command(sys_arguements, headers_name, current_filter_list):
    if len(sys_arguements) < 3:
        raise IndexError("No selection made")

    #Checking property name
    property_name = sys_arguements[2]
    filters = [*current_filter_list]
    if property_name in headers_name[1:]:
        if len(sys_arguements) > 3:
            selected_job = sys_arguements[3]

            #Doing Selected Jobs
            if selected_job == '-a':
                if len(sys_arguements) > 6:
                    raise IndexError("Too much arguements")

                #Checking filter type for the property name
                if len(sys_arguements) > 4:
                    filter_value = validate_data(property_name, sys_arguements[4]).replace(" ", "%20")
                    single_filter_text = f"{property_name}={filter_value}"
                    if len(sys_arguements) > 5:
                        filter_type = sys_arguements[5]
                        is_valid_number = check_number(filter_value)

                        if filter_type == ">" and is_valid_number:
                            single_filter_text = f"{property_name}>{filter_value}"

                        elif filter_type == "<" and is_valid_number:
                            single_filter_text = f"{property_name}<{filter_value}"

                        elif filter_type == "=":
                            single_filter_text = f"{property_name}={filter_value}"

                        else:
                            raise IndexError("Invaild filter type")

                    for single_filter in filters:
                        if property_name in single_filter:
                            raise IndexError("Filter already exists")

                    print(f"Filter added: {single_filter_text}")
                    filters.append(single_filter_text)
                    return "&".join(filters)

                else:
                    raise IndexError("No comparison value")

            elif selected_job == "-d":
                if len(sys_arguements) > 4:
                    raise IndexError("Too many arguements")

                #Deleting filter with property name
                for index in range(len(filters)):
                    single_filter_text = filters[index]

                    if property_name in single_filter_text:
                        filters.remove(single_filter_text)
                        print(f"Filter deleted: {single_filter_text}")
                        return "&".join(filters)

                raise IndexError("No filter to delete")

            else:
                raise IndexError("Invalid job selected")

        else:
            raise IndexError("No job selected")

    else:
        #Clears all filters
        if property_name == "clear":
            print("Cleared all filters")
            return ""
        
        raise IndexError("Property does not exist")