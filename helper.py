def create_table_row(list_row_elements):
    joined_string = " ".join('' if row_element is None else f"{row_element:<20}" for row_element in list_row_elements)

    print(joined_string)

def filter_list_to_sql(filters, is_addition=False):
    filter_statements = ""

    if len(filters) < 1:
        return filter_statements

    filter_statement_list = []
    for single_filter_text in filters:
        split_on = "="
        new_single_filter_text = ""
        if ">" in single_filter_text:
            split_on = ">"

        elif "<" in single_filter_text:
            split_on = "<"

        property_name, check_value = single_filter_text.split(split_on)
        if check_number(check_value):
            filter_statement_list.append(f"{property_name} {split_on} {check_value}")

        else:
            check_value = check_value.replace("%20", " ")
            filter_statement_list.append(f"{property_name} = '{check_value}'")

    filter_statements = " AND ".join(filter_statement_list)
    if is_addition:
        filter_statements = f" AND ({filter_statements})"

    else:
        filter_statements = f"WHERE {filter_statements}"

    return filter_statements

def check_number(possible_number):
    try:
        float(possible_number)
        return True

    except ValueError:
        return False

def validate_data(property_name, changed_value):
    if property_name == "name" or property_name == "building" or property_name == "room" or property_name == "placement":
        if check_number(changed_value):
            raise IndexError("Name can not be a number")

        if len(changed_value) > 20:
            raise IndexError("Name must be under 20 characters")
    
    if property_name == "quanity":
        if not check_number(changed_value):
            raise IndexError("Quanity can not be text")
                        
    if property_name == "unit":
        if check_number(changed_value):
            raise IndexError("Unit can not be a number")
                    
        if " " in changed_value:
            raise IndexError("No spaces in units")

    return changed_value