from flask import Flask, render_template_string
from flask_flatpages import FlatPages
from flask_flatpages.utils import pygmented_markdown
import requests
def jinja_renderer(text):
  prerendered_body = render_template_string(text)
  return pygmented_markdown(prerendered_body)

app = Flask(__name__)

# Default Values for config
app.config['SECTION_MAX_LINKS'] = 10
app.config['FLATPAGES_HTML_RENDERE'] = jinja_renderer
app.config.from_object('config')
pages = FlatPages(app)

from fragforce.views import general
#from fragforce.views import events
from fragforce.views import pages

app.register_blueprint(general.mod)
#app.register_blueprint(events.mod)
app.register_blueprint(pages.mod)

@app.context_processor
def tracker_data():
  def print_bar(goal, total, percent, label):
    return '   <div>' + \
           '     <div class="progress-text">' + \
           '       <span class="label">' + str(label) + '</span>' + \
           '     </div>' + \
           '     <div class="progress-amount">' + \
           '       <span class="label"> $' + u'{:0,.0f}'.format(float(total)) + ' &#47; $' + u'{:0,.0f}'.format(float(goal)) + '</span>' + \
           '     </div>' + \
           '   </div>' + \
           '   <div class="progress">' + \
           '     <div class="progress-bar" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="' + str(percent) + '%; max-width: ' + str(percent) + '%; min-width: 2em; width: ' + str(percent) + '%;">' + \
           '     ' + str(percent) + '% ' + \
           '     </div>' + \
           '   </div>'
  def print_bars():
    extralife_total = 0
    extralife_goal = 0
    extralife_percent = 0
    childsplay_total = 0
    childsplay_goal = 0
    childsplay_percent = 0
    full_total = 0
    full_goal = 0
    full_percent = 0
    try:
      r = requests.get('http://www.extra-life.org/index.cfm?fuseaction=donorDrive.team&teamID=27290&format=json')
      if r.status_code == 200:
        data = r.json()
        extralife_total = data['totalRaisedAmount']
        extralife_goal = data['fundraisingGoal']
        if extralife_goal > 0:
          extralife_percent = u'{:0,.2f}'.format(100 * (extralife_total / extralife_goal))
    except requests.exceptions.RequestException as e:
      fail=True
    try:
      r = requests.get('http://donate.childsplaycharity.org/api/event/a452b820a2be5af7bafe5188a0b8337f/json', verify=True)
      if r.status_code == 200:
        data = r.json()
        childsplay_total = data['total']
        childsplay_goal = data['goal']
        childsplay_percent = data['percentage']
    except requests.exceptions.RequestException as e:
      fail=True
    full_total = extralife_total + childsplay_total
    full_goal = extralife_goal + childsplay_goal
    if full_goal > 0:
      full_percent = u'{:0,.2f}'.format(100 * (full_total / full_goal))
    else:
      full_percent = 0
    return print_bar(extralife_goal, extralife_total, extralife_percent, "Extra Life") + \
            print_bar(childsplay_goal, childsplay_total, childsplay_percent, "Childs Play") + \
            print_bar(full_goal, full_total, full_percent, "Totals")
  return dict(
          print_bar=print_bar,
          print_bars=print_bars,
          extralife_link="http://team.fragforce.org",
          childsplay_link="http://childsplay.fragforce.org") 
