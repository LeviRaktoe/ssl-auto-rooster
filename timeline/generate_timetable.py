import bs4
import datetime

starttime = datetime.timedelta(hours=8,minutes=30)
half_hour = datetime.timedelta(minutes=30)
quarter = datetime.timedelta(minutes=15)

with open("timeline_base.html") as t:
    text = t.read()
    soup = bs4.BeautifulSoup(text, features="lxml")

td = soup.find(id="start")

entry = soup.new_tag("div", attrs={"class": "time_marker half"})
entry.append("21:30")
td.insert_after(entry)

entry = soup.new_tag("div", attrs={"class": "time_marker"})
entry.append("...")
td.insert_after(entry)

with open("timeline_style.txt", "w") as f:
    for i in reversed(range(45)):
        extra_class = ""
        if i % 4 == 2:
            extra_class = " half full"
        elif i % 2 == 0:
            extra_class = " half"
        
        entry = soup.new_tag("div", attrs={"class": f"time_marker{extra_class}"})
        time = starttime + quarter * i
        hour = int(time.total_seconds() // 3600)
        min = int(time.total_seconds() % 3600 // 60)
        lines = [f".start-{hour}-{min:02} {{", f"\tgrid-row-start: {i+2};","}",f".end-{hour}-{min:02} {{", f"\tgrid-row-end: {i+2};","}","\n"]
        f.write('\n'.join(lines))
        entry.append("{:}:{:02}".format(hour, 
        hour = int(time.total_seconds() // 3600)
        min = int(time.total_seconds() % 3600 // 60)
        lines = [f".start-{hour}-{min:02} {{", f"\tgrid-row-start: {i+2};","}",f".end-{hour}-{min:02} {{", f"\tgrid-row-end: {i+2};","}","\n"]
        f.write('\n'.join(lines))
        entry.append("{:}:{:02}".format(hour, min))
        td.insert_after(entry)

        
        entry = soup.new_tag("div", attrs={"class": f"time_marker{extra_class}"})
        time = starttime + quarter * i
        hour = int(time.total_seconds() // 3600)
        min = int(time.total_seconds() % 3600 // 60)
        lines = [f".start-{hour}-{min:02} {{", f"\tgrid-row-start: {i+2};","}",f".end-{hour}-{min:02} {{", f"\tgrid-row-end: {i+2};","}","\n"]
        f.write('\n'.join(lines))
        entry.append("{:}:{:02}".format(hour, min))
        td.insert_after(entry)


            extra_class = " half full"
        elif i % 2 == 0:
            extra_class = " half"
        
        entry = soup.new_tag("div", attrs={"class": f"time_marker{extra_class}"})
        time = starttime + quarter * i
        hour = int(time.total_seconds() // 3600)
        min = int(time.total_seconds() % 3600 // 60)
        lines = [f".start-{hour}-{min:02} {{", f"\tgrid-row-start: {i+2};","}",f".end-{hour}-{min:02} {{", f"\tgrid-row-end: {i+2};","}","\n"]
        f.write('\n'.join(lines))
        entry.append("{:}:{:02}".format(hour, min))
        td.insert_after(entry)



with open("timeline.html", "w") as t:
    t.write(str(soup.prettify()))

    t.write(str(soup.prettify()))

            extra_class = " half full"
        elif i % 2 == 0:
            extra_class = " half"
        
        entry = soup.new_tag("div", attrs={"class": f"time_marker{extra_class}"})
        time = starttime + quarter * i
        hour = int(time.total_seconds() // 3600)
        min = int(time.total_seconds() % 3600 // 60)
        lines = [f".start-{hour}-{min:02} {{", f"\tgrid-row-start: {i+2};","}",f".end-{hour}-{min:02} {{", f"\tgrid-row-end: {i+2};","}","\n"]
        f.write('\n'.join(lines))
        entry.append("{:}:{:02}".format(hour, min))
        td.insert_after(entry)



with open("timeline.html", "w") as t:
    t.write(str(soup.prettify()))

