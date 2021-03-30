import time

contacts = []
VALUES = ["first", "last", "phone", "time"]


# Read the lines from data file and send to scraping
def analyze(data_file_name):
    with open(data_file_name, "r") as f:
        collect_codes(f.readline())
        for i in range(1, 4):
            collect_data(f.readline(), VALUES[i])
        format_time()


# Formatting date for readability
def format_time():
    for c in contacts:
        d = c[VALUES[3]]
        obj = time.localtime(int(d))
        c[VALUES[3]] = time.strftime('%Y-%m-%d %H:%M:%S', obj)


# Collect eace contact code and first name
def collect_codes(names_line):
    global contacts
    reduced_line = names_line[4:]
    while reduced_line != "\n":
        c = {"code": reduced_line[0:4]}
        reduced_line = reduced_line[4:]
        name_length = int(reduced_line[0:5], 16)
        reduced_line = reduced_line[5:]
        c[VALUES[0]] = reduced_line[0:name_length].replace("\xa0", " ")
        reduced_line = reduced_line[name_length:]
        contacts.append(c)


# Collect last names, phone numbers and date from data
def collect_data(line_from, type):
    global contacts
    reduced_line = line_from[4:]
    while reduced_line != "\n":
        code = reduced_line[0:4]
        reduced_line = reduced_line[4:]
        name_length = int(reduced_line[0:5], 16)
        reduced_line = reduced_line[5:]
        for c in contacts:
            if c["code"] == code:
                c[type] = reduced_line[0:name_length].replace("\xa0", " ")
        reduced_line = reduced_line[name_length:]

# Saving contacts to a file and printing to screen
def save_res(to_file):
    with open(to_file, "w") as f:
        for c in contacts:
            s = ""
            for v in VALUES:
                if v in c:
                    s += v + ": " + c[v] + " "
            f.write(s)
            f.write("\n")
            print(s)


if __name__ == '__main__':
    file_at_work = "ex_v8.txt"
    file_name = input("What is the name of the file to analyze?\nIf v8 press Enter")
    if file_name != "":
        file_at_work = file_name
    analyze(file_at_work)
    save_res("res_" + file_at_work)
