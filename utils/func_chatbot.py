import json

dict_func_args = {
    'find_employee': {'name': 'some name'},
    'find_lang_speakers': {'language': 'some language'},
    'find_residents': {'city': 'some city'}
}

def find_employee(org_chart, name):
    def find_name(org_chart, name): # helper function that recursively searches the org chart
        employees = [] 
        for emp_name, info in org_chart.items(): # iterate over each employee in the org chart
            if name.lower() in emp_name.lower(): # if the name in the org chart matches (or contains) the requested name, add the employee to the list
                # essential to exclude Direct_Reports when returning employee info, as it would return every single entry below them in the org chart
                match_info = {field: info[field] for field in info if field not in ['Direct_Reports']}  # exclude any unwanted fields
                employees.append((emp_name, match_info)) # append name and desired info (NOT all direct reports) to list
            direct_report_employees = find_name(info['Direct_Reports'], name)   # recursively search the direct reports of the current employee
            employees += direct_report_employees                                # and add any matching direct reports to the employees list

        return employees # after iterating over all employees and direct reports, return the list of matching employees
    
    employees = find_name(org_chart, name) # call the helper function to start the search

    return json.dumps(employees) # convert result to JSON and return it

def find_lang_speakers(org_chart, language):
    def find_speakers(org_chart, language):
        speakers = []

        for name, info in org_chart.items():
            if language in info['languages']:
                match_info = {field: info[field] for field in info if field not in ['Direct_Reports']} 
                speakers.append((name, match_info))
        
            speakers += find_speakers(info['Direct_Reports'], language)

        return speakers

    speakers = find_speakers(org_chart, language)
    return json.dumps(speakers)