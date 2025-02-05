import pandas as pd
import bs4

DAY_END = "21:30:00"
MONTHS = ['ERROR','januari','februari','maart','april','mei','juni','juli','augustus','september','oktober','november','december']

class Event:
    def __init__(self, name, time_start, time_end):
        self.name = name
        self.time_start = time_start
        self.time_end = time_end
    
    def __str__(self):
        return f"{self.name} {self.time_start} {self.time_end}"

class Presentation(Event):
    def __init__(self, name, time_start, time_end, presenter):
        super().__init__(name, time_start, time_end)
        self.presenter = presenter

    def __str__(self):
        return f"{self.name} {self.presenter} {self.time_start} {self.time_end}"

class Observation(Event):
    def __init__(self, time_start, time_end, observer):
        super().__init__("observatie", time_start, time_end)
        self.observer = observer
        self.name = ''

    def __str__(self):
        return f"{self.observer} {self.time_start} {self.time_end}"

    
class Day:
    def __init__(self, date, events : list[Event]):
        self.date = date
        self.events = events
    def __str__(self):
        return f"{self.date}\n{self.events}"
    
def read_day_df(day_df : pd.DataFrame):
    start_end_df = day_df.loc[:,['time','event','docent']][day_df['event'] != day_df['event'].shift(1)]
    start_end_df['end'] = start_end_df['time'].shift(-1)
    def build_event(row):
        if row['docent'] == "":
            return Event(row['event'], row['time'], row['end'])
        else:
            return Presentation(row['event'], row['time'], row['end'], row['docent'])
    events = start_end_df.apply(build_event, axis=1).tolist()[:-1]

    se_obs_df = day_df.loc[:,['time','observatie']][day_df['observatie'] != day_df['observatie'].shift(1)]
    se_obs_df['end'] = se_obs_df['time'].shift(-1)
    se_obs_df = se_obs_df[se_obs_df['observatie'] != '']
    observations = se_obs_df.apply(lambda row: Observation(row['time'],row['end'],row['observatie']), axis=1).to_list()
    return events + observations

def make_event_soup(event : Event, document : bs4.BeautifulSoup):
    class_attr = ['event']
    if type(event) == Presentation:
        class_attr.append('teacher-one')
    elif type(event) == Observation:
        class_attr.append('observatie')
    else:
        if event.name.lower().startswith('oefenen') or event.name.lower().startswith('avondprogramma'):
            class_attr.append('oefenen')
        elif event.name.lower().startswith('pauze') or event.name.lower().startswith('avondeten'):
            class_attr.append('pauze')
        elif event.name.lower().startswith('entertainment'):
            class_attr.append('entertainment')
        else:
            class_attr.append('misc')


    def format_time_attr(time):
        if(time == None):
            time = DAY_END
        hours, minutes = time.split(':')[:2]
        hours = hours[1] if hours[0] == '0' else hours
        return f'{hours}-{minutes}'

    class_attr.append(f'start-{format_time_attr(event.time_start)}')
    class_attr.append(f'end-{format_time_attr(event.time_end)}')
    
    class_attr = " ".join(class_attr)

    new_soup = document.new_tag('div', attrs={'class':class_attr})
    new_soup.string = event.name
    return new_soup

def fill_event(day_div: bs4.element.Tag, event_soup):
    events_div = day_div.find('div',attrs={'class':'events'})
    events_div.append(event_soup)

def insert_events(day_index, day : Day, document : bs4.BeautifulSoup):
    soup_events = [make_event_soup(event, document) for event in day.events]
    day_div = document.find('div', attrs={'id':f'dag{day_index}'})
    day_div.attrs['class'].remove('inactief')
    for event_soup in soup_events:
        fill_event(day_div, event_soup)

def insert_dates(dates, document : bs4.BeautifulSoup):
    years, months, days = list(zip(*[date.split('-') for date in dates]))
    formatted = ''
    if len(dates) == 3:
        if len(set(months)) > 1:
            if months[0] == months[1]:
                formatted = f'{int(days[0])} en {int(days[1])} {MONTHS[int(months[0])]}, {int(days[2])} {MONTHS[int(months[2])]} {years[0]}'
            else:
                formatted = f'{int(days[0])} en {int(days[1])} {MONTHS[int(months[0])]}, {int(days[2])} {MONTHS[int(months[2])]} {years[0]}'
        else:
            formatted = f'{int(days[0])}, {int(days[1])} en {int(days[2])} {MONTHS[int(months[0])]} {years[0]}'
    elif len(dates) == 2:
        if len(set(months)) > 1:
            formatted = f'{int(days[0])} {MONTHS[int(months[0])]} en {int(days[1])} {MONTHS[int(months[1])]} {years[0]}'
        else:
            formatted = f'{int(days[0])} en {int(days[1])} {MONTHS[int(months[0])]} {years[0]}'
    else:
        raise Exception('4 daagse data niet geimplementeerd')

    dates_p = document.find('h2',attrs={'id':'data'})
    dates_p.string = formatted

def insert_periode(periode, document : bs4.BeautifulSoup):
    periode_tag = document.find('h1',attrs={'id':'periode'})
    periode_tag.string = f'Periode {periode}'

def insert_subtitle(aantal_dagen, cursusreeks, vak, niveau, document : bs4.BeautifulSoup):
    dagen_string = ''
    if aantal_dagen == 2:
        dagen_string = 'Tweedaagse'
    elif aantal_dagen == 3:
        dagen_string = 'Driedaagse'
    
    subtitle_tag = document.find('h2', attrs={'id':'cursusbeschrijving'})
    subtitle_tag.string = f'{dagen_string} {cursusreeks} {vak} {niveau}'

def insert_opgaven(opgaven : pd.DataFrame, document : bs4.BeautifulSoup):
    def new_row(strings, document : bs4.BeautifulSoup):
        row = document.new_tag('tr')
        for s in strings:
            table_data = document.new_tag('td')
            table_data.string = s
            row.append(table_data)
        return row

    table_tag = document.find('table', attrs={'id':'opgaven-table'})
    for onderwerp in opgaven['onderwerp'].unique():
        opgaven_rows = opgaven[opgaven['onderwerp'] == onderwerp].loc[:,['type','opgaven']].values
        rows_to_append = [new_row(opgaven_row, document) for opgaven_row in opgaven_rows]

        onderwerp_tag = document.new_tag('td',attrs={'rowspan':f'{len(rows_to_append)}'})
        onderwerp_tag.string = onderwerp

        rows_to_append[0].insert(0, onderwerp_tag)
        for r in rows_to_append:
            table_tag.append(r)

def main():
    rooster = pd.read_csv('input/cursusplanning.csv').fillna("")

    periode = int(float(rooster['periode'].iloc[0]))

    dates = rooster['datums'][rooster['datums'] != ''].to_list()
    aantal_dagen = len(dates)

    vak = rooster['vak'].iloc[0]
    niveau = rooster['niveau'].iloc[0]
    cursusreeks = rooster['reeks'].iloc[0]

    day_dfs = [pd.DataFrame(zip(*[rooster.loc[1:,col] for col in rooster.columns if col[0] == str(i)]), columns=["time","event","docent","training","observatie"]) for i in range(1, aantal_dagen + 1)]

    days = [Day(dates[i], read_day_df(day_df=day_dfs[i])) for i in range(aantal_dagen)]

    opgaven = None
    if aantal_dagen == 2:
        opgaven = pd.read_csv('input/opgavenlijst_tweedaagse.csv').fillna('')
    elif aantal_dagen == 3:
        opgaven = pd.read_csv('input/opgavenlijst_driedaagse.csv').fillna('')
    else:
        raise Exception('Alleen 2 of 3 daags opgavenlijst')

    with open('input/template.html') as f:
        template_soup = bs4.BeautifulSoup(f.read(), 'html.parser')

    for i, day in enumerate(days, start=1):
        insert_events(i, day, template_soup)

    insert_dates(dates, template_soup)

    insert_periode(periode, template_soup)

    insert_subtitle(aantal_dagen, cursusreeks, vak, niveau, template_soup)

    insert_opgaven(opgaven, template_soup)

    with open('input/praktisch.html') as f:
        praktisch_soup = bs4.BeautifulSoup(f.read(), 'html.parser')

    praktisch_div = template_soup.find('div',attrs={'id':'praktisch'})
    praktisch_div.append(praktisch_soup)


    with open("output.html", "w") as file:
        file.write(template_soup.prettify())

if __name__ == "__main__":
    main()