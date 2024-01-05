from datetime import datetime, timedelta, time
from collections import defaultdict
from appointments.models import Appointment

def get_time_range(start, end, delta):
    current = start
    while current <= end:          
        yield current
        current += delta
     

class TimeTable():
    def __init__(self, date):
        self.css_class = 'timeTable'
        self.start = datetime.combine(date, time(8,0,0))
        self.end = datetime.combine(date, time(18,0,0))
        self.disabled_timestamps = ["08:00 AM", "08:30 AM", "13:30 PM", "14:00 PM"]
        self.time_range = [dt.strftime("%H:%M %p") for dt in 
                        get_time_range(self.start, self.end, timedelta(minutes=30))]

    
    def set_start_end_times(self, user):
        self.start = datetime.combine(self.start.date(), user.start_time)
        self.end = datetime.combine(self.end.date(), user.end_time)

    def render(self, appointments, user):
        if user.start_time and user.end_time: self.set_start_end_times(user)
        blocks = 0
        v = []
        a = v.append
        a(f"<div class='{self.css_class}'>")
        a('\n')
        for timestamp in self.time_range:
            appointment = [x for x in appointments if x.time.strftime("%H:%M %p") == timestamp]
            if timestamp in self.disabled_timestamps:
                css_class = 'disabled'
            elif appointment:
                css_class = appointment[0].get_state_display()
                blocks = appointment[0].length / 30
            elif blocks <= 1:
                css_class = ''
                blocks = 0
            else:
                blocks -= 1


            a(f"<button class='{css_class}' onclick='openAppointmentModal(this)' data-stamp='{timestamp}'>{timestamp}</button>")
        a('\n')
        a("</div>")

        return ''.join(v)


class WeeklyCalendar():
    def __init__(self):
        self.start = datetime.combine(datetime.date(datetime.now()), time(8,0,0))
        self.end = datetime.combine(datetime.date(datetime.now()), time(17,30,0))
        self.disabled_timestamps = ["08:00 AM", "08:30 AM", "13:30 PM"]
        self.time_range = [dt.strftime("%H:%M %p") for dt in 
                        get_time_range(self.start, self.end, timedelta(minutes=30))]
    
    def get_week(self, date):
        day_idx = (date.weekday() + 1) % 7  # turn sunday into 0, monday into 1, etc.
        sunday = date - timedelta(days=day_idx)
        date = sunday
        for n in range(7):
            if not(n == 6 or n == 0): yield date
            date += timedelta(days=1)

    def get_appointment(self, date, time):
        appointment = Appointment.objects.filter(date=date, time=time)
        if len(appointment) == 0: return  
        print(appointment[0])
        return appointment[0]

    def render(self, date):
        weekdays = list(self.get_week(date))
        blocks = defaultdict(None)
        v = []
        a = v.append
        a("<table class='calendar'>")
        a("<colgroup> <col  style='width: 10%;'></colgroup>")
        a("<tr>")
        a(f"<th>{date.year}</th>")
        for day in weekdays:
            a(f"<th>{day.strftime('%a %d/%m')}</th>")
        a("</tr>")
        
        for time in self.time_range:
            a("<tr>")
            a(f"<td>{time}</td>")
            for day in weekdays:
                css_class = btn_inner = appointment_id = ''
                if time in self.disabled_timestamps: css_class = 'disabled'
                else:
                    appointment = self.get_appointment(day, time[:-3])
                    block = blocks.get(day)
                    if block:
                        css_class = block[2]
                        block[0] -= 1
                        if block[0] <= 1: blocks.pop(day) 
                    elif appointment: 
                        appointment_id = appointment.id
                        css_class = appointment.get_state_display()
                        btn_inner = appointment.service
                        n_block = appointment.length / 30
                        if n_block > 1:
                            blocks[day] = [n_block, time, css_class]

                a(f"<td><button onclick='openAppointmentModal(this);' data-id='{appointment_id}' data-stamp='{time}' data-date={day} class='{css_class}'>{btn_inner}</button></td>")
            a("</tr>")
        a("</table>")
        return ''.join(v)
        


